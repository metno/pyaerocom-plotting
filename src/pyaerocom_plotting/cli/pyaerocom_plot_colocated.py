#!/usr/bin/env python3
"""
pyaerocom_plot_colocated: create plots pyaerocom's colocated data files
"""

import argparse
import sys
import numpy as np

from pyaerocom_plotting.const import DEFAULT_OUTPUT_DIR, PLOT_NAMES_COL
from pyaerocom_plotting.plotting import Plotting
from pyaerocom import ColocatedData


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
\t  The following line plots the time series plot (model mean) for the file {colors['BOLD']}./hm/ts/ALL-Aeronet-od550aer-Column.json{colors['END']}
\t  pyaerocom_plot_json -o /tmp -p overall_ts_SU -f /lustre/storeB/users/jang/aeroval-local-web/data/c3s/SU_Paper/hm/ts/ALL-Aeronet-od550aer-Column.json

""",
    )
    parser.add_argument("-f", "--file", help="file to read")
    parser.add_argument("-g", "--gcos", help="file to read", default=0)
    parser.add_argument("-t", "--title", help="plot title", nargs="+")
    parser.add_argument("-p", "--plottype", help="plot type(s) to plot", nargs="+")
    parser.add_argument(
        "-l", "--list", help="list supported plot types", action="store_true"
    )
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

    if args.gcos:
        if args.gcos == 1:
            options["gcos"] = True
        else:
            options["gcos"] = False
    else:
        options["gcos"] = False

    if args.outdir:
        options["outdir"] = args.outdir

    if args.plottype:
        options["plottype"] = args.plottype

    if args.title:
        options["plottitle"] = " ".join(args.title)
    else:
        options["plottitle"] = None

    if args.list:
        print(f"supported plottypes are:")
        for t in PLOT_NAMES_COL:
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
    # e.g. json_read for reading aeroval json files
    for _pidx, _ptype in enumerate(options["plottype"]):
        if _ptype == "scatterdensity":
            # scatterdensity
            col_data = col_read(options)
            plt_obj = Plotting(plotdir=options["outdir"])
            col_data_monthly = col_data.resample_time(
                to_ts_type="monthly", how="mean", min_num_obs=3
            )
            plt_obj.plot_scatterdensity(col_data_monthly)
        elif _ptype == "scatterplot":
            # classic scatterplot
            col_data = col_read(options)
            col_data_monthly = col_data.resample_time(
                to_ts_type="monthly", how="mean", min_num_obs=3
            )
            plt_obj = Plotting(plotdir=options["outdir"])
            plt_obj.plot_scatter(col_data_monthly, title=options["plottitle"], plot_gcos=options["gcos"])
        elif _ptype == "gcos":
            # gcos fractions
            col_data = col_read(options)
            col_data_monthly = col_data.resample_time(
                to_ts_type="monthly", how="mean", min_num_obs=3
            )
            from pyaerocom_plotting.stats import gcos_percentages

            gcos_stats = gcos_percentages(col_data)

            # print(gcos_stats)
            # print(f"GCOS fractions {col_data.model_name} / {col_data.obs_name}")
            out_arr = []
            out_header_arr = []
            out_header_arr.append("model_name")
            out_header_arr.append("obs_name")
            out_header_arr.append("start_time")
            out_header_arr.append("stop_time")
            out_arr.append(col_data_monthly.model_name)
            out_arr.append(col_data_monthly.obs_name)
            out_arr.append(np.datetime_as_string(col_data_monthly.time.min()))
            out_arr.append(np.datetime_as_string(col_data_monthly.time.max()))

            for crit in gcos_stats:
                out_arr.append(f"{gcos_stats[crit]:.1%}")
                out_header_arr.append(crit)

                # print(f"{crit}: {gcos_stats[crit]}")
            print(",".join(out_header_arr))
            print(",".join((out_arr)))
            assert gcos_stats
        else:
            print(f"plottype {_ptype} unknown. Skipping...")


def col_read(options: dict) -> ColocatedData:
    """read colocated data object data using pyaerocom"""
    col_data = ColocatedData(options["file"])
    return col_data


if __name__ == "__main__":
    main()