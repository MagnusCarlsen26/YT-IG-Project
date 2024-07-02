from PIL import Image, ImageDraw, ImageFont, ImageOps

def thumbnail(image_path, text, font_size=24, text_color=(0, 0, 0), background_color=(255, 255, 255), margin=10, border_width=5):
    try:
        finalText = ''
        chars = 0
        for word in text.split():
            if chars + len(word) > 25:
                finalText += '\n'
                chars = 0
            finalText += ' '
            finalText += word
            chars += len(word)
        text = finalText
        with Image.open(image_path) as img:
            target_width = 9
            target_height = 16

            width, height = img.size
            if width / height > target_width / target_height:
                new_width = int(height * target_width / target_height)
                new_height = height
                left = (width - new_width) // 2
                top = 0
                right = left + new_width
                bottom = height
            else:
                new_width = width
                new_height = int(width * target_height / target_width)
                left = 0
                top = (height - new_height) // 2
                right = width
                bottom = top + new_height

            img_with_text = img.crop((left, top, right, bottom))
            img_with_text = img_with_text.resize((new_width, new_height))

            img_with_text = ImageOps.expand(img_with_text, border=border_width, fill=(0, 0, 0))  

            draw = ImageDraw.Draw(img_with_text)
            font = ImageFont.truetype("arial.ttf", font_size)

            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            x = (img_with_text.width - text_width) // 2
            y = (img_with_text.height - text_height) // 2

            draw.rectangle((x - margin, y - margin, x + text_width + margin, y + text_height + margin), fill=background_color)

            draw.text((x, y), text, text_color, font=font)
            img_with_text.save("thumbnail.jpg")
    except Exception as e:
        print(f"Cannot create thumbnail for {image_path}")
        print(e)
