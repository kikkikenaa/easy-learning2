from gtts import gTTS

def generate_audio(text_file, output_file="topics_audio.mp3"):
    try:
        with open(text_file, "r") as f:
            text = f.read()

        tts = gTTS(text=text, lang="en")
        tts.save(output_file)
        print(f"Audio saved as {output_file}")

    except Exception as e:
        print(f"Error generating audio: {e}")

if __name__ == "__main__":
    generate_audio("selected_content.txt")
