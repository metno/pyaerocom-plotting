#!/usr/bin/env python3
"""
pyaerocom plot: crerate plots using the pyaerocom API
"""

import argparse
import subprocess
import sys
from pathlib import Path
from tempfile import mkdtemp

from pyaerocom_plotting.const import (DEFAULT_OUTPUT_DIR, DEFAULT_TS_TYPE,
                                      PLOT_NAMES_JSON)
from pyaerocom_plotting.plotting import Plotting
from pyaerocom_plotting.readers import AerovalJsonData


def main():
    # define some terminal colors to be used in the help
    colors = {
        "BOLD": "\033[1m",
        "UNDERLINE": "\033[4m",
        "END": "\033[0m",
        "PURPLE": "\033[95m",
        "CYAN": "\033[96m",
        "DARKCYAN": "\033[36m",
        "BLUE": "\033[94m",
        "GREEN": "\033[92m",
        "YELLOW": "\033[93m",
        "RED": "\033[91m",
    }

    parser = argparse.ArgumentParser(
        description="create plots based on json files created with Met Norway's pyaerocom/aeroval package",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""{colors['BOLD']}Example usages:{colors['END']}
\t{colors['UNDERLINE']}- basic usage:{colors['END']}
\t  The following line plots the pixelmap for the model {colors['BOLD']}ECMWF_CAMS_REAN{colors['END']} for the year {colors['BOLD']}2019{colors['END']} for the variable {colors['BOLD']}od550aer{colors['END']}
\t  pyaerocom_plot_json -p mmtimeseries -f <json-file>

""",
    )
    parser.add_argument("-f", "--file", help="file to read")
    parser.add_argument("-p", "--plottype", help="plot type(s) to plot", nargs="+")
    parser.add_argument(
        "-l", "--list", help="list supported plot types", action="store_true"
    )
    # parser.add_argument(
    #     "-s",
    #     "--startyear",
    #     help="startyear to read",
    # )
    # parser.add_argument(
    #     "-e", "--endyear", help="endyear to read; defaults to startyear.", nargs="?"
    # )
    # parser.add_argument("-v", "--variables", help="variable(s) to read", nargs="+")
    # parser.add_argument(
    #     "--tstype",
    #     help=f"tstype to read; defaults to {colors['BOLD']}{DEFAULT_TS_TYPE}{colors['END']}",
    #     nargs="?",
    # )
    parser.add_argument(
        "-o",
        "--outdir",
        help=f"output directory for the plot files; defaults to {DEFAULT_OUTPUT_DIR}",
        default=".",
    )

    args = parser.parse_args()
    options = {}
    if args.file:
        options["file"] = args.file

    if args.outdir:
        options["outdir"] = args.outdir

    if args.plottype:
        options["plottype"] = args.plottype

    if args.list:
        print(f"supported plottypes are:")
        for t in PLOT_NAMES_JSON:
            print(f"\t- {t}")
        sys.exit(0)

    # error handling:
    if "file" not in options:
        print("file error")
        sys.exit(1)
    if "plottype" not in options:
        print("plottype error")
        sys.exit(4)

    # start plotting by loop through the supplied plot types
    # OBS: depending on the plottype the corresponding reading class has to be called
    # e.g. pya_read for reading model data via pyaerocom
    for _pidx, _ptype in enumerate(options["plottype"]):
        if _ptype == "overall_ts":
            # overall_ts
            json_data = json_read(options)
            plt_obj = Plotting(plotdir=options["outdir"])
            plt_obj.plot_aeroval_overall_time_series(json_data)
        elif _ptype == "overall_ts_SU":
            # overall_ts
            json_data = json_read(options)
            plt_obj = Plotting(plotdir=options["outdir"])
            plt_obj.plot_aeroval_overall_time_series_SU_Paper(json_data)
        else:
            print(f"plottype {_ptype} unknown. Skipping...")


def json_read(options: dict) -> AerovalJsonData:
    """read model data using pyaerocom"""
    json_data = AerovalJsonData()
    json_data.read(options["file"])

    return json_data


if __name__ == "__main__":
    main()
