import subprocess
import json
import streamlit as st

# Get relevant study content from session state
selected_content = st.session_state.get("selected_content", "")
selected_topics = st.session_state.get("selected_topics", [])

if selected_content and selected_topics:
    # Convert topics to JSON format for passing to scripts
    topics_json = json.dumps([", ".join([word for word, _ in topic]) for topic in selected_topics])

    # Save relevant content to a file (for text-to-speech & video generation)
    with open("selected_content.txt", "w") as f:
        f.write(selected_content)

    # Run animation script
    subprocess.run(["python", "generate_animation.py", topics_json])

    # Run audio script
    subprocess.run(["python", "generate_audio.py", "selected_content.txt"])

    # Merge video & audio
    subprocess.run(["python", "combine_video_audio.py"])

else:
    st.warning("No relevant topics found. Please upload files in the Upload section.")
