import os
import time
import shutil
import zipfile
import tempfile
from flask import Flask, request, render_template, send_file
from converters.docx_to_pdf import convert_docx_to_pdf
from converters.pdf_to_docx import convert_pdf_to_docx
from converters.ppt_to_pdf import convert_ppt_to_pdf
from converters.jpg_to_png import convert_jpg_to_png
from converters.png_to_jpg import convert_png_to_jpg
from utils.file_utils import (
    get_user_folder,
    handle_uploaded_files,
    delete_original_files,
)

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'supersecretkey'


# Удаление старых папок
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
        docx_paths = handle_uploaded_files(uploaded_files, user_folder)
        pdf_paths = convert_docx_to_pdf(docx_paths)
        delete_original_files(docx_paths)
        if pdf_paths:
            return render_template('download.html', files=pdf_paths)
    return render_template('docx_to_pdf.html')


@app.route('/convert-ppt-to-pdf', methods=['GET', 'POST'])
def ppt_to_pdf_page():
    user_folder = get_user_folder()
    if request.method == 'POST':
        uploaded_files = request.files.getlist('files')
        ppt_paths = handle_uploaded_files(uploaded_files, user_folder)
        pdf_paths = convert_ppt_to_pdf(ppt_paths)
        delete_original_files(ppt_paths)
        if pdf_paths:
            return render_template('download.html', files=pdf_paths)
    return render_template('ppt_to_pdf.html')


@app.route('/convert-pdf-to-docx', methods=['GET', 'POST'])
def pdf_to_docx_page():
    user_folder = get_user_folder()
    if request.method == 'POST':
        uploaded_files = request.files.getlist('files')
        pdf_paths = handle_uploaded_files(uploaded_files, user_folder)
        docx_paths = convert_pdf_to_docx(pdf_paths)
        delete_original_files(pdf_paths)
        if docx_paths:
            return render_template('download.html', files=docx_paths)
    return render_template('pdf_to_docx.html')


@app.route('/convert-jpg-to-png', methods=['GET', 'POST'])
def jpg_to_png_page():
    user_folder = get_user_folder()
    if request.method == 'POST':
        uploaded_files = request.files.getlist('files')
        jpg_paths = handle_uploaded_files(uploaded_files, user_folder)
        png_paths = convert_jpg_to_png(jpg_paths)
        delete_original_files(jpg_paths)
        if png_paths:
            return render_template('download.html', files=png_paths)
    return render_template('jpg_to_png.html')


@app.route('/convert-png-to-jpg', methods=['GET', 'POST'])
def png_to_jpg_page():
    user_folder = get_user_folder()
    if request.method == 'POST':
        uploaded_files = request.files.getlist('files')
        png_paths = handle_uploaded_files(uploaded_files, user_folder)
        jpg_paths = convert_png_to_jpg(png_paths)
        delete_original_files(png_paths)
        if jpg_paths:
            return render_template('download.html', files=jpg_paths)
    return render_template('png_to_jpg.html')


@app.route('/uploads/<filename>')
def download_file(filename):
    user_folder = get_user_folder()
    file_path = os.path.join(user_folder, filename)
    if os.path.isfile(file_path):
        response = send_file(file_path, as_attachment=True, download_name=filename)
        response.headers["Content-Disposition"] = f"attachment; filename*=UTF-8''{filename}"
        return response
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
