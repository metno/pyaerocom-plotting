from pathlib import Path
import simplejson as json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import theilslopes, kendalltau


modelvar = "od550aer"
modelvar = "od550aer"
obsnetwork = "AeronetSDAV3L2"
obsnetwork = "AeronetSunV3L2"
datatype = "Column"
obsvar = modelvar
filter = "ALL"

plot_stat_prop = "mab"
plot_stat_props = [plot_stat_prop]
# INFILE = "/home/jang/data/aeroval-local-web/data/c3s/LTS_dual_view/hm/ts/ALL-AeronetSunV3L2-od550aer-Column.json"
# INFILE = "/home/jang/data/aeroval-local-web/remote-webserver/data/c3s/LTS_MODIS/hm/ts/ALL-AeronetSunV3L2-od550aer-Column.json"
# INFILE = "/home/jang/data/aeroval-local-web/data/c3s/IASI_LTS/hm/ts/ALL-AeronetSDAV3L2-od550dust-Column.json"
INFILE = "/home/jang/data/aeroval-local-web/data/c3s/combined.dual.view/hm/ts/ALL_AeronetSunV3L2_od550aer_Column.json"

OUTDIR = "/home/jang/data/c3s2_aerosol/PQAR_202509/images"

# default_colors = "skyblue,black,lightgreen,skyblue,black,lightgreen".split(",")
# default_colors = "skyblue,black,lightgreen,orange,skyblue,black,lightgreen,orange".split(",")
default_colors = "skyblue,black,lightgreen,orange,darkviolet,skyblue,black,lightgreen,orange,darkviolet".split(",")
# default_style = "-,-,-,--,--,--,--".split(",")
# default_style = "-,-,-,-,--,--,--,--,--".split(",")
default_style = "-,-,-,-,-,--,--,--,--,--,--".split(",")
ms_per_year = 1.e3*60*60*24*365
# title="AOD - ALL - 1995-2022"
# title="AOD - ALL - 2003-2018"
title="dust AOD - ALL - 2007-2013"
subtitle=""

def main():
    # file=Path("/home/jang/data/aeroval-local-web/remote-webserver/data/c3s/LTS_dual_view/map/AeronetSunV3L2-od550aer_Column_LTS.ADV-od550aer_1995-2022.json")
    file = Path(INFILE)
    if file.exists():
        outfile = Path(OUTDIR) / f"{file.name}.png"
        with open(file) as infile:
            json_dict = json.load(infile)
        models = json_dict[modelvar][obsnetwork][datatype].keys()
        datadict = {}
        series = {}
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        modelno=len(models)
        for m_idx, model in enumerate(models):
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



            for key in datadict[model]:
                if key == "time":
                    continue
                if key not in plot_stat_props:
                    continue
                datadict[model][key]["val"] = np.array(datadict[model][key]["val"], dtype=float)
                datadict[model][key]["time"] = np.array(datadict[model][key]["time"], dtype=float)
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
                series[model][key] = pd.Series(
                    data=datadict[model][key]["val"],
                    index=pd.to_datetime(datadict[model][key]["time"], unit='ms'),
                    name=f"{model}",
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
            kind="line", ax=ax, color=default_colors, style=default_style
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
                    default_style[m_idx + modelno],
                    color=default_colors[m_idx + modelno],
                    label=f"trend[1/10y]:{datadict[model][key]['trend']*10:-.3f};pval:{datadict[model][key]['pval']:.2f}",
                )
            )
        dummy = ax.set_xlabel("time")
        dummy = ax.set_ylabel("mean absolute bias")
        # ax.set_ylim((None, 0.14))
        dummy = ax.set_title(title)

        # pdtime = pd.to_datetime(datadict[model][key]["time"])
        # for idx, col in enumerate(df_theil):
        #     if col == "views":
        #         continue
        #     print(f"col: {col}, {df_theil[col].values[np.array([0, -1])]}")
        #
        #     dummy = plt.plot(
        #         [pdtime[x] for x in idxs],
        #         df_theil[col].values[np.array([0, -1])],
        #         color=default_colors[idx],
        #         linestyle="-",
        #     )
        #
        ax.legend(ncols=2)
        plt.savefig(outfile, dpi=300)
        print(f"{outfile} saved")

        # resdf=df.resample("M").nearest()
        # outfile = Path(OUTDIR) / f"{file.name}.resampled.png"
        # plot = resdf.plot.line(title="Theil-Sen trends of MAB",color=default_colors, style=default_style)
        # dummy=plot.set_xlabel("time")
        # dummy=plot.set_ylabel("mean absolute bias")
        # # dummy = plt.axhline(PLT_PARAM[options['statparameter'][0]]['axhline'], color='grey', linestyle='-')
        #
        # plt.savefig(outfile, dpi=300)
        # print(f"{outfile} saved")

        print(models)


if __name__ == "__main__":
    main()
