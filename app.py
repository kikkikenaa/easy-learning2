import streamlit as st
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import nltk
import string
from collections import Counter

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Streamlit app
st.title("Easy Learning - Analyze Notes and Exam Papers")

# File uploaders
st.sidebar.header("Upload Files")
notes_file = st.sidebar.file_uploader("Upload your notes (PDF)", type="pdf")
exam_file = st.sidebar.file_uploader("Upload exam papers (PDF)", type="pdf")

# Function to extract text from PDF
def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to preprocess text
def preprocess_text(text):
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Tokenize and remove stopwords
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    return " ".join(filtered_tokens)

# Function to analyze exam papers
def analyze_exam_papers(text):
    # Tokenize sentences
    sentences = sent_tokenize(text)
    # Tokenize words
    words = word_tokenize(text)
    # Count word frequencies
    word_freq = Counter(words)
    # Get the 10 most common words
    most_common = word_freq.most_common(10)
    return most_common

# Function to highlight important areas in notes
def highlight_important_areas(notes_text, important_terms):
    highlighted_text = notes_text
    for term, _ in important_terms:
        highlighted_text = highlighted_text.replace(term, f"**{term}**")
    return highlighted_text

# Main logic
if notes_file is not None and exam_file is not None:
    # Extract text from files
    notes_text = extract_text_from_pdf(notes_file)
    exam_text = extract_text_from_pdf(exam_file)

    # Preprocess text
    cleaned_notes = preprocess_text(notes_text)
    cleaned_exam = preprocess_text(exam_text)

    # Analyze exam papers
    important_terms = analyze_exam_papers(cleaned_exam)
    st.write("Frequently Tested Topics:")
    st.write(important_terms)

    # Highlight important areas in notes
    highlighted_notes = highlight_important_areas(notes_text, important_terms)
    st.write("Highlighted Notes:")
    st.markdown(highlighted_notes)

elif notes_file is not None:
    st.warning("Please upload exam papers to analyze frequently tested topics.")
elif exam_file is not None:
    st.warning("Please upload notes to highlight important areas.")
else:
    st.info("Upload your notes and exam papers to get started.")