import streamlit as st
from PyPDF2 import PdfReader
from transformers import pipeline

# Load summarization pipeline
summarizer = pipeline("summarization")

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

    # Generate summary
    st.write("Summary:")
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    st.write(summary[0]['summary_text'])