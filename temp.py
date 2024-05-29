from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip, concatenate_videoclips
from moviepy.video.tools.subtitles import SubtitlesClip, TextClip
import speech_recognition as sr
import pydub # New library for mp3 handling

# File paths
video_path = "your_video.mp4"
audio_path = "your_audio.mp3"

# Convert mp3 to wav using pydub
sound = pydub.AudioSegment.from_mp3(audio_path)
sound.export("temp_audio.wav", format="wav")

# Load video and audio
video_clip = VideoFileClip(video_path)
audio_clip = VideoFileClip("temp_audio.wav") # Load the converted wav file

def generate_text_clip(txt, duration):
    return TextClip(
        txt, 
        font="Arial", 
        fontsize=24, 
        color="white", 
        bg_color="black", 
        method="caption"  # Ensures it's on a black background
    ).set_position(("center", "bottom")).set_duration(duration)

# Speech-to-Text using speech_recognition
recognizer = sr.Recognizer()
with sr.AudioFile(audio_path) as source:
    audio_data = recognizer.record(source)
    text = recognizer.recognize_google(audio_data)  

# Split the text into lines to match the audio
subtitles = [(text, t) for t in audio_clip.subclip(0, audio_clip.duration).iter_frames(fps=10)]  # Adjust fps as needed
generator = lambda txt: TextClip(txt, font='Arial', fontsize=24, color='white')
subtitles = SubtitlesClip(subtitles, generator)

# Composite video with text and audio
final_clip = CompositeVideoClip([
    video_clip, 
    subtitles.set_position(("center", "bottom")),
]).set_audio(audio_clip)

# Export the final video
final_clip.write_videofile("final_video_with_text.mp4")
