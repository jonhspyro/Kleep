from moviepy.editor import AudioFileClip
import os
import music_tag
from typing import Tuple , List

def make_album_folder(album_name: str) -> str:
    """Create album folder and return sanitized path"""
    safe_name : str = "".join(c for c in album_name if c.isalnum() or c in (' ', '-', '_'))
    try:
        os.makedirs(safe_name, exist_ok=True)
        return safe_name
    except Exception as e:
        raise Exception(f"Failed to create album directory: {str(e)}")


def song_clipper(audio: AudioFileClip,
                 track_timestamps: List[Tuple[float, float]],
                 track_names: List[str],
                 album_name: str,
                 artist: str,
                 thumbnail_path: str) -> None:
    """Clip audio file track by track"""
    
    album_name_dir : str = make_album_folder(album_name)
    t_len : int = len(track_timestamps)

    artwork_data : bytes = None
    if thumbnail_path and os.path.exists(thumbnail_path):
        try:
            with open(thumbnail_path, 'rb') as img_file:
                artwork_data = img_file.read()
        except Exception as e:
            print(f"Warning: Could not read thumbnail: {e}")
        
    for i in range(t_len):
        start_time : int = min(track_timestamps[i][0], audio.duration)
        end_time : int = min(track_timestamps[i][1], audio.duration)

        print("From: " + str(track_timestamps[i][0]) + " To: " + str(track_timestamps[i][1]))

        new_clip = audio.subclip(start_time, end_time)
        
        songname = os.path.join(album_name_dir, track_names[i] + ".mp3")
        print(songname)
        new_clip.write_audiofile(songname)
        
        f = music_tag.load_file(songname)
        f["totaltracks"] = t_len
        f["title"] = track_names[i]
        f["album"] = album_name
        f["artist"] = artist
        f["tracknumber"] = i + 1
        if artwork_data:
            f["artwork"] = artwork_data
        f.save()

def kleep(filename: str,
          track_timestamps: List[Tuple[float, float]],
          track_names: List[str],
          album_name: str,
          artist: str,
          thumbnail_path: str) -> None:
    """Load audio file as a AudioFileClip object"""

    audio = AudioFileClip(filename)
    
    song_clipper(audio, track_timestamps, track_names, album_name, artist, thumbnail_path)
        