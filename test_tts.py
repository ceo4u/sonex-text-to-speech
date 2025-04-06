import requests
import os
import json

def generate_audio(text, output_file="output.wav"):
    """
    Generate audio from text using the TTS API
    
    Args:
        text (str): The text to convert to speech
        output_file (str): The output file path
    
    Returns:
        bool: True if successful, False otherwise
    """
    # Get the API key from the environment or use the default from tts_app.py
    api_key = os.environ.get('API_KEY', None)
    
    # If API key is not set, we'll rely on the default in tts_app.py
    # which is generated using secrets.token_urlsafe(32)
    
    # API endpoint
    url = "http://localhost:5000/generate"
    
    # Request headers
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key if api_key else "default-key"  # We'll handle auth error if it occurs
    }
    
    # Request data
    data = {
        "text": text
    }
    
    try:
        # Send POST request
        print(f"Sending request to {url} with text: {text[:50]}...")
        response = requests.post(url, headers=headers, json=data)
        
        # Check if request was successful
        if response.status_code == 200:
            # Save the audio file
            with open(output_file, "wb") as f:
                f.write(response.content)
            print(f"Audio saved to {output_file}")
            return True
        else:
            # Print error message
            print(f"Error: {response.status_code}")
            try:
                print(response.json())
            except:
                print(response.text)
            return False
    
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
