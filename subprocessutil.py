#!/usr/bin/env python2

import subprocess
import sys

def execute(command, cwd=None):
    process = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd)

    # Poll process for new output until finished
    while True:
        next_line = process.stdout.readline()
        if next_line == "" and process.poll() is not None:
            break
        sys.stdout.write(next_line)
        sys.stdout.flush()

    output = process.communicate()[0]
    exit_code = process.returncode

    if (exit_code == 0):
        return True
    else:
        return False
