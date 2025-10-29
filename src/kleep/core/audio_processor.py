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
                 artist: str) -> None:
    """Clip audio file track by track"""
    
    album_name_dir : str = make_album_folder(album_name)

    t_len : int = len(track_timestamps)
        
    for i in range(t_len):
        start_time : int = min(track_timestamps[i][0], audio.duration)
        end_time : int = min(track_timestamps[i][1], audio.duration)

        print("From: " + str(track_timestamps[i][0]) + " To: " + str(track_timestamps[i][1]))

        new_clip = audio.subclip(start_time, end_time)
        
        songname = os.path.join(album_name_dir, track_names[i] + ".mp3")
        print(songname)
        print("sim\n")
        new_clip.write_audiofile(songname)
        
        f = music_tag.load_file(os.path.join(album_name_dir, track_names[i] + ".mp3"))
        f["totaltracks"] = str(t_len)
        f["title"] = str(track_names[i])
        f["album"] = str(album_name) 
        f["artist"] = str(artist)
        f["tracknumber"] = str(i + 1)
        f.save()

def kleep(filename: str,
          track_timestamps: List[Tuple[float, float]],
          track_names: List[str],
          album_name: str,
          artist: str) -> None:
    """Load audio file as a AudioFileClip object"""

    audio = AudioFileClip(filename)
    
    song_clipper(audio, track_timestamps, track_names, album_name, artist)
        