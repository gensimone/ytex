#!/bin/sh

# EXAMPLE
# This command will downloads all the music available on YouTube Music for "Tom Waits"
# NOTE: make sure you have yt-dlp installed and available in your PATH
yt-exp "Tom Waits" | awk '{print $NF}' | yt-dlp -o "~/yt-dlp/%(uploader)s/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s" --embed-metadata --embed-thumbnail -t mp3 -a -
