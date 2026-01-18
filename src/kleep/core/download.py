from kleep.utils.sanitisation import timestamp_to_seconds, clean_str
from kleep.core.no_info import get_track_names_timestamps
from kleep.utils.sanitisation import make_album_folder
from kleep.core.VideoClass import VideoClass
from kleep.utils.config import get_output_dir
from typing import Tuple , List 
from pytubefix import YouTube
from pathlib import Path
import requests
import click
import os

def getchapters(yt: YouTube):

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
            track_time_stamps.append((start, yt.length))

    return track_names, track_time_stamps

def getkey_moments(yt: YouTube):

    track_names : List[str] = []
    track_time_stamps: List[Tuple[int, int]] = []

    key_moments = yt.key_moments
    key_moments_len : int = len(key_moments)

    for i in range (key_moments_len) :
            moment : str = str(key_moments[i])
            content = moment.replace("<KeyMoment: ", "").replace(">", "")
            parsed_key_moment = content.split(" | ")

            track_names.append(parsed_key_moment[0])
            if i!= key_moments_len -1:

                next_moment : str = str(key_moments[i + 1])
                content = next_moment.replace("<KeyMoment: ", "").replace(">", "")
                parsed_next_key_moment = content.split(" | ")

                start = int(timestamp_to_seconds(parsed_key_moment[1]))
                end = int(timestamp_to_seconds(parsed_next_key_moment[1]))
                track_time_stamps.append((start, end))
            else:
                start = int(timestamp_to_seconds(parsed_key_moment[1]))
                track_time_stamps.append((start, yt.length))

    return track_names, track_time_stamps

def download_thumbnail(yt: YouTube, location: str) -> str:
    """Download video thumbnail and save it next to the audio file"""
    try:
        thumbnail_url = yt.thumbnail_url
        
        thumbnail_path = os.path.join(location, 'thumbnail.jpg')
        
        response = requests.get(thumbnail_url)
        response.raise_for_status()
        
        with open(thumbnail_path, 'wb') as f:
            f.write(response.content)
        
        return thumbnail_path
    
    except Exception as e:
        print(f"Warning: Could not download thumbnail: {e}")
        return None

def timeStampsParser(yt : YouTube, filename : str, location : str) -> VideoClass:
    """Return track names and respective timestamps"""

    video_length : int = yt.length 
    video_author : str = yt.author
    track_names : List[str] = []
    track_time_stamps: List[Tuple[int, int]] = []
    thumbnail_path : str = download_thumbnail(yt, location)
    album_name : Path = make_album_folder(yt.title)

    if yt.key_moments:

        track_names, track_time_stamps = getkey_moments(yt)

    elif yt.chapters:
         
        track_names, track_time_stamps = getchapters(yt)

    else:
        # No info given by author
        track_time_stamps, track_names = get_track_names_timestamps(video_length)
        
        return VideoClass(yt.title, video_author, location, filename, album_name, thumbnail_path, track_names, track_time_stamps)
    return VideoClass(yt.title, video_author, location, filename, album_name, thumbnail_path, track_names, track_time_stamps)

def download_audio(link : str) -> VideoClass:
    """Downloads requested video to an mp3 file"""

    yt : YouTube = YouTube(link)
    if not yt.title or not yt.watch_url:
            raise ValueError("Invalid YouTube link")
    
    click.echo(f"Kleeping: {yt.title}")
    
    filename : str = clean_str(yt.title)
    output_dir : str = get_output_dir()
    location : str = output_dir / filename
    
    stream = yt.streams.get_audio_only()
    if not stream:
        raise FileNotFoundError(f"Failed to load {filename}")
    
    stream.download(filename = filename, output_path = str(location))
    if not location.exists():
            raise FileNotFoundError(f"Failed to download {filename}")

    return timeStampsParser(yt, filename, location)
