# File Converter Web Service - Updated for Dynamic File Conversion

# Directory Structure:
# /file_converter_project
# ├── app.py          # Main entry point for the backend
# ├── static/         # Static files for frontend (CSS, JS)
# ├── templates/      # HTML templates
# ├── converters/     # File conversion logic modules
# │   ├── docx_to_pdf.py
# ├── uploads/        # Temporary storage for uploaded files
# └── requirements.txt # Dependencies

# app.py (Backend using Flask)
from flask import Flask, request, render_template, send_file, session
from converters.docx_to_pdf import convert_docx_to_pdf
from converters.pdf_to_docx import convert_pdf_to_docx
import os
import uuid
import time
import shutil
import zipfile
import tempfile

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'docx', 'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'supersecretkey'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def secure_filename_custom(filename):
    import re
    filename = re.sub(r'[^а-яА-Яa-zA-Z0-9_.-]', '_', filename)
    return filename

def get_user_folder():
    session_id = session.get('session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    return user_folder

@app.before_request
def clean_up_old_folders():
    max_age_seconds = 30
    current_time = time.time()
    for folder_name in os.listdir(UPLOAD_FOLDER):
        folder_path = os.path.join(UPLOAD_FOLDER, folder_name)
        if os.path.isdir(folder_path):
            last_modified = os.path.getmtime(folder_path)
            if current_time - last_modified > max_age_seconds:
                try:
                    shutil.rmtree(folder_path)
                except Exception as e:
                    print(f"Error deleting folder {folder_path}: {e}")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/convert-docx-to-pdf', methods=['GET', 'POST'])
def docx_to_pdf_page():
    user_folder = get_user_folder()
    if request.method == 'POST':
        uploaded_files = request.files.getlist('files')
        docx_paths = []

        for file in uploaded_files:
            if file and allowed_file(file.filename):
                filename = secure_filename_custom(file.filename)
                path = os.path.join(user_folder, filename)
                file.save(path)
                docx_paths.append(path)

        pdf_paths = convert_docx_to_pdf(docx_paths)
        
        # Удаление оригиналов после конвертации
        for docx_path in docx_paths:
            if os.path.exists(docx_path):
                os.remove(docx_path)
        
        if pdf_paths:
            return render_template('download.html', files=pdf_paths)
    return render_template('docx_to_pdf.html')

@app.route('/convert-pdf-to-docx', methods=['GET', 'POST'])
def pdf_to_docx_page():
    user_folder = get_user_folder()
    if request.method == 'POST':
        uploaded_files = request.files.getlist('files')
        pdf_paths = []

        for file in uploaded_files:
            if file and allowed_file(file.filename):
                filename = secure_filename_custom(file.filename)
                path = os.path.join(user_folder, filename)
                file.save(path)
                pdf_paths.append(path)

        docx_paths = convert_pdf_to_docx(pdf_paths)
        
        # Удаление оригиналов после конвертации
        for pdf_path in pdf_paths:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
        
        if docx_paths:
            return render_template('download.html', files=docx_paths)
    return render_template('pdf_to_docx.html')

@app.route('/uploads/<filename>')
def download_file(filename):
    user_folder = get_user_folder()
    file_path = os.path.join(user_folder, filename)
    if os.path.isfile(file_path):
        response = send_file(file_path, as_attachment=True, download_name=filename)
        response.headers["Content-Disposition"] = f"attachment; filename*=UTF-8''{filename}"
        return response
    else:
        return "File not found.", 404

@app.route('/download-all')
def download_all():
    user_folder = get_user_folder()
    files = os.listdir(user_folder)
    if len(files) == 1:
        file_path = os.path.join(user_folder, files[0])
        return send_file(file_path, as_attachment=True)

    temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
    with zipfile.ZipFile(temp_zip.name, 'w') as zipf:
        for filename in files:
            file_path = os.path.join(user_folder, filename)
            if os.path.isfile(file_path):
                zipf.write(file_path, arcname=filename)
    return send_file(temp_zip.name, as_attachment=True, download_name='converted_files.zip')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
