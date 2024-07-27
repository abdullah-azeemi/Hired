# pip install assemblyai
# pip install elevenlabs==0.3.0b0
# pip install openai
# pip install python-mpv
# pip install pyaudio
# pip install "assemblyai[extras]"



import os
from dotenv import load_dotenv
import assemblyai as aai
from elevenlabs import generate, stream
import openai
import pyaudio


load_dotenv()

assemblyai_api_key = os.getenv('aai_key')
openai_api_key = os.getenv('open_ai_key')
elevenlabs_api_key = os.getenv('eleven_labs_key')

class AI_Assistant:
    def __init__(self):
        aai.settings.api_key = assemblyai_api_key
        openai.api_key = openai_api_key
        self.elevenlabs_api_key = elevenlabs_api_key

        self.transcriber = None

        # Prompt
        self.full_transcript = [
            {"role": "system", "content": "You are a interviewer at a software company. Be resourceful and efficient."},
        ]

###### Step 2: Real-Time Transcription with AssemblyAI ######
        
    def start_transcription(self):
        self.transcriber = aai.RealtimeTranscriber(
            sample_rate=16000,
            on_data=self.on_data,
            on_error=self.on_error,
            on_open=self.on_open,
            on_close=self.on_close,
            end_utterance_silence_threshold=1000
        )

        self.transcriber.connect()
        microphone_stream = aai.extras.MicrophoneStream(sample_rate=16000)
        self.transcriber.stream(microphone_stream)
    
    def stop_transcription(self):
        if self.transcriber:
            self.transcriber.close()
            self.transcriber = None

    def on_open(self, session_opened: aai.RealtimeSessionOpened):
        print("Session ID:", session_opened.session_id)
        return

    def on_data(self, transcript: aai.RealtimeTranscript):
        if not transcript.text:
            return

        if isinstance(transcript, aai.RealtimeFinalTranscript):
            self.generate_ai_response(transcript)
        else:
            print(transcript.text, end="\r")

    def on_error(self, error: aai.RealtimeError):
        print("An error occurred:", error)
        return

    def on_close(self):
        return

###### Step 3: Pass real-time transcript to OpenAI ######
    
    def generate_ai_response(self, transcript):
        self.stop_transcription()

        self.full_transcript.append({"role": "user", "content": transcript.text})
        print(f"\Interviewer: {transcript.text}", end="\r\n")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.full_transcript
        )

        ai_response = response.choices[0].message['content']

        self.generate_audio(ai_response)

        self.start_transcription()
        print(f"\nReal-time transcription: ", end="\r\n")

###### Step 4: Generate audio with ElevenLabs ######
        
    def generate_audio(self, text):
        self.full_transcript.append({"role": "assistant", "content": text})
        print(f"\nAI Interviewer: {text}")

        audio_stream = generate(
            api_key=self.elevenlabs_api_key,
            text=text,
            voice="Alice",
            stream=True
        )

        stream(audio_stream)

greeting = "Thank you for applying to our company. I am here to interview you. Give me your introduction"

ai_assistant = AI_Assistant()
ai_assistant.generate_audio(greeting)
ai_assistant.start_transcription()


