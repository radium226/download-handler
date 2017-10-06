#!/usr/bin/env python2

#!/usr/bin/env python2

from pathlib2 import Path

from .subprocessutil import execute


class BeetImportError(Exception):
    def __init__(self):
        super(BeetImportError, self).__init__()


def beet_import(album_file_path):
    command = [
        "beet",
        "--library=%s" % (Path.home() / Path("Personal/Media/Music/By Artist/beet.db")),
        "--directory=%s" % (Path.home() / Path("Personal/Media/Music/By Artist")),
        "import",
        "--quiet",
        "."
    ]

    def skipping_should_not_be_in_output(exit_code, lines):
        for line in lines:
            if "Skipping." in line:
                return False
        return True

    if not execute(command, in_folder=str(album_file_path), return_decider=skipping_should_not_be_in_output):
        raise BeetImportError()
