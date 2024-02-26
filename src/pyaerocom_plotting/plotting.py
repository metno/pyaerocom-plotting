from pathlib import Path

import cartopy.crs as ccrs
import cartopy.feature as cf
import iris.plot as iplt
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from pyaerocom import ColocatedData
from pyaerocom.aeroval.glob_defaults import var_ranges_defaults

from pyaerocom_plotting.readers import AerovalJsonData, PyaModelData
from pyaerocom_plotting.const import (
    USER_FRIENDLY_VAR_NAMES,
    USER_FRIENDLY_OBS_NAMES,
    USER_FRIENDLY_MODEL_NAMES,
)


class Plotting:
    """plotting class with methods for each supported plot"""

    __version__ = "0.0.3"
    DEFAULT_DPI = 300

    def __init__(self, plotdir: [str, Path]):
        self._plotdir = plotdir

    def plot_scatter(
        self,
        plot_obj: ColocatedData,
        title: str = None,
        plot_gcos=True,
        gcos_err_percent: float = 0.1,
        gcos_abs_err: float = 0.03,
            plot_log = False,
        **kwargs,
    ):
        """method to plot scatterplots using pyaerocom

        due to lack of pyaerocom API documentation this uses the iris infrastructure which is also
        retained in pyaerocom's GriddedData object
        """

        import matplotlib.pyplot as plt
        import numpy as np

        from pyaerocom_plotting.const import GCOS_CRITERION

        # gcos_err_percent = 0.1
        # gcos_abs_err = 0.03
        # gcos_ stuff
        gcos_x_data_low = np.arange(19) * 0.005 + 0.005
        gcos_x_data_middle = np.arange(19) * 0.05 + 0.1
        gcos_x_data_high = np.arange(19) * 0.5 + 1.0
        gcos_x_data = np.array(
            [gcos_x_data_low, gcos_x_data_middle, gcos_x_data_high]
        ).flatten()
        gcos_y_data = np.add(gcos_x_data, np.multiply(gcos_x_data, gcos_err_percent))
        # gcos_y_data = np.multiply(gcos_x_data, gcos_err_percent)
        gcos_y_data[gcos_y_data <= gcos_abs_err] = gcos_abs_err
        # i_DummyArr = where(f_GCOSYDataDiffpercent lt fC_GCOSAbsCrit / fC_GCOSPercentCrit, i_Dummy)
        # i_MinPercentVal = f_GCOSYDataDiffpercent[i_DummyArr[-1] + 1]
        # if i_Dummy gt 0 then f_GCOSYDataDiffpercent[i_DummyArr]=f_GCOSXData[i_DummyArr]+fC_GCOSAbsCrit

        fig = plt.figure(
            figsize=(12, 12),
        )
        ax = fig.add_subplot(1, 1, 1)

        plots = []
        obs_data = plot_obj.data.data[0, :, :].flatten()
        obs_name = plot_obj.metadata["data_source"][0]
        model_data = plot_obj.data.data[1, :, :].flatten()
        model_name = plot_obj.metadata["data_source"][1]
        aerocom_var_name = plot_obj.var_name[1]
        model_var = plot_obj.var_name[1]
        upper_var_val = max(var_ranges_defaults[model_var]["scale"])
        lower_var_val = min(var_ranges_defaults[model_var]["scale"])

        # xlim = [0.01, int(np.ceil(np.nanmax(model_data)))]
        # ylim = [0.01, int(np.ceil(np.nanmax(obs_data)))]


        if plot_log:
            ax.set_yscale("log")
            ax.set_xscale("log")
            xlim = [0.01, 10.0]
            ylim = [0.01, 10.0]
        else:
            xlim = [lower_var_val, upper_var_val]
            ylim = [lower_var_val, upper_var_val]
