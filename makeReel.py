import moviepy.editor as mp
import speech_recognition as sr
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
from moviepy.config import change_settings

IMAGEMAGICK_PATH = r'C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe'
change_settings({'IMAGEMAGICK_BINARY':IMAGEMAGICK_PATH})
video = VideoFileClip("video.mp4")

audio = AudioFileClip("audio.wav")
video = video.set_audio(audio)

recognizer = sr.Recognizer()
with sr.AudioFile("audio.wav") as source:
    audio_data = recognizer.record(source)
    text = recognizer.recognize_google(audio_data)

words = text.split()
chunk_size = 10 
chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

chunk_duration = 5  

subtitle_clips = []
for i, chunk in enumerate(chunks):
    start_time = i * chunk_duration
    end_time = (i + 1) * chunk_duration
    text_clip = TextClip(chunk, fontsize=24, color='white', bg_color='black')
    text_clip = text_clip.set_position(('center', 'bottom')).set_duration(chunk_duration)
    text_clip = text_clip.set_start(start_time)
    subtitle_clips.append(text_clip)

final_video = CompositeVideoClip([video] + subtitle_clips)
a = AudioFileClip('audio.mp3')
final_video.write_videofile("output_video_with_subtitles.mp4", codec="libx264", audio_codec="aac")
