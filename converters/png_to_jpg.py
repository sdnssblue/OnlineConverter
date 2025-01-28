from PIL import Image
import os

def convert_png_to_jpg(png_filepaths):
    converted_files = []
    for png_filepath in png_filepaths:
        if png_filepath.endswith('.png'):
            jpg_filepath = os.path.splitext(png_filepath)[0] + '.jpg'
            try:
                with Image.open(png_filepath) as img:
                    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                        background = Image.new("RGB", img.size, (255, 255, 255))
                        img = img.convert("RGBA")
                        background.paste(img, mask=img.split()[3])
                        background.save(jpg_filepath, "JPEG")
                    else:
                        img.convert('RGB').save(jpg_filepath, "JPEG")
                converted_files.append(jpg_filepath)
            except Exception as e:
                print(f"Ошибка при конвертации {png_filepath}: {e}")
    return converted_files
