from TTS.api import TTS
import os
import time
import argparse

def generate_audio(text, output_file="output.wav", model_name="tts_models/en/ljspeech/glow-tts"):
    """
    Generate audio from text using the specified TTS model
    
    Args:
        text (str): The text to convert to speech
        output_file (str): The output file path
        model_name (str): The TTS model to use
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        start_time = time.time()
        
        print(f"Loading TTS model: {model_name}")
        
        # Initialize TTS
        tts = TTS(model_name=model_name, progress_bar=True)
        
        print(f"Generating audio for text: {text[:50]}...")
        
        # Generate audio
        tts.tts_to_file(text=text, file_path=output_file)
        
        end_time = time.time()
        print(f"Audio saved to {output_file}")
        print(f"Total processing time: {end_time - start_time:.2f} seconds")
        return True
        
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return False

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Generate audio from text using TTS")
    parser.add_argument("--text", type=str, help="Text to convert to speech", 
                        default="Hello, this is a test of the Sonex Text to Speech API.")
    parser.add_argument("--output", type=str, help="Output file path", default="output.wav")
    parser.add_argument("--model", type=str, help="TTS model to use", 
                        default="tts_models/en/ljspeech/glow-tts")
    args = parser.parse_args()
    
    # Generate audio
    success = generate_audio(args.text, args.output, args.model)
    
    if success:
        print("Audio generation successful!")
    else:
        print("Audio generation failed.")
