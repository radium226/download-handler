#!/usr/bin/env python3

from transmissionrpc import Client

if __name__ == "__main__":
    client = Client('localhost', port=9091)
    torrents = client.get_torrents()
    for torrent in torrents:
        if "S02E05" in torrent.name:
            client.remove_torrent(torrent.id)
