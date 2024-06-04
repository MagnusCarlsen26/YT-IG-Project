import googleapiclient.discovery
from pytube import YouTube
from moviepy.editor import VideoFileClip, concatenate_videoclips
import random
import os
from dotenv import load_dotenv,dotenv_values

load_dotenv()

def download_and_edit_shorts(query , num_shorts=10):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=os.getenv('YT_API'))

    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        videoDuration="short",
        maxResults=num_shorts
    )
    response = request.execute()

    clips = []
    for item in response["items"]:
        video_id = item["id"]["videoId"]
        video_url = f"https://www.youtube.com/shorts/{video_id}"

        try:
            yt = YouTube(video_url)
            stream = yt.streams.get_highest_resolution()
            file_path = stream.download(output_path="shorts/")
            clip = VideoFileClip(file_path)

            start_time = random.uniform(0, max(0, clip.duration - 5))  
            end_time = min(clip.duration, start_time + 5) 
            clip = clip.subclip(start_time, end_time)

            clips.append(clip)
        except Exception as e:
            print(f"Error downloading/editing {video_url}: {e}")

    print('All shorts downloaded ...')

    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile("stitched_shorts.mp4")

    print('Shorts are Stiched ...')

