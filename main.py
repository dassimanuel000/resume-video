

from datetime import datetime
from engine import append_new_line
from function import convert_mp4_to_mp3, download_video, define_text, summarize_text, generate_audios, sync_video_with_audio
from speech_to_text import speech_to_text


file_save = 'all-text.txt'

user_input = input("Enter your video URL ( eg: file:///video.mp4 | https://website.com/video.mp4 ):")
if user_input:
    video_path = download_video(str(user_input), '.')
    audio_path = convert_mp4_to_mp3(video_path)
    global_text= define_text(audio_path, video_path)
    append_new_line(f'{file_save}', str(global_text))
    all_text = speech_to_text(audio_path, file_save, 'en-US')
    append_new_line(f'{file_save}', str("---------Resume----------"))
    summary = summarize_text(all_text)
    append_new_line(f'{file_save}', str(summary))
    print(summary)
    audio_generate = generate_audios(text_prompt=summary, file='audio_summary.mp3')
    video_final = sync_video_with_audio(video_path, audio_generate)
    print('Video Summary :' + str(video_final))
else:
    print("No input provided.")
    