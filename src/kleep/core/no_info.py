from kleep.utils.sanitisation import check_valid_timestamp, timestamp_to_seconds, seconds_to_timestamp
from typing import List, Tuple


def get_track_names( count : int ):
    """Get track names from user"""

    track_names : List[str] = []

    for i in range(1, count + 1):
        name = input(f"Enter name for track {i}: ").strip()
        while not name:
            name = input(f"Name cannot be empty.\nEnter name for track {i}: ").strip()
        track_names.append(name)

    return track_names

def get_track_timestamps( count : int, video_length : int ):
    """Get Time stamps for each track"""

    track_times : List[int] = []
    track_time_stamps : List[Tuple[int,int]] = []
    track_names : List[str] = get_track_names( count )

    print("Now enter a timestamp for each track (format HH:MM:SS, MM:SS)")
    for name in track_names:
        ts = input(f"Enter timestamp for '{name}': ").strip()
        if ts and check_valid_timestamp(ts, video_length):
            ts = timestamp_to_seconds(ts)
        else:
            ts = None
        while ts is None:
            ts = input(f"Enter valid timestamp.\nVideo limit is '{seconds_to_timestamp(video_length)}'\nEnter timestamp for '{name}': ").strip()
            if ts and check_valid_timestamp(ts, video_length):
                ts = timestamp_to_seconds(ts)
            else:
                ts = None

        track_times.append(ts)

    for i in range(count):
        if i != count - 1:
            time_stamp : tuple = (track_times[i], track_times[i + 1])
            track_time_stamps.append(time_stamp)
    else:
            time_stamp : tuple = (track_times[i], video_length)
            track_time_stamps.append(time_stamp)

    return track_time_stamps, track_names

def get_track_names_timestamps( video_length : int ):
    """Gather missing information from user"""

    print("No track names or timestamps found.")

    while True:
        try:
            count = int(input("How many tracks are in this audio? ").strip())
            if count > 0:
                break
        except ValueError:
            print("Please enter a integer...")
            continue

    return get_track_timestamps( count, video_length )
