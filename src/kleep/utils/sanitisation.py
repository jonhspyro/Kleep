from kleep.utils.config import get_output_dir
import re

def timestamp_to_seconds(timestamp : str):
    """Convert timestamp to seconds"""
    parts = timestamp.split(':')
    if len(parts) == 2:  
        return int(parts[0]) * 60 + int(parts[1])
    elif len(parts) == 3: 
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    return int(parts[0])

def seconds_to_timestamp(seconds: int) -> str:
    """Convert seconds to HH:MM:SS."""
    total = int(seconds)
    hours = total // 3600
    minutes = (total % 3600) // 60
    secs = total % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def make_album_folder(album_name: str) -> str:
    """Create album folder in configured output directory and return sanitized path"""
    output_dir = get_output_dir()
    safe_dir_name : str = "".join(c for c in album_name if c.isalnum() or c in (' ', '-', '_'))
    album_path = output_dir / safe_dir_name
    album_path.mkdir(parents=True, exist_ok=True)
    return str(album_path)
    
def clean_str(title : str) -> str:
    """Creates clean title for mp3 download"""
    return "".join(c for c in f"{title}.mp3" if c.isalnum() or c in (' ', '-', '_', '.'))

def check_valid_timestamp(time_stamp : str, video_length : int) -> bool:
    """Check if timestamp is valid"""
    colon_format = re.fullmatch(r"(\d{2}:){1,2}\d{2}", time_stamp)
    int_format = re.fullmatch(r"\d+", time_stamp)
    
    if not (colon_format or int_format):
        return False
    
    parts = time_stamp.split(':')

    if len(parts) == 2:
        minutes, seconds = int(parts[0]), int(parts[1])
        if not( 0 <= minutes < 60 and 0 <= seconds < 60):
            return False
        
    elif len(parts) == 3:
        hours, minutes, seconds = int(parts[0]), int(parts[1]), int(parts[2])
        if not( 0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60):
            return False
         
    check_time_stamp = timestamp_to_seconds(time_stamp)

    return 0 <= check_time_stamp < video_length
