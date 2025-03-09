from moviepy.editor import TextClip, CompositeVideoClip, VideoClip
from moviepy.video.fx.all import fadein, fadeout
import json

def generate_topic_animation(topics, output_file="topics_animation.mp4"):
    """
    Generates a text-based animation from a list of topics.
    
    Parameters:
    topics (list): List of topic strings to display.
    output_file (str): Name of the output video file.
    """
    clips = []
    duration_per_topic = 3  # Each topic appears for 3 seconds

    for i, topic in enumerate(topics):
        text = TextClip(topic, fontsize=70, color="white", size=(1280, 720))
        text = text.set_duration(duration_per_topic).fadein(1).fadeout(1)
        text = text.set_position("center")

        clips.append(text)

    # Combine all text clips
    final_clip = CompositeVideoClip(clips)
    
    # Write to a file
    final_clip.write_videofile(output_file, fps=24)
    print(f"✅ Animation saved as {output_file}")

# If run as a script
if __name__ == "__main__":
    import sys
    
    # Read topics from command-line argument (JSON string)
    topics = json.loads(sys.argv[1])  
    generate_topic_animation(topics)
