from TTS.api import TTS
import os
import time

def generate_audio_fast(text, output_file="output.wav"):
    """
    Generate audio directly using the TTS library with optimized settings for speed
    
    Args:
        text (str): The text to convert to speech
        output_file (str): The output file path
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        start_time = time.time()
        
        # Use a faster model for quicker generation
        # The 'tts_models/en/ljspeech/fast_pitch' model is faster than tacotron2
        model_name = os.environ.get('TTS_MODEL', 'tts_models/en/ljspeech/fast_pitch')
        print(f"Loading TTS model: {model_name}")
        
        # Initialize TTS with progress bar disabled for speed
        tts = TTS(model_name=model_name, progress_bar=False)
        
        print(f"Generating audio for text: {text[:50]}...")
        
        # Generate audio with optimized settings
        tts.tts_to_file(text=text, file_path=output_file)
        
        end_time = time.time()
        print(f"Audio saved to {output_file}")
        print(f"Total processing time: {end_time - start_time:.2f} seconds")
        return True
        
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return False

if __name__ == "__main__":
    # Your provided input text
    text = """The error message you're encountering—undefined reference to 'WinMain'—typically arises when the linker expects a Windows GUI application entry point (WinMain) but cannot find it. This situation often occurs when building console applications with MinGW, as it defaults to GUI subsystem settings."""
    
    # Generate audio
    success = generate_audio_fast(text)
    
    if success:
        print("Audio generation successful!")
    else:
        print("Audio generation failed.")
