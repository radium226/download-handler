#!/usr/bin/env python2

import shutil
import os
from pathlib2 import Path
import mimetypes

from .listutil import first
from .subprocessutil import execute


class FolderEmblems:

    def __init__(self, folder_path):
        self._folder_path = folder_path

    def set_emblem(self, emblem_name):
        execute([
            "gio",
            "set",
            "-t", "stringv",
             str(self._folder_path),
             "metadata::emblems",
             "emblem-%s" % emblem_name
        ])

    def unset_emblem(self, emblem_name):
        execute([
            "gio",
            "set",
            "-t", "unset",
             str(self._folder_path),
             "metadata::emblems"
        ])


def delete_file(file_path, trash=True):
    if trash:
        execute(["gio", "trash", str(file_path)])
    else:
        pass

def delete_folder(folder_path, trash=True):
    if trash:
        execute(["gio", "trash", str(folder_path)])
    else:
        pass

def folder_emblems(folder_path):
    return FolderEmblems(folder_path)


def file_mime_type(file_path):
    mime_type, _ = mimetypes.guess_type(str(file_path))
    primary_and_secondary_mime_types = mime_type.split("/")
    primary_mime_type = primary_and_secondary_mime_types[0]
    secondary_mime_type = primary_and_secondary_mime_types[1]
    return (primary_mime_type, secondary_mime_type)


def is_video_file(file_path):
    primary_mime_type, _ = file_mime_type(file_path)
    return primary_mime_type == "video"


def list_folders(folder_path, recursive=True, absolute=False):
    if recursive:
        sub_folder_paths = map( # We make all sub folders relative to the folder
            lambda sub_folder_path: sub_folder_path.relative_to(folder_path),
            filter( # We remove the folder (which is also returned by walk)
                lambda sub_folder_path: sub_folder_path != folder_path,
                [ Path(sub_folder_path[0]) for sub_folder_path in os.walk(str(folder_path)) ]
            )
        )
    else:
        sub_folder_paths = filter( # We keep only the folders
            lambda file_or_folder_path: (folder_path / file_or_folder_path).is_dir(),
            map( # We retreive Path instead of string
                Path,
                os.listdir(str(folder_path))
            )
        )
    return map( # If needed, we make all sub folders relative to the folder
        lambda sub_folder_path: (folder_path / sub_folder_path) if absolute else sub_folder_path,
        sub_folder_paths
    )


def locate_file_by_name(folder_path, file_name, absolute=False):
    return first(filter(
        lambda file_path: file_path.name == file_name,
        list_files(folder_path, absolute=absolute, recursive=True)
    ))


def list_files(folder_path, recursive=True, absolute=False):
    file_paths = []
    if recursive:
        for sub_folder_path, _, file_paths_in_sub_folder in os.walk(str(folder_path)):
            for file_path in file_paths_in_sub_folder:
                file_paths.append(Path(sub_folder_path).relative_to(folder_path) / Path(file_path))
    else:
        file_paths = filter( # We keep only the files
            lambda file_or_folder_path: (folder_path / file_or_folder_path).is_file(),
            map( # We retreive Path instead of string
                Path,
                os.listdir(str(folder_path))
            )
        )
    return map( # If needed, we make all sub folders relative to the folder
        lambda file_path: (folder_path / file_path) if absolute else file_path,
        file_paths
    )


def copy_file(origin_folder_path, file_path, target_folder_path):
    shutil.copy(
        str(origin_folder_path / file_path),
        str(target_folder_path / file_path)
    )


def copy_folder(origin_folder_path, target_folder_path):
    # We first create the folders
    for sub_folder_path in list_folders(origin_folder_path):
        (target_folder_path / sub_folder_path).mkdir(exist_ok=True)

    # Then we copy the files
    for file_path in list_files(origin_folder_path):
        copy_file(origin_folder_path, file_path, target_folder_path)


def first_non_empty_folder(folder_path, absolute=False, visited_folder_path = Path(".")):
    non_empty_folder_path = None
    if len(list_files(folder_path / visited_folder_path, recursive=False)) > 0:
        return folder_path / visited_folder_path if absolute else visited_folder_path
    else:
        sub_folder_paths = list_folders(folder_path / visited_folder_path, recursive=False)
        if len(sub_folder_paths) != 1:
            return folder_path / visited_folder_path if absolute else visited_folder_path# The one in argument, because we cannot go further
        else:
            return first_non_empty_folder(folder_path, absolute=absolute, visited_folder_path=visited_folder_path / first(sub_folder_paths))


if __name__ == "__main__":
    print(locate_file_by_name(Path("./tests4"), "The.Orville.S01E03.720p.HDTV.x264-AVS.mkv"))
    '''
    for absolute in [True, False]:
        print(first_non_empty_folder("./tests3", absolute=absolute))
        print(first_non_empty_folder("./tests2", absolute=absolute))
    for absolute in [True, False]:
        for recursive in [True, False]:
            for i in list_folders(Path("./tests"), recursive=recursive, absolute=absolute): #, "./tests2")
                print(i)
            print("-----")

    print("")
    print("=====")
    print("")

    for absolute in [True, False]:
        for recursive in [True, False]:
            for i in list_files(Path("./tests"), recursive=recursive, absolute=absolute): #, "./tests2")
                print(i)
            print("-----")

    copy_folder(Path("./tests"), Path("./tests2"))
    '''
