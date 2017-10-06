#!/usr/bin/env python2

from guessit import guessit
from pathlib2 import Path
from imdb import IMDb
from tempfile import mkdtemp
from pyunpack import Archive

from .listutil import first
from .pathutil import file_mime_type, is_video_file, is_audio_file, locate_file_by_name, folder_emblems

from .download import Download
from .subdl import subdl
from .beet import beet_import

def single_video(download):
    biggest_file_paths = first(download.group_files_by_size())
    if len(biggest_file_paths) == 1: # If there is only one file in the group containing the biggest files
        biggest_file_path = first(biggest_file_paths)
        if is_video_file(biggest_file_path): # If the file is a video
            return biggest_file_path
    return None


class EpisodeHandler:

    def __init__(self):
        self._tv_series_folder_path = Path.home() / Path("Personal/Media/Videos/TV Series")

    def can_handle(self, download):
        video_file_path = single_video(download)
        if video_file_path:
            video_file_name = video_file_path.name
            guess = guessit(video_file_name)
            return guess["type"] == "episode" # If it's an episode
        return False

    def _make_target_folder(self, episode_file_name):
        guess = guessit(episode_file_name)
        title = guess["title"]
        season = guess["season"]
        episode = guess["episode"]

        imdb = IMDb()
        tv_series = first(filter(lambda movie: movie["kind"] == "tv series", imdb.search_movie(title)))
        imdb.update(tv_series)
        years = tv_series["series years"]

        target_folder_path = self._tv_series_folder_path / Path("%s [%s]" % (title, years)) / Path("Se%02d" % season) / Path("Ep%02d" % episode)
        target_folder_path.mkdir(exist_ok=True, parents=True)

        return target_folder_path

    def _download_subtitles(self, folder_path, episode_file_name):
        episode_file_path = locate_file_by_name(folder_path, episode_file_name)
        subdl(folder_path / episode_file_path)

    def handle(self, download):
        episode_file_name = download.biggest_file.name
        target_folder_path = self._make_target_folder(episode_file_name)
        folder_emblems(target_folder_path).set_emblem("new")
        download.copy_to(target_folder_path)
        self._download_subtitles(target_folder_path, episode_file_name)


    def __repr__(self):
        return "EpisodeHandler"


class MovieHandler:

    def __init__(self):
        self._movie_folder_path = Path.home() / Path("Personal/Media/Videos/Movies")

    def can_handle(self, download):
        video_file_path = single_video(download)
        if video_file_path:
            video_file_name = video_file_path.name
            guess = guessit(video_file_name)
            return guess["type"] == "movie" # If it's a movie
        return False

    def _download_subtitles(self, folder_path, movie_file_name):
        movie_file_path = locate_file_by_name(folder_path, movie_file_name)
        subdl(folder_path / movie_file_path)

    def _make_target_folder(self, movide_file_name):
        guess = guessit(movide_file_name)
        title = guess["title"]

        imdb = IMDb()
        movie = first(filter(lambda movie: movie["kind"] == "movie", imdb.search_movie(title)))
        year = movie["year"]

        target_folder_path = self._movie_folder_path / Path("%s [%s]" % (title, year))
        target_folder_path.mkdir(exist_ok=True, parents=True)

        return target_folder_path

    def handle(self, download):
        movie_file_name = download.biggest_file.name
        target_folder_path = self._make_target_folder(movie_file_name)
        folder_emblems(target_folder_path).set_emblem("new")
        download.copy_to(target_folder_path)
        self._download_subtitles(target_folder_path, movie_file_name)

    def __repr__(self):
        return "MovieHandler"


class ArchiveHandler:

    def __init__(self):
        pass

    def can_handle(self, download):
        if download.file_count == 1:
            file_path = download.biggest_file
            _, secondary_mime_type = file_mime_type(file_path)
            if secondary_mime_type == "x-rar-compressed":
                return True
        return False

    def handle(self, download):
        archive_file_path = download.biggest_file
        temp_folder_path = Path(mkdtemp(prefix=archive_file_path.name, dir=str(archive_file_path.parent)))
        Archive(str(archive_file_path)).extractall(str(temp_folder_path))
        fake_download = Download(temp_folder_path)
        handler = HandlerFinder().find_handler(fake_download)
        handler.handle(fake_download)

    def __repr__(self):
        return "ArchiveHandler"


class AlbumHandler:

    def __init__(self):
        pass

    def can_handle(self, download):
        biggest_file_paths = download.biggest_files
        if len(biggest_file_paths) >= 2 and all(map(is_audio_file, biggest_file_paths)):
            return True
        return False

    def handle(self, download):
        album_folder_path = download.folder
        beet_import(album_folder_path)

    def __repr__(self):
        return "AlbumHandler"


class UnknownHandlerError(Exception):
    def __init__(self):
        super(BeetImportError, self).__init__()


class UnknownHandler:

    def __init__(self):
        pass

    def can_handle(self, download):
        return True

    def handle(self, download):
        raise UnknownHandlerError()

    def __repr__(self):
        return "UnknownHandler"


class HandlerFinder:

    def __init__(self):
        pass
        self._known_handlers = [
            EpisodeHandler(),
            MovieHandler(),
            ArchiveHandler(),
            AlbumHandler()
        ]
        self._unknown_handler = UnknownHandler()

    def find_handler(self, download):
        for handler in self._known_handlers:
            if handler.can_handle(download):
                return handler
        return self._unknown_handler


if __name__ == "__main__":
    archive_file_path = Path.home() / Path("Downloads/www.NewAlbumReleases.net_All_Pigs_Must_Die_-_Hostage_Animal_(2017).rar")
    print(file_mime_type(archive_file_path))

    #for file_or_folder_path in [Path("/home/adrien/Desktop/The.Orville.S01E03.720p.HDTV.x264-AVS[rarbg]"), Path("/home/adrien/Personal/Media/Videos/Movies/Zero Dark Thirty [2012]"), Path("/home/adrien/Personal/Media/Videos/Movies/Zero Dark Thirty [2012]/Zero.Dark.Thirty.2012.720p.BrRip.x264.BOKUTOX.YIFY.mp4")]:
    #    download =  Download(file_or_folder_path)
    #    handler_finder = HandlerFinder()
    #    handler = handler_finder.find_handler(download)
    #    print(handler)
    #    handler.handle(download)
    #    print("------")
