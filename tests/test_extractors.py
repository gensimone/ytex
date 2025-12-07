from innertube import InnerTube
from yt_ex import extractors


# Currently we are using only WEB_REMIX client.
innertube_client = InnerTube("WEB_REMIX")


def test_get_channel_id() -> None:
    data = innertube_client.search("Tom Waits")
    print('--- JSON')
    print(data)
    print('---')
    channel_id = extractors.get_channel_id(data)
    assert channel_id


def test_get_playlists() -> None:
    channel_id = "MPADUC39N3pyt2Z15oOMjouokl8A"
    data = innertube_client.browse(channel_id)
    playlists = extractors.get_playlists(data)
    assert playlists


def test_get_videos() -> None:
    playlist_id = "OLAK5uy_lNXnmaMKjo1H2dvYPT6YXWYNal6x5XkDc"
    data = innertube_client.next(playlist_id=playlist_id)
    videos = extractors.get_videos(data)
    assert videos
