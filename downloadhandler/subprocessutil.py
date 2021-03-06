#!/usr/bin/env python3

import subprocess
import sys

def execute(command, in_folder=None, return_decider=lambda exit_code, output: exit_code == 0):
    process = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=str(in_folder) if in_folder else None)

    lines = []
    # Poll process for new output until finished
    while True:
        next_line = process.stdout.readline()
        if next_line == b"" and process.poll() is not None:
            break
        sys.stdout.write(next_line.decode("utf-8"))
        sys.stdout.flush()
        lines.append(next_line)

    output = process.communicate()[0]
    exit_code = process.returncode

    return return_decider(exit_code, list(map(lambda line: line.decode("utf-8"), lines)))
