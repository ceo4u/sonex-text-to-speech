from TTS.api import TTS
import os

def generate_audio(text, output_file="direct_test.wav"):
    """
    Generate audio directly using the TTS library
    
    Args:
        text (str): The text to convert to speech
        output_file (str): The output file path
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Initialize TTS with the same model as in tts_app.py
        model_name = os.environ.get('TTS_MODEL', 'tts_models/en/ljspeech/tacotron2-DDC_ph')
        print(f"Loading TTS model: {model_name}")
        
        # Initialize TTS
        tts = TTS(model_name=model_name, progress_bar=True)
        
        # Generate audio
        print(f"Generating audio for text: {text[:50]}...")
        tts.tts_to_file(text=text, file_path=output_file)
        
        print(f"Audio saved to {output_file}")
        return True
        
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return False

if __name__ == "__main__":
    # Text to convert to speech
    text = "Hello, this is a test of the Sonex Text to Speech API. I hope you enjoy this demonstration!"
    
    # Generate audio
    success = generate_audio(text)
    
    if success:
        print("Audio generation successful!")
    else:
        print("Audio generation failed.")
