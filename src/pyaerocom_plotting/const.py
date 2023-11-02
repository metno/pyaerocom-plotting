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
