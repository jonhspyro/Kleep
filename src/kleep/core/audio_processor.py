
from kleep.utils.sanitisation import clean_str
from kleep.core.VideoClass import VideoClass
from kleep.utils.fixheader import fix_mp3s
from moviepy.editor import AudioFileClip
from tqdm import tqdm
import music_tag
import os


def handle_thumbnail(thumbnail_path : str) -> bytes:
    """ Loads artwork from thumbnail """
    if thumbnail_path and os.path.exists(thumbnail_path):
        with open(thumbnail_path, 'rb') as img_file:
            return img_file.read()
        
def handle_metadata(video : VideoClass, thumbnail : bytes,
                     songname : str, song_index : int) -> None:
    """ Adds information to song metadata"""

    f = music_tag.load_file(songname)
    f["totaltracks"] = len(video.track_time_stamps)
    f["tracktitle"] = video.track_names[song_index]
    f["album"] = video.albumname
    f["artist"] = video.artist
    f["albumartist"] = video.artist
    f["tracknumber"] = song_index + 1
    if thumbnail:
        f["artwork"] = thumbnail
    f.save()

def song_clipper(audio: AudioFileClip, video : VideoClass) -> None:
    """ Clip audio file track by track """
  
    t_len : int = len(video.track_time_stamps)
    
    thumbnail : bytes = handle_thumbnail(video.thumbnail_path)

    pbar = tqdm(range(t_len), smoothing=50/t_len)
    for song_index in pbar:

        pbar.set_description(f"Processing song number: {song_index}")

        start_time : int = min(video.track_time_stamps[song_index][0], audio.duration)
        end_time : int = min(video.track_time_stamps[song_index][1], audio.duration)

        new_clip = audio.subclip(start_time, end_time)
        songname = os.path.join(video.albumname, clean_str(video.track_names[song_index] + ".mp3"))
        new_clip.write_audiofile(songname, verbose=False, logger=None)

        handle_metadata(video, thumbnail, songname, song_index)

def process_file(video : VideoClass) -> None:
    """ Load audio file as a AudioFileClip object """
    audio = AudioFileClip(str(video.location) + "/" + video.filename)
    
    song_clipper(audio, video)
    fix_mp3s(video)
        