import streamlit as st
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import nltk
import string
import spacy
from transformers import pipeline

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load Hugging Face summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

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

    # Step 1: Preprocess the text
    def preprocess_text(text):
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        # Tokenize and remove stopwords
        tokens = word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
        return " ".join(filtered_tokens)

    cleaned_text = preprocess_text(text)
    st.write("Cleaned Text:")
    st.write(cleaned_text)

    # Step 2: Identify key topics using TF-IDF
    st.write("Key Topics:")
    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([cleaned_text])
        feature_names = vectorizer.get_feature_names_out()
        tfidf_scores = tfidf_matrix.toarray()[0]

        # Get top 10 important terms
        top_terms = [feature_names[i] for i in tfidf_scores.argsort()[-30:]]
        st.write(top_terms)
    except Exception as e:
        st.error(f"Error extracting key topics: {e}")

    # Step 3: Summarize the content using Hugging Face
    st.write("Advanced Summary:")
    try:
        summary = summarizer(text, max_length=1130, min_length=300, do_sample=False)
        st.write(summary[0]['summary_text'])
    except Exception as e:
        st.error(f"Error generating summary: {e}")