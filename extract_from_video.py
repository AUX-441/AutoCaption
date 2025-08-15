# extract_from_video.py
import json
import os
import random
import time
import whisper
from moviepy import VideoFileClip


class extract_text:

    def Get_Config_Path(self):
        try:
            with open("config/config.json", "r", encoding="utf-8") as Paths:
                CONFIG = json.load(Paths)
                return CONFIG
        except FileNotFoundError:
            print("File not Found: config/config.json")
            return None

        except json.JSONDecoder:
            print(f"Error Decoding JSON file :{CONFIG}...")

    def extract_texts(self):
        CONFIG = self.Get_Config_Path()
        if not CONFIG:
            print("CONFIG file not found.")
            return

        try:
            Directory = os.getcwd()
            print(f"Current Directory : {Directory} ...")

            log_file = CONFIG["logs_filename"]
            Convert_path = CONFIG["converted_audio_dir"]
            log_directory = CONFIG["logs_dir"]

            full_log_directory = os.path.join(log_directory, log_file)
            full_convert_directory = os.path.join(Convert_path)

            if os.path.exists(Convert_path):
                print(f"Directory {Convert_path} Already exist Continuing ...")
            else:
                os.makedirs(Convert_path)
                print(f"Success Directory {Convert_path} Created Succesfully ...")

            if os.path.exists(log_directory):
                print(f"Directory {log_directory} Already exist Continuing ...")
            else:
                os.makedirs(log_directory)
                print(f"Success Directory {log_directory} Created Succesfully ...")

            video_path = CONFIG["video_path"]
            video_name = os.path.basename(video_path)
            video_input = VideoFileClip(video_path)

            converted_audio_path = os.path.join(CONFIG["converted_audio_dir"], "Converted.wav")
            video_input.audio.write_audiofile(converted_audio_path)
            print("Converted Success ...")

            model = whisper.load_model("medium")
            extracted_settings = model.transcribe(converted_audio_path)

            if extracted_settings["segments"]:
                video_duration = extracted_settings["segments"][-1]["end"]
            else:
                video_duration = 0

            video_words = len(extracted_settings["text"].split())
            video_language = extracted_settings["language"]
            texts = extracted_settings["text"]

            print("Duration :", video_duration)
            print("Length :", video_words)
            print("Language :", video_language)
            print("Extracted Text :", texts)

            segments = extracted_settings.get("segments", [])
            segment_data = []

            for seg in segments:
                segment_data.append({
                    "start": seg["start"],
                    "end": seg["end"],
                    "text": seg["text"]
                })

            try:
                json_data = {
                    "Video_name": video_name,
                    "duration_seconds": video_duration,
                    "word_count": video_words,
                    "language": video_language,
                    "segments": segment_data
                }

                data = []
                if os.path.exists(full_log_directory):
                    with open(full_log_directory, "r", encoding="utf-8") as f:
                        try:
                            data = json.load(f)
                        except:
                            data = []

                data.append(json_data)
                with open(full_log_directory, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                    print(f"Success Logs Written Succesfully to :{full_log_directory}...")

            except IndexError as index:
                print(f"Failed to Written the Logs into the file : {index}...")

        except Exception as e:
            print(f"Failed to extract text from the Video : {e}...")

if __name__ == "__main__":
    C = extract_text()
    C.extract_texts()