# Schema validation for CSV data contracts
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pandas as pd

try:
    import yaml
except ImportError:  # pragma: no cover - fallback for minimal environments
    yaml = None


def _resolve_path(path: str | Path) -> Path:
    """Resolve a relative project path into an absolute filesystem path.

    Args:
        path: A file or directory path, which may be relative to the repository root.

    Returns:
        A fully resolved Path object pointing to the target file.
    """
    path_obj = Path(path)
    if not path_obj.is_absolute():
        path_obj = (Path(__file__).resolve().parents[2] / path_obj).resolve()
    return path_obj


def _normalize_string(value: Any) -> str:
    """Convert a CSV cell value to a trimmed string, treating nulls as empty strings.

    Args:
        value: The raw value pulled from a pandas Series.

    Returns:
        A cleaned string with surrounding whitespace removed, or an empty string when the value is null.
    """
    if value is None or pd.isna(value):
        return ""
    return str(value).strip()


def _parse_decimal(value: Any) -> float | None:
    """Parse a CSV numeric string into a float while stripping currency and percent symbols.

    Args:
        value: A raw value from the CSV, such as "$123,456" or "12.5%".

    Returns:
        A float representation of the value, or None if the string cannot be parsed as a decimal.
    """
    text = _normalize_string(value)
    if text == "":
        return None
    text = text.replace("$", "").replace(",", "").replace("%", "")
    if text.startswith("(") and text.endswith(")"):
        text = f"-{text[1:-1]}"
    try:
        return float(text)
    except ValueError:
        return None


def _parse_bool(value: Any) -> bool | None:
    """Convert common CSV boolean representations into a Python bool.

    Args:
        value: A raw CSV value such as TRUE, FALSE, 1, 0, YES, or NO.

    Returns:
        A boolean value when recognized, otherwise None.
    """
    if value is None or pd.isna(value):
        return None
    if isinstance(value, bool):
        return value
    text = _normalize_string(value).upper()
    if text in {"TRUE", "T", "1", "YES", "Y"}:
        return True
    if text in {"FALSE", "F", "0", "NO", "N"}:
        return False
    return None


def _parse_date(value: Any) -> pd.Timestamp | None:
    """Attempt to parse a CSV date-like string into a pandas Timestamp.

    Args:
        value: A value from the CSV that should represent a date.

    Returns:
        A pandas Timestamp if parsing succeeds; otherwise None.
    """
    if value is None or pd.isna(value):
        return None
    text = _normalize_string(value)
    if text == "":
        return None
    try:
        return pd.to_datetime(text)
    except (TypeError, ValueError):
        return None


