import streamlit as st
from PyPDF2 import PdfReader

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

    # Initialize session state variables for navigation if not already initialized
    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0

    if chunks:
        st.write("### PDF Text Chunks")
        
        # Display the current chunk of text
        st.write(f"#### Chunk {st.session_state.current_index + 1}")
        st.write(chunks[st.session_state.current_index])

        # Simulate swipe-up and swipe-down behavior with buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Swipe Up"):
                if st.session_state.current_index > 0:
                    st.session_state.current_index -= 1
                    st.experimental_rerun()

        with col2:
            if st.button("Swipe Down"):
                if st.session_state.current_index < len(chunks) - 1:
                    st.session_state.current_index += 1
                    st.experimental_rerun()

else:
    st.write("Please upload a PDF file to start reading.")
