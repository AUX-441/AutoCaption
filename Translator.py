import json
import os
import re
from deep_translator import GoogleTranslator
from concurrent.futures import ThreadPoolExecutor, as_completed


class Translator:
    def Get_Config_Path(self):
        try:
            with open("config/config.json", "r", encoding="utf-8") as Paths:
                CONFIG = json.load(Paths)
                return CONFIG
        except FileNotFoundError:
            print("File not Found: config/config.json")
            return None

    def translate_segment(self, segment):
        original_text = segment.get("text", "")
        try:
            translated = GoogleTranslator(source="auto", target="fa").translate(original_text)
        except Exception as e:
            translated = "[Failed to Translate]"
            print(f"Translation failed for '{original_text}': {e}")

        translated = ''.join(ch for ch in translated if ch.isprintable() and ch not in ['\u200c', '\u200b', '\ufeff', '\xa0'])
        translated = translated.replace('\u200b', '').replace('\u200c', '')
        translated = re.sub(r"\s+([.,،؛])", r"\1", translated)

        return {
            "start": segment["start"],
            "end": segment["end"],
            "original": original_text,
            "translated": translated
        }

    def Translating_Farsi(self):
        CONFIG = self.Get_Config_Path()
        if not CONFIG:
            print("CONFIG file not found.")
            return

        try:
            black_list = CONFIG["blacklist_dir"]
            black_json = CONFIG["blacklist_filename"]
            full = os.path.join(black_list, black_json)

            os.makedirs(black_list, exist_ok=True)

            Data_json_translating = {
                "darn": "لعنت",
                "bollocks": "چرند",
                "bugger": "بی‌ادب",
                "bloody": "خونی",
                "cock": "اشغال",
                "cunt": "عوضی",
                "hell": "جهنم",
                "jerk": "احمق",
                "motherfucker": "لعنتی",
                "twat": "احمق",
                "whore": "فاحشه",
                "slut": "فاحشه",
                "kill": "از بین بردن",
                "sex": "رابطه",
                "drugs": "مواد",
                "pussy": "فاحشه",
                "douche": "احمق",
                "fag": "همجنسگرا (تحقیرآمیز)",
                "nigger": "سیاه پوست",
                "retard": "احمق"
            }

            with open(full, "w", encoding="utf-8") as Source:
                json.dump(Data_json_translating, Source, ensure_ascii=False, indent=2)
                print(f"Blacklist written to: {full}")

            logs_path = os.path.join(CONFIG["logs_dir"], CONFIG["logs_filename"])
            with open(logs_path, "r", encoding="utf-8") as read:
                subscripting = json.load(read)
                if not subscripting:
                    print("No transcription found.")
                    return

                latest_entry = subscripting[-1]
                text = latest_entry.get("transcription", "")
                print(f"Latest Transcription: {text}")

                words = text.split()
                temp_name = []
                possible_names = []

                for word in words:
                    if re.match(r"[A-Z][a-z]*['-]?[A-Z]?[a-z]*", word):
                        temp_name.append(word)
                    else:
                        if temp_name:
                            possible_names.append(' '.join(temp_name))
                            temp_name = []
                if temp_name:
                    possible_names.append(' '.join(temp_name))

                print(f"Names found: {possible_names}")

                segments = latest_entry.get("segments", [])
                translated_segments = []

                with ThreadPoolExecutor(max_workers=10) as executor:
                    futures = [executor.submit(self.translate_segment, seg) for seg in segments]
                    for future in as_completed(futures):
                        try:
                            translated_segments.append(future.result())
                        except Exception as e:
                            print(f"Translation error: {e}...")

                translated_output_path = os.path.join("logs", "translated_segments.json")
                with open(translated_output_path, "w", encoding="utf-8") as f:
                    json.dump(translated_segments, f, ensure_ascii=False, indent=2)
                    print(f"Translated segments saved to: {translated_output_path}")
                    return True

        except Exception as e:
            print(f"Error in Translating_Farsi: {e}")
            return None


if __name__ == "__main__":
    C = Translator()
    C.Translating_Farsi()
