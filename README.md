# 🗣️ Text-to-Speech (TTS) Python Application

This project is a lightweight Text-to-Speech (TTS) application built in Python. It converts text input into human-like speech using various TTS implementations and outputs `.wav` audio files. The application includes testing utilities, Docker support, and configurable rendering options.

---

## 🔧 Features

- ✅ Convert custom text input into `.wav` audio files.
- 🧪 Includes test scripts for easy debugging and validation.
- 🐳 Docker support for seamless deployment across environments.
- ⚙️ Customizable settings through `render.yaml`.

---


> 📝 **Note:** You can listen to `direct_test.wav`, `final.wav`, or `output.wav` by clicking **"View raw"** on GitHub.

---

## 🚀 Quick Start

### 🔹 1. Install Dependencies

```bash
pip install -r requirements.txt

2. Run the Main TTS Application

python tts_app.py

🔹 3. Test with Alternate Method

python direct_tts.py

📦 Docker Support
Run the app inside a Docker container for easy deployment:


docker build -t tts-app .
docker run -v $(pwd):/app tts-app
⚠️ Ensure Docker is installed and running on your system.

📝 License
This project is licensed under the MIT License. See the LICENSE file for details.

