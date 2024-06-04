import os
import random
from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import VideoFileClip
from pytube import YouTube
import random

def download_background(id, download_path='video.mp4'):
    
    url = f"https://www.youtube.com/watch?v={id}"
    yt = YouTube(url)

    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

    if not stream:
        print("Error: No suitable progressive MP4 stream found.")
        return
    print(f"Downloading video with resolution: {stream.resolution}") 

    stream.download(filename=download_path)

    random_interval_path = extract_random_interval(download_path) 
    print(f"Random 1-minute interval saved to: {random_interval_path}")

def extract_random_interval(video_path, interval_duration=90, output_path='video.mp4'):
    clip = VideoFileClip(video_path)
    original_width, original_height = clip.size
    target_aspect_ratio = 9/16 

    if original_width / original_height > target_aspect_ratio:
        new_width = int(original_height * target_aspect_ratio)
        new_height = original_height
        x1 = (original_width - new_width) // 2
        y1 = 0
    else:
        new_width = original_width
        new_height = int(original_width / target_aspect_ratio)
        x1 = 0
        y1 = (original_height - new_height) // 2

    video_duration = int(clip.duration)
    if video_duration <= interval_duration:
        print("The video is shorter than or equal to the interval duration.")
        clip.close()
        return None

    start_time = random.randint(0, video_duration - interval_duration)
    end_time = start_time + interval_duration

    random_interval_clip = clip.subclip(start_time, end_time).crop(x1=x1, y1=y1, x2=x1+new_width, y2=y1+new_height) 
    random_interval_clip = random_interval_clip.resize((1080, 1920))
    random_interval_clip.write_videofile(output_path, codec="libx264")

    clip.close()
    random_interval_clip.close()
    print('Made background Video ...')
    return output_path
