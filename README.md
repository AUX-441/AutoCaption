# Persian Video Subtitle Translator

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/flask-2.0%2B-lightgrey)
![FFmpeg](https://img.shields.io/badge/FFmpeg-required-orange)
![Whisper](https://img.shields.io/badge/OpenAI_Whisper-medium-blueviolet)

A powerful web application that automatically translates English video subtitles to Persian (Farsi) and burns them into the video with proper formatting.

## 🌟 Features

- **Automatic Speech Recognition** using OpenAI's Whisper model
- **English-to-Persian Translation** with Google Translate API
- **SRT Generation** with proper timing and formatting
- **Subtitle Burning** into videos using FFmpeg
- **Web Interface** for easy upload and management
- **Queue System** for processing multiple videos
- **Real-time Status Updates** for each video
- **Automatic Cleanup** of temporary files
- **Formal-to-Casual Persian Conversion** for natural translations

## 🛠️ Technical Stack

- **Backend**: Flask (Python)
- **Speech-to-Text**: OpenAI Whisper (medium model)
- **Translation**: Google Translator API
- **Video Processing**: FFmpeg
- **Text Processing**: Custom Persian text normalizer
- **Concurrency**: Python Threading

## 📦 Installation

### Prerequisites

1. Python 3.8+
2. FFmpeg (must be in system PATH)
3. Whisper dependencies (see [openai/whisper](https://github.com/openai/whisper))

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
Start the application:

bash
python app.py
Access the web interface at http://localhost:5000

Upload your video files (MP4 format recommended)

Click "Start Processing" to begin translation

Download processed videos when ready

🏗️ Project Structure
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
├── templates/            # Flask templates (not shown in code)
└── requirements.txt      # Python dependencies
🔧 Configuration
Edit config/config.json to customize:

json
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
Video Upload: User uploads video through web interface

Audio Extraction: Extract audio track using MoviePy

Speech Recognition: Transcribe audio using Whisper

Translation: Translate English text to Persian

Text Normalization: Apply Persian text rules and formatting

SRT Generation: Create subtitle file with proper timing

Subtitle Burning: Burn subtitles into video using FFmpeg

Cleanup: Remove temporary files

Download: Make processed video available for download

🌐 API Endpoints
POST /: Upload video files

POST /start_processing: Start processing queue

GET /status: Get processing status

GET /check_file/<filename>: Check if file is ready

GET /download/<filename>: Download processed video

POST /delete/<filename>: Delete uploaded file

📜 License
MIT License

🙏 Acknowledgments
OpenAI for the Whisper model

Google for translation services

FFmpeg team for video processing

Persian NLP community for text normalization rules

📊 Performance Notes
Processing time depends on video length and hardware

Medium Whisper model provides best balance of accuracy/speed

Recommended max video length: 30 minutes

Queue system prevents resource overutilization

🐛 Known Issues
Long videos may timeout during processing

Some special characters may not render perfectly

Complex English sentences may not translate ideally

text

This README includes:
1. SEO-optimized title and description
2. Badges for key technologies
3. Clear installation instructions
4. Comprehensive feature list
5. Detailed project structure
6. Configuration documentation
7. Processing pipeline explanation
8. API endpoint reference
9. License information
10. Performance considerations

The markdown is formatted for excellent GitHub rendering and includes keywords that would help with discoverability. You may want to add screenshots of the interface and example videos to make it even more compelling.
