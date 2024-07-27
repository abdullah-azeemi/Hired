import os
from dotenv import load_dotenv
import speech_recognition as sr
from elevenlabs import generate, stream
import pyttsx3
import requests

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv('GEMINI_API_KEY')
elevenlabs_api_key = os.getenv('eleven_labs_key')
print(f"Gemini API Key: {gemini_api_key}")

class AI_Assistant:
    def __init__(self):
        self.gemini_api_key = gemini_api_key
        self.elevenlabs_api_key = elevenlabs_api_key

        # Prompt
        self.full_transcript = [
            {"role": "system", "content": "You are an interviewer at a software company. Be resourceful and efficient."},
        ]
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()

    def speak_text(self, text):
        engine = pyttsx3.init()
        engine.say(text)
        print('\n' + text)
        engine.runAndWait()

    def start_transcription(self):
        print("Listening... Press Ctrl+C to stop.")
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
            try:
                while True:
                    print("Listening...")
                    audio = self.recognizer.listen(source)
                    text = self.recognize_audio(audio)
                    if text:
                        print("Transcribed Text:", text)
                        self.generate_ai_response(text)
            except KeyboardInterrupt:
                print("Recording stopped.")

    def recognize_audio(self, audio):
        try:
            return self.recognizer.recognize_google(audio).lower()
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None

    def generate_ai_response(self, transcript_text):
        self.full_transcript.append({"role": "user", "content": transcript_text})
        print(f"\nInterviewer: {transcript_text}")

        response = self.query_gemini(transcript_text)

        if response:
            print(f"Raw AI Response: {response}")  # Debug print
            ai_response = response['candidates'][0]['content']['parts'][0]['text']
            self.generate_audio(ai_response)
        else:
            print("No response from AI service")

    def query_gemini(self, text):
        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "contents": [
                {
                    "parts": [
                        {"text": text}
                    ]
                }
            ]
        }

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={self.gemini_api_key}"
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error querying AI service: {e}")
            return None

    def generate_audio(self, text):
        self.full_transcript.append({"role": "assistant", "content": text})
        print(f"\nAI Interviewer: {text}")

        try:
            audio_stream = generate(
                api_key=self.elevenlabs_api_key,
                text=text,
                voice="Alice",
                stream=True
            )

            if audio_stream:
                stream(audio_stream)
            else:
                print("Error: No audio stream returned")
        except Exception as e:
            print(f"Error generating audio: {e}")

# Usage example
greeting = "Thank you for applying to our company. I am here to interview you. Give me your introduction"
ai_assistant = AI_Assistant()
ai_assistant.speak_text(greeting)
ai_assistant.start_transcription()
