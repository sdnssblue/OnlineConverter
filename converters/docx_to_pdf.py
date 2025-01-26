from docx2pdf import convert
import pythoncom

def convert_docx_to_pdf(docx_filepaths):
    converted_files = []
    pythoncom.CoInitialize()
    try:
        for docx_filepath in docx_filepaths:
            if docx_filepath.endswith('.docx'):
                pdf_filepath = docx_filepath.replace('.docx', '.pdf')
                convert(docx_filepath, pdf_filepath)
                converted_files.append(pdf_filepath)
    finally:
        pythoncom.CoUninitialize()
    return converted_files