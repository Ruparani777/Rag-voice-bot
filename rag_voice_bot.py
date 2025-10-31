import os
import speech_recognition as sr
from gtts import gTTS
import faiss
import numpy as np
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tempfile
import playsound
from transformers import pipeline


def load_pdf(path):
    print("📄 Loading PDF data...")
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def split_text(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_text(text)


def create_vector_store(chunks):
    print("🧠 Creating vector database...")
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    vectors = model.encode(chunks)
    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)
    return index, model


def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak your question...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print("🗣️ You said:", text)
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        return None
    except sr.RequestError:
        print("⚠️ Speech Recognition service unavailable.")
        return None

# -----------------------------

def retrieve_answer(question, model, index, chunks):
    question_vector = model.encode([question])
    D, I = index.search(question_vector, k=3)
    relevant_texts = [chunks[i] for i in I[0]]
    combined = " ".join(relevant_texts)

    print("\n💡 Retrieved relevant text:\n")
    print(combined[:500] + "..." if len(combined) > 500 else combined)

    # Summarize the result for concise answer
    print("\n🧩 Summarizing answer...")
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(combined, max_length=100, min_length=30, do_sample=False)[0]["summary_text"]

    print("\n✅ Final summarized answer:\n", summary)
    return summary



def speak_text(text):
    tts = gTTS(text=text, lang="en")

    # Detect user's Desktop path 
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    output_path = os.path.join(desktop_path, "tts_output.mp3")

    os.makedirs(desktop_path, exist_ok=True)

    #  output
    tts.save(output_path)
    print(f"🔊 Speaking answer... ({output_path})")
    playsound.playsound(output_path)


def main():
    print("🤖 Initializing Offline RAG Voice Bot...")
    pdf_path = r"C:\Users\gopic\OneDrive\Desktop\Sample_data.pdf"

    pdf_text = load_pdf(pdf_path)
    chunks = split_text(pdf_text)
    index, model = create_vector_store(chunks)

    question = recognize_speech()
    if question:
        answer = retrieve_answer(question, model, index, chunks)
        speak_text(answer)
    else:
        print("⚠️ No question detected. Please try again.")

if __name__ == "__main__":
    main()
