# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
import pandas as pd
from utils.zip_handler import extract_and_check

app = Flask(__name__)
app.secret_key = "rahasia123"

UPLOAD_FOLDER = 'uploads'
EXTRACT_FOLDER = 'extracted'
RESULT_FOLDER = 'results'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXTRACT_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'zip_file' not in request.files:
            flash('Tidak ada file yang dipilih')
            return redirect(request.url)
        
        file = request.files['zip_file']
        if file.filename == '':
            flash('Tidak ada file yang dipilih')
            return redirect(request.url)

        if file and file.filename.endswith('.zip'):
            zip_path = os.path.join(UPLOAD_FOLDER, 'temp.zip')
            file.save(zip_path)

            try:
                results = extract_and_check(
                    zip_path,
                    extract_to=EXTRACT_FOLDER,
                    result_to=RESULT_FOLDER
                )

                # Simpan ke Excel
                df = pd.DataFrame(results)
                excel_path = os.path.join(RESULT_FOLDER, 'hasil_pengecekan.xlsx')
                df.to_excel(excel_path, index=False)

                return redirect(url_for('result'))

            except Exception as e:
                flash(f'Error: {str(e)}')
                return redirect(request.url)
        else:
            flash('Harus file ZIP')
            return redirect(request.url)

    return render_template('index.html')

@app.route('/result')
def result():
    excel_path = os.path.join(RESULT_FOLDER, 'hasil_pengecekan.xlsx')
    if os.path.exists(excel_path):
        df = pd.read_excel(excel_path)
        table = df.to_html(classes='table table-striped', index=False)
        return render_template('result.html', table=table)
    else:
        flash("Belum ada hasil")
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    directory = "results"
    try:
        return send_from_directory(directory, filename, as_attachment=True)
    except Exception as e:
        return "File tidak ditemukan", 404

if __name__ == '__main__':
    app.run(debug=True)