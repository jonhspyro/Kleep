
from pathlib import Path
import subprocess
import os

def fix_mp3s(directory: Path, filename : str, thumbnail_path : str):
    """Fix MP3 files by removing XING headers."""
    mp3_files = directory.glob("*.mp3")
    
    for file in mp3_files:
        print(f"Processing: {file.name}")
        tmpfile = file.with_stem(f"{file.stem}_fixed")
        
        try:
            subprocess.run([
                "ffmpeg", "-hide_banner", "-loglevel", "error",
                "-i", str(file),
                "-c:a", "copy",
                "-write_xing", "0",
                str(tmpfile)
            ], check=True)

            tmpfile.replace(file)
            print(f"Fixed: {file.name}")
            
        except subprocess.CalledProcessError:
            print(f"Failed: {file.name}")
            if tmpfile.exists():
                tmpfile.unlink()
    
    os.remove(filename)
    os.remove(thumbnail_path)