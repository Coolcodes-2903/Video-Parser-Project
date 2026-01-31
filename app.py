"""
VIDEO PARSER - Part 1
Upload a video → Extract audio → Convert to text with timestamps

Run with: streamlit run app.py
"""

import streamlit as st
import whisper
import tempfile
import os
import subprocess
import json
from pathlib import Path

# Create folders for storing files
UPLOAD_FOLDER = Path("uploads")
TRANSCRIPT_FOLDER = Path("transcripts")
UPLOAD_FOLDER.mkdir(exist_ok=True)
TRANSCRIPT_FOLDER.mkdir(exist_ok=True)


def extract_audio(video_path, audio_path):
    """Extract audio from video using ffmpeg"""
    command = [
        "ffmpeg",
        "-i", str(video_path),
        "-vn",  # No video
        "-acodec", "mp3",
        "-y",  # Overwrite output file
        str(audio_path)
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.returncode == 0


def format_timestamp(seconds):
    """Convert seconds to HH:MM:SS format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def transcribe_audio(audio_path):
    """Transcribe audio to text with timestamps using Whisper"""
    model = whisper.load_model("base")
    result = model.transcribe(str(audio_path), word_timestamps=True)
    
    segments = []
    for segment in result["segments"]:
        segments.append({
            "start": round(segment["start"], 2),
            "end": round(segment["end"], 2),
            "text": segment["text"].strip()
        })
    
    return segments


def save_transcript(video_name, segments):
    """Save transcript to JSON file"""
    transcript_file = TRANSCRIPT_FOLDER / f"{video_name}.json"
    with open(transcript_file, "w") as f:
        json.dump({
            "video_name": video_name,
            "segments": segments
        }, f, indent=2)
    return transcript_file


# ============================================
# STREAMLIT UI
# ============================================

st.set_page_config(
    page_title="Video Parser",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Video Parser")
st.markdown("**Upload a video → Get text transcript with timestamps**")
st.markdown("---")

# File uploader
uploaded_file = st.file_uploader(
    "Upload your video file",
    type=["mp4", "mov", "avi", "mkv", "webm"],
    help="Supported formats: MP4, MOV, AVI, MKV, WEBM"
)

if uploaded_file is not None:
    # Show file info
    st.success(f"✅ Uploaded: **{uploaded_file.name}** ({uploaded_file.size / 1024 / 1024:.1f} MB)")
    
    # Save uploaded file temporarily
    video_path = UPLOAD_FOLDER / uploaded_file.name
    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Process button
    if st.button("🚀 Process Video", type="primary"):
        
        # Step 1: Extract Audio
        with st.spinner("Step 1/2: Extracting audio from video..."):
            audio_path = UPLOAD_FOLDER / f"{video_path.stem}.mp3"
            success = extract_audio(video_path, audio_path)
            
            if not success:
                st.error("❌ Failed to extract audio. Make sure ffmpeg is installed.")
                st.code("brew install ffmpeg", language="bash")
                st.stop()
            
            st.success("✅ Audio extracted!")
        
        # Step 2: Transcribe
        with st.spinner("Step 2/2: Converting audio to text (this may take a few minutes)..."):
            segments = transcribe_audio(audio_path)
            st.success(f"✅ Transcription complete! Found {len(segments)} segments.")
        
        # Save transcript
        transcript_file = save_transcript(video_path.stem, segments)
        st.info(f"💾 Transcript saved to: `{transcript_file}`")
        
        st.markdown("---")
        st.subheader("📝 Transcript with Timestamps")
        
        # Display transcript
        for i, segment in enumerate(segments):
            col1, col2 = st.columns([1, 5])
            with col1:
                st.markdown(f"**{format_timestamp(segment['start'])}**")
            with col2:
                st.markdown(segment["text"])
        
        # Download button
        transcript_text = "\n".join([
            f"[{format_timestamp(s['start'])} - {format_timestamp(s['end'])}] {s['text']}"
            for s in segments
        ])
        
        st.download_button(
            label="📥 Download Transcript",
            data=transcript_text,
            file_name=f"{video_path.stem}_transcript.txt",
            mime="text/plain"
        )

else:
    # Show instructions when no file uploaded
    st.info("👆 Upload a video file to get started")
    
    st.markdown("### How it works:")
    st.markdown("""
    1. **Upload** - Select a video file (Zoom recording, Loom, etc.)
    2. **Process** - Click the button to extract audio and transcribe
    3. **View** - See the full transcript with timestamps
    4. **Download** - Save the transcript as a text file
    """)

# Footer
st.markdown("---")
st.markdown("*Video Parser v1.0 - Your first step to searchable videos*")
