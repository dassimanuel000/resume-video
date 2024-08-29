
import datetime
import mimetypes
import subprocess
from urllib.parse import urlparse
from moviepy import editor
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip

import os
import PySimpleGUI as sg
import requests
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
from datetime import timedelta
from PIL import Image
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav


def generate_audios(text_prompt, file):
    preload_models()
        
    audio_array = generate_audio(text_prompt)

    file = get_unique_filename(file)
    write_wav(file, SAMPLE_RATE, audio_array)
    if True:
        return file
    
def get_video_duration(video_path):
    with VideoFileClip(video_path) as video:
        duration = video.duration  # duration in seconds
    return duration


def capture_screenshots(video_path, output_folder):
    output_folder = get_unique_filename(output_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get video duration
    duration = get_video_duration(video_path)
    clip = VideoFileClip(video_path)
    
    # Capture screenshots at every 10% of the video duration
    for i in range(1, 11): 
        try:
            time = (i / 10) * duration  
            frame = clip.get_frame(time)
            image = Image.fromarray(frame)
            
            output_path = os.path.join(output_folder, f'screenshot_{i}.png')
            image.save(output_path)
        except Exception as e:
            print(f"Error: {e}")
    
    # Close the video clip
    clip.close()
    return output_folder


def sync_video_with_audio(video_initial, audio_path, duration_per_image=2):
    image_folder = 'images_from_video'
    image_folder = capture_screenshots(video_initial, image_folder)
    output_video_path = get_unique_filename(video_initial)
    images = sorted([img for img in os.listdir(image_folder) if img.endswith((".png", ".jpg", ".jpeg"))])
    
    with open("images.txt", "w") as file:
        for image in images:
            file.write(f"file '{os.path.join(image_folder, image)}'\n")
            file.write(f"duration {duration_per_image}\n")
        file.write(f"file '{os.path.join(image_folder, images[-1])}'\n")

    # Create the FFmpeg command
    command = [
        "ffmpeg",
        "-y",  # Overwrite output files without asking
        "-f", "concat",  # Input file format is concat
        "-safe", "0",  # Unsafe mode, required for non-standard filenames
        "-i", "images.txt",  # The input file list
        "-i", audio_path,  # Input audio file
        "-pix_fmt", "yuv420p",  # Pixel format
        "-c:v", "libx264",  # Video codec
        "-r", "25",  # Frame rate
        "-c:a", "aac",  # Audio codec
        "-b:a", "192k",  # Audio bitrate
        "-shortest",  # Ensure the video is the same length as the audio
        output_video_path  # Output video file
    ]

    # Run the FFmpeg command
    try:
        # Run the command
        subprocess.run(command, check=True)
        os.remove("images.txt")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    return output_video_path


def define_text(audio_path, video_path ):
        
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.datetime.now().strftime("%H:%M:%S")

    global_text = f"""
    ------------------------------------------------------------------------------------------
    Date: {current_date}
    Hour: {current_time}
    Audio Path: {audio_path}
    Video Path: {video_path}
    """
    return global_text


def summarize_text(text, max_length=130, min_length=30):
    model_name = "facebook/bart-large-cnn"
    summarizer = pipeline("summarization", model=model_name)
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']


def is_file_url(url):
    parsed_url = urlparse(url)
    return parsed_url.scheme == 'file' or parsed_url.scheme == '' and os.path.exists(url)


def download_video(url, save_path):
    if 'http' in url or 'www.' in url :
        # If the URL is a web URL, download the file
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        content_type = response.headers.get('Content-Type')
        extension = mimetypes.guess_extension(content_type) if content_type else '.mp4'
        
        video_filename = url.split('/')[-1].split('?')[0]
        if not video_filename.endswith(extension):
            video_filename += extension
        
        full_path = os.path.join(save_path, video_filename)
        
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
        with open(full_path, 'wb') as video_file:
            for chunk in response.iter_content(chunk_size=8192):
                video_file.write(chunk)
        return full_path
    else:
        
        # If the URL is a local file path, copy it to the save path
        local_path = url.replace('file://', '') if url.startswith('file://') else url
        video_filename = os.path.basename(local_path)
        full_path = os.path.join(save_path, video_filename)
        
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
        if os.path.exists(local_path):
            return full_path
        else:
            raise FileNotFoundError(f"The file at {local_path} does not exist.")
        

def get_content_type(file_name):
    mime_type, _ = mimetypes.guess_type(file_name)
    if mime_type is not None:
        return mime_type
    return 'application/octet-stream'

def get_extension_from_mime_type(mime_type):
    mime_to_extension = {
        'image/jpeg': 'jpg',
        'image/png': 'png',
        'video/mp4': 'mp4',
        'video/webm': 'webm',
        'video/x-matroska': 'mkv',
        'video/x-msvideo': 'avi',
        'application/octet-stream': 'bin'
    }
    return mime_to_extension.get(mime_type, 'bin')


def get_unique_filename(file_path):
    base_name, ext = os.path.splitext(file_path)
    unique_path = file_path
    
    
    counter = 1
    while os.path.exists(unique_path):
        unique_path = f"{base_name}_{counter}{ext}"
        counter += 1
    
    return unique_path

def convert_mp4_to_mp3(video_path):
    if '\\' in video_path:
        video_path = video_path.replace('\\', '/')
    video = editor.VideoFileClip(video_path)  
    audio = video.audio
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    initial_audio_path = f"{base_name}.mp3"
    
    audio_path = get_unique_filename(initial_audio_path)
    audio.write_audiofile(audio_path)
    return audio_path