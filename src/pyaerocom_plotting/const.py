#!/usr/bin/env python3
"""
pyaerocom-plotting

some common constant definitions


"""
from getpass import getuser
from random import randint
from socket import gethostname
from uuid import uuid4
import numpy as np

HOSTNAME = gethostname()
USER = getuser()
TMP_DIR = "/tmp"
RUN_UUID = uuid4()
RND = randint(0, int(1e9))
DEFAULT_OUTPUT_DIR = "."

PLOT_NAMES = ["pixelmap", "monthly_weighted_mean"]
PLOT_NAMES_JSON = [
    "overall_ts",
    "evaluation_ts",
    "overall_ts_SU",
]
PLOT_NAMES_COL = [
    "scatterdensity",
    "scatterplot",
    "gcos",
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

GCOS_CRITERION = dict(
    od550aer={"gcos_err_percent": 0.1, "gcos_abs_err": 0.03},
    od550lt1aer={"gcos_err_percent": 0.1, "gcos_abs_err": 0.03},
)
GCOS_CRITERION_V2 = dict(
    od550aer=dict(
        goal={"gcos_err_percent": 0.04, "gcos_abs_err": 0.02},
        breakthrough={"gcos_err_percent": 0.1, "gcos_abs_err": 0.03},
        threshold={"gcos_err_percent": 0.2, "gcos_abs_err": 0.06},
    ),
    od550lt1aer=dict(
        goal={"gcos_err_percent": 0.04, "gcos_abs_err": 0.02},
        breakthrough={"gcos_err_percent": 0.1, "gcos_abs_err": 0.03},
        threshold={"gcos_err_percent": 0.2, "gcos_abs_err": 0.06},
    ),
    ssa670aer=dict(
        goal={"gcos_err_percent": np.nan, "gcos_abs_err": 0.1},
        breakthrough={"gcos_err_percent": np.nan, "gcos_abs_err": 0.2},
        threshold={"gcos_err_percent": np.nan, "gcos_abs_err": 0.4},
    ),
)

USER_FRIENDLY_VAR_NAMES = {
    "od550aer": "total AOD",
    "od550lt1aer": "FM AOD",
    "od550dust": "dust AOD",
    "ssa670aer": "SSA @ 670nm",
    "proxyzdust": "DLH",
    "zdust": "DLH",
    "proxyzaerosol": "ALH",
    "zaerosol": "ALH",
}
USER_FRIENDLY_OBS_NAMES = {
    "AeronetSunV3Lev2.daily": "AERONET Sun",
    "AeronetSDAV3Lev2.daily": "AERONET SDA",
    "AeronetInvV3Lev2.daily": "AERONET INV",
    "AeronetSunV3Lev2": "AERONET Sun",
    "AeronetSDAV3L2": "AERONET SDA",
}

USER_FRIENDLY_MODEL_NAMES = {
    "MODIS6.1terra": "MODIS.terra",
    "AATSR_ADV.v4.1": "AATSR.ADV",
    "AATSR_ensemble.v3.1": "AATSR.Ens",
    "AATSR_ensemble.v3.2": "AATSR.Ens",
    "AATSR_ORAC_v4.02": "AATSR.ORAC",
    "AATSR_SU_v4.35": "AATSR.SU",
    "AATSR_SU_v4.35.1": "AATSR.SU",
    "MERIS_DLR_v7.0a": "MERIS.DLR",
    "MERIS_ensemble.v1.0": "MERIS.Ens",
    "MERIS_XBAER_v2.3": "MERIS.XBAER",
    "OLCI_ensemble.v1.1": "OLCI.Ens",
    "OLCI_S4O_v2.0": "OLCI.S4O",
    "OLCI_XBAER_v1.0": "OLCI.XBAER",
    "PARASOL_GRASP_V2.20": "PARASOL.GRASP",
    "Parasol.Grasp": "PARASOL.GRASP",
    "SLSTR_ensemble.v2.3": "SLSTR.Ens",
    "SLSTR_ensemble.v2.4": "SLSTR.Ens",
    "SLSTR_ORAC_v1.00": "SLSTR.ORAC",
    "SLSTR_ORAC_v5.00.3A": "SLSTR.ORAC",
    "SLSTR_SDV.v2.30": "SLSTR.SDV",
    "SLSTR_SU_v1.12": "SLSTR.SU",
    "SLSTR_SU_v1.14.1": "SLSTR.SU",
    "IASI_DLR.v7.1.DN": "IASI.DLR",
    "IASI_LMD_V2.2.DN": "IASI.LMD",
    "IASI.LMD.LTS": "IASI.LMD",
    "IASI_MAPIR_v5.1.DN": "IASI.MAPIR",
    "IASI_MAPIR_v5.11": "IASI.MAPIR",
    "IASI.MAPIR.LTS": "IASI.MAPIR",
    "IASI_ULB.v9.DN": "IASI.ULB",
    "IASI_ensemble.v1.4": "IASI.Ens",
    "ADV.combined": "ADV/SDV",
    "ORAC.combined": "ORAC",
    "SU.combined": "SU",
    "Ensemble.combined": "Ensemble",
    "S4O.combined": "S4M/S4O",
    "XBAER.combined": "XBAER",
}

USER_COLOURS = {
    "ATSR-2": "brown",
    "AATSR": "green",
    "SLSTR-A": "red",
    "SLSTR-B": "blue",
    "IASI.MAPIR": "black",
    "IASI.LMD": "black",
    "PARASOL.GRASP": "black",
    "Parasol.Grasp": "black",
}

USER_YLIM = {
    "proxyzdust": (0.0, 5.0),
    "proxyzaerosol": (0.0, 5.0),
    "od550aer": (0.0, 2.0),
}
