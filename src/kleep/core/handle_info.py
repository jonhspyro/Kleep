from kleep.core.audio_processor import process_file
from kleep.core.download import download_audio
from kleep.core.VideoClass import VideoClass


def kleep():
    """Handles information from Youtube video"""

    link = str(input("\nPlease enter a YouTube link: "))

    video : VideoClass = download_audio(link)

    keep_title = input("Do you want to keep the original title of video as album name? (y/N): ").lower()
    if keep_title != 'y':
        video.title = str(input("Enter desired album name: "))
    
    keep_artist = input("Do you want to keep the original author as album artist name? (y/N): ").lower()
    if keep_artist!= 'y':
        video.artist = str(input("Enter desired artist name: "))
    process_file(video)

    print("Kleeped!\n")