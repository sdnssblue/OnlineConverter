import os
import time
import shutil
from threading import Timer

def clear_old_user_folders(base_folder, max_age_seconds=30):
    current_time = time.time()
    for folder_name in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder_name)
        if os.path.isdir(folder_path):
            last_modified = os.path.getmtime(folder_path)
            if current_time - last_modified > max_age_seconds:
                try:
                    shutil.rmtree(folder_path)
                except Exception as e:
                    print(f"Error deleting folder {folder_path}: {e}")

def clear_upload_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

def delayed_clear_uploads(folder_path, delay=10):
    Timer(delay, clear_upload_folder, [folder_path]).start()