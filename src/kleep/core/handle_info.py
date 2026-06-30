from kleep.core.audio_processor import process_file
from kleep.core.download import download_audio
from kleep.core.video import VideoClass
import click

def kleep(link: str, album_title: str = None, album_artist: str = None, album_genre: str = None, album_year: str = None) -> None:
    """Handles information from Youtube video, downloads, and processes it"""

    # 1. Download audio and parse track info
    video : VideoClass = download_audio(link)

    # 2. Handle Album Title
    if album_title is not None:
        video.title = album_title
    else:
        
        keep_title = click.confirm(
            f"Do you want to keep the original title '{video.title}' as the album name?", 
            default=True
        )
        if not keep_title:
            video.title = click.prompt("Enter desired album name")
    
    # 3. Handle Album Artist
    if album_artist is not None:
        video.artist = album_artist
    else:
       
        keep_artist = click.confirm(
            f"Do you want to keep the original author '{video.artist}' as the album artist name?", 
            default=True
        )
        if not keep_artist:
            video.artist = click.prompt("Enter desired artist name")
 
    # 4. Handle Album Genre
    if album_genre is not None:
        video.genre = album_genre

    # 5. Handle Album Year
    if album_year is not None:
        video.year = album_year
                  
    process_file(video)
