# utils/zip_handler.py
import zipfile
from pathlib import Path
from .checker import check_folder_completeness

def extract_and_check(zip_path, extract_to, result_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    extract_path = Path(extract_to)
    results = []

    for student_folder in extract_path.iterdir():
        if student_folder.is_dir():
            result = check_folder_completeness(student_folder)
            result["Nama Pendaftar"] = student_folder.name
            results.append(result)

    return results