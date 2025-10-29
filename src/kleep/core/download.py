from pytubefix import YouTube
from kleep.core.timestamps import timestamp_to_seconds
import os
from typing import Tuple , List


def chapter_parser(yt : YouTube, filename : str) -> Tuple[str, List[str], List[Tuple[int, int]], int, str, str]:
    """Return track names and respective timestamps"""

    video_end : int = yt.length 
    video_author : str = yt.author

    if not yt.chapters:
        # No info given by author
        return yt.title, [], [], video_end, video_author, filename

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
            track_time_stamps.append((start, video_end))
            
    video_end = 0
    
    return yt.title, track_names, track_time_stamps, video_end, video_author, filename



def download_audio(link : str) -> Tuple[str, List[str], List[Tuple[int, int]], int, str, str]:
    """Downloads requested video to an mp3 file"""

    try:

        yt : YouTube = YouTube(link)
        if not yt.title or not yt.watch_url:
                raise ValueError("Invalid YouTube link")

        filename : str = f"{yt.title}.mp3"
        filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.'))

        stream = yt.streams.get_audio_only()
        if not stream:
            raise FileNotFoundError(f"Failed to download {filename}")
        
        stream.download(filename = filename)
        if not os.path.exists(filename):
                raise FileNotFoundError(f"Failed to download {filename}")

        return chapter_parser(yt, filename)

    except Exception as e:
        
        if 'filename' in locals() and os.path.exists(filename):
            os.remove(filename)
        raise Exception(f"Download failed: {str(e)}")
    

    
    
    