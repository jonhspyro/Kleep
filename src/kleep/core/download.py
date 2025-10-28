from pytubefix import YouTube
import kleep.core.timestamps as c2s
import os


def chapter_parser(yt : YouTube, filename : str):
    """Return track names and respective timestamps"""

    video_end : int = yt.length 
    video_author : str = yt.author

    if not yt.chapters:
        # No info given by author
        return yt.title, [], [], video_end, video_author, filename

    track_names : list[str] = []
    track_time_stamps : list[tuple] = []

    chap_len : int = len(yt.chapters)

    for i in range(chap_len):
        
        track_names.append(yt.chapters[i].title)
        if i != chap_len - 1:
            start,  end = c2s.timestamp_to_seconds(yt.chapters[i].start_label), c2s.timestamp_to_seconds(yt.chapters[i + 1].start_label)
            time_stamp : tuple = (start, end)
            track_time_stamps.append(time_stamp)
        else:
            start= c2s.timestamp_to_seconds(yt.chapters[i].start_label)
            time_stamp : tuple = (start, video_end)
            track_time_stamps.append(time_stamp)
    
    return yt.title, track_names, track_time_stamps, 0, video_author, filename



def download_audio(link : str):
    """Downloads requested video to an mp3 file"""

    try:

        yt : YouTube = YouTube(link)
        if not yt.title or not yt.watch_url:
                raise ValueError("Invalid YouTube link")
        
        # filename : str = yt.title + ".mp3"

        filename = f"{yt.title}.mp3"
        filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.'))

        stream = yt.streams.get_audio_only()
        if not stream:
            raise FileNotFoundError(f"Failed to download {filename}")
        
        stream.download(filename = filename)
        if not os.path.exists(filename):
                raise FileNotFoundError(f"Failed to download {filename}")

        return chapter_parser(yt, filename)

    except Exception as e:
        # Clean up partial downloads if they exist
        if 'filename' in locals() and os.path.exists(filename):
            os.remove(filename)
        raise Exception(f"Download failed: {str(e)}")
    

    
    
    