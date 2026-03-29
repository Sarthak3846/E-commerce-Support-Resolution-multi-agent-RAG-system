# E-commerce Support Resolution Multi-Agent RAG System

## Overview

This project implements a multi-agent Retrieval-Augmented Generation (RAG) system for resolving customer support tickets in an e-commerce setting. The system uses structured policy documents to make grounded decisions with citations, ensuring reliable and explainable outputs.

The pipeline integrates multiple agents:

* Triage Agent for classification
* Retriever Agent for policy lookup
* Resolver Agent for decision-making
* Compliance Agent for validation

---

## Features

* Multi-agent architecture
* RAG-based policy retrieval using FAISS
* Structured JSON outputs
* Citation-backed reasoning
* Streamlit-based user interface
* Handles approval, denial, partial approval, and escalation cases

---

## Project Structure

```
project_root/
├── app/
│   ├── main.py
│   ├── components.py
├── agents/
│   ├── triage_agent.py
│   ├── retriever_agent.py
│   ├── resolver_agent.py
│   ├── compliance_agent.py
│   ├── orchestrator.py
├── rag/
│   ├── ingestion.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── retriever.py
├── data/
│   ├── raw/
│   ├── processed/
│   ├── chunks.json
├── vector_store/
│   ├── faiss_index.bin
│   ├── metadata.json
├── utils/
│   ├── llm.py
├── requirements.txt
├── README.md
```

---

## Setup Instructions

### 1. Clone the Repository

```
git clone <your-repo-url>
cd <project-folder>
```

---

### 2. Create Virtual Environment

```
python -m venv venv
```

Activate:

```
venv\Scripts\activate   (Windows)
source venv/bin/activate (Mac/Linux)
```

---

### 3. Install Dependencies

```
pip install -r requirements.txt
```

If missing:

```
pip install sentence-transformers faiss-cpu torch torchvision streamlit
```

---

### 4. Set API Key

Create a `.env` file:

```
GEMINI_API_KEY=your_api_key_here
```

Ensure your `utils/llm.py` loads this key.

---

### 5. Data Preparation

Place all policy documents in:

```
data/raw/
```

Run ingestion:

```
python rag/ingestion.py
```

---

### 6. Chunking

```
python rag/chunking.py
```

---

### 7. Build Embeddings and Vector Store

```
python rag/embeddings.py
```

This creates:

```
vector_store/faiss_index.bin
vector_store/metadata.json
```

---

### 8. Run the Application

```
streamlit run app/main.py
```

Open in browser:

```
http://localhost:8501
```

---

## How the System Works

### Pipeline

```
User Input
→ Triage Agent
→ Retriever (FAISS)
→ Resolver Agent
→ Compliance Agent
→ Final Output
```

---

### RAG Implementation

* Chunk Size: ~400–500 words
* Overlap: ~50 words
* Embedding Model: sentence-transformers/all-MiniLM-L6-v2
* Vector Store: FAISS (L2 similarity)
* Top-k Retrieval: 4 chunks

---

### Decision Logic

* Uses retrieved policy chunks only
* Enforces citation requirement
* Falls back to escalation if insufficient evidence
* Handles edge cases and exceptions

---

## Data Sources

* Amazon Returns, Refund, Shipping Policies
* Flipkart Policies
* eBay Buyer Protection and Returns
* Meesho Policies
* Synthetic policies for exceptions and promotions

Each source is documented with URL and access date.

---

## Example Use Cases

* Wrong size product → refund approval
* Non-returnable item → denial
* Missing information → escalation
* Damaged item → refund/replacement

---

## Running Tests (Optional)

You can create test tickets and evaluate:

* decision correctness
* citation presence
* system behavior under edge cases

---

## Notes

* Ensure FAISS index is built before running the app
* Ensure correct file paths (absolute paths recommended)
* Avoid modifying cleaned policy structure

---

## License

This project is for educational and evaluation purposes.
