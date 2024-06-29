import os
import requests
import stable_whisper
from voiceover.elevenLabs import elevenlabs
from voiceover.aws_polly import aws_polly
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.config import change_settings
import moviepy.editor as mpe
from background.background import download_background , random_60s_crop
from requests_toolbelt.multipart.encoder import MultipartEncoder

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

def generate_captions(video_path, model_size="base"):
    model = stable_whisper.load_model(model_size)
    result = model.transcribe(
        video_path,
        word_timestamps=True,
        min_word_dur=0.1
    )

    captions = []
    captions = []
    caption_style = {
        'position': 'bottom', 
        'fontsize': 35,
        'color': 'black',      # Text color is white for better contrast
        'font': 'Arial-Bold',
        'margin': 5,
        'bg_color': 'white',       # No background for the main text
        'border_width': 5,
        'border_color': 'white',
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
        # Main text clip (white text)
        caption_text = TextClip(
            finalText, 
            fontsize=caption_style['fontsize'], 
            color=caption_style['color'],
            font=caption_style['font'], 
            method='label',
            bg_color=caption_style['bg_color']
        ).set_position('center')

        # Background clip (semi-transparent black)
        caption_border = TextClip(
            finalText, 
            fontsize=caption_style['fontsize'], 
            color=caption_style['border_color'],
            font=caption_style['font'], 
            method='label',
        ).set_position('center')

        # Apply margin to the border text
        caption_border = caption_border.margin(
            left=caption_style['border_width'],
            right=caption_style['border_width'],
            top=caption_style['border_width'],
            bottom=caption_style['border_width']
        ).set_position('center')

        # Apply margin
        if caption_style['position'] == 'bottom':
            caption_text = caption_text.margin(bottom=caption_style['margin'])
            caption_border = caption_border.margin(bottom=caption_style['margin'])
        else:  
            caption_text = caption_text.margin(top=caption_style['margin'])
            caption_border = caption_border.margin(top=caption_style['margin'])
        
        # Create combined clip with background and text on top
        caption = CompositeVideoClip([caption_border, caption_text])
        caption = caption.set_start(start).set_end(end).set_position('center')

        captions.append(caption)

    video = VideoFileClip(video_path)
    final_video = CompositeVideoClip([video] + captions)
    final_video.write_videofile("output_with_captions.mp4")

def postToIg() :
    print('Posting to IG ...')
    response = requests.post('http://localhost:5000/loginNow')
    try :
        print(response.text)
        print(response.text.success)
    except :
        pass

    if response.status_code == 200 :
        print("Logged into IG ...")
        m = MultipartEncoder(fields={
            'video': ('Final Video.mp4', open('politicalFacts.mp4', 'rb'), 'video/mp4'),
            'image': ('image.jpg', open('image.jpg', 'rb'), 'image/jpeg'),
            'caption' : 'Demo Caption',
        })
        response = requests.post('http://localhost:5000/publishVideo', data=m, headers={'Content-Type': m.content_type})
        print(response.text)
        print("Posted on IG.")
        response = requests.post('http://localhost:5000/publishStoryVideo', data=m, headers={'Content-Type': m.content_type})
        print(response.text)

from scripting.onThisDay import scripting
from scripting.news import makeNews
from scripting.motivation.motivation import motivation
from scripting.worldfacts.wordfacts import worldfacts
from caption.generateCaption import generateCaption

script = scripting()
# script = makeNews('Hollywood news')
# script = motivation()
# script = worldfacts()
# caption = generateCaption(script)

# print(f"Number of words = {len(script.split())} ")

aws_regions = [
    "us-east-2",      # US East (Ohio)
    "us-east-1",      # US East (N. Virginia)
    "us-west-1",      # US West (N. California)
    "us-west-2",      # US West (Oregon)
    "af-south-1",     # Africa (Cape Town)
    "ap-east-1",      # Asia Pacific (Hong Kong)
    "ap-south-1",     # Asia Pacific (Mumbai) 
    "ap-northeast-1",  # Asia Pacific (Tokyo)
    "ap-northeast-2",  # Asia Pacific (Seoul)
    "ap-northeast-3",  # Asia Pacific (Osaka)
    "ap-southeast-1",  # Asia Pacific (Singapore)
    "ap-southeast-2",  # Asia Pacific (Sydney)
    "ap-southeast-3",  # Asia Pacific (Jakarta)
    "ca-central-1",    # Canada (Central)
    "eu-central-1",    # Europe (Frankfurt)
    "eu-west-1",      # Europe (Ireland)
    "eu-west-2",      # Europe (London)
    "eu-west-3",      # Europe (Paris)
    "eu-north-1",     # Europe (Stockholm)
    "eu-south-1",     # Europe (Milan)
    "eu-south-2",     # Europe (Spain)
    "me-south-1",     # Middle East (Bahrain)
    "sa-east-1",      # South America (São Paulo)
    # ... (and any newer regions added by AWS)
]
random_60s_crop('video.mp4')

for aws_region in aws_regions :
    try :
        print(f"Trying {aws_region}")
        aws_polly(script,aws_region)
        break
    except Exception as e:
        print(f"Failed {e}")

os.system("ffmpeg -i audio.mp3 audio.wav") 

combine_video_and_audio("output.mp4", "audio.wav")

generate_captions("Final Video.mp4")

postToIg()