import kleep.core.timestamps as c2s

def get_tn(track_names : list, count : int):
    """Get track names from user"""
    for i in range(1, count + 1):
        name = input(f"Enter name for track {i}: ").strip()
        while not name:
            name = input(f"Name cannot be empty.\nEnter name for track {i}: ").strip()
        track_names.append(name)

    return track_names

def get_tt(track_time_stamps : list, track_names : list, count : int, video_length : int):
    """Get Time stamps for each track"""
    track_times= []
    print("Now enter a timestamp for each track (format HH:MM:SS, MM:SS)")
    for name in track_names:
        ts = input(f"Enter timestamp for '{name}': ").strip()
        if ts:
            ts = c2s.timestamp_to_seconds(ts)
        else:
            ts = None
        while ts is None:
            user_input = input(f"Timestamp cannot be empty.\nEnter timestamp for '{name}': ").strip()
            if user_input:
                ts = c2s.timestamp_to_seconds(user_input)
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

    return track_time_stamps

def get_tt_tn(track_names : list, track_time_stamps : list, video_length : int):
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
    track_names = get_tn(track_names, count)
    track_time_stamps = get_tt(track_time_stamps, track_names, count, video_length)

    return track_time_stamps, track_names
