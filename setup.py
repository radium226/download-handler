#!/usr/bin/env python3

from setuptools import setup
from glob import glob
import os

setup(
    name="download-handler",
    version="0.1",
    description="A small tool to handle downloads",
    url="https://github.com/radium226/download-handler",
    license="GPL",
    packages=["downloadhandler"],
    zip_safe=True,
    install_requires=[
        "halo",
        "guessit",
        "imdbpy",
        "pathlib2",
        "patool",
        "pyunpack",
        "fuzzywuzzy"
    ],
    extra_requires={
        "percentiles": ["numpy"]
    },
    scripts=["scripts/handle-download"]
)
