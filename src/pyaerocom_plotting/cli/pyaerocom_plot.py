#!/usr/bin/env python3
"""
pyaerocom plot: crerate plots using the pyaerocom API
"""

import argparse
import subprocess
import sys
from pathlib import Path
from tempfile import mkdtemp

from pyaerocom_plotting.const import DEFAULT_OUTPUT_DIR


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
        epilog=f"""{colors['BOLD']}Example usages:{colors['END']}""",
    )
    parser.add_argument("-m", "--models", help="models(s) to read", nargs="+")
    parser.add_argument(
        "-s",
        "--startyear",
        help="startyear to read",
    )
    parser.add_argument("-e", "--endyear", help="endyear to read; ", nargs="?")
    parser.add_argument("-v", "--variables", help="variable(s) to read", nargs="+")
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

    import pyaerocom.io as pio
    from pyaerocom.exceptions import VarNotAvailableError

    model_obj = {}
    model_data = {}

    for _model in options["models"]:
        model_obj[_model] = pio.ReadGridded(_model)

        model_data[_model] = {}
        for _var in options["vars"]:
            try:
                model_data[_model][_var] = model_obj[_model].read_var(
                    var_name=_var,
                    start=int(options["startyear"]),
                    stop=int(options["endyear"]),
                    ts_type="daily",
                )
            except VarNotAvailableError:
                print(
                    "Error: variable {_var} not available in files and can also not be computed. Skipping..."
                )

    for _model in options["models"]:
        for _var in options["vars"]:
            try:
                print(model_data[_model][_var])
            except KeyError:
                pass


if __name__ == "__main__":
    main()
