# 🏢 DocBrain -- Enterprise Multi-Document Knowledge Brain

An AI-powered **Retrieval-Augmented Generation (RAG)** application built with **Streamlit + LangChain + Google Gemini**, designed to analyze and answer questions from multiple PDF documents.

---

## 🚀 Features

* 📄 Upload multiple PDF documents
* 🧠 Automatic text extraction and chunking
* 🔍 Semantic search using FAISS vector database
* 🤖 Context-aware question answering using Gemini
* ⚡ Fast retrieval with cached embeddings
* 📚 Source traceability (view retrieved chunks)

---

## 🏗️ Architecture Overview

```
PDF Upload → Text Extraction → Chunking → Embeddings → FAISS Vector DB
                                                     ↓
                                               Retriever
                                                     ↓
                                               LLM (Gemini)
                                                     ↓
                                               Final Answer
```

---

## 🛠️ Tech Stack

* **Frontend**: Streamlit
* **LLM**: Google Gemini (via LangChain)
* **Embeddings**: text-embedding-004
* **Vector Store**: FAISS
* **Backend Logic**: LangChain RAG pipeline

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/enterprise-doc-brain.git
cd enterprise-doc-brain
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Setup Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

---

## ▶️ Running the App

```bash
streamlit run app.py
```

---

## 📂 Project Structure

```
.
├── app.py
├── faiss_index/        # Generated vector database
├── .env
├── requirements.txt
└── README.md
```

---

## 🔄 How It Works

### 1. Upload PDFs

* Files are read using `pypdf`
* Text is extracted page-by-page

### 2. Text Chunking

* Split into manageable chunks
* Uses overlap for context continuity

### 3. Embedding Generation

* Converts text into vectors using Google embeddings

### 4. Vector Storage

* Stored in FAISS for fast similarity search

### 5. Query Processing

* User query → embedded → similarity search
* Top relevant chunks retrieved

### 6. Answer Generation

* Gemini model generates response using retrieved context

---

## ⚙️ Configuration

### Chunking Parameters

```python
chunk_size = 1200
chunk_overlap = 150
```

### Retrieval

```python
k = 4  # number of chunks retrieved
```

### Model

```python
gemini-1.5-flash-latest
```

---

## ⚠️ Limitations

* ❌ Does not support scanned PDFs (no OCR yet)
* ❌ No conversation memory (single-turn QA)
* ❌ FAISS stored locally (not scalable yet)

---

## 🔮 Future Improvements

* 🧠 Add conversational memory
* 🔍 Hybrid search (semantic + keyword)
* 🗂️ Metadata filtering (file name, page number)
* ☁️ Cloud vector DB (Pinecone / Weaviate)
* 🖼️ OCR support for scanned documents
* ⚡ Streaming responses

---

## 🐛 Troubleshooting

### API Key Error

Ensure `.env` file contains:

```
GOOGLE_API_KEY=your_key
```

---

### No Text Extracted

* Your PDF may be scanned
* Use OCR tools like `pytesseract`

---

### FAISS Not Found

* Ensure documents are processed before querying

---

## 📜 License

This project is open-source and available under the MIT License.

---

## 👤 Author

Built as a scalable RAG system for document intelligence and enterprise knowledge retrieval.

---

## 💡 Tip

For best results:

* Use clean, text-based PDFs
* Avoid scanned or image-heavy documents
* Ask specific, context-rich questions

---

**Ready to turn your documents into an intelligent knowledge system 🚀**
