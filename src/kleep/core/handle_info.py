from kleep.core.download import download_audio
# from kleep.core.no_info import get_track_names_timestamps
from kleep.core.audio_processor import process_file
from kleep.utils.fixheader import fix_mp3s
from kleep.utils.sanitisation import make_album_folder
from pathlib import Path

def kleep():
    """Handles information from Youtube video"""

    link = str(input("\nPlease enter a YouTube link: "))
    title, artist, filename, thumbnail_path, track_names, track_time_stamps = download_audio(link)

    keep_title = input("Do you want to keep the original title of video as album name? (y/N): ").lower()
    if keep_title != 'y':
        title = str(input("Enter desired album name: "))
    
    keep_artist = input("Do you want to keep the original author as album artist name? (y/N): ").lower()
    if keep_artist!= 'y':
        artist = str(input("Enter desired artist name: "))
    
    album_name  : Path = make_album_folder(title)

    process_file(filename, track_time_stamps, track_names, album_name, artist, thumbnail_path)

    fix_mp3s(Path(album_name), filename, thumbnail_path)

    print("Kleeped!\n")