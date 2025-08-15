# app.py
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, jsonify, session, after_this_request
import os
import json
import uuid
import threading
from queue import Queue
from main import Main_Model
import warnings
import logging
from datetime import datetime
import shutil
from threading import Timer
import base64
import glob


app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)
app.logger.setLevel(logging.WARNING)
warnings.filterwarnings("ignore", category=UserWarning)

UPLOAD_FOLDER = 'Videos'
OUTPUT_FOLDER = 'output'
CONFIG_PATH = 'config/config.json'
PROCESS_STATUS_DIR = 'process_status'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(PROCESS_STATUS_DIR, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

processing_queue = Queue()

def load_status(filename=None):
    if filename:
        status_path = os.path.join(PROCESS_STATUS_DIR, f"{filename}.json")
        if os.path.exists(status_path):
            with open(status_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    else:
        all_status = {}
        for file in os.listdir(PROCESS_STATUS_DIR):
            if file.endswith('.json'):
                with open(os.path.join(PROCESS_STATUS_DIR, file), 'r', encoding='utf-8') as f:
                    filename_key = file.replace('.json', '')
                    data = json.load(f)
                    all_status[filename_key] = data
        return all_status


def save_status(status_dict, filename):
    status_dict['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_path = os.path.join(PROCESS_STATUS_DIR, f"{filename}.json")
    with open(status_path, 'w', encoding='utf-8') as f:
        json.dump(status_dict, f, ensure_ascii=False, indent=2)


def update_config(filename):
    config = {
        "video_path": os.path.join(UPLOAD_FOLDER, filename),
        "converted_audio_dir": "Converted_Videos",
        "logs_dir": "logs",
        "logs_filename": "logs.json",
        "translated_segments_filename": "translated_segments.json",
        "blacklist_dir": "black_list",
        "blacklist_filename": "black_list.json",
        "srt_output_dir": "SRT",
        "srt_suffix": "_translated.srt",
        "srt_path": f"SRT/{os.path.splitext(filename)[0]}_translated.srt",
        "output_video_path": f"{OUTPUT_FOLDER}/{os.path.splitext(filename)[0]}_translated.mp4",
        "formal_2_casual": "formal2casual_dataset/formal_to_casual_dict.json"
    }
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
    return config


def process_video(filename):
    status = load_status(filename)
    status['state'] = "processing"
    save_status(status, filename)

    config = update_config(filename)
    try:
        model = Main_Model()
        model.extract_texts(config)
        model.Translating_Farsi(config)
        model.Generate_SRT(config)
        model.replace_words_in_srt(config)
        model.burn_subtitle(config)
        status['state'] = "ended"

        output_filename = os.path.basename(config['output_video_path'])
        status['output_filename'] = output_filename

    except Exception as e:
        status['state'] = f"error: {str(e)}..."
    save_status(status, filename)

    try:
        base_filename = filename.replace('.mp4', '')
        paths_to_delete = [
            os.path.join(app.config['UPLOAD_FOLDER'], filename),
            "Converted_Videos",
            "logs",
            app.config['UPLOAD_FOLDER'],
        ]

        for path in paths_to_delete:
            try:
                if os.path.isfile(path):
                    os.remove(path)
                    print(f"Deleted file: {path}...")
                elif os.path.isdir(path):
                    shutil.rmtree(path)
                    print(f"Deleted folder: {path}...")
            except Exception as e:
                print(f"Error deleting {path}: {e}...")

        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    except Exception as cleanup_error:
        print(f"Cleanup failed: {cleanup_error}...")



worker_started = False

def queue_worker():
    while True:
        filename = processing_queue.get()
        if filename is None:
            break
        process_video(filename)
        processing_queue.task_done()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        files = request.files.getlist('video_files')
        if not files:
            return "no file selected ...", 400

        for uploaded_file in files:
            if uploaded_file.filename == '':
                continue
            unique_filename = f"{uuid.uuid4().hex}.mp4"
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            uploaded_file.save(upload_path)

            status = {
                'state': "waiting for processing",
                'original_name': uploaded_file.filename
            }
            save_status(status, unique_filename)

        return redirect(url_for('index'))

    all_status = load_status()
    files_status = []
    for fn, data in all_status.items():
        files_status.append({
            "filename": fn,
            "state": data.get('state', ''),
            "last_updated": data.get('last_updated', ''),
            "original_name": data.get('original_name', fn),
            "output_filename": data.get('output_filename', None)
        })

    return render_template('index.html', files_status=files_status)



@app.route('/start_processing', methods=['POST'])
def start_processing():
    global worker_started
    if not worker_started:
        threading.Thread(target=queue_worker, daemon=True).start()
        worker_started = True

    all_status = load_status()
    for filename, data in all_status.items():
        state = data.get('state', '')
        if state == "waiting for processing" or "error" in state.lower():
            processing_queue.put(filename)
    return jsonify({"message": "Processing has been queued."})


@app.route('/status')
def get_status():
    try:
        status_data = load_status()
        return jsonify(status_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/check_file/<filename>')
def check_file(filename):
    output_dir = app.config['OUTPUT_FOLDER']
    file_path = os.path.join(output_dir, filename)
    if os.path.exists(file_path):
        return jsonify({"ready": True})
    pattern = os.path.join(output_dir, filename + '*')
    matches = glob.glob(pattern)
    return jsonify({"ready": len(matches) > 0})


@app.route('/download/<filename>')
def download_file(filename):
    output_folder = app.config['OUTPUT_FOLDER']
    status_folder = PROCESS_STATUS_DIR

    file_path = os.path.join(output_folder, filename)
    app.logger.info(f"[DOWNLOAD] initial request for file: {file_path}")

    if not os.path.exists(file_path):
        pattern = os.path.join(output_folder, filename + '*')
        matches = glob.glob(pattern)
        if matches:
            file_path = matches[0]
            filename = os.path.basename(file_path)
            app.logger.info(f"[DOWNLOAD] matched to existing file: {file_path}")

    if not os.path.exists(file_path):
        app.logger.warning(f"[DOWNLOAD] File not found after mapping: {file_path}")
        return "file doesn't exist ...", 404

    try:
        possible_status = os.path.join(status_folder, f"{os.path.splitext(filename)[0]}.json")
        if os.path.exists(possible_status):
            os.remove(possible_status)
            app.logger.info(f"[DOWNLOAD] Deleted status file: {possible_status}")
    except Exception as e:
        app.logger.error(f"[DOWNLOAD] Error deleting status file: {e}")

    def delete_after_delay(path):
        try:
            if os.path.exists(path):
                os.remove(path)
                app.logger.info(f"[DOWNLOAD] Deleted output video after delay: {path}")
        except Exception as e:
            app.logger.error(f"[DOWNLOAD] Error deleting output video: {e}")

    Timer(180, delete_after_delay, args=[file_path]).start()
    return send_from_directory(output_folder, filename, as_attachment=True)


@app.route('/delete/<filename>', methods=['POST'])
def delete_uploaded_file(filename):
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    status_path = os.path.join(PROCESS_STATUS_DIR, f"{filename}.json")

    response = {"deleted": False, "message": "Error while deleting file ..."}

    try:
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(status_path):
            os.remove(status_path)
        response["deleted"] = True
        response["message"] = "Succesfully Deleted File..."
    except Exception as e:
        response["message"] = f"Error while deleting File : {str(e)}..."

    return jsonify(response)

@app.after_request
def after_request(response):
    return response

if __name__ == '__main__':
    app.run(debug=False)
