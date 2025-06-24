# ⚖️ Pakistan Legal Assistant (PPC Search AI)

A smart legal assistant trained on the **Pakistan Penal Code**. Ask any question and get relevant legal sections with simplified answers — all powered by **LangChain**, **ChromaDB**, and **LLMs via OpenRouter**.

---

## 🚀 Features

- 🔍 Semantic search on Pakistan Penal Code
- 📑 Extracts, chunks, and indexes law text for high-accuracy retrieval
- 🧠 Uses HuggingFace sentence-transformers for embeddings
- 🤖 Answers powered by OpenRouter-compatible LLMs
- 🎛️ Simple Streamlit frontend

---

## 🧰 Tech Stack

| Component     | Tech Used                                     |
|---------------|-----------------------------------------------|
| Embeddings    | `intfloat/e5-base-v2`      |
| Vector Store  | `Chroma` (local persistent DB)                |
| LLM Backend   | `OpenRouter` (free-tier compatible)           |
| Interface     | `Streamlit`                                   |
| Extraction    | Custom PDF text parsing + chunking            |

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repo

```bash
git clone https://github.com/AfsheenMahmood/lexi.git
cd lexi
