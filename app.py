import streamlit as st
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import sent_tokenize
import nltk

# Download NLTK data
nltk.download('punkt')

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

    # Generate summary using TF-IDF
    st.write("Summary:")
    try:
        # Tokenize sentences
        sentences = sent_tokenize(text)
        
        # Check if there are enough sentences to summarize
        if len(sentences) < 3:
            st.warning("The text is too short to generate a meaningful summary.")
        else:
            # Use TF-IDF to score sentences
            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = vectorizer.fit_transform(sentences)
            sentence_scores = tfidf_matrix.sum(axis=1)
            
            # Get top 3 sentences with the highest scores
            top_sentences = [sentences[i] for i in sentence_scores.argsort(axis=0)[-3:]]
            summary = " ".join(top_sentences)
            st.write(summary)
    except Exception as e:
        st.error(f"Error generating summary: {e}")