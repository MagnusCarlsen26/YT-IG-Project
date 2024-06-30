from moviepy.editor import VideoFileClip, AudioFileClip

def combineAudioVideo(video_path, audio_path, output_path="Final Video.mp4"):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    shorter_duration = min(video.duration, audio.duration)
    video = video.subclip(0, shorter_duration)
    audio = audio.subclip(0, shorter_duration) 

    final_video = video.set_audio(audio)

    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")