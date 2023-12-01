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
    "monthly_weighted_mean"
]
PLOT_NAMES_JSON = [
    "overall_ts",
    "overall_ts_SU",
]

DEFAULT_TS_TYPE = "daily"

TS_ANNOTATIONS = {
      "2023/06/27": "48r1",
      "2021/10/13": "47r3",
      "2021/05/19": "47r2",
      "2020/10/06": "47r1",
      "2019/07/09": "46r1",
      "2018/06/26": "45r1",
      "2017/09/26": "43r3",
      "2017/01/24": "43r1",
      "2016/06/21": "41r2",
      "2015/09/03": "41r1",
      "2014/09/18": "40r2",
      "2014/02/19": "40r1",
      "2013/10/07": "38r2",
#      "2012/07/05": "37r3",
#      "2009/09/01": "36r1"
    }
