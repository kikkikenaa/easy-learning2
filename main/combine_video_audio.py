import imageio_ffmpeg as ffmpeg
import subprocess
import os
import shutil

def merge_video_audio(video_path, audio_path, output_path):
    """
    Merges a video file with an audio file using imageio_ffmpeg.

    Parameters:
    video_path (str): Path to the video file (MP4, AVI, etc.).
    audio_path (str): Path to the audio file (MP3, WAV, etc.).
    output_path (str): Path to save the final output video.
    """
    # Check if FFmpeg is installed
    ffmpeg_path = ffmpeg.get_ffmpeg_exe() or shutil.which("ffmpeg")
    if not ffmpeg_path:
        print("❌ Error: FFmpeg is not installed. Install it first.")
        return

    # Check if video and audio files exist
    if not os.path.exists(video_path):
        print(f"❌ Error: Video file '{video_path}' not found.")
        return
    if not os.path.exists(audio_path):
        print(f"❌ Error: Audio file '{audio_path}' not found.")
        return

    # FFmpeg command
    command = [
        ffmpeg_path, "-i", video_path, "-i", audio_path,
        "-c:v", "copy", "-c:a", "aac", "-strict", "experimental",
        output_path
    ]
    
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"✅ Successfully merged {video_path} and {audio_path} into {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print("Make sure imageio[ffmpeg] is installed correctly.")

# Example usage
if __name__ == "__main__":
    merge_video_audio("video.mp4", "audio.mp3", "output.mp4")
