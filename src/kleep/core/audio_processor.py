from kleep.utils.sanitisation import clean_str
from kleep.core.VideoClass import VideoClass
from kleep.utils.fixheader import fix_mp3s
import imageio_ffmpeg
from tqdm import tqdm
import subprocess
import os


def handle_thumbnail(thumbnail_path: str) -> bytes:
    """Loads artwork from thumbnail"""
    if thumbnail_path and os.path.exists(thumbnail_path):
        with open(thumbnail_path, 'rb') as img_file:
            return img_file.read()


def song_clipper(video: VideoClass) -> None:
    """Clip audio file track by track using ffmpeg directly"""
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    t_len: int = len(video.track_time_stamps)
    audio_path = str(video.location) + "/" + video.filename

    pbar = tqdm(range(t_len), smoothing=50 / t_len)
    for song_index in pbar:
        pbar.set_description(f"Processing song number: {song_index}")

        start_time = video.track_time_stamps[song_index][0]
        end_time = video.track_time_stamps[song_index][1]
        duration = end_time - start_time

        songname = os.path.join(video.albumname, clean_str(video.track_names[song_index]))

        subprocess.run([
            ffmpeg_exe, "-hide_banner", "-loglevel", "error",
            "-ss", str(start_time),
            "-t", str(duration),
            "-i", audio_path,
            "-c:a", "libmp3lame",
            songname
        ], check=True)


def process_file(video: VideoClass) -> None:
    """Load audio file and process it"""
    thumbnail: bytes = handle_thumbnail(video.thumbnail_path)
    song_clipper(video)
    fix_mp3s(video, thumbnail)