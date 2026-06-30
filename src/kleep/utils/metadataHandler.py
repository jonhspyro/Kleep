from kleep.core.video import VideoClass
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, TCON, TYER, TRCK, APIC
from pathlib import Path
import imageio_ffmpeg
import subprocess
import shutil
import os

def handle_thumbnail(thumbnail_path: str) -> bytes:
    """Loads artwork from thumbnail"""
    if thumbnail_path and os.path.exists(thumbnail_path):
        with open(thumbnail_path, 'rb') as img_file:
            return img_file.read()


def fix_mp3s(video: VideoClass):
    """Fix MP3 files by removing XING headers, then write metadata"""

    thumbnail = handle_thumbnail(video.thumbnail_path)

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

        id3 = ID3(str(file))

        # Clear existing frames to avoid duplicates
        id3.clear()

        # Track info
        id3["TIT2"] = TIT2(encoding=3, text=video.track_names[song_index])
        id3["TALB"] = TALB(encoding=3, text=video.title)
        id3["TPE1"] = TPE1(encoding=3, text=video.artist)
        id3["TPE2"] = TPE2(encoding=3, text=video.artist)
        id3["TRCK"] = TRCK(encoding=3, text=f"{song_index + 1}/{len(video.track_time_stamps)}")

        if video.genre:
            id3["TCON"] = TCON(encoding=3, text=video.genre)
        if video.year:
            id3["TYER"] = TYER(encoding=3, text=str(video.year))

        # Thumbnail
        if thumbnail:
            id3["APIC"] = APIC(
                encoding=3,
                mime="image/jpg",
                type=3,  # Cover (front)
                desc="Cover",
                data=thumbnail,
            )

        # ID3v2.3 because most compatible with players 
        id3.save(str(file), v2_version=3)

    if video.location and Path(video.location).exists():
        shutil.rmtree(video.location)