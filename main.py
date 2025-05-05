from flask import Flask, send_from_directory, request, render_template
import os
import aesencrypt
from utils import *
import threading
import time

# === CONFIGURATION ===
EXPIRY_SECONDS = 24 * 60 * 60  # 24 hours
PAGES_DIR = os.path.join(os.getcwd(), 'page')
NOTES_DIR = os.path.join(os.getcwd(), 'notes')

app = Flask(__name__)

# === ROUTES ===

@app.route('/<path:filename>')
def serve_page(filename):
    if os.path.exists(os.path.join(PAGES_DIR, filename)):
        return send_from_directory(PAGES_DIR, filename)
    return "File not found", 404

@app.route('/', methods=['POST', 'GET'])
def serve_page_index():
    return serve_page('index.html')

@app.route('/create', methods=['POST'])
def create():
    note = request.form['note']
    note_idhash = generate_md5_hash(str(generate_random_str(8)))
    random_password = str(generate_random_str(16))
    encrypted_note = aesencrypt.encrypt(str(note), random_password)

    with open(os.path.join(NOTES_DIR, note_idhash), 'w') as note_file:
        note_file.write(encrypted_note)

    with open(os.path.join(NOTES_DIR, f"{note_idhash}.key"), 'w') as key_file:
        key_file.write(random_password)

    base_url = request.host_url
    message = f"{base_url}open/{note_idhash}"
    return render_template('created.html', message=message)

@app.route('/open/<note_id>', methods=['GET', 'POST'])
def open_note(note_id):
    note_path = os.path.join(NOTES_DIR, f"{note_id}")
    key_path = os.path.join(NOTES_DIR, f"{note_id}.key")

    if not os.path.exists(note_path) or not os.path.exists(key_path):
        return render_template('notfound.html')

    if request.method == 'POST':
        try:
            with open(note_path, 'r') as note_file:
                encrypted_note = note_file.read()
            with open(key_path, 'r') as key_file:
                password = key_file.read()

            decrypted_note = aesencrypt.decrypt(encrypted_note, password)

            os.remove(note_path)
            os.remove(key_path)

            return render_template('opened.html', note=decrypted_note)

        except Exception as e:
            return f"An error occurred while opening the note: {str(e)}", 500

    return render_template('confirm_open.html', note_id=note_id)

# === FILE CLEANUP FUNCTION ===

def delete_old_files():
    current_time = time.time()
    for filename in os.listdir(NOTES_DIR):
        filepath = os.path.join(NOTES_DIR, filename)
        if os.path.isfile(filepath):
            file_age = current_time - os.path.getmtime(filepath)
            if file_age > EXPIRY_SECONDS:
                os.remove(filepath)

def start_file_cleanup():
    while True:
        delete_old_files()
        time.sleep(60)

# === MAIN ===

if __name__ == '__main__':
    threading.Thread(target=start_file_cleanup, daemon=True).start()
    app.run(debug=True)
