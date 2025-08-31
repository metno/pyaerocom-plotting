from pathlib import Path
import simplejson as json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import theilslopes, kendalltau

import argparse
import subprocess
import sys
from tempfile import mkdtemp

from pyaerocom_plotting.const import DEFAULT_OUTPUT_DIR, DEFAULT_TS_TYPE, PLOT_NAMES, USER_FRIENDLY_MODEL_NAMES
from pyaerocom_plotting.plotting import Plotting



# modelvar = "od550aer"
# modelvar = "od550aer"
# obsnetwork = "AeronetSDAV3L2"
# obsnetwork = "AeronetSunV3L2"
datatype = "Column"
# obsvar = modelvar
filter = "ALL"

plot_stat_prop = "mab"
plot_stat_props = [plot_stat_prop]
# INFILE = "/home/jang/data/aeroval-local-web/data/c3s/LTS_dual_view/hm/ts/ALL-AeronetSunV3L2-od550aer-Column.json"
# INFILE = "/home/jang/data/aeroval-local-web/remote-webserver/data/c3s/LTS_MODIS/hm/ts/ALL-AeronetSunV3L2-od550aer-Column.json"
# INFILE = "/home/jang/data/aeroval-local-web/data/c3s/IASI_LTS/hm/ts/ALL-AeronetSDAV3L2-od550dust-Column.json"
INFILE = "/home/jang/data/aeroval-local-web/data/c3s/combined.dual.view/hm/ts/ALL_AeronetSunV3L2_od550aer_Column.json"

OUTDIR = "/home/jang/data/c3s2_aerosol/PQAR_202509/images"

# DEFAULT_COLORS = "skyblue,black,lightgreen,skyblue,black,lightgreen".split(",")
# DEFAULT_COLORS = "skyblue,black,lightgreen,orange,skyblue,black,lightgreen,orange".split(",")
DEFAULT_COLORS = "skyblue,black,lightgreen,orange,darkviolet,skyblue,black,lightgreen,orange,darkviolet".split(",")
# DEFAULT_STYLE = "-,-,-,--,--,--,--".split(",")
# DEFAULT_STYLE = "-,-,-,-,--,--,--,--,--".split(",")
DEFAULT_STYLE = "-,-,-,-,-,--,--,--,--,--,--".split(",")
DATA_STYLE = "-"
TRENDS_STYLE = "--"
ms_per_year = 1.e3*60*60*24*365
# title="AOD - ALL - 1995-2022"
# title="AOD - ALL - 2003-2018"
title="dust AOD - ALL - 2007-2013"
subtitle=""

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
        description="create trend plots with Met Norway's pyaerocom package",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""{colors['BOLD']}Example usages:{colors['END']}
\t{colors['UNDERLINE']}- basic usage:{colors['END']}
\t  The following line plots the pixelmap for the model {colors['BOLD']}ECMWF_CAMS_REAN{colors['END']} for the year {colors['BOLD']}2019{colors['END']} for the variable {colors['BOLD']}od550aer{colors['END']}
\t  pyaerocom_plot -p pixelmap -m ECMWF_CAMS_REAN -s 2019 -v od550aer

