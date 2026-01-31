# Video Parser Project

**Part 1:** Upload a video → Extract audio → Convert to text with timestamps

## Setup (One Time)

### Step 1: Fix Homebrew Permissions
Open Terminal and run:
```bash
sudo chown -R $(whoami) /usr/local/Cellar /usr/local/Homebrew /usr/local/bin /usr/local/lib /usr/local/share /usr/local/opt
```
Enter your Mac password when asked.

### Step 2: Install FFmpeg
```bash
brew install ffmpeg
```

### Step 3: Install Python Dependencies
```bash
cd ~/Video-Parser-Project
pip3 install -r requirements.txt
```

## How to Run

```bash
cd ~/Video-Parser-Project
streamlit run app.py
```

This opens a web page in your browser where you can:
1. Upload a video file
2. Click "Process Video"
3. See the transcript with timestamps
4. Download the transcript

## Project Structure

```
Video-Parser-Project/
├── app.py              # Main app with UI
├── requirements.txt    # Dependencies
├── uploads/            # Uploaded videos (auto-created)
├── transcripts/        # Saved transcripts (auto-created)
└── README.md           # This file
```

## What Happens When You Process a Video

1. **Video → Audio**: FFmpeg extracts the audio track
2. **Audio → Text**: Whisper AI converts speech to text with timestamps
3. **Save**: Transcript saved as JSON for searching later
