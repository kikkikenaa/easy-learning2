import streamlit as st
from PyPDF2 import PdfReader
import nltk
import string
from collections import Counter
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

st.title("Easy Learning - Analyze Notes and Exam Papers")

# Retrieve uploaded files from session state
notes_files = st.session_state.get("notes_files", [])
exam_files = st.session_state.get("exam_files", [])

# Function to extract text from PDFs
def extract_text_from_pdf(files):
    text = ""
    for file in files:
        try:
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as e:
            st.error(f"Error reading {file.name}: {e}")
    return text.strip()

# Function to preprocess text
def preprocess_text(text):
    if not text:
        return ""

    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    text = ''.join([char for char in text if not char.isdigit()])  # Remove numbers

    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]

    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]

    return " ".join(lemmatized_tokens)

# Function to extract key topics from exam papers
def extract_topics(text):
    if not text:
        return []

    vectorizer = CountVectorizer(stop_words="english")
    topic_model = BERTopic(vectorizer_model=vectorizer)

    sentences = sent_tokenize(text)
    topics, probs = topic_model.fit_transform(sentences)
    
    topic_freq = topic_model.get_topic_freq()
    top_topics = topic_freq['Topic'][1:6]  # Get top 5 topics (excluding -1 which is noise)

    return [topic_model.get_topic(topic) for topic in top_topics]

# Function to find relevant content in notes based on most tested topics
def extract_relevant_notes(notes_text, key_topics):
    relevant_sentences = []
    sentences = sent_tokenize(notes_text)

    # Check if sentences in notes contain the most tested topics
    for sentence in sentences:
        for topic in key_topics:
            for term, _ in topic:
                if term in sentence:
                    relevant_sentences.append(sentence)
                    break  # Move to the next sentence after finding a match

    return " ".join(relevant_sentences)

# Process uploaded files
if notes_files and exam_files:
    st.write("Processing files...")

    # Extract text from PDFs
    notes_text = extract_text_from_pdf(notes_files)
    exam_text = extract_text_from_pdf(exam_files)

    # Preprocess text
    cleaned_notes = preprocess_text(notes_text)
    cleaned_exam = preprocess_text(exam_text)

    # Extract key topics
    key_topics = extract_topics(cleaned_exam)

    if key_topics:
        st.subheader("Frequently Tested Topics:")
        for i, topic in enumerate(key_topics):
            st.write(f"Topic {i+1}: {', '.join([word for word, _ in topic])}")

        # Extract only relevant content from notes
        relevant_notes = extract_relevant_notes(notes_text, key_topics)

        # Display relevant content
        st.subheader("Relevant Study Areas from Notes:")
        st.markdown(relevant_notes, unsafe_allow_html=True)

        # Store for video & audio generation
        st.session_state["selected_content"] = relevant_notes
        st.session_state["selected_topics"] = key_topics
    else:
        st.warning("No significant topics detected in exam papers.")

elif not notes_files and not exam_files:
    st.warning("Please upload your files in the Upload section first.")
