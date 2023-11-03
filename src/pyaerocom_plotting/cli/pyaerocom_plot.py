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
                                      PLOT_NAMES)
from pyaerocom_plotting.plotting import Plotting
from pyaerocom_plotting.readers import PyaModelData


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
        description="create plots with Met Norway's pyaerocom package",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""{colors['BOLD']}Example usages:{colors['END']}
\t{colors['UNDERLINE']}- basic usage:{colors['END']}
\t  The following line plots the pixelmap for the model {colors['BOLD']}ECMWF_CAMS_REAN{colors['END']} for the year {colors['BOLD']}2019{colors['END']} for the variable {colors['BOLD']}od550aer{colors['END']}
\t  pyaerocom_plot -p pixelmap -m ECMWF_CAMS_REAN -s 2019 -v od550aer

""",
    )
    parser.add_argument("-m", "--models", help="models(s) to read", nargs="+")
    parser.add_argument("-p", "--plottype", help="plot type(s) to plot", nargs="+")
    parser.add_argument(
        "-l", "--list", help="list supported plot types", action="store_true"
    )
    parser.add_argument(
        "-s",
        "--startyear",
        help="startyear to read",
    )
    parser.add_argument(
        "-e", "--endyear", help="endyear to read; defaults to startyear.", nargs="?"
    )
    parser.add_argument("-v", "--variables", help="variable(s) to read", nargs="+")
    parser.add_argument(
        "--tstype",
        help=f"tstype to read; defaults to {colors['BOLD']}{DEFAULT_TS_TYPE}{colors['END']}",
        nargs="?",
    )
    parser.add_argument(
        "-o",
        "--outdir",
        help=f"output directory for the plot files; defaults to {DEFAULT_OUTPUT_DIR}",
        default=".",
    )

    args = parser.parse_args()
    options = {}
    if args.models:
        options["models"] = args.models

    if args.outdir:
        options["outdir"] = args.outdir

    if args.plottype:
        options["plottype"] = args.plottype

    if args.list:
        print(f"supported plottypes are:")
        for t in PLOT_NAMES:
            print(f"\t- {t}")
        sys.exit(0)

    if args.startyear:
        options["startyear"] = int(args.startyear)

    if args.endyear:
        options["endyear"] = int(args.endyear)
    else:
        # use startyear
        options["endyear"] = options["startyear"] + 1

    if args.variables:
        options["vars"] = args.variables

    # error handling:
    if "models" not in options:
        print("model error")
        sys.exit(1)
    if "startyear" not in options:
        print("start year error")
        sys.exit(2)
    if "vars" not in options:
        print("var error")
        sys.exit(3)
    if "plottype" not in options:
        print("plottype error")
        sys.exit(4)

    # start plotting by loop through the supplied plot types
    # OBS: depending on the plottype the corresponding reading class has to be called
    # e.g. pya_read for reading model data via pyaerocom
    for _ptype in PLOT_NAMES:
        if _ptype in options["plottype"]:
            model_data = pya_read(options=options)
            plt_obj = Plotting(plotdir=options["outdir"])
            plt_obj.plot_pixel_map(model_data)
        else:
            print(f"plottype {_ptype} unknown. Skipping...")


def pya_read(options: dict) -> PyaModelData:
    """read model data using pyaerocom"""
    model_data = PyaModelData()
    for _model in options["models"]:
        model_data.read(
            _model, options["vars"], options["startyear"], options["endyear"]
        )
    return model_data


if __name__ == "__main__":
    main()
