import json
import os

class Generate_srt:

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

    def Generate_SRT(self):
        CONFIG = self.Get_Config_Path()
        if not CONFIG:
            print("CONFIG file not found.")
            return

        try:
            input_path = os.path.join("logs", "translated_segments.json")
            output_dir = CONFIG["srt_output_dir"]

            with open(os.path.join(CONFIG["logs_dir"], CONFIG["logs_filename"]), "r", encoding="utf-8") as f:
                logs = json.load(f)
                last_entry = logs[-1]
                base_name = os.path.splitext(last_entry["Video_name"])[0]
                srt_filename_translated = f"{base_name}_translated.srt"
                srt_filename_original = f"{base_name}_original.srt"

            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
                print(f"Directory {output_dir} created.")

            output_path_translated = os.path.join(output_dir, srt_filename_translated)
            output_path_original = os.path.join(output_dir, srt_filename_original)

            with open(input_path, "r", encoding="utf-8") as src:
                segments = json.load(src)

            segments.sort(key=lambda x: x["start"])

            with open(output_path_translated, "w", encoding="utf-8") as out_translated, \
                 open(output_path_original, "w", encoding="utf-8") as out_original:

                index = 1
                for i, seg in enumerate(segments):
                    start = round(float(seg["start"]), 3)
                    end = round(float(seg["end"]), 3)
                    translated_text = seg.get("translated", "").strip()
                    original_text = seg.get("original", "").strip()

                    if not translated_text or len(translated_text) > 200:
                        print(f"WARNING Skipped translated line :{index} due to empty or long text ...")
                        continue

                    if start >= end:
                        print(f"WARNING Skipped line :{index} due to bad timing: {start} > {end}...")
                        continue

                    if i > 0 and start < segments[i - 1]["end"]:
                        start = round(segments[i - 1]["end"] + 0.01, 3)

                    if i < len(segments) - 1 and end > segments[i + 1]["start"]:
                        end = round(segments[i + 1]["start"] - 0.01, 3)

                    if end - start < 0.5:
                        end = start + 0.5

                    def to_srt_time(seconds):
                        hrs = int(seconds // 3600)
                        mins = int((seconds % 3600) // 60)
                        secs = int(seconds % 60)
                        millis = int((seconds - int(seconds)) * 1000)
                        return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"

                    start_time = to_srt_time(start)
                    end_time = to_srt_time(end)

                    out_translated.write(f"{index}\n{start_time} --> {end_time}\n{translated_text}\n\n")

                    out_original.write(f"{index}\n{start_time} --> {end_time}\n{original_text}\n\n")

                    index += 1

            print(f"SRT File Created Successfully: {output_path_translated}")
            print(f"Original English SRT Created Successfully: {output_path_original}")

            with open(output_path_translated, "r", encoding="utf-8") as f:
                preview = ''.join([next(f) for _ in range(10)])
                print("\n[Preview of Translated SRT output:]\n" + preview)

            with open(output_path_original, "r", encoding="utf-8") as f:
                preview = ''.join([next(f) for _ in range(10)])
                print("\n[Preview of Original English SRT output:]\n" + preview)

        except Exception as e:
            print(f"ERROR Failed to generate SRT: {e} ...")

if __name__ == "__main__":
    C = Generate_srt()
    C.Get_Config_Path()
    C.Generate_SRT()
