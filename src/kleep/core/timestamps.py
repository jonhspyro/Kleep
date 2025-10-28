def timestamp_to_seconds(timestamp : str):
    """Convert timestamp to seconds"""
    parts = timestamp.split(':')
    if len(parts) == 2:  
        return int(parts[0]) * 60 + int(parts[1])
    elif len(parts) == 3: 
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    return int(parts[0])