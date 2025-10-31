# Rag-voice-bot
# 🎙️ Offline RAG Voice Bot

## 🧠 Overview
This project is an **offline Retrieval-Augmented Generation (RAG) Voice Bot** created as part of the **L&L AI Solutions Evaluation Task**.

It listens to your voice question 🎤, searches for the answer from your local **PDF document**, and speaks the answer out loud 🔊 — all running **offline** using **Hugging Face models** and **LangChain**.

---

## ⚙️ Tech Stack
- **Python 3.13**
- **LangChain** – for text chunking and retrieval
- **FAISS** – for vector similarity search
- **Sentence Transformers** – for embeddings
- **Transformers (Hugging Face)** – for offline summarization
- **SpeechRecognition**, **gTTS**, **playsound** – for voice input/output
- **PyPDF2** – for reading the PDF data

---

## 🧩 How It Works
1. 🎙️ User asks a question using their voice  
2. 📝 The bot converts speech → text  
3. 🔍 The system searches your **PDF** for the most relevant information  
4. 🧠 A Hugging Face model summarizes the answer  
5. 🔊 The bot speaks the answer using text-to-speech  

---

## 📁 Project Structure
