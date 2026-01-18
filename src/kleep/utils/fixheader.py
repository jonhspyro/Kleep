from kleep.core.VideoClass import VideoClass
from pathlib import Path
import subprocess
import shutil

def fix_mp3s(video : VideoClass):

    """Fix MP3 files by removing XING headers"""

    directory : Path = Path(video.albumname)
    mp3_files = directory.glob("*.mp3")
    
    for file in mp3_files:
        
        tmpfile = file.with_stem(f"{file.stem}_fixed")
        
        subprocess.run([
                "ffmpeg", "-hide_banner", "-loglevel", "error",
                "-i", str(file),
                "-c:a", "copy",
                "-write_xing", "0",
                str(tmpfile)
            ], check=True)

        tmpfile.replace(file)

    shutil.rmtree(video.location)
    