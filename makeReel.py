from background.background import download_background , random_60s_crop
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
# # script = makeNews('Bollywood news')
# print(len(script.split()))
# random_60s_crop('video.mp4')
# aws_polly(script)

# os.system("ffmpeg -i audio.mp3 audio.wav") 

IMAGEMAGICK_PATH = r'C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe'
change_settings({'IMAGEMAGICK_BINARY':IMAGEMAGICK_PATH})

def combine_video_and_audio(video_path, audio_path):

    video = mpe.VideoFileClip(video_path)
    audio = mpe.AudioFileClip(audio_path)

    shorter_duration = min(video.duration, audio.duration)
    video = video.subclip(0, shorter_duration) 
    audio = audio.subclip(0, shorter_duration) 

    final_video = video.set_audio(audio)

    final_video.write_videofile("Final Video.mp4", codec="libx264", audio_codec="aac")

# combine_video_and_audio("output.mp4", "audio.wav")

import stable_whisper
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

def generate_captions(video_path, model_size="base"):
    model = stable_whisper.load_model(model_size)
    result = model.transcribe(
        video_path, 
        word_timestamps=True,
        min_word_dur=0.1  
    )

    captions = []
    caption_style = {
        'position': 'bottom', 
        'fontsize': 15,
        'color': 'white',      # Text color is white for better contrast
        'font': 'Arial-Bold',
        'margin': 5,
        'bg_color': None,       # No background for the main text
        'border_width': 5,
        'border_color': 'black',
    }

    for segment in result.segments:
        start, end, text = segment.start, segment.end, segment.text
        finalText = ''
        chars = 0
        for word in text.split():
            if chars + len(word) > 25:
                finalText += '\n'
                chars = 0
            finalText += ' '
            finalText += word
            chars += len(word)

        # Main text clip
        caption_text = TextClip(
            finalText, 
            fontsize=caption_style['fontsize'], 
            color=caption_style['color'],
            font=caption_style['font'], 
            method='label'
        )

        # Border text clip
        caption_border = TextClip(
            finalText, 
            fontsize=caption_style['fontsize'], 
            color=caption_style['border_color'],
            font=caption_style['font'], 
            method='label',
        )

        # Apply margin to the border text
        caption_border = caption_border.margin(
            left=caption_style['border_width'],
            right=caption_style['border_width'],
            top=caption_style['border_width'],
            bottom=caption_style['border_width']
        )

        # Set the position of both text clips
        combined_clip = CompositeVideoClip([caption_border, caption_text])
        combined_clip = combined_clip.set_start(start).set_end(end).set_position('center')

        caption_text = caption_text.set_start(start).set_end(end).set_position('center')
        caption_border = caption_border.set_start(start).set_end(end).set_position('center')

        # Apply margin based on 'position' to both text clips
        if caption_style['position'] == 'bottom':
            combined_clip = combined_clip.margin(bottom=caption_style['margin'])
        else:
            combined_clip = combined_clip.margin(top=caption_style['margin'])

        # Combine the border and text clips to form the final caption
        final_caption = CompositeVideoClip([caption_border, caption_text])
        captions.append(final_caption)

    video = VideoFileClip(video_path)
    final_video = CompositeVideoClip([video] + captions)
    final_video.write_videofile("output_with_captions.mp4")


generate_captions("Final Video.mp4")
