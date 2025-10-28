from kleep.core.download import download_audio
from kleep.utils.no_info import get_tt_tn
from kleep.core.audio_processor import kleep
import os
import subprocess
import time

if __name__ == "__main__":
    link = str(input("Please enter a YouTube link: "))
    title, track_names, track_time_stamps, video_length, author, filename = download_audio(link)
    
    max_attempts = 10
    attempts = 0
    while not (os.path.exists(filename) and os.path.getsize(filename) > 0):
        time.sleep(1)
        attempts += 1
        if attempts >= max_attempts:
            print(f"Error: File {filename} not found after {max_attempts} seconds")
            exit(1)


    keep_title = input("Do you want to keep the original title of video as album name? (y/n): ").lower()
    if keep_title != 'y':
        title = str(input("Enter new title: "))
    
    keep_author = input("Do you want to keep the original author as album artist name? (y/n): ").lower()
    if keep_author!= 'y':
        author = str(input("Enter new title: "))

    if video_length != 0:

        track_time_stamps, track_names = get_tt_tn(track_names, track_time_stamps , video_length)

    kleep(filename, track_time_stamps, track_names, title, author)

    # Run the fix script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, "fix_mp3s.sh")
    output_dir = title  # Directory is in the same location as script
    print(f"\nFixing MP3 files in: {output_dir}")
    subprocess.run(["bash", script_path], cwd=output_dir, check=True)
    os.remove(filename)
    print("Done!")
        




    