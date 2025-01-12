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
        
        # Use a markdown block to insert custom JS for swipe functionality
        swipe_js = """
        <script>
        let currentIndex = 0;
        const chunks = %s;  // This will be the chunks of text as an array.
        const output = document.getElementById('output');

        function displayChunk(index) {
            output.innerHTML = '<h3>Chunk ' + (index + 1) + '</h3><p>' + chunks[index] + '</p>';
        }

        displayChunk(currentIndex);

        // Swipe Up and Swipe Down event listeners
        let touchStartY = 0;
        let touchEndY = 0;

        document.body.addEventListener('touchstart', function(e) {
            touchStartY = e.changedTouches[0].screenY;
        });

        document.body.addEventListener('touchend', function(e) {
            touchEndY = e.changedTouches[0].screenY;
            if (touchStartY > touchEndY + 50) { // Swipe Down
                if (currentIndex < chunks.length - 1) {
                    currentIndex++;
                    displayChunk(currentIndex);
                }
            } else if (touchStartY < touchEndY - 50) { // Swipe Up
                if (currentIndex > 0) {
                    currentIndex--;
                    displayChunk(currentIndex);
                }
            }
        });
        </script>
        """ % (str(chunks))  # Insert the chunks of text in JavaScript

        st.markdown(swipe_js, unsafe_allow_html=True)

        # Create an output div where the chunks will be displayed
        st.markdown('<div id="output"></div>', unsafe_allow_html=True)

else:
    st.write("Please upload a PDF file to start reading.")
