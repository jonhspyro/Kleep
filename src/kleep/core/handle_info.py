from kleep.core.audio_processor import process_file
from kleep.core.download import download_audio
from kleep.core.VideoClass import VideoClass
import click

def kleep(link: str, album_title: str = None, album_artist: str = None) -> None:
    """Handles information from Youtube video, downloads, and processes it"""

    # 1. Download audio and parse track info
    video : VideoClass = download_audio(link)

    # 2. Handle Album Title (interactive or command-line option)
    if album_title is not None:
        video.title = album_title
    else:
        # Use click.confirm for interactive prompt
        keep_title = click.confirm(
            f"Do you want to keep the original title '{video.title}' as the album name?", 
            default=True
        )
        if not keep_title:
            video.title = click.prompt("Enter desired album name")
    
    # 3. Handle Album Artist (interactive or command-line option)
    if album_artist is not None:
        video.artist = album_artist
    else:
        # Use click.confirm for interactive prompt
        keep_artist = click.confirm(
            f"Do you want to keep the original author '{video.artist}' as the album artist name?", 
            default=True
        )
        if not keep_artist:
            video.artist = click.prompt("Enter desired artist name")
                  
    process_file(video)
