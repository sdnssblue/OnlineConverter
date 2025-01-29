import fitz  # PyMuPDF
import os

def convert_pdf_to_jpg(pdf_filepaths):
    converted_files = []
    
    for pdf_filepath in pdf_filepaths:
        if pdf_filepath.endswith('.pdf'):
            doc = fitz.open(pdf_filepath)
            output_folder = os.path.splitext(pdf_filepath)[0] + "_images"
            os.makedirs(output_folder, exist_ok=True)
            
            for i, page in enumerate(doc):
                images = page.get_images(full=True)
                for img_index, img in enumerate(images):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    img_ext = base_image["ext"]
                    img_filename = os.path.join(output_folder, f"page_{i+1}_img_{img_index+1}.{img_ext}")
                    
                    with open(img_filename, "wb") as f:
                        f.write(image_bytes)

                    converted_files.append(img_filename)

    return converted_files
