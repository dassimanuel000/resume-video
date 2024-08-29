
# Project: Video Summarization and Audio Synchronization

This project is a Python-based tool that processes a video (either locally or online), extracts and summarizes the audio, and generates a new video with the summarized audio. The project can handle various video formats and provides a streamlined way to condense long videos into shorter, summarized versions.

<img src="G.PNG" witdh='720' height='420'/>

## Example

| Media Type          | Initial Version | Summarized Version |
|---------------------|-----------------|--------------------|
| **Text**            | "you must manage your emotions you got to master the order taking the L is being a boss you going to lose you going to win you know so you got to be able to grow and take from from whatever the situation is regardless of what it is and sometimes I may not be the best at dealing with my emotions sometimes I do it's like that though I leave my door open for good business" | '"Sometimes I may not be the best at dealing with my emotions sometimes I do it\'s like that though I leave my door open for good business" "You got to be able to grow and take from from whatever the situation is regardless of what it is"' |
| **Video**           | [Initial Video](https://www.youtube.com/shorts/KcZgZ4b0zr0) | [Summarized Video](https://youtube.com/shorts/49mlfpyk4hE?feature=share) |


## Directory Structure

```plaintext
├── config/
│   ├── requirements.txt  # List of required Python packages
├── ./
│   ├── main.py           # Main script that runs the entire process
│   ├── functions.py      # Contains all the helper functions for processing
├── media/
│   ├── input_video/      # Folder to store input videos
│   ├── output_video/     # Folder to store the final summarized video
│   ├── audio/            # Folder to store audio files generated during processing
├── README.md             # This readme file
└── .gitignore            # Git ignore file to exclude unnecessary files
```

## Configuration

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/dassimanuel000/resume-video.git
   cd resume-video
   ```

2. **Install Dependencies**:
   Ensure you have Python installed, and then install the required Python packages:
   ```bash
   pip install -r config/requirements.txt
   ```

## Use

To use the project, run the `main.py` script with the following command:

```bash
python main.py
```

### Example Usage

When prompted, enter the video URL (either a local file path or an online video link):

```bash
Enter your video URL (eg: file:///video.mp4 | https://website.com/video.mp4): 
```

The script will:
1. Download the video (if online).
2. Convert the video to audio.
3. Transcribe the audio to text.
4. Summarize the transcribed text.
5. Generate a new audio file with the summarized text.
6. Create a new video using the summarized audio.

The final summarized video will be saved in the `media/output_video/` directory.

## Additional Instructions

- The project relies on several Python packages listed in the `requirements.txt` file. Ensure all dependencies are installed by running:
  ```bash
  pip install -r config/requirements.txt
  ```

- All outputs (audio files, summarized videos) are stored in the `media/` directory under their respective subdirectories (`audio`, `output_video`).

## Author

This project was developed by [Your Name]. Feel free to reach out for any questions or contributions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

