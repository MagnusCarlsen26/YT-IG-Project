from moviepy.editor import VideoFileClip, AudioFileClip,CompositeAudioClip

def addBgMusic(video_path, background_music_path, output_path="final_video_with_music.mp4"):
    video_clip = VideoFileClip(video_path)
    original_audio = video_clip.audio  # Extract original audio
    background_music = AudioFileClip(background_music_path)

    background_music = background_music.subclip(0, video_clip.duration)
    background_music = background_music.volumex(0.3) 

    final_audio = CompositeAudioClip([original_audio, background_music])

    final_video = video_clip.set_audio(final_audio)

    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")