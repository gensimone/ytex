from dataclasses import dataclass


@dataclass
class Playlist:
    title: str
    album_type: str
    release_year: int
    playlist_id: str


@dataclass
class Song:
    title: str
    video_id: str
