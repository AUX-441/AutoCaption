# burn_srt.py
import json
import os
import subprocess
import Regex


class burn_SRT:
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

    def burn_subtitle(self):

        CONFIG = self.Get_Config_Path()
        try:
            if not CONFIG:
                print("Failed to found CONFIG File ...")

            try:
                from Regex import replace_words_in_srt
                Regex.replace_words_in_srt()
                print("Successfully execute Replace Regex Function ...")
            except ImportError as e:
                print(f"Failed to execute Function Regex :{e}...")

            Output_Video = "output"
            if os.path.exists(Output_Video):
                print(f"Directory :{Output_Video} Already exist continuing ...")
            else:
                os.makedirs(Output_Video, exist_ok=True)
                print(f"Success Directory :{Output_Video} Created Succesfully ...")

            Video_path = CONFIG["video_path"]
            SRT_path = CONFIG["srt_path"]
            output_path = CONFIG["output_video_path"]

            try:

                command = [
                    "ffmpeg",
                    "-threads", "6",
                    "-i", Video_path,
                    "-vf", f"subtitles={SRT_path}:fontsdir=fonts:force_style='FontName=Vazir Regular FD'",
                    "-c:v", "libx264",
                    "-preset", "veryfast",
                    "-c:a", "copy",
                    output_path
                ]


                subprocess.run(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               universal_newlines=True,
                               bufsize=1
                               )
                print(f"Successfully Created Video with subtitles :{Output_Video}...")
            except subprocess.CalledProcessError as err:
                print(f"Failed while using FFMPEG : {err}")
        except Exception as errors:
            print(f"Failed to Create Subtitle for the video :{errors}...")


if __name__ == "__main__":
    C = burn_SRT()
    C.burn_subtitle()
