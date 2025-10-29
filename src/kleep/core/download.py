from pytubefix import YouTube
from kleep.core.timestamps import timestamp_to_seconds
import os
from typing import Tuple , List
import requests


def download_thumbnail(yt: YouTube, audio_filename: str) -> str:
    """Download video thumbnail and save it next to the audio file"""
    try:
        thumbnail_url = yt.thumbnail_url
        
        base_name = os.path.splitext(audio_filename)[0]
        thumbnail_path = f"{base_name}.jpg"
        
        response = requests.get(thumbnail_url)
        response.raise_for_status()
        
        with open(thumbnail_path, 'wb') as f:
            f.write(response.content)
        
        return thumbnail_path
    except Exception as e:
        print(f"Warning: Could not download thumbnail: {e}")
        return None

def chapter_parser(yt : YouTube, filename : str) -> Tuple[str, List[str], List[Tuple[int, int]], int, str, str]:
    """Return track names and respective timestamps"""

    video_end : int = yt.length 
    video_author : str = yt.author
    thumbnail_path : str = download_thumbnail(yt, filename)

    if not yt.chapters:
        # No info given by author
        return yt.title, [], [], video_end, video_author, filename, thumbnail_path

    track_names : List[str] = []
    track_time_stamps: List[Tuple[int, int]] = []

    chap_len : int = len(yt.chapters)

    for i in range(chap_len):
        
        track_names.append(yt.chapters[i].title)
        if i != chap_len - 1:
            start = int(timestamp_to_seconds(yt.chapters[i].start_label))
            end = int(timestamp_to_seconds(yt.chapters[i + 1].start_label))
            track_time_stamps.append((start, end))
        else:
            start = int(timestamp_to_seconds(yt.chapters[i].start_label))
            track_time_stamps.append((start, video_end))
            
    video_end = 0
    
    return yt.title, track_names, track_time_stamps, video_end, video_author, filename, thumbnail_path

def download_audio(link : str) -> Tuple[str, List[str], List[Tuple[int, int]], int, str, str]:
    """Downloads requested video to an mp3 file"""

    try:

        yt : YouTube = YouTube(link)
        if not yt.title or not yt.watch_url:
                raise ValueError("Invalid YouTube link")

        filename : str = f"{yt.title}.mp3"
        filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.'))

        stream = yt.streams.get_audio_only()
        if not stream:
            raise FileNotFoundError(f"Failed to download {filename}")
        
        stream.download(filename = filename)
        if not os.path.exists(filename):
                raise FileNotFoundError(f"Failed to download {filename}")

        return chapter_parser(yt, filename)

    except Exception as e:
        
        if 'filename' in locals() and os.path.exists(filename):
            os.remove(filename)
        raise Exception(f"Download failed: {str(e)}")
    

    
    
    