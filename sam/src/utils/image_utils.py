from PIL import Image
import os

def compress_image(file_path, quality=75):
    try:
        img = Image.open(file_path)
        compressed_path = file_path.replace(os.path.splitext(file_path)[1], '_compressed' + os.path.splitext(file_path)[1])
        if img.format == 'GIF': img.save(compressed_path)
        else: img.save(compressed_path, quality=quality)
        return os.path.basename(compressed_path)
    except Exception as e:
        print(f"Erro ao comprimir imagem: {str(e)}")
        return None

def resize_image(file_path, width=None, height=None, percent=50):
    try:
        img = Image.open(file_path)
        resized_path = file_path.replace(os.path.splitext(file_path)[1], '_thumbnail' + os.path.splitext(file_path)[1])
        
        if img.format == 'GIF':
            img.save(resized_path)
        else:
            original_width, original_height = img.size
            
            if not width and not height:
                width = int(original_width * (percent / 100))
                height = int(original_height * (percent / 100))
            elif width and not height:
                height = int((width / float(original_width)) * original_height)
            elif height and not width:
                width = int((height / float(original_height)) * original_width)
            
            resized_img = img.resize((width, height))
            
            resized_img.save(resized_path)
        return os.path.basename(resized_path)
    except Exception as e:
        print(f"Erro ao redimensionar imagem: {str(e)}")
        return None

def crop_and_resize_image(file_path, size=256):
    try:
        img = Image.open(file_path)
        resized_path = file_path.replace(os.path.splitext(file_path)[1], '_croped' + os.path.splitext(file_path)[1])
        
        if img.format == 'GIF':
            img.save(resized_path)
        else:
            width, height = img.size
            min_dim = min(width, height)
            left = (width - min_dim) // 2
            top = (height - min_dim) // 2
            right = (width + min_dim) // 2
            bottom = (height + min_dim) // 2
            img_cropped = img.crop((left, top, right, bottom))
            img_resized = img_cropped.resize((size, size))
            img_resized.save(resized_path)
        return os.path.basename(resized_path)
    except Exception as e:
        print(f"Erro ao processar imagem: {str(e)}")
        return None
