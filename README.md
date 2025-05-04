# interview_task
# interview

# 🤖 AI-Powered HR Chatbot with FastAPI & LangChain

An intelligent HR chatbot using **LangChain**, **FastAPI**, and **Groq LLaMA 3.1-8B**. It processes HR-related CSV data and answers queries with source citations and contextual understanding.

---

## 🚀 Features

- 🤖 Uses Groq-hosted LLaMA 3.1-8B-Instant for real-time responses
- 🧠 Maintains chat history with memory (ConversationBufferMemory)
- 📄 Answers include citations from HR CSV files
- 📊 Supports BLEU score evaluation
- ⚙️ Modular FastAPI-based architecture
- 📁 Vector store persistence using ChromaDB

---

## 🖥️ OS Compatibility

✅ Works on:

- **Linux / Ubuntu**
- **Windows (PowerShell or Command Prompt)**

Instructions are provided for both platforms below.

---

## 📁 Project Structure

```
.
├── app.py                      # FastAPI app entry point
├── routes/
│   └── chat.py                  # API route for chat endpoint
├── services/
│   ├── chat_service.py          # Chat logic and LLM integration
│   ├── HRM_master_Dataset.csv   # HR data source
│   └── Work_summary.csv         # Work summary data
├── accuracy_score/
│   ├── collect_responses.py     # Response collection utility
│   └── llm_evaluation.py        # BLEU evaluation
├── core/
│   └── config.py                # Settings via pydantic
├── db/                          # Chroma vector store directory
├── requirements.txt
└── README.md


---

## ⚙️ Installation

### 1. Clone the Repository

bash
git clone "repo"



### 2. Create Virtual Environment

#### 🐧 Linux / Ubuntu
bash
python3 -m venv venv
uv venv venv
source venv/bin/activate


#### 🪟 Windows

powershell
python -m venv venv
venv\Scripts\activate


### 3. Install Dependencies

bash
pip install -r requirements.txt
linux
uv pip install -r requirements.txt


### 4. Set Environment Variables

Create a `.env` file in the project root:

env
GROQ_API_KEY=your_groq_api_key
CHROMA_PERSIST_DIRECTORY=db
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
CHUNK_SIZE=1000


---

## ▶️ Run the Application

### 🌐 Start FastAPI Server

#### Linux / Ubuntu

bash
uvicorn main:app --reload


#### Windows

powershell
uvicorn main:app --reload


Once running, access the Swagger UI:

> 📍 http://127.0.0.1:3000/chat

---

## 📬 Sample API Request

### **POST** `/chat/`

**Body:**

json
{
  "question": "Who is responsible for the onboarding process?"
}


**Response:**
json
{
  "answer": "The onboarding process is managed by the HR team.",
  "sources": [
    "HRM_master_Dataset.csv"
  ]
}


---

## 📊 BLEU Score Evaluation

Optional BLEU evaluation example (for testing model output quality):

python
from services.chat_service import ChatService

service = ChatService()
reference = "The onboarding is handled by HR."
candidate = "HR manages onboarding."
print(service.calculate_bleu(reference, candidate))  # Output: BLEU Score


---

## 🧩 Key Dependencies

text
# FastAPI, LLM & LangChain
fastapi, uvicorn, langchain, langchain-groq

# Embeddings & Transformers
sentence-transformers, transformers, torch

# Vector Storage
chromadb, faiss-cpu

# Utilities
pandas, lxml, python-dotenv, pydantic, sacrebleu


Install all using:

bash
pip install -r requirements.txt


---

## ✅ Tips for Both OS

| Task                  | Linux / Ubuntu                   | Windows                         |
|-----------------------|----------------------------------|----------------------------------|
| Create venv           | uv venv venv                   | python -m venv venv           |
| Activate venv         | source venv/bin/activate       | venv\Scripts\activate       |
| Run server            | python app.py                   | uvicorn main:app --reload     |
| Install requirements  | uv pip install -r requirements.txt| pip install -r requirements.txt|