def validate_schema(contract_path: str | Path = "metadata/loan_application_contract.yaml", csv_path: str | Path | None = None) -> bool:
    """Validate a CSV file against a YAML data contract and report schema violations.

    Args:
        contract_path: Path to the YAML contract file. Defaults to the repository loan_application_contract.yaml.
        csv_path: Optional explicit path to the CSV being validated. If omitted, the contract's dataset.path is used.

    Returns:
        True when the CSV meets the contract requirements, otherwise False after printing validation errors.
    """
    if yaml is None:
        raise ImportError("PyYAML is required to read the data contract.")

    contract_file = _resolve_path(contract_path)
    if not contract_file.exists():
        raise FileNotFoundError(f"Contract file not found: {contract_file}")

    with contract_file.open("r", encoding="utf-8") as fh:
        contract = yaml.safe_load(fh) or {}

    dataset_cfg = contract.get("dataset", {})
    if csv_path is None:
        csv_path = dataset_cfg.get("path")
    csv_file = _resolve_path(csv_path) if csv_path else None
    if csv_file is None:
        raise ValueError(
            "CSV path is missing from the contract or function arguments.")
    if not csv_file.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_file}")

    try:
        df = pd.read_csv(csv_file, dtype=str, keep_default_na=False)
    except Exception as exc:  # pragma: no cover - defensive for malformed CSVs
        print(f"Failed to read CSV: {exc}")
        return False

    errors: list[str] = []

    expected_row_count = dataset_cfg.get("expected_row_count")
    if expected_row_count is not None and len(df) != expected_row_count:
        errors.append(
            f"Row count mismatch: expected {expected_row_count}, found {len(df)} in {csv_file.name}."
        )

    fields = contract.get("fields", [])
    field_map = {field["name"]: field for field in fields if "name" in field}

    missing_columns = [name for name in field_map if field_map[name].get(
        "required") and name not in df.columns]
    for col in missing_columns:
        errors.append(f"Missing required column: {col}")

    for field_name, field_cfg in field_map.items():
        if field_name not in df.columns:
            continue

        series = df[field_name]
        # start at 2 to match CSV data rows after header
        for idx, raw_value in enumerate(series, start=2):
            value = raw_value
            if value is None or _normalize_string(value) == "":
                if field_cfg.get("required"):
                    errors.append(
                        f"Row {idx}: '{field_name}' is required and is missing.")
                continue

            field_type = field_cfg.get("type", "string").lower()
            value_text = _normalize_string(value)

            if field_type == "string":
                if "pattern" in field_cfg:
                    if not re.fullmatch(field_cfg["pattern"], value_text):
                        errors.append(
                            f"Row {idx}: '{field_name}' does not match pattern '{field_cfg['pattern']}'."
                        )
                if "allowed_values" in field_cfg:
                    allowed = [str(item)
                               for item in field_cfg["allowed_values"]]
                    if value_text not in allowed:
                        errors.append(
                            f"Row {idx}: '{field_name}' has value '{value_text}', expected one of {allowed}."
                        )

            elif field_type == "integer":
                try:
                    int_value = int(value_text)
                except ValueError:
                    errors.append(
                        f"Row {idx}: '{field_name}' is not an integer: '{value_text}'.")
                    continue
                minimum = field_cfg.get("minimum")
                maximum = field_cfg.get("maximum")
                if minimum is not None and int_value < minimum:
                    errors.append(
                        f"Row {idx}: '{field_name}' is below minimum {minimum}.")
                if maximum is not None and int_value > maximum:
                    errors.append(
                        f"Row {idx}: '{field_name}' exceeds maximum {maximum}.")

            elif field_type == "decimal":
                num = _parse_decimal(value)
                if num is None:
                    errors.append(
                        f"Row {idx}: '{field_name}' is not a valid decimal: '{value_text}'.")
                    continue
                minimum = field_cfg.get("minimum")
                maximum = field_cfg.get("maximum")
                if minimum is not None and num < minimum:
                    errors.append(
                        f"Row {idx}: '{field_name}' is below minimum {minimum}.")
                if maximum is not None and num > maximum:
                    errors.append(
                        f"Row {idx}: '{field_name}' exceeds maximum {maximum}.")

            elif field_type == "boolean":
                bool_value = _parse_bool(value)
                if bool_value is None:
                    errors.append(
                        f"Row {idx}: '{field_name}' is not a valid boolean value: '{value_text}'.")
                    continue
                allowed_values = field_cfg.get("allowed_values")
                if allowed_values is not None:
                    expected = {str(item).upper() for item in allowed_values}
                    if str(bool_value).upper() not in expected and str(value_text).upper() not in expected:
                        errors.append(
                            f"Row {idx}: '{field_name}' has value '{value_text}', expected one of {allowed_values}."
                        )

            elif field_type == "date":
                if _parse_date(value) is None:
                    errors.append(
                        f"Row {idx}: '{field_name}' is not a valid date: '{value_text}'.")

    primary_key = dataset_cfg.get("primary_key") or []
    for key_field in primary_key:
        if key_field not in df.columns:
            continue
        clean = df[key_field].map(lambda v: _normalize_string(v))
        if (clean == "").any():
            errors.append(
                f"Primary key field '{key_field}' contains null values.")
        duplicates = clean[clean.duplicated(keep=False)]
        if not duplicates.empty:
            dup_vals = ", ".join(sorted(set(duplicates.tolist())))
            errors.append(
                f"Primary key field '{key_field}' contains duplicate values: {dup_vals}.")

    if errors:
        print("Schema validation failed:")
        for error in errors:
            print(f"- {error}")
        return False

    print(f"Schema validation passed for {csv_file.name}.")
    return True


if __name__ == "__main__":
    validate_schema()
