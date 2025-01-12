import streamlit as st
from PyPDF2 import PdfReader
import os

# Function to sanitize the text
def sanitize_text(text):
    return text.encode('utf-8', 'replace').decode('utf-8')

# Function to split the text into chunks
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

# Function to extract text from PDF
def extract_pdf_text(pdf_file):
    reader = PdfReader(pdf_file)
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text()
    return sanitize_text(extracted_text)

# Streamlit UI
st.title("Digestible PDF Reader")
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    extracted_text = extract_pdf_text(uploaded_file)
    chunks = split_into_chunks(extracted_text)

    if chunks:
        st.write("### PDF Text Chunks")
        
        # Add slider to simulate swipe
        current_index = st.slider("Navigate Chunks", 0, len(chunks) - 1, 0, 1)

        # Display the current chunk
        st.write(f"#### Chunk {current_index + 1}")
        st.write(chunks[current_index])

        # Add buttons for swipe navigation (up and down)
        if st.button("Swipe Up"):
            if current_index > 0:
                current_index -= 1
            st.write(f"#### Chunk {current_index + 1}")
            st.write(chunks[current_index])

        if st.button("Swipe Down"):
            if current_index < len(chunks) - 1:
                current_index += 1
            st.write(f"#### Chunk {current_index + 1}")
            st.write(chunks[current_index])

else:
    st.write("Please upload a PDF file to start reading.")
