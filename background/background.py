import os
import random
from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip

def download_background(id, download_path='video.mp4'):
    url = f"https://www.youtube.com/watch?v={id}"  
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    stream.download(filename=download_path)
    random_interval_path = extract_random_interval(download_path)
    print(f"Random 1-minute interval saved to: {random_interval_path}")


def extract_random_interval(video_path, interval_duration=60, output_path='background.mp4'):
    clip = VideoFileClip(video_path)
    video_duration = int(clip.duration)
    
    if video_duration <= interval_duration:
        print("The video is shorter than or equal to the interval duration.")
        return None

    start_time = random.randint(0, video_duration - interval_duration)
    end_time = start_time + interval_duration

    random_interval_clip = clip.subclip(start_time, end_time)
    random_interval_clip.write_videofile(output_path, codec="libx264")
    
    clip.close()
    random_interval_clip.close()
    
    return output_path