""",
    )
    # parser.add_argument("-m", "--models", help="models(s) to read", nargs="+")
    # parser.add_argument("-p", "--plottype", help="plot type(s) to plot", nargs="+")
    # parser.add_argument("--varscalefile", help="user defined variable scale file",)
    parser.add_argument("-v", "--variables", help="variable(s) to read", nargs="+")
    parser.add_argument("--obsnetwork", help="obs network to read", nargs=1)
    parser.add_argument("-t", "--title", help="plot title", nargs="+")
    parser.add_argument("-r", "--removemodel", help="models to remove from plot", nargs="+")
    parser.add_argument("-f", "--file", help="file to read", nargs=1)
    parser.add_argument("-l", "--upperlimit", help="upper plot limit", nargs=1)
    parser.add_argument(
        "-o",
        "--outfile",
        help=f"output file name",
        default=".",
    )
    args = parser.parse_args()
    options = {}
    if args.file:
        options["file"] = args.file
    if args.outfile:
        options["outfile"] = args.outfile
    if args.title:
        options["plottitle"] = " ".join(args.title)
    else:
        options["plottitle"] = None

    if args.variables:
        options["vars"] = args.variables

    if args.obsnetwork:
        options["obsnetwork"] = args.obsnetwork

    if args.removemodel:
        options["removemodel"] = args.removemodel
    else:
        options["removemodel"] = []

    if args.upperlimit:
        options["upperlimit"] = args.upperlimit[0]
    else:
        options["upperlimit"] = None

    for _var in options["vars"]:
        plot(_var, options)

def plot(modelvar, options):
    # file=Path("/home/jang/data/aeroval-local-web/remote-webserver/data/c3s/LTS_dual_view/map/AeronetSunV3L2-od550aer_Column_LTS.ADV-od550aer_1995-2022.json")
    infile = Path(options["file"][0])
    obsnetwork = options["obsnetwork"][0]
    obsvar = modelvar
    if infile.exists():
        outfile = Path(options["outfile"])
        with open(infile) as infile:
            json_dict = json.load(infile)
        # models = json_dict[modelvar][obsnetwork][datatype].keys()
        models = []
        datadict = {}
        series = {}
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        modelno=len(models)
        for m_idx, model in enumerate(json_dict[modelvar][obsnetwork][datatype].keys()):
            if model in options["removemodel"]:
                continue
            models.append(model)
            print(f"reading model {model}...")
            datadict[model] = dict(time=[])
            series[model] = {}
            series[f"{model}.theil"] = {}
            for time in json_dict[modelvar][obsnetwork][datatype][model][obsvar][
                filter
            ]:
                datadict[model]["time"].append(float(time))
                for key in json_dict[modelvar][obsnetwork][datatype][model][obsvar][
                    filter
                ][time]:
                    val = json_dict[modelvar][obsnetwork][datatype][model][obsvar][
                                filter
                            ][time][key]

                    try:
                        datadict[model][key]["time"].append(float(time))
                        # datadict[model][key]["val"].append(val)
                        # )
                        datadict[model][key]["val"].append(
                            json_dict[modelvar][obsnetwork][datatype][model][obsvar][
                                filter
                            ][time][key]
                        )
                    except KeyError:
                        datadict[model][key] = dict(
                            time=[float(time)],
                            # val=[val],
                            val=[json_dict[modelvar][obsnetwork][datatype][model][obsvar][
                                filter
                            ][time][key]],
                        )


            data_style = []
            trend_style = []
            for key in datadict[model]:
                if key == "time":
                    continue
                if key not in plot_stat_props:
                    continue
                datadict[model][key]["val"] = np.array(datadict[model][key]["val"], dtype=float)
                datadict[model][key]["time"] = np.array(datadict[model][key]["time"], dtype=float)
                data_style.append(DATA_STYLE)
                trend_style.append(TRENDS_STYLE)
                # for _vidx, _val in enumerate(datadict[model][key]["val"]):
                #     if _val is None:
                #         datadict[model][key]["val"][_vidx] = np.nan
                # add theilslope data
                datadict[model][key]["theil_result"] = theilslopes(
                    datadict[model][key]["val"], x=datadict[model][key]["time"],
                    nan_policy='omit',
                )
                datadict[model][key]["theil_sen"] = datadict[model][key][
                    "theil_result"
                ][1] + datadict[model][key]["theil_result"][0] * np.array(
                    datadict[model][key]["time"]
                )
                # if np.isnan(datadict[model][key]["theil_sen"]):
                #     print("nan")
                datadict[model][key]["diff"] = (
                    datadict[model][key]["theil_sen"][-1]
                    - datadict[model][key]["theil_sen"][0]
                )
                datadict[model][key]["time_diff"] = (
                    datadict[model][key]["time"][-1] - datadict[model][key]["time"][0]
                )
                datadict[model][key]["trend"] = (
                    datadict[model][key]["diff"]
                    / datadict[model][key]["time_diff"]
                    *ms_per_year
                )
                datadict[model][key]["kendalltau_result"] = kendalltau(
                    datadict[model][key]["time"],
                    datadict[model][key]["val"],
                    nan_policy="omit",
                )
                datadict[model][key]["pval"] = datadict[model][key][
                    "kendalltau_result"
                ][1]

                # plot = ax.plot(
                #     pd.to_datetime(datadict[model][key]["time"]),
                #     datadict[model][key]["val"]
                #                 ,)
                # convert to pd.series
                print(f"{model}.{key}")
                if model in USER_FRIENDLY_MODEL_NAMES:
                    prt_model = USER_FRIENDLY_MODEL_NAMES[model]
                else:
                    prt_model = model
                series[model][key] = pd.Series(
                    data=datadict[model][key]["val"],
                    index=pd.to_datetime(datadict[model][key]["time"], unit='ms'),
                    name=f"{prt_model}",
                )
                # plot = ax.plot(series[model][key])
                # plot = ax.plot(
                #     pd.to_datetime(datadict[model][key]["time"]),
                #     datadict[model][key]["val"]
                #                 ,)

                series[f"{model}.theil"][key] = pd.Series(
                    data=datadict[model][key]["theil_sen"],
                    index=pd.to_datetime(datadict[model][key]["time"]),
                    name=f"trend[1/10y]:{datadict[model][key]['trend']*10:.3f};pval:{datadict[model][key]['pval']:.2f}",
                )

        # datadict[model].time=json_dict[modelvar][obsnetwork][datatype][model][obsvar][filter]
        # prepare pd.Dataframe for easy plotting

        df_full = pd.concat([series[model][plot_stat_prop] for model in models], axis=1)
        df_full.loc[pd.to_datetime("2015-01-15")] = np.nan
        # df_theil = pd.concat(
        #     [series[f"{model}.theil"][plot_stat_prop] for model in models], axis=1
        # )
        # # df_theil.loc[pd.to_datetime("2015-01-15")]=
        # df = pd.concat([df_full, df_theil], axis=1)
        #
        plot = df_full.plot(
            kind="line", ax=ax, color=DEFAULT_COLORS, style=DEFAULT_STYLE
        )
        idxs = [0, -1]
        plots = []
        for m_idx, model in enumerate(models):
            key = plot_stat_prop
            print(f"{model}:{datadict[model][key]['trend']}")
            plots.append(
                ax.plot(
                    pd.to_datetime(datadict[model][key]["time"], unit='ms'),
                    datadict[model][key]["theil_sen"],
                    TRENDS_STYLE,
                    # DEFAULT_STYLE[m_idx + modelno],
                    color=DEFAULT_COLORS[m_idx + modelno],
                    label=f"trend[1/10y]:{datadict[model][key]['trend']*10:-.3f};pval:{datadict[model][key]['pval']:.2f}",
                )
            )
        dummy = ax.set_xlabel("time")
        dummy = ax.set_ylabel("mean absolute bias")
        if options["upperlimit"] is not None:
            # ax.set_ylim((None, options["upperlimit"]))
            ax.set_ylim((None, 0.14))

        dummy = ax.set_title(options["plottitle"])

        # pdtime = pd.to_datetime(datadict[model][key]["time"])
        # for idx, col in enumerate(df_theil):
        #     if col == "views":
        #         continue
        #     print(f"col: {col}, {df_theil[col].values[np.array([0, -1])]}")
        #
        #     dummy = plt.plot(
        #         [pdtime[x] for x in idxs],
        #         df_theil[col].values[np.array([0, -1])],
        #         color=DEFAULT_COLORS[idx],
        #         linestyle="-",
        #     )
        #
        ax.legend(ncols=2)
        plt.savefig(outfile, dpi=300)
        print(f"{outfile} saved")

        # resdf=df.resample("M").nearest()
        # outfile = Path(OUTDIR) / f"{file.name}.resampled.png"
        # plot = resdf.plot.line(title="Theil-Sen trends of MAB",color=DEFAULT_COLORS, style=DEFAULT_STYLE)
        # dummy=plot.set_xlabel("time")
        # dummy=plot.set_ylabel("mean absolute bias")
        # # dummy = plt.axhline(PLT_PARAM[options['statparameter'][0]]['axhline'], color='grey', linestyle='-')
        #
        # plt.savefig(outfile, dpi=300)
        # print(f"{outfile} saved")

        print(models)


if __name__ == "__main__":
    main()
