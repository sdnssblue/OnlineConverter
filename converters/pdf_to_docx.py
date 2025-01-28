import comtypes.client
import pythoncom
import os

def convert_pdf_to_docx(pdf_filepaths):
    converted_files = []
    pythoncom.CoInitialize()
    try:
        for pdf_filepath in pdf_filepaths:
            if pdf_filepath.endswith('.pdf'):
                # Преобразуем в абсолютный путь
                pdf_filepath = os.path.abspath(pdf_filepath)

                # Проверяем, существует ли файл
                if not os.path.isfile(pdf_filepath):
                    print(f"Файл не найден: {pdf_filepath}")
                    continue

                docx_filepath = pdf_filepath.replace('.pdf', '.docx')
                try:
                    # Инициализируем Word через COM-интерфейс
                    word = comtypes.client.CreateObject('Word.Application')
                    word.Visible = False  # Не показываем GUI Word
                    doc = word.Documents.Open(pdf_filepath)  # Открываем PDF
                    doc.SaveAs(docx_filepath, FileFormat=16)  # Конвертируем в DOCX
                    doc.Close()
                    word.Quit()

                    converted_files.append(docx_filepath)  # Добавляем в список результатов
                except Exception as e:
                    print(f"Ошибка при конвертации {pdf_filepath}: {e}")
    finally:
        pythoncom.CoUninitialize()  # Завершаем COM-сессию
    return converted_files
