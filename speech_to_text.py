
import os
import speech_recognition as sr
from pydub import AudioSegment

from engine import append_new_line



def prepare_voice_file(path: str):
    """
    Converts the input audio file to WAV format if necessary and returns the path to the WAV file.
    """
    
    if os.path.splitext(path)[1] == '.wav':
        return path
    elif os.path.splitext(path)[1] in ('.mp3', '.m4a', '.ogg', '.flac'):
        audio_file = AudioSegment.from_file(
            path, format=os.path.splitext(path)[1][1:])
        wav_file = os.path.splitext(path)[0] + '.wav'
        audio_file.export(wav_file, format='wav')
        return wav_file
    else:
        raise ValueError(
            f'Unsupported audio format: {format(os.path.splitext(path)[1])}')


def transcribe_audio(audio_data, language):
    """
    Transcribes audio data to text using Google's speech recognition API.
    """
    r = sr.Recognizer()
    text = r.recognize_google(audio_data, language=language)
    return text

        

        

def speech_to_text(input_path: str, output_path: str, language: str):
    """
    Transcribes an audio file at the given path to text and writes the transcribed text to the output file.
    
    """
    wav_file = prepare_voice_file(input_path)
    with sr.AudioFile(wav_file) as source:
        audio_data = sr.Recognizer().record(source)
        text = transcribe_audio(audio_data, language)
        append_new_line(f'{output_path}', str(text))
        return text


# if __name__ == '__main__':
#     print('Please enter the path to an audio file (WAV, MP3, M4A, OGG, or FLAC):')
#     input_path = input().strip()
#     if not os.path.isfile(input_path):
#         print('Error: File not found.')
#         exit(1)
#     else:
#         print('Please enter the path to the output file:')
#         output_path = input().strip()
#         print('Please enter the language code (e.g. en-US):')
#         language = input().strip()
#         try:
#             speech_to_text(input_path, output_path, language)
#         except Exception as e:
#             print('Error:', e)
#             exit(1)
