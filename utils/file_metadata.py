# file_metadata.py
from pymediainfo import MediaInfo

def get_file_metadata(file_path):
    media_info = MediaInfo.parse(file_path)
    for track in media_info.tracks:
        print(track.to_data())
