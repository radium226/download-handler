#!/usr/bin/env python3

from imdb import IMDb
from pprint import pprint

def first(l, default=None):
    return default if len(l) < 1 else l[0]

if __name__ == "__main__":
    title = "altered carbon"

    imdb = IMDb()
    tv_series = first([movie for movie in imdb.search_movie(title) if movie["kind"] == "tv series"])
    imdb.update(tv_series)

    print(vars(tv_series))

    print(tv_series["title"])
