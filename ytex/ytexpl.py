import sys, os
from . import extractors as ex
from argparse import ArgumentParser
from innertube.clients import InnerTube


def get_parser() -> ArgumentParser:
    parser = ArgumentParser(description='')
    _ = parser.add_argument('query', type=str, help='query to make')
    _ = parser.add_argument('-s', '--stdin',   action='store_true', default=False, help='read input from stdin')
    _ = parser.add_argument('-i', '--id',      action='store_true', default=False, help='include playlist ID to stdout')
    _ = parser.add_argument('-t', '--title',   action='store_true', default=False, help='include title to stdout')
    _ = parser.add_argument('-y', '--year',    action='store_true', default=False, help='include year to stdout')
    _ = parser.add_argument('-j', '--type',    action='store_true', default=False, help='include playlist type to stdout')
    _ = parser.add_argument('-a', '--all',     action='store_true', default=True,  help='include any information extracted to stdout (default behavior)')
    return parser


def main() -> None:
    parser = get_parser()
    args = parser.parse_args()

    innertube_client = InnerTube('WEB_REMIX')
    response = innertube_client.search(args.query)
    try:
        channel_id = ex.get_channel_id(response)
    except (KeyError, IndexError):
        print(f'no results\n')
        sys.exit(1)

    response = innertube_client.browse(f"MPAD{channel_id}")
    playlists = ex.get_playlists(response)

    # this is not optimal but 'playlists' is usually a very small array (like 10-100 elements)
    max_title = max([len(p.title) for p in playlists])
    max_album_type = max([len(p.album_type) for p in playlists])
    try:
        for p in playlists:
            title = f"{p.title}{' ' * (max_title - len(p.title))}"
            album_type = f"{p.album_type}{' ' * (max_album_type - len(p.album_type))}"
            if args.all:
                print(f"{title} {album_type} {p.release_year} {p.playlist_id}")
            else:
                if args.title:
                    print(title, end=' ')
                if args.type:
                    print(album_type, end=' ')
                if args.year:
                    print(p.release_year, end=' ')
                if args.id:
                    print(p.playlist_id, end=' ')
                print()
    except BrokenPipeError:
        # Python flushes standard streams on exit;
        # redirect remaining output to devnull to avoid another BrokenPipeError at shutdown
        devnull = os.open(os.devnull, os.O_WRONLY)
        _ = os.dup2(devnull, sys.stdout.fileno())
        sys.exit(1)  # Python exits with error code 1 on EPIPE


if __name__ == '__main__':
  main()

