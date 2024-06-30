import stable_whisper
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

def subtitle(video_path, model_size="base"):
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
        'color': 'black',    
        'font': 'Arial-Bold',
        'margin': 5,
        'bg_color': 'white',      
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

        caption_text = TextClip(
            finalText, 
            fontsize=caption_style['fontsize'], 
            color=caption_style['color'],
            font=caption_style['font'], 
            method='label',
            bg_color=caption_style['bg_color']
        ).set_position('center')

        caption_border = TextClip(
            finalText, 
            fontsize=caption_style['fontsize'], 
            color=caption_style['border_color'],
            font=caption_style['font'], 
            method='label',
        ).set_position('center')

        caption_border = caption_border.margin(
            left=caption_style['border_width'],
            right=caption_style['border_width'],
            top=caption_style['border_width'],
            bottom=caption_style['border_width']
        ).set_position('center')

        if caption_style['position'] == 'bottom':
            caption_text = caption_text.margin(bottom=caption_style['margin'])
            caption_border = caption_border.margin(bottom=caption_style['margin'])
        else:  
            caption_text = caption_text.margin(top=caption_style['margin'])
            caption_border = caption_border.margin(top=caption_style['margin'])
        
        caption = CompositeVideoClip([caption_border, caption_text])
        caption = caption.set_start(start).set_end(end).set_position('center')

        captions.append(caption)

    video = VideoFileClip(video_path)
    final_video = CompositeVideoClip([video] + captions)
    final_video.write_videofile("output_with_captions.mp4")
