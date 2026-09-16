# RAG System Architecture
<img width="1460" height="885" alt="image" src="https://github.com/user-attachments/assets/4400a299-63c1-4377-8305-f81402ba4af0" />



## Summary
This architecture describes an end-to-end Retrieval-Augmented Generation (RAG) Platform designed to handle both structured and unstructured data and serve accurate, context-aware responses to users.

The system is organized into three core layers within the RAG Pipeline:

**1. Data Sources**
The platform ingests two types of data:

-  _Structured — Databases, tables, CSV, APIs_
-  _Unstructured — Documents, PDFs, images, text_

**2. Ingestion & Processing Layer**
Two distinct ingest paths:

-  Structured Path: Data goes through Extract-Transform-Load (ETL) and is routed directly to the Structured Store. No parsing or embedding needed.
-  Unstructured Path: Data goes through Parsing → Chunking → Embedding, where documents are broken into chunks and converted into vectors, then routed via the Vector Path to the Vector Store.

This separation ensures tabular data stays queryable and unstructured content becomes semantically searchable.

**3. Storage & Retrieval Layer**
The heart of the RAG system:

-  Structured Store and Vector Store hold the processed knowledge
-  Hybrid Search combines keyword and semantic search across both stores
-  Reranking refines results to return only the most relevant context

**4. Application & Generation Layer**
Retrieved context is consumed by downstream applications:

-  ML, API, and Report services for traditional use cases
-  Generative AI&LLMsfor synthesizing final, grounded answers

**User Query Flow:**
-  Unlike document ingestion, a user query is never parsed or chunked. It follows a lightweight path:
-  User → Embed Query → Vector Store / Hybrid Search → Reranking → Generative AI → Response

The query is embedded into a vector, matched against stored knowledge, reranked, and then passed with context to the LLM to generate a fact-grounded response.
