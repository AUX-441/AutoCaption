import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class Main_Model:

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


    def extract_texts(self, CONFIG):
        if not CONFIG:
            print("CONFIG file not found.")
            return

        try:
            from extract_from_video import extract_text
            class_for_extract_text = extract_text()
            class_for_extract_text.Get_Config_Path()
            class_for_extract_text.extract_texts()
            print("Successfully Executed extracted_from_video.py ...")
        except ImportError as import_error:
            print(f"Failed to Executed Function extracted_from_video.py  : {import_error}")


    def Translating_Farsi(self, CONFIG):
        if not CONFIG:
            print("CONFIG file not found.")
            return

        try:
            from Translator import Translator
            class_translate = Translator()
            class_translate.Get_Config_Path()
            class_translate.Translating_Farsi()
            print("Successfully Execute Translator.py Module ...")
        except Exception as e:
            print(f"Failed to Execute Translator.py Module due to : {e}...")


    def Generate_SRT(self, CONFIG):
        if not CONFIG:
            print("CONFIG file not found.")
            return

        try:
            from srt_generator import Generate_srt
            class_generate_Srt = Generate_srt()
            class_generate_Srt.Get_Config_Path()
            class_generate_Srt.Generate_SRT()
            print("Succesfully Executed Generate_srt.py Module ...")
        except ImportError as import_error:
            print(f"Failed to execute function Generate_srt.py due to :{import_error}...")



    def replace_words_in_srt(self,CONFIG):

        try:
            if not CONFIG:
                print("Failed to found CONFIG file ...")
            try:
                from Regex import replace_words_in_srt
                file_path = CONFIG.get("srt_path") if CONFIG else None
                if replace_words_in_srt(file_path):
                    print("Successfully Executed Replacing to SRT ...")
            except ImportError as emp:
                print(f"Failed to Execute Replacing to SRT due to :{emp}... ")
        except Exception as e:
            print(f"Failed to Execute Function Regex.py due to :{e}...")


    def burn_subtitle(self, CONFIG):
        try:
            if not CONFIG:
                print("Failed to found CONFIG File ...")

            try:
                from burn_srt import burn_SRT
                class_burn = burn_SRT()
                class_burn.Get_Config_Path()
                class_burn.burn_subtitle()
                print("Successfully Executed burn_srt.py functions ...")
            except Exception as e:
                print(f"Failed to Execute Function burn_srt.py due to : {e}...")
        except ModuleNotFoundError as ntf:
            print(f"Modules on Class burn_srt not found due to : {ntf}...")


if __name__ == "__main__":
    app = Main_Model()
    config_data = app.Get_Config_Path()
    app.extract_texts(config_data)
    app.Translating_Farsi(config_data)
    app.Generate_SRT(config_data)
    app.replace_words_in_srt(config_data)
    app.burn_subtitle(config_data)
