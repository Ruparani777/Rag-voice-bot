# Rag-voice-bot
# 🎙️ RAG Voice Bot

## 🧠 Overview
This project is an **Retrieval-Augmented Generation (RAG) Voice Bot**

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

Rag-voice-bot/
1. rag_voice_bot.py # Main voice bot script
2. Sample_data.pdf # 
3.README.md # Project documentation
4.Output pdf 

---

## 🧰 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Ruparani777/Rag-voice-bot.git
   cd Rag-voice-bot


2.Install the dependencies:
pip install SpeechRecognition pyaudio gtts playsound langchain langchain-community faiss-cpu PyPDF2 sentence-transformers transformers


🚀 Run the Bot
python rag_voice_bot.py

🤖 Initializing Offline RAG Voice Bot...
🎤 Speak your question...
🗣️ You said: what is artificial intelligence

💡 Retrieved relevant text:
Artificial Intelligence (AI) refers to the simulation of human intelligence in machines...

🔊 Speaking answer...


Author

Ruparani Thupakula
roopathupakula01@gmail.com


---

### 🧩 Step 3: Commit the README
- Scroll down → select **“Commit directly to the main branch”**
- Click the green **“Commit new file”** button ✅

---

### 🧩 Step 4: Verify
Now your repository page will automatically show your new README beautifully formatted! 🎉  

---


