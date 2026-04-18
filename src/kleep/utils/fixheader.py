from kleep.core.VideoClass import VideoClass
from pathlib import Path
import imageio_ffmpeg
import subprocess
import music_tag
import shutil


def fix_mp3s(video: VideoClass, thumbnail: bytes):
    """Fix MP3 files by removing XING headers, then write metadata"""

    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    directory: Path = Path(video.albumname)
    mp3_files = sorted(directory.glob("*.mp3"))

    for song_index, file in enumerate(mp3_files):
        tmpfile = file.with_stem(f"{file.stem}_fixed")

        # Remux to remove XING header
        subprocess.run([
            ffmpeg_exe, "-hide_banner", "-loglevel", "error",
            "-i", str(file),
            "-c:a", "copy",
            "-write_xing", "0",
            str(tmpfile)
        ], check=True)

        tmpfile.replace(file)

        f = music_tag.load_file(str(file))
        f["totaltracks"] = len(video.track_time_stamps)
        f["tracktitle"] = video.track_names[song_index]
        f["album"] = video.title
        f["artist"] = video.artist
        f["albumartist"] = video.artist
        f["tracknumber"] = song_index + 1
        f["year"] = video.year
        if thumbnail:
            f["artwork"] = thumbnail
        f.save()

    shutil.rmtree(video.location)