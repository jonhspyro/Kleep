from dataclasses import dataclass
from typing import Tuple, List

@dataclass
class VideoClass:
    """Class for video information."""
   
    title : str
    artist : str
    filename : str
    albumname : str
    thumbnail_path: str
    track_names : List[str]
    track_time_stamps : List[Tuple[int, int]]

    def __init__(self, title : str, 
                 artist : str , 
                 filename : str, 
                 albumname : str,
                 thumbnail_path: str, 
                 track_names : List[str], 
                 track_time_stamps : List[Tuple[int, int]]):
        
        self.title = title
        self.artist = artist
        self.filename = filename
        self.albumname = albumname
        self.thumbnail_path = thumbnail_path
        self.track_names = track_names
        self.track_time_stamps = track_time_stamps
        

        