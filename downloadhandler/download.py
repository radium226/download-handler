#!/usr/bin/env python3

import shutil
import numpy as np
from pathlib2 import Path

from .pathutil import delete_file, delete_folder, list_files, list_folders, first_non_empty_folder, copy_folder, copy_file
from .listutil import first

class Download:

    def __init__(self, file_or_folder_path):
        self._file_or_folder_path = file_or_folder_path

    def delete(self, trash=True):
        if self._file_or_folder_path.is_dir():
            delete_folder(self._file_or_folder_path, trash=trash)
        else:
            delete_file(self._file_or_folder_path, trash=trash)

    @property
    def biggest_file(self):
        return first(first(self.group_files_by_size()))

    @property
    def file_count(self):
        return 1 if self._file_or_folder_path.is_file() else len(list_files(self._file_or_folder_path, absolute=False))

    @property
    def folder(self):
        if self._file_or_folder_path.is_dir():
            return self._file_or_folder_path
        return None

    def copy_to(self, target_folder_path):
        if self._file_or_folder_path.is_dir():
            folder_path = self._file_or_folder_path
            origin_folder_path = folder_path / first_non_empty_folder(folder_path)
            copy_folder(origin_folder_path, target_folder_path)
        else:
            file_path = self._file_or_folder_path
            copy_file(file_path.parent, file_path.name, target_folder_path)

    @property
    def biggest_files(self):
        return first(self.group_files_by_size())

    def group_files_by_size(self, percentile_count=5):
        if self._file_or_folder_path.is_dir():
            folder_path = self._file_or_folder_path
            file_paths = list_files(folder_path, absolute=False)
            file_paths_and_sizes = [(file_path, (folder_path / file_path).stat().st_size) for file_path in file_paths]

            file_sizes = np.array([file_path_and_size[1] for file_path_and_size in file_paths_and_sizes])

            size_percentiles = [np.percentile(file_sizes, percent) for percent in range(0, 100 + 1, int(100 / percentile_count))]

            size_ranges = [[size_percentiles[i], size_percentiles[i + 1]] for i in range(0, len(size_percentiles) - 1)]

            def size_range_of(size):
                return first([size_range for size_range in size_ranges if size_range[0] <= size and size <= size_range[1]])

            file_paths_and_size_ranges = sorted(
                [(file_path_and_size[0], size_range_of(file_path_and_size[1])) for file_path_and_size in file_paths_and_sizes],
                key=lambda file_path_and_size_range: file_path_and_size_range[1],
                reverse=True
            )

            return [size_range_and_file_paths[1] for size_range_and_file_paths in sorted(
                    [size_range_and_file_paths for size_range_and_file_paths in [(size_range, [file_path_and_size_range[0] for file_path_and_size_range in file_paths_and_size_ranges if file_path_and_size_range[1] == size_range]) for size_range in size_ranges] if len(size_range_and_file_paths[1]) > 0],
                    key=lambda size_range_and_file_paths: size_range_and_file_paths[0][0],
                    reverse=True
                )]
        else:
            file_path = self._file_or_folder_path
            return [[file_path]]


if __name__ == "__main__":
    download = Download(Path("/home/adrien/Desktop/The.Orville.S01E01.720p.HDTV.x264-AVS[rarbg]"))
    for t in download.group_files_by_size():
            print(t)
