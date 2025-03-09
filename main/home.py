import streamlit as st

st.title("Welcome to Easy Learning")

st.write(
    "This app helps you analyze your study materials. Start by uploading your files on the 'Upload Files' page."
)

st.sidebar.header("Navigation")
st.sidebar.page_link("pages/1_Upload_Files.py", label="Upload Files", icon="📂")
st.sidebar.page_link("pages/2_Analyze_Files.py", label="Analyze Files", icon="📊")
