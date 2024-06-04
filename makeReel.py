from background.background import download_background , extract_random_interval
from scripting.onThisDay import scripting
from scripting.news import makeNews
from voiceover.elevenLabs import elevenlabs
from voiceover.aws_polly import aws_polly
import moviepy.editor as mp
import speech_recognition as sr
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
from moviepy.config import change_settings
import moviepy.editor as mpe
import os

# script = scripting()
script = makeNews('Bollywood news')
# extract_random_interval('u7kdVe8q5zs')
# aws_polly(script)

# os.system("ffmpeg -i audio.mp3 audio.wav") 

# IMAGEMAGICK_PATH = r'C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe'
# change_settings({'IMAGEMAGICK_BINARY':IMAGEMAGICK_PATH})

# def combine_video_and_audio(video_path, audio_path):

#     video = mpe.VideoFileClip(video_path)
#     audio = mpe.AudioFileClip(audio_path)

#     shorter_duration = min(video.duration, audio.duration)
#     video = video.subclip(0, shorter_duration) 
#     audio = audio.subclip(0, shorter_duration) 

#     final_video = video.set_audio(audio)

#     final_video.write_videofile("Final Video.mp4", codec="libx264", audio_codec="aac")

# combine_video_and_audio("video.mp4", "audio.wav")
