
from flask import Flask, render_template, request
import elevenlabs
import os
import logging

app = Flask(__name__, template_folder='templates', static_folder='static')

# Set your API key securely
ELEVENLABS_API_KEY = '33b05fc0cf62eb2d5f0783bf50a12add'
elevenlabs.set_api_key(ELEVENLABS_API_KEY)

# Define a list of voice IDs and their corresponding names
voice_ids = [
    {"id": "oWAxZDx7w5VEj9dCyTzz", "name": "Grace"},
    {"id": "pNInz6obpgDQGcFmaJgB", "name": "Adam"},
    {"id": "VR6AewLTigWG4xSOukaG", "name": "Arnold"},
    {"id": "CYw3kZ02Hs0563khs1Fj", "name": "Dave"},
    {"id": "AZnzlk1XvdvUeBnXmlld", "name": "Domi"},
    {"id": "MF3mGyEYCl7XYWbV9V6O", "name": "Elli"},
    {"id": " LcfcDJNUP1GQjkzn1xUU", "name": "Emily"},
    {"id": "g5CIjZEefAph4nQFvHAz", "name": "Ethan"},
    {"id": " D38z5RcWu1voky8WS1ja", "name": "Fin"},
    {"id": "ZQe5CZNOzWyzPSCn5a3c", "name": "James"},
    {"id": "bVMeCyTHy58xNoL34h3p", "name": "Jeremy"},
    {"id": "t0jbNlBVZ17f02VDIeMI", "name": "Jessie"},
    {"id": " Zlb1dXrM653N07WRdFW3", "name": "Joseph"},
    {"id": "TxGEqnHWrfWFTfGW9XjX", "name": "Josh"},
    {"id": "TX3LPaxmHKxFdv7VOQHJ", "name": "Liam"},
    {"id": " XrExE9yKIg1WjnnlVkGX", "name": "Matilda"},
    {"id": " flq6f7yk4E4fJM5XTYuZ", "name": "Michael"},
    {"id": " zrHiDhphv9ZnVXBqCLjz", "name": "Mimi"},
    {"id": "piTKgcLEGmPE4e6mEKli", "name": "Nicole"},
    {"id": "ODq5zmih8GrVes37Dizd", "name": "Patrick"},
    {"id": "21m00Tcm4TlvDq8ikWAM", "name": "Rachel"},
    {"id": "yoZ06aMxZJJ28mfd3POQ", "name": "Sam"},
    {"id": "pMsXgVXv3BLzUgSXRplE", "name": "Serena"},
    {"id": "GBv7mTt0atIp3Br8iCZE", "name": "Thomas"},
    {"id": " N2lVS1w4EtoT3dr4eOWO", "name": "Callum"},
    {"id": " IKne3meq5aSn9XLyUdCD", "name": "Charlie"},
    {"id": "XB0fDUnXU5powFXDhCwa", "name": "Charlotte"},]
    # Add more voice IDs as needed


# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/', methods=['GET', 'POST'])
def ttsindex():
    if request.method == 'POST':
        # Get the text input and selected voice ID from the form
        user_text = request.form.get('user_text')
        selected_voice_id = request.form.get('voice_id')

        # Validate form inputs
        if not user_text or not selected_voice_id:
            return render_template('error.html', error_message='Invalid form inputs.')

        # Find the selected voice settings based on the voice ID
        selected_voice_settings = next((v for v in voice_ids if v['id'] == selected_voice_id), None)

        if selected_voice_settings:
            try:
                # Create a Voice object with the selected settings
                voice = elevenlabs.Voice(
                    voice_id=selected_voice_settings['id'],
                    settings=elevenlabs.VoiceSettings(
                        stability=selected_voice_settings.get('stability', 0),
                        similarity_boost=selected_voice_settings.get('similarity_boost', 0.75)
                    )
                )

                # Generate audio from user input text using the selected voice
                audio = elevenlabs.generate(
                    text=user_text,
                    voice=selected_voice_settings['name']
                )

                # Save the audio to a file in the 'static' folder
                elevenlabs.save(audio, "static/audio.mp3")

                # Render a template or return a response
                return render_template('ttsindex.html', user_text=user_text, voice_ids=voice_ids, selected_voice_id=selected_voice_id)

            except Exception as e:
                # Handle API request errors
                logging.error(f'Error during TTS generation: {str(e)}')
                return render_template('error.html', error_message='Error during TTS generation.')

    # Render the initial form on GET request
    return render_template('ttsindex.html', user_text=None, voice_ids=voice_ids, selected_voice_id=voice_ids[0]['id'])

if __name__ == '__main__':
    app.run(debug=True)

