import streamlit as st
from PyPDF2 import PdfReader

# Streamlit app
st.title("Easy Learning - Upload Your Notes")

# File uploader
uploaded_file = st.file_uploader("Upload your notes (PDF)", type="pdf")

if uploaded_file is not None:
    # Extract text from PDF
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    # Display the extracted text
    st.write("Extracted Text:")
    st.write(text)