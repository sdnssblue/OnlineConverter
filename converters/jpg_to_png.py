from PIL import Image
import os

def convert_jpg_to_png(jpg_filepaths):
    converted_files = []
    for jpg_filepath in jpg_filepaths:
        if jpg_filepath.lower().endswith(('.jpg', '.jpeg')):
            png_filepath = os.path.splitext(jpg_filepath)[0] + '.png'
            try:
                with Image.open(jpg_filepath) as img:
                    img.save(png_filepath, format='PNG')
                converted_files.append(png_filepath)
            except Exception as e:
                print(f"Ошибка при конвертации {jpg_filepath}: {e}")
    return converted_files
