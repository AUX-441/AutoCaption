# 🎬 Persian Video Subtitle Translator

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.2+-blue?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![OpenAI Whisper](https://img.shields.io/badge/Whisper-OpenAI-orange?logo=openai&logoColor=white)](https://openai.com/research/whisper)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-4.x-red?logo=ffmpeg&logoColor=white)](https://ffmpeg.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A **powerful Python web application** that automatically translates English video subtitles to Persian (Farsi) and burns them directly into your videos with precise timing and formatting. Perfect for content creators, educators, and video enthusiasts who want Persian subtitles in a snap.

---

## 🌟 Features

- **Automatic Speech Recognition**: Uses OpenAI's Whisper model (medium) for high-accuracy transcription.
- **English → Persian Translation**: Powered by Google Translate API.
- **SRT Subtitle Generation**: Proper timing and formatting guaranteed.
- **Subtitle Burning**: Embed subtitles into videos via FFmpeg.
- **User-Friendly Web Interface**: Upload, manage, and track your videos easily.
- **Queue System**: Handle multiple video translations efficiently.
- **Real-Time Status Updates**: Monitor processing status live.
- **Automatic Cleanup**: Temporary files removed to save storage.
- **Formal-to-Casual Persian Conversion**: Natural and fluent translations.
- **Custom Persian Text Normalization**: Improves readability and accuracy.

---

## 🛠️ Technical Stack

| Component | Technology |
|-----------|-----------|
| Backend | Flask (Python) |
| Speech-to-Text | OpenAI Whisper (medium) |
| Translation | Google Translator API |
| Video Processing | FFmpeg |
| Text Processing | Custom Persian text normalizer |
| Concurrency | Python Threading |

---

## 📦 Installation

### Prerequisites

- Python 3.8+
- FFmpeg (must be in system PATH)
- Whisper dependencies (`openai/whisper`)

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/persian-video-translator.git
cd persian-video-translator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p Videos output process_status config Converted_Videos logs SRT black_list fonts

# Create config file
echo '{}' > config/config.json
🚀 Usage
bash
Copy
Edit
# Start the application
python app.py
Access the web interface at http://localhost:5000

Upload your video files (MP4 recommended)

Click Start Processing

Download processed videos when ready

🏗️ Project Structure
text
Copy
Edit
text
├── app.py                # Main Flask application
├── main.py               # Core processing pipeline
├── extract_from_video.py # Audio extraction and transcription
├── Translator.py         # Translation module
├── Generate_srt.py       # SRT file generation
├── burn_srt.py           # Subtitle burning with FFmpeg
├── Regex.py              # Persian text normalization
├── config/               # Configuration files
├── Videos/               # Uploaded videos storage
├── output/               # Processed videos output
├── process_status/       # Processing status files
├── templates/            # Flask templates
└── requirements.txt      # Python dependencies
🔧 Configuration
Edit config/config.json to customize paths and behavior:

json
Copy
Edit
{
  "video_path": "path/to/input/video",
  "converted_audio_dir": "Converted_Videos",
  "logs_dir": "logs",
  "logs_filename": "logs.json",
  "translated_segments_filename": "translated_segments.json",
  "blacklist_dir": "black_list",
  "blacklist_filename": "black_list.json",
  "srt_output_dir": "SRT",
  "srt_suffix": "_translated.srt",
  "srt_path": "SRT/output_translated.srt",
  "output_video_path": "output/output_translated.mp4",
  "formal_2_casual": "formal2casual_dataset/formal_to_casual_dict.json"
}
⚙️ Processing Pipeline
Video Upload: User uploads video via web interface

Audio Extraction: Extract audio track using MoviePy

Speech Recognition: Transcribe audio using Whisper

Translation: Translate English text to Persian

Text Normalization: Apply Persian formatting rules

SRT Generation: Create subtitle file with proper timing

Subtitle Burning: Burn subtitles into video with FFmpeg

Cleanup: Remove temporary files

Download: Processed video available for download

🌐 API Endpoints
Method	Endpoint	Description
POST	/	Upload video files
POST	/start_processing	Start processing queue
GET	/status	Get processing status
GET	/check_file/<filename>	Check if file is ready
GET	/download/<filename>	Download processed video
POST	/delete/<filename>	Delete uploaded file

📊 Performance Notes
Processing time depends on video length and hardware

Medium Whisper model balances accuracy & speed

Recommended max video length: 30 minutes

Queue system prevents resource overutilization

🐛 Known Issues
Long videos may timeout during processing

Some special characters may not render perfectly

Complex English sentences may not translate ideally

📜 License
MIT License © 2025

🙏 Acknowledgments
OpenAI for Whisper model

Google for translation services

FFmpeg for video processing

Persian NLP community for text normalization rules

