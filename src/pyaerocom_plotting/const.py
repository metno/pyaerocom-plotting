#!/usr/bin/env python3
"""
pyaerocom-plotting

some common constant definitions


"""
from getpass import getuser
from random import randint
from socket import gethostname
from uuid import uuid4

HOSTNAME = gethostname()
USER = getuser()
TMP_DIR = "/tmp"
RUN_UUID = uuid4()
RND = randint(0, 1e9)
DEFAULT_OUTPUT_DIR = "."

PLOT_NAMES = [
    "pixelmap",
]
PLOT_NAMES_JSON = [
    "overall_ts",
    "overall_ts_SU",
]

DEFAULT_TS_TYPE = "daily"

# some plot defaults
DEFAULT_DPI = 300
MAP_AXES_ASPECT = 1.5
FIGSIZE_DEFAULT = (16, 10)
# text positions for annotations in scatter plots
SCAT_ANNOT_XYPOS = [
    (0.01, 0.95),
    (0.01, 0.90),
    (0.3, 0.90),
    (0.01, 0.86),
    (0.3, 0.86),
    (0.01, 0.82),
    (0.3, 0.82),
    (0.01, 0.78),
    (0.3, 0.78),
    (0.8, 0.1),
    (0.8, 0.06),
]
