import nltk

def download_nltk_package():
    """
    Downloads the 'punkt' tokenizer if not already available.
    """
    try:
        nltk.data.find('tokenizers/punkt')  # Check if 'punkt' is already downloaded
        print("✅ 'punkt' tokenizer is already installed.")
    except LookupError:
        print("📥 Downloading 'punkt' tokenizer...")
        nltk.download('punkt')
        print("✅ Download complete.")

if __name__ == "__main__":
    download_nltk_package()
