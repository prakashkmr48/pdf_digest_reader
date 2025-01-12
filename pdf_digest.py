import streamlit as st
from PyPDF2 import PdfReader
import os

def sanitize_text(text):
    return text.encode('utf-8', 'replace').decode('utf-8')

def split_into_chunks(text, chunk_size=500):
    words = text.split()
    chunks = []
    current_chunk = []
    for word in words:
        current_chunk.append(word)
        if len(" ".join(current_chunk)) >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def extract_pdf_text(pdf_file):
    reader = PdfReader(pdf_file)
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text()
    return sanitize_text(extracted_text)

st.title("Digestible PDF Reader")
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    extracted_text = extract_pdf_text(uploaded_file)
    chunks = split_into_chunks(extracted_text)

    if chunks:
        st.write("### PDF Text Chunks")
        for i, chunk in enumerate(chunks):
            st.write(f"#### Chunk {i + 1}")
            st.write(chunk)

else:
    st.write("Please upload a PDF file to start reading.")
