import os
import requests
import random
from dotenv import load_dotenv
from utility import Gemini,toMarkdown
from voiceover.elevenLabs import elevenlabs
from voiceover.aws_polly import aws_polly
from moviepy.config import change_settings
from background.background import download_background , random_60s_crop
from requests_toolbelt.multipart.encoder import MultipartEncoder
from video.addBgMusic import addBgMusic
from video.combineAudioVideo import combineAudioVideo
from video.subtitle import subtitle
from video.thumbnail import thumbnail

load_dotenv()

IMAGEMAGICK_PATH = r'C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe'
change_settings({'IMAGEMAGICK_BINARY':IMAGEMAGICK_PATH})

def postToIg(username,caption,videoPath,imagePath) :
    print('Posting to IG ...')
    response = requests.post('http://localhost:5000/loginNow',json = {            'username' : "reddit."+username,
            'password' : os.getenv("reddit."+username)})

    data = response.json()
    print(data)
    if response.status_code == 200 and data['success']:
        print("Logged into IG ...")
        m = MultipartEncoder(fields={
            'video': ('Final Video.mp4', open(videoPath, 'rb'), 'video/mp4'),
            'image': ('image.jpg', open(imagePath, 'rb'), 'image/jpeg'),
            'caption' : caption,
        })
        response = requests.post('http://localhost:5000/publishVideo', data=m, headers={'Content-Type': m.content_type})
        print(response.text)
        print("Posted on IG...")
        # response = requests.post('http://localhost:5000/publishStoryVideo', data=m, headers={'Content-Type': m.content_type})
        # print(response.text)


from scripting.onThisDay import scripting
from scripting.news import makeNews
from scripting.motivation import motivation
from scripting.wordfacts import worldfacts
from scripting.reddit import get_subreddit_threads
from caption.redditCaption import generateCaption

igAccounts = {
    'askfeminists' : 'AskFeminists',
    'askwomen' : 'AskWomen',
    'askmen' : 'AskMen' 
}

bg = [
    'assets/bg/csgo.mp4',
    'assets/bg/gta.mp4',
    'assets/bg/minecraft.mp4',
    'assets/bg/minecraft2.mp4'
]

thumbnailImgs = [
    r'assets/thumbnails/csgo.jpg',
    r'assets/thumbnails/gta.jpg',
    r'assets/thumbnails/minecraft.jpg',
    r'assets/thumbnails/minecraft2.jpg'
]

music = [
    'assets/music/1.mp3',
    'assets/music/2.mp3',
    'assets/music/3.mp3',
    'assets/music/4.mp3',
    'assets/music/5.mp3',
]

for igAccount in igAccounts :
    
    subreddit = igAccounts[igAccount]
    content = get_subreddit_threads(subreddit)
    caption = generateCaption(content['title'],subreddit)
    script = content['title'] +  '.' + '\n' + '\n' + content['comment'] + '. Follow for more. Thankyou.'

    print(f"Number of words = {len(script.split())} ")

    randomBg = random.randint(0,len(bg)-1)
    random_60s_crop(bg[randomBg])

    aws_polly(script)

    os.system("ffmpeg -i audio.mp3 audio.wav") 

    combineAudioVideo("output.mp4", "audio.wav")

    subtitle("Final Video.mp4")

    randomMusic = random.randint(0,len(music) -1)
    addBgMusic("output_with_captions.mp4",music[randomMusic] )

    thumbnail(thumbnailImgs[randomBg], text=content['title'] , font_size=32)

    postToIg(igAccount,caption,"final_video_with_music.mp4",'thumbnail.jpg')
    os.remove("audio.mp3")
    os.remove("audio.wav")
    os.remove("output.mp4")
    os.remove("output_with_captions.mp4")
    os.remove("Final Video.mp4")
    os.remove("thumbnail.jpg")