# 🎥 YouTube Transcript Q&A Bot

An AI-powered application that allows users to **chat with any YouTube video** by leveraging **Retrieval-Augmented Generation (RAG)**.

Built using **LangChain, HuggingFace, FAISS, and Streamlit**, this app extracts video transcripts and enables intelligent question answering using **Llama 3.1**.

---

## 🚀 Live Demo

*(Add your deployed link here later)*

---

## ✨ Features

* 🎥 Extracts transcripts from YouTube videos
* 🤖 Uses LLM (Llama 3.1 / Mistral) for answering queries
* 🔍 Semantic search using FAISS vector database
* 🧠 Context-aware responses using RAG pipeline
* ⚡ Fast and interactive Streamlit UI
* 🔐 Secure API key input via sidebar

---

## 🧠 How It Works

1. User provides YouTube video URL or ID
2. Transcript is fetched using `youtube-transcript-api`
3. Text is split into chunks
4. Embeddings are generated using HuggingFace models
5. Stored in FAISS vector database
6. Relevant context is retrieved based on query
7. LLM generates accurate answer using context

---

## 🛠️ Tech Stack

* Python
* Streamlit
* LangChain
* HuggingFace (Llama 3.1 / Mistral)
* FAISS (Vector DB)
* YouTube Transcript API

---

## 📂 Project Structure

```id="x7l2kp"
YouTube-RAG-App/
│── app.py
│── requirements.txt
│── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```id="m2zqgp"
git clone https://github.com/HARSH-GOHIL-git/youtube-rag-app.git
cd youtube-rag-app
```

---

### 2️⃣ Install dependencies

```id="i7cl7z"
pip install -r requirements.txt
```

---

### 3️⃣ Run the application

```id="cs2v9k"
streamlit run app.py
```

---

## 🔑 Setup API Key

* Get your API key from HuggingFace
* Paste it into the sidebar inside the app

---

## 📸 Usage

1. Enter YouTube video URL or ID
2. Click **"Process Video"**
3. Ask any question about the video
4. Get intelligent, context-based answers

---

## 📊 Example

**Input:**

```id="dr6n9x"
What is the main topic of the video?
```

**Output:**

```id="0klr0z"
The video discusses...
```

---

## 🚀 Future Improvements

* 🎥 Support for multiple videos
* 💾 Save chat history
* 🌐 Deploy on cloud (Streamlit / Render)
* 🧾 Add source citations
* 🎤 Voice-based interaction

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork and improve.

---

## 👨‍💻 Author

**Harsh Gohil**
🔗 GitHub: https://github.com/HARSH-GOHIL-git

---

## ⭐ Support

If you found this project helpful, please give it a ⭐ on GitHub!
