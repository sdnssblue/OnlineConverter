import os
import re
import uuid
from flask import session

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'docx', 'pdf', 'jpg', 'jpeg', 'png', 'ppt', 'pptx'}


# Проверка допустимых форматов
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Генерация безопасного имени файла
def secure_filename_custom(filename):
    return re.sub(r'[^а-яА-Яa-zA-Z0-9_.-]', '_', filename)


# Получение уникальной папки пользователя
def get_user_folder():
    session_id = session.get('session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
    user_folder = os.path.join(UPLOAD_FOLDER, session_id)
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    return user_folder


# Загрузка файлов
def handle_uploaded_files(uploaded_files, user_folder):
    file_paths = []
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename_custom(file.filename)
            path = os.path.join(user_folder, filename)
            file.save(path)
            file_paths.append(path)
    return file_paths


# Удаление оригинальных файлов после конвертации
def delete_original_files(file_paths):
    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)
