from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from TTS.api import TTS
import os
import secrets
import tempfile
import logging
from werkzeug.middleware.proxy_fix import ProxyFix

# Initialize Flask app
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
CORS(app, resources={r"/generate": {"origins": os.environ.get('ALLOWED_ORIGINS', "*")}})

# Configuration
API_KEY = os.environ.get('API_KEY', secrets.token_urlsafe(32))
MODEL_NAME = os.environ.get('TTS_MODEL', 'tts_models/en/ljspeech/tacotron2-DDC_ph')
TEMP_DIR = os.environ.get('TEMP_DIR', tempfile.gettempdir())

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('TTS-API')

# Initialize TTS model once at startup
try:
    logger.info(f"Loading TTS model: {MODEL_NAME}")
    tts = TTS(model_name=MODEL_NAME, progress_bar=False)
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load TTS model: {str(e)}")
    raise RuntimeError("Could not initialize TTS model") from e

def require_api_key(func):
    """API Key authentication middleware"""
    def wrapper(*args, **kwargs):
        provided_key = request.headers.get('X-API-Key')
        if not provided_key or provided_key != API_KEY:
            logger.warning(f"Unauthorized access attempt from {request.remote_addr}")
            return jsonify({"error": "Unauthorized"}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@app.route('/generate', methods=['POST'])
@require_api_key
def generate_audio():
    """Generate audio from text"""
    data = request.get_json()
    text = data.get('text', '').strip()
    
    if not text:
        logger.error("Empty text in request")
        return jsonify({"error": "Text parameter is required"}), 400
        
    if len(text) > 1000:
        logger.warning(f"Text too long ({len(text)} characters)")
        return jsonify({"error": "Text exceeds 1000 character limit"}), 413

    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(dir=TEMP_DIR, suffix='.wav', delete=False) as temp_file:
            output_path = temp_file.name
            
        # Generate audio
        logger.info(f"Generating audio for text: {text[:50]}...")
        tts.tts_to_file(text=text, file_path=output_path)
        
        # Send file and cleanup
        response = send_file(
            output_path,
            mimetype='audio/wav',
            as_attachment=True,
            download_name='output.wav'
        )
        
        # Cleanup after response is sent
        response.call_on_close(lambda: os.remove(output_path))
        
        return response

    except Exception as e:
        logger.error(f"Generation error: {str(e)}", exc_info=True)
        if os.path.exists(output_path):
            os.remove(output_path)
        return jsonify({"error": "Audio generation failed"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "model": MODEL_NAME,
        "temp_dir": TEMP_DIR
    })

if __name__ == '__main__':
    # Print development API key
    if not os.environ.get('API_KEY'):
        logger.info(f"🔑 Development API Key: {API_KEY}")
        
    # Start server
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host=os.environ.get('HOST', '0.0.0.0'),
        port=port,
        threaded=True
    )