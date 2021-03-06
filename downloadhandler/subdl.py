#!/usr/bin/env python3

from pathlib2 import Path

from .subprocessutil import execute

def subdl(video_file_path):
    command = [
        "subdl",
        "--existing=overwrite",
        "./%s" % video_file_path.name
    ]
    return execute(command, in_folder=video_file_path.parent)
