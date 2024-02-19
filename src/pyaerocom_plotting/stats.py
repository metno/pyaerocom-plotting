#!/usr/bin/env python3
"""
pyaerocom-plotting

some common staistics definitions


"""
import numpy as np
from pyaerocom import ColocatedData

from pyaerocom_plotting.const import GCOS_CRITERION_V2


def gcos_percentages(coldata: ColocatedData) -> dict:
    """small helper function to calculate the GCOS percentages

    noted here:
    https://library.wmo.int/viewer/58111?medianame=GCOS-245_2022_GCOS_ECVs_Requirements_#page=109&viewer=picture&o=bookmark&n=0&q=

    :param coldata: ColocatedData object
    :return: dictionary of GCOS percentages
    """

    obs_data = coldata.data.data[0, :, :].flatten()
    model_data = coldata.data.data[1, :, :].flatten()
    var_name = coldata.var_name[1]

    # remove nans
    data_sum = obs_data + model_data
    idx_pos = np.where(~np.isnan(data_sum))
    idx_nan = np.where(np.isnan(data_sum))

    obs_data = obs_data[idx_pos]
    model_data = model_data[idx_pos]

    # calculate some numbers
    # absolute difference
    absdiff = np.abs(obs_data - model_data)

    gcos_diff_x_percent = absdiff / model_data
    gcos_diff_y_percent = absdiff / obs_data

    # go through the three GCOS criterions...
    outdict = {}
    for crit in GCOS_CRITERION_V2[var_name]:
        # np.where returns tuples of ndarrs!
        gcos_diff_x_arr = np.where(
            gcos_diff_x_percent <= GCOS_CRITERION_V2[var_name][crit]["gcos_err_percent"]
        )[0]
        gcos_diff_y_arr = np.where(
            gcos_diff_y_percent <= GCOS_CRITERION_V2[var_name][crit]["gcos_err_percent"]
        )[0]

        gcos_diff_abs_crit_arr = np.where(
            absdiff <= GCOS_CRITERION_V2[var_name][crit]["gcos_abs_err"]
        )[0]
        gcos_crit_idxs = np.unique(
            np.concatenate((gcos_diff_x_arr, gcos_diff_y_arr, gcos_diff_abs_crit_arr))
        )
        outdict[crit] = gcos_crit_idxs.size / idx_pos[0].size

    assert outdict
    return outdict