# xlim=(0,6), ylim=(0.6)
        plots.append(
            ax.scatter(
                obs_data,
                model_data,
                marker="+",
                color="black",
            )
        )
        # ax.hexbin(x, y, gridsize=20)
        if plot_gcos:
            pass
            plots.append(
                ax.plot(gcos_x_data, gcos_y_data, color="lightgreen", linewidth=3)
            )
            plots.append(
                ax.plot(gcos_y_data, gcos_x_data, color="lightgreen", linewidth=3)
            )

        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        # ax.plot([xlim[0], ylim[0]], [xlim[-1], ylim[-1]], color="grey", linewidth=1, linestyle="--")
        ax.plot(xlim, ylim, color="grey", linewidth=2, linestyle="--")
        if title is not None:
            ax.set_title(title)
        else:
            try:
                ax.set_title(f"scatter plot  {USER_FRIENDLY_VAR_NAMES[model_var]}")
            except KeyError:
                ax.set_title(f"scatter plot {model_var}")

        try:
            plt.xlabel(f"{USER_FRIENDLY_MODEL_NAMES[model_name]}")
        except KeyError:
            plt.xlabel(f"{model_name}")

        try:
            plt.ylabel(f"{USER_FRIENDLY_OBS_NAMES[obs_name]}")
        except KeyError:
            plt.ylabel(f"{obs_name}")

        ax.set_aspect("equal")
        filename = f"{self._plotdir}/scatter_{model_name}-{obs_name}.png"
        print(f"saving file: {filename}")
        plt.savefig(filename, dpi=self.DEFAULT_DPI)
        plt.close()

        pass

    def plot_scatterdensity(
        self,
        plot_obj: ColocatedData,
        title: str = None,
        plot_gcos=True,
        colormap: str = "viridis_r",
        gcos_color="black",
        gcos_err_percent: float = 0.1,
        gcos_abs_err: float = 0.03,
        **kwargs,
    ):
        """method to plot scatterplots using pyaerocom

        due to lack of pyaerocom API documentation this uses the iris infrastructure which is also
        retained in pyaerocom's GriddedData object
        """
        import pandas as pd

        fig = plt.figure(
            figsize=(12, 12),
        )
        ax = fig.add_subplot(1, 1, 1)

        gcos_x_data_low = np.arange(19) * 0.005 + 0.005
        gcos_x_data_middle = np.arange(19) * 0.05 + 0.1
        gcos_x_data_high = np.arange(19) * 0.5 + 1.0
        gcos_x_data = np.array(
            [gcos_x_data_low, gcos_x_data_middle, gcos_x_data_high]
        ).flatten()
        gcos_y_data = np.add(gcos_x_data, np.multiply(gcos_x_data, gcos_err_percent))
        # gcos_y_data = np.multiply(gcos_x_data, gcos_err_percent)
        gcos_y_data[gcos_y_data <= gcos_abs_err] = gcos_abs_err

        plots = []
        obs_data = plot_obj.data.data[0, :, :].flatten()
        obs_name = plot_obj.metadata["data_source"][0]
        model_data = plot_obj.data.data[1, :, :].flatten()
        model_name = plot_obj.metadata["data_source"][1]
        model_var = plot_obj.var_name[1]
        upper_var_val = max(var_ranges_defaults[model_var]["scale"])

        # cmap = mpl.colormaps[colormap]
        bins = (
            np.arange(0, upper_var_val + 0.05, 0.05),
            np.arange(0, upper_var_val + 0.05, 0.05),
        )
        # hist_data = np.histogram2d(model_data, obs_data, bins=bins)[0]
        cmcolors = mpl.colormaps[colormap](np.arange(256))
        cmcolors[0] = np.ones(4)
        cmap = mpl.colors.ListedColormap(
            cmcolors, name="griesiemap", N=cmcolors.shape[0]
        )

        hist_data = np.histogram2d(model_data, obs_data, bins=bins)
        hist_data[0][hist_data[0] == 0] = -1

        # bounds = var_ranges_defaults[_var]['scale']
        # bounds = np.array((  0,  10,  20,  30,  40,  50,  60,  70,  80,  90, 100,  200, 300, 400, 500, 1000, 2000, 3000, 4000, 5000), dtype=float)
        bounds = np.array(
            (
                1,
                10,
                20,
                30,
                40,
                50,
                60,
                70,
                80,
                90,
                100,
                200,
                300,
                400,
                500,
                1000,
                2000,
            ),
            dtype=float,
        )
        norm = mpl.colors.BoundaryNorm(
            bounds,
            cmap.N,
            extend="both",
        )
        # norm = mpl.colors.Normalize(vmin=0, vmax=hist_data.max())
        # norm = mpl.colors.LogNorm(vmin=0.01, vmax=hist_data.max())
        # ax.scatter(x, y, s=sizes, c=colors, vmin=0, vmax=100)
        # plots.append(ax.hist2d(model_data, obs_data, bins=bins, cmap=cmap, norm=norm))
        plots.append(
            ax.pcolormesh(
                hist_data[1], hist_data[2], hist_data[0], cmap=cmap, norm=norm
            )
        )
        # ax.hexbin(x, y, gridsize=20)
        xlim = [0.0, upper_var_val]
        ylim = [0.0, upper_var_val]
        # ax.set_yticks(bins[0])
        # ax.set_yticklabels(ylabels)
        # ax.set_xticks(bins[1])
        # ax.set_xticklabels(xlabels)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_aspect("equal")

        ax.plot(xlim, ylim, color="black", linewidth=1, linestyle="--")
        if plot_gcos:
            pass
            plots.append(
                ax.plot(gcos_x_data, gcos_y_data, color=gcos_color, linewidth=1.5)
            )
            plots.append(
                ax.plot(gcos_y_data, gcos_x_data, color=gcos_color, linewidth=1.5)
            )

        if title is not None:
            ax.set_title(title)
        else:
            try:
                ax.set_title(f"scatterdensity {USER_FRIENDLY_VAR_NAMES[model_var]}")
            except KeyError:
                ax.set_title(f"scatterdensity {model_var}")

        fig.colorbar(
            mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
            ax=ax,
            orientation="vertical",
            aspect=15,
            extend="max",
            label="number of occurrences",
        )
        try:
            plt.xlabel(f"{USER_FRIENDLY_MODEL_NAMES[model_name]}")
        except KeyError:
            plt.xlabel(f"{model_name}")

        try:
            plt.ylabel(f"{USER_FRIENDLY_OBS_NAMES[obs_name]}")
        except KeyError:
            plt.ylabel(f"{obs_name}")

        startdate = pd.to_datetime(str(plot_obj.time.data.min())).strftime("%Y%m%d")
        enddate = pd.to_datetime(str(plot_obj.time.data.max())).strftime("%Y%m%d")
        filename = f"{self._plotdir}/scatterdensity_{model_var}_{model_name}-{obs_name}-{startdate}-{enddate}.png"
        print(f"saving file: {filename}")
        plt.savefig(filename, dpi=self.DEFAULT_DPI)
        plt.close()

        pass

    def plot_pixel_map(
        self,
        model_obj: PyaModelData,
        ts_type: str = "yearly",
        title: str = None,
        colormap: str = None,
        plot_grid: bool = False,
    ):
        """method to plot pixelmaps

        due to lack of pyaerocom API documentation this uses the iris infrastructure which is also
        retained in pyaerocom's GriddedData object
        """

        import iris
        import iris.analysis.cartography
        import iris.plot as iplt
        import iris.quickplot as qplt

        crs_latlon = ccrs.PlateCarree()
        # this will be a monthly plot for now
        # create monthly plot data
        mdata = {}
        # ts_type = "monthly"
        yticks = np.arange(-90, 91, 30)
        ylabels = [f"{x:-2.0f}°" for x in yticks]
        xticks = np.arange(-180, 181, 30)
        xlabels = [f"{x:-2.0f}°" for x in xticks]

        for _model in model_obj.models:
            mdata[_model] = {}
            for _var in model_obj.variables:
                if colormap is None:
                    colormap = var_ranges_defaults[_var]["colmap"]
                cmap = mpl.colormaps[colormap]
                bounds = var_ranges_defaults[_var]["scale"]
                norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend="both")
                # norm = mpl.colors.Normalize(vmin=0, vmax=2)

                mdata[_model][_var] = model_obj.data[_model][_var].resample_time(
                    ts_type
                )
                # loop through the resulting time steps
                for _idx in range(mdata[_model][_var]["time"].points.size):
                    plots = []

                    fig = plt.figure(
                        figsize=(16, 9),
                    )

                    # ax = fig.add_subplot(1, 1, 1)
                    ax = plt.axes(projection=crs_latlon)

                    ts_data = mdata[_model][_var][_idx]
                    unit = str(ts_data.unit)
                    if unit != "1":
                        fig.colorbar(
                            mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
                            ax=ax,
                            orientation="vertical",
                            label=str(ts_data.unit),
                        )
                    else:
                        fig.colorbar(
                            mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
                            ax=ax,
                            orientation="vertical",
                            aspect=15,
                            extend="max",
                        )

                    if ts_type == "monthly":
                        filename = f"{self._plotdir}/pixelmap_{_model}_{_var}_m{ts_data['time'].cell(0).point.month:02}{ts_data['time'].cell(0).point.year}_{ts_type}.png"
                    elif ts_type == "yearly":
                        filename = f"{self._plotdir}/pixelmap_{_model}_{_var}_y{ts_data['time'].cell(0).point.year}_{ts_type}.png"
                    else:
                        raise ValueError(f"Unrecognized ts_type: {ts_type}")

                    if title is None:
                        plt_title = f"{_var} {_model} {ts_data['time'].cell(0).point.year} {ts_type}"
                    else:
                        plt_title = (
                            f"{title} {ts_data['time'].cell(0).point.year} {ts_type}"
                        )

                    plt.title(plt_title)
                    plots.append(iplt.pcolormesh(ts_data.cube, norm=norm, cmap=cmap))
                    # qplt.pcolormesh(ts_data.cube)
                    ax.add_feature(cf.COASTLINE, linewidth=0.75, color="black")
                    ax.add_feature(cf.BORDERS, linewidth=0.75, color="black")
                    if plot_grid:
                        ax.gridlines(crs=crs_latlon, linestyle="-")
                    ax.set_yticks(yticks)
                    ax.set_yticklabels(ylabels)
                    ax.set_xticks(xticks)
                    ax.set_xticklabels(xlabels)
                    # ax.set_yticks(np.arange(0, 100.1, 100/3))
                    ax.set_xlabel("longitude")
                    ax.set_ylabel("latitude")
                    print(f"saving file: {filename}")
                    plt.savefig(filename, dpi=self.DEFAULT_DPI)
                    plt.close()

    def plot_weighted_means(self, model_obj: PyaModelData):
        """method to plot weighted means"""

        # this will be a monthly plot for now
        # create monthly plot data
        from datetime import datetime

        import iris.analysis.cartography
        import matplotlib.pyplot as plt
        from matplotlib.dates import DateFormatter, MonthLocator, YearLocator
        from matplotlib.ticker import FuncFormatter
        from pyaerocom.helpers import cftime_to_datetime64

        mdata = {}
        ts_type = "monthly"
        for _model in model_obj.models:
            mdata[_model] = {}
            fig = plt.figure(
                figsize=(21, 6),
            )
            ax = fig.add_subplot(1, 1, 1)

            plots = []
            for _var in model_obj.variables:
                mdata[_model][_var] = model_obj.data[_model][_var].resample_time(
                    ts_type
                )
                weights = mdata[_model][_var].area_weights
                mean = mdata[_model][_var].cube.collapsed(
                    ["latitude", "longitude"], iris.analysis.MEAN, weights=weights
                )
                # the actual data is in mean.data as masked numpy array
                time = cftime_to_datetime64(
                    mean.coord("time").points,
                    cfunit=str(mean.coord("time").units),
                    calendar=mean.coord("time").units.calendar,
                )
                print(time)
                if _var == "od550so4":
                    plots.append(
                        ax.plot(
                            time,
                            mean.data,
                            linewidth=2.0,
                            marker="o",
                            label="sulphate",
                            color="blue",
                        )
                    )
                    maxmean = max(mean.data)
                elif _var == "od550oa":
                    plots.append(
                        ax.plot(
                            time,
                            mean.data,
                            linewidth=2.0,
                            marker="o",
                            label="organics",
                            color="red",
                        )
                    )
                elif _var == "od550bc":
                    plots.append(
                        ax.plot(
                            time,
                            mean.data,
                            linewidth=2.0,
                            marker="o",
                            label="black carbon",
                            color="green",
                        )
                    )
                elif _var == "od550ss":
                    plots.append(
                        ax.plot(
                            time,
                            mean.data,
                            linewidth=2.0,
                            marker="o",
                            label="sea salt",
                            color="purple",
                        )
                    )
                elif _var == "od550dust":
                    plots.append(
                        ax.plot(
                            time,
                            mean.data,
                            linewidth=2.0,
                            marker="o",
                            label="dust",
                            color="orange",
                        )
                    )
                elif _var == "od550no3":
                    plots.append(
                        ax.plot(
                            time,
                            mean.data,
                            linewidth=2.0,
                            marker="o",
                            label="nitrate",
                            color="brown",
                        )
                    )
                elif _var == "od550nh4":
                    plots.append(
                        ax.plot(
                            time,
                            mean.data,
                            linewidth=2.0,
                            marker="o",
                            label="ammonium",
                            color="cyan",
                        )
                    )
                elif _var == "od550soa":
                    plots.append(
                        ax.plot(
                            time,
                            mean.data,
                            linewidth=2.0,
                            marker="o",
                            label="sec organics",
                            color="magenta",
                        )
                    )

            plt.title("Global monthly mean speciated AOD at 550nm for the CAMS o-suite")
            plt.ylabel("weighted mean")
            ax.legend(loc="upper left", fontsize=10)
            # plt.xlabel("time")
            ax = plt.gca()
            ax.grid(color="#DDDDDD", linestyle="dashed")
            ax.set_ylim(ymin=0)
            month_fmt = DateFormatter("%b")

            def m_fmt(x, pos=None):
                return month_fmt(x)[0]

            ax.xaxis.set_major_locator(MonthLocator(bymonth=[2, 4, 6, 8, 10, 12]))
            ax.xaxis.set_major_formatter(FuncFormatter(m_fmt))
            # add second x-axis with Years
            sec_xaxis = ax.secondary_xaxis(-0.1)
            sec_xaxis.xaxis.set_major_locator(YearLocator(month=7))
            sec_xaxis.xaxis.set_major_formatter(DateFormatter("%Y"))
            # Hide the second x-axis spines and ticks
            sec_xaxis.spines["bottom"].set_visible(False)
            sec_xaxis.tick_params(length=0, labelsize=14, pad=-3)

            print(max(mean.data))
            ax.axvline(datetime(2023, 6, 27), color="black", linestyle="--")
            ax.text(datetime(2023, 6, 27), maxmean, "48r1", ha="center", fontsize=10)
            ax.axvline(datetime(2021, 10, 13), color="black", linestyle="--")
            ax.text(datetime(2021, 10, 13), maxmean, "47r3", ha="center", fontsize=10)
            ax.axvline(datetime(2021, 5, 19), color="black", linestyle="--")
            ax.text(datetime(2021, 5, 19), maxmean, "47r2", ha="center", fontsize=10)
            ax.axvline(datetime(2020, 10, 6), color="black", linestyle="--")
            ax.text(datetime(2020, 10, 6), maxmean, "47r1", ha="center", fontsize=10)
            ax.axvline(datetime(2019, 7, 9), color="black", linestyle="--")
            ax.text(datetime(2019, 7, 9), maxmean, "46r1", ha="center", fontsize=10)
            ax.axvline(datetime(2018, 6, 26), color="black", linestyle="--")
            ax.text(datetime(2018, 6, 26), maxmean, "45r1", ha="center", fontsize=10)
            ax.axvline(datetime(2017, 9, 26), color="black", linestyle="--")
            ax.text(datetime(2017, 9, 26), maxmean, "43r3", ha="center", fontsize=10)
            ax.axvline(datetime(2017, 1, 24), color="black", linestyle="--")
            ax.text(datetime(2017, 1, 24), maxmean, "43r1", ha="center", fontsize=10)
            ax.axvline(datetime(2016, 6, 21), color="black", linestyle="--")
            ax.text(datetime(2016, 6, 21), maxmean, "41r2", ha="center", fontsize=10)
            ax.axvline(datetime(2015, 9, 3), color="black", linestyle="--")
            ax.text(datetime(2015, 9, 3), maxmean, "41r1", ha="center", fontsize=10)
            ax.axvline(datetime(2014, 9, 18), color="black", linestyle="--")
            ax.text(datetime(2014, 9, 18), maxmean, "40r2", ha="center", fontsize=10)
            ax.axvline(datetime(2014, 2, 19), color="black", linestyle="--")
            ax.text(datetime(2014, 2, 19), maxmean, "40r1", ha="center", fontsize=10)
            ax.axvline(
                datetime(2013, 10, 7), label="38r2", color="black", linestyle="--"
            )
            ax.text(datetime(2013, 10, 7), maxmean, "38r2", ha="center", fontsize=10)
            # ax.axvline(datetime(2012,7,5),color='black',linestyle='--')
            # ax.text(datetime(2012,7,5), max(mean.data),'37r3', ha='center')
            # ax.axvline(datetime(2009,9,1),color='black',linestyle='--')
            # ax.text(datetime(2009,9,1), max(mean.data),'36r1', ha='center')
            filename = f"{self._plotdir}/monthlyweightedmean_{_model}.png"
            print(f"saving file: {filename}")
            plt.savefig(filename, dpi=self.DEFAULT_DPI)
            plt.close()

    def plot_aeroval_overall_time_series_SU_Paper(
        self,
        json_data: AerovalJsonData,
        stat_prop: str = "data_mean",
        title: str = None,
        colours: list[str] = [],
    ):
        """method to plot the time series plot from aeroval's overall evaluation
        SPECIAL version for SU paper!!"""
        import matplotlib.pyplot as plt
        import numpy as np

        LABEL_SUBSTITUTES = {
            "SLSTR.SU.A": "SLSTR-A",
            "SLSTR.SU.B": "SLSTR-B",
            "AATSR": "AATSR",
            "ATSR2": "ATSR-2",
        }
        COLOURS = {
            "ATSR-2": "brown",
            "AATSR": "green",
            "SLSTR-A": "red",
            "SLSTR-B": "blue",
        }

        # fig, ax = plt.subplots()
        # fig = plt.figure(figsize=(16, 9), layout="constrained")
        fig = plt.figure(
            figsize=(16, 9),
        )
        ax = fig.add_subplot(1, 1, 1)
        # ax = fig.add_axes([0.15, 0.15, 0.8, 0.75])

        plots = []
        # [file][_var][_obsnetwork][_code][_model][_modelvar]
        mdata = json_data.data[json_data.files[0]][json_data.vars[0]][
            json_data.obsnetworks[0]
        ][json_data.code[0]]
        # to get the right model order
        models = ["ATSR2", "AATSR", "SLSTR.SU.A", "SLSTR.SU.B"]
        # for _midx, _model in enumerate(sorted(json_data.models)):
        for _midx, _model in enumerate(models):
            # does not work without the conversion to integer in between
            ts = np.array(
                list(mdata[_model][json_data.modelvars[0]][json_data.regions[0]]),
                dtype=int,
            ).astype("datetime64[ms]")
            ts_keys = list(mdata[_model][json_data.modelvars[0]][json_data.regions[0]])
            ts_vals = [
                mdata[_model][json_data.modelvars[0]][json_data.regions[0]][x][
                    stat_prop
                ]
                for x in ts_keys
            ]
            try:
                label = LABEL_SUBSTITUTES[_model]
                color = COLOURS[label]
            except NameError:
                label = _model
                color = None
            plots.append(ax.plot(ts, ts_vals, linewidth=2.0, color=color, label=label))
            # add reference data if the plot property is "data_mean"
            if stat_prop == "data_mean":
                # get color of last plot
                last_color = plots[-1][0].get_color()
                ts_vals = [
                    mdata[_model][json_data.modelvars[0]][json_data.regions[0]][x][
                        "refdata_mean"
                    ]
                    for x in ts_keys
                ]
                plots.append(
                    ax.plot(
                        ts,
                        ts_vals,
                        linewidth=2.0,
                        c="black",
                        ls="dotted",
                        label=f"_ref {_model}",
                    )
                )

        ts_vals = [np.nan for x in range(len(ts_vals))]
        ax.plot(
            ts,
            ts_vals,
            linewidth=2.0,
            c="black",
            ls="dotted",
            label=f"Aeronet",
        )
        ax.legend()
        ax.set_ylim(0, None)
        plt.xlabel("Year")
        plt.ylabel("Mean Monthly AOD")
        plt.minorticks_on()
        # plt.grid(True)

        if title is None:
            plt.title(json_data.regions[0])
        else:
            plt.title(title)

        filename = f"{self._plotdir}/overallts_{json_data.vars[0]}_{stat_prop}_{json_data.obsnetworks[0]}_{json_data.code[0]}.png"
        print(f"saving file: {filename}")
        plt.savefig(filename, dpi=self.DEFAULT_DPI)
        plt.close()
        # plt.show()
        # print(_midx)


