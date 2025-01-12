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

# Initialize state variables if not already in session
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

if uploaded_file:
    extracted_text = extract_pdf_text(uploaded_file)
    chunks = split_into_chunks(extracted_text)

    if chunks:
        st.write("### PDF Text Chunks")
        
        # Display the current chunk of text
        st.write(f"#### Chunk {st.session_state.current_index + 1}")
        st.write(chunks[st.session_state.current_index])

        # Creating a custom HTML/JS component for swipe navigation
        swipe_js = f"""
        <script>
        let currentIndex = {st.session_state.current_index};
        const chunks = {str(chunks)};
        const output = document.getElementById('output');

        function displayChunk(index) {{
            output.innerHTML = '<h3>Chunk ' + (index + 1) + '</h3><p>' + chunks[index] + '</p>';
        }}

        displayChunk(currentIndex);

        // Detect swipe gestures
        let touchStartY = 0;
        let touchEndY = 0;

        document.body.addEventListener('touchstart', function(e) {{
            touchStartY = e.changedTouches[0].screenY;
        }});

        document.body.addEventListener('touchend', function(e) {{
            touchEndY = e.changedTouches[0].screenY;
            if (touchStartY > touchEndY + 50) {{ // Swipe Down
                if (currentIndex < chunks.length - 1) {{
                    currentIndex++;
                    displayChunk(currentIndex);
                    window.parent.postMessage({{ currentIndex: currentIndex }}, "*");
                }}
            }} else if (touchStartY < touchEndY - 50) {{ // Swipe Up
                if (currentIndex > 0) {{
                    currentIndex--;
                    displayChunk(currentIndex);
                    window.parent.postMessage({{ currentIndex: currentIndex }}, "*");
                }}
            }}
        }});
        </script>
        <style>
        #output {{
            padding: 20px;
            background: #f4f4f9;
            border-radius: 8px;
            height: 300px;
            overflow-y: auto;
        }}
        </style>
        <div id="output"></div>
        """
        
        # Inject custom JS for swipe navigation into Streamlit
        st.markdown(swipe_js, unsafe_allow_html=True)
        
        # Update session state after swipe actions
        if st.session_state.current_index != currentIndex:
            st.session_state.current_index = currentIndex
            st.experimental_rerun()

else:
    st.write("Please upload a PDF file to start reading.")
