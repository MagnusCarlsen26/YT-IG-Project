from background.background import download_background
from scripting.onThisDay import scripting
from voiceover.texttospeech import generate_speech
import moviepy.editor as mp
import speech_recognition as sr
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
from moviepy.config import change_settings

# !ffmpeg -i audio.mp3 audio.wav


IMAGEMAGICK_PATH = r'C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe'
change_settings({'IMAGEMAGICK_BINARY':IMAGEMAGICK_PATH})

def create_video_with_subtitles(video_path, audio_path):

    try:
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        return

    video = video.set_audio(audio)

    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            print("Error: Audio could not be understood")
            return
        except sr.RequestError as e:
            print(f"Error: Could not request results from Google Speech Recognition service; {e}")
            return

    words = text.split()
    chunk_size = 10 
    chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    chunk_duration = 5  

    text_position = ('center', video.h - 100) 

    def generate_text_clip(txt):
        return TextClip(
            txt, 
            fontsize=24, 
            color='white', 
            bg_color='black', 
            font='Arial-Bold',  
            stroke_color='black',  
            stroke_width=1
        )

    subtitle_clips = []
    for i, chunk in enumerate(chunks):
        start_time = i * chunk_duration
        end_time = (i + 1) * chunk_duration
        text_clip = generate_text_clip(chunk)
        text_clip = text_clip.set_position(text_position).set_duration(chunk_duration)
        text_clip = text_clip.set_start(start_time).crossfadein(0.5).crossfadeout(0.5) 
        subtitle_clips.append(text_clip)

    final_video = CompositeVideoClip([video] + subtitle_clips)
    final_video.write_videofile("output_video_with_subtitles.mp4", codec="libx264", audio_codec="aac")


if __name__ == "__main__":
    create_video_with_subtitles("video.mp4", "audio.wav")