def plot_aeroval_overall_time_series(
    self,
    json_data: AerovalJsonData,
    stat_prop: str = "data_mean",
    title: str = None,
):
    """method to plot the time series plot from aeroval's overall evaluation"""
    import matplotlib.pyplot as plt
    import numpy as np

    # fig, ax = plt.subplots()
    fig = plt.figure(figsize=(16, 9), layout="constrained")
    ax = fig.add_subplot(1, 1, 1)
    # ax = fig.add_axes([0.15, 0.15, 0.8, 0.75])

    plots = []
    # [file][_var][_obsnetwork][_code][_model][_modelvar]
    mdata = json_data.data[json_data.files[0]][json_data.vars[0]][
        json_data.obsnetworks[0]
    ][json_data.code[0]]
    for _midx, _model in enumerate(json_data.models):
        # does not work without the conversion to integer in between
        ts = np.array(
            list(mdata[_model][json_data.modelvars[0]][json_data.regions[0]]),
            dtype=int,
        ).astype("datetime64[ms]")
        ts_keys = list(mdata[_model][json_data.modelvars[0]][json_data.regions[0]])
        ts_vals = [
            mdata[_model][json_data.modelvars[0]][json_data.regions[0]][x][stat_prop]
            for x in ts_keys
        ]
        plots.append(ax.plot(ts, ts_vals, linewidth=2.0, label=_model))
        # add reference data if the plot property is "data_mean"
        if stat_prop == "data_mean":
            # get color of last plot
            last_color = plots[-1][0].get_color()
            ts_vals = [
                mdata[_model][json_data.modelvars[0]][json_data.regions[0]][x][
                    "refdata_mean"
                ]
                for x in ts_keys
            ]
            plots.append(
                ax.plot(
                    ts,
                    ts_vals,
                    linewidth=2.0,
                    c=last_color,
                    ls="dotted",
                    label=f"ref {_model}",
                )
            )

    ax.legend()
    plt.xlabel("time")
    plt.ylabel(json_data.modelvars[0])
    if title is None:
        plt.title(json_data.regions[0])
    else:
        plt.title(title)

    filename = f"{self._plotdir}/overallts_{json_data.vars[0]}_{stat_prop}_{json_data.obsnetworks[0]}_{json_data.code[0]}.png"
    print(f"saving file: {filename}")
    plt.savefig(filename, dpi=self.DEFAULT_DPI)
    plt.close()
    # plt.show()
    # print(_midx)
    pass
