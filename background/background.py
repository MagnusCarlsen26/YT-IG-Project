import random
from pytube import YouTube
import random
import moviepy.editor as mpe
from moviepy.video.fx.crop import crop
import time

def download_background(id, download_path='video.mp4'):
    url = f"https://www.youtube.com/watch?v={id}"
    yt = YouTube(url)

    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

    if not stream:
        print("Error: No suitable progressive MP4 stream found.")
        return

    print(f"Downloading video with resolution: {stream.resolution}")
    stream.download(filename=download_path)
    time.sleep(5)
    random_interval_path = random_60s_crop(download_path)
    print(f"Random 1-minute interval saved to: {random_interval_path}")

def random_60s_crop(video_path, output_path = "output.mp4"):
    video = mpe.VideoFileClip(video_path)

    max_start = max(0, video.duration - 60)
    start_time = random.uniform(0, max_start)
    end_time = start_time + 60

    cropped_video = video.subclip(start_time, end_time)

    w, h = cropped_video.size

    new_w = int(h * 9 / 16)
    if new_w > w:  
        new_h = int(w * 16 / 9)
        new_w = w
    else:
        new_h = h

    x1, y1 = (w - new_w) // 2, (h - new_h) // 2
    x2, y2 = x1 + new_w, y1 + new_h
    final_video = crop(cropped_video, x1=x1, y1=y1, x2=x2, y2=y2)

    final_video.write_videofile(output_path, codec='libx264', audio_codec='aac') 
    video.close()
