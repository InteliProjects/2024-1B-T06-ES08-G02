from flask import Flask, request, jsonify, render_template, send_from_directory, redirect, url_for, Response
import os
import time
import sqlite3
import bcrypt
import random
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['LOG_FILE'] = 'upload_log.txt'
app.config['DATABASE'] = 'files.db'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


def init_db():
    with sqlite3.connect(app.config['DATABASE']) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                size INTEGER NOT NULL,
                type TEXT NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        conn.commit()

def insert_file(file_info):
    with sqlite3.connect(app.config['DATABASE']) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO files (name, date, size, type, password_hash) 
            VALUES (?, ?, ?, ?, ?)
        ''', (file_info['name'], file_info['date'], file_info['size'], file_info['type'], file_info['password_hash']))
        conn.commit()

def get_files():
    with sqlite3.connect(app.config['DATABASE']) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT name, date, size, type FROM files')
        return cursor.fetchall()

def get_file_password_hash(filename):
    with sqlite3.connect(app.config['DATABASE']) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT password_hash FROM files WHERE name = ?', (filename,))
        result = cursor.fetchone()
        return result[0] if result else None

def log_upload(file_info, erro_forjado, upload_speed):
    with open(app.config['LOG_FILE'], 'a') as log_file:
        log_file.write(f"{file_info['name']},{file_info['date']},{file_info['size']},{file_info['type']},{erro_forjado},{upload_speed}\n")

def get_upload_logs():
    logs = []
    if os.path.exists(app.config['LOG_FILE']):
        with open(app.config['LOG_FILE'], 'r') as log_file:
            for line in log_file:
                parts = line.strip().split(',')
                if len(parts) == 6:
                    name, date, size, type, erro_forjado, upload_speed = parts
                    logs.append({
                        "name": name,
                        "date": date,
                        "size": size,
                        "type": type,
                        "erro_forjado": erro_forjado == 'True',
                        "upload_speed": float(upload_speed)
                    })
    return logs

@app.route('/')
def index():
    files = get_files()
    file_list = [{'name': file[0], 'date': file[1], 'size': file[2], 'type': file[3]} for file in files]

    upload_logs = get_upload_logs()
    return render_template('index.html', files=file_list, logs=upload_logs)

@app.route('/files')
def list_files():
    files = get_files()
    file_list = [{'name': file[0], 'date': file[1], 'size': file[2]} for file in files]
    return jsonify({'files': file_list})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and 'password' in request.form:
        start_time = time.time()
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        end_time = time.time()
        
        upload_speed = end_time - start_time
        
        file_info = {
            "name": filename,
            "date": time.ctime(os.path.getctime(file_path)),
            "size": os.path.getsize(file_path),
            "type": file.filename.split('.')[-1],
            "password_hash": bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        }
        erro_forjado = random.random() < 0.15  
        log_upload(file_info, erro_forjado, upload_speed)
        insert_file(file_info)

        metadata = {
            "name": file_info["name"],
            "date": file_info["date"],
            "size": file_info["size"],
            "type": file_info["type"]
        }

        return jsonify({'metadata': metadata, 'erro_forjado': erro_forjado, 'upload_speed': upload_speed})
    return jsonify({"error": "File upload failed"}), 500

@app.route('/uploads/<filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
    if request.method == 'POST':
        password = request.form['password'].encode('utf-8')
        password_hash = get_file_password_hash(filename)
        if password_hash and bcrypt.checkpw(password, password_hash):
            return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
        else:
            error = "Senha inválida. Por favor, tente novamente."
            return render_template('file_access.html', filename=filename, error=error)
    return render_template('file_access.html', filename=filename)

@app.route('/delete/<filename>')
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    with sqlite3.connect(app.config['DATABASE']) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM files WHERE name = ?', (filename,))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/updates')
def updates():
    def generate():
        last_state = None
        while True:
            files = get_files()
            file_list = [{'name': file[0], 'date': file[1], 'size': file[2], 'type': file[3]} for file in files]
            current_state = json.dumps(file_list)
            if current_state != last_state:
                yield 'data: {}\n\n'.format(current_state)
                last_state = current_state
    return Response(generate(), mimetype='text/event-stream')


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)