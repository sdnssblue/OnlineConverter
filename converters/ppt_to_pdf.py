import comtypes.client
import pythoncom
import os

def convert_ppt_to_pdf(ppt_filepaths):
    converted_files = []
    pythoncom.CoInitialize()  # Инициализация COM
    try:
        powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
        powerpoint.Visible = 1  # Делаем приложение видимым (1 - да, 0 - нет)

        for ppt_filepath in ppt_filepaths:
            if ppt_filepath.endswith(('.ppt', '.pptx')):
                ppt_filepath = os.path.abspath(ppt_filepath)  # Преобразуем путь в абсолютный
                pdf_filepath = os.path.splitext(ppt_filepath)[0] + '.pdf'
                try:
                    presentation = powerpoint.Presentations.Open(ppt_filepath, WithWindow=False)
                    presentation.SaveAs(pdf_filepath, 32)  # 32 - формат PDF
                    presentation.Close()
                    converted_files.append(pdf_filepath)
                except Exception as e:
                    print(f"Ошибка при конвертации {ppt_filepath}: {e}")
        powerpoint.Quit()
    finally:
        pythoncom.CoUninitialize()  # Завершаем COM-сессию
    return converted_files
