# utils/checker.py
import re

def normalize(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_document_mapping():
    return {
        "CV": ["cv", "curriculum vitae", "daftar riwayat hidup"],
        "Essay Diri": ["essay", "motivasi", "diri", "personal statement"],
        "Essay Lab Informatika": ["essay lab", "essay laboratorium", "informatika", "komputer"],
        "KRS": ["krs", "kartu rencana studi", "rencana studi"],
        "KTM": ["ktm", "kartu tanda mahasiswa", "mahasiswa"],
        "Pas Foto": ["pas foto", "pasfoto", "foto", "photo"],
        "Rangkuman Nilai": ["rangkuman nilai", "transkrip", "nilai", "ipk", "transcript"],
        "Surat Lamaran": ["surat lamaran", "lamaran kerja", "application letter"]
    }

def check_folder_completeness(folder_path):
    from pathlib import Path
    files = [f.stem for f in folder_path.iterdir() if f.is_file()]
    normalized_files = [normalize(f) for f in files]

    mapping = get_document_mapping()
    result = {}

    for doc, keywords in mapping.items():
        clean_keywords = [normalize(kw) for kw in keywords]
        found = any(any(kw in nf for kw in clean_keywords) for nf in normalized_files)
        result[doc] = "✅ Ada" if found else "❌ Tidak Ada"

    return result