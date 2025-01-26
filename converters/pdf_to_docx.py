from pdf2docx import Converter
import os

def convert_pdf_to_docx(pdf_filepaths):
    converted_files = []
    for pdf_filepath in pdf_filepaths:
        if pdf_filepath.endswith('.pdf'):
            docx_filepath = os.path.splitext(pdf_filepath)[0] + '.docx'
            try:
                converter = Converter(pdf_filepath)
                converter.convert(docx_filepath, start=0, end=None, multi_processing=True)
                converter.close()
                converted_files.append(docx_filepath)
            except Exception as e:
                print(f"Ошибка конвертации {pdf_filepath}: {e}")
    return converted_files

