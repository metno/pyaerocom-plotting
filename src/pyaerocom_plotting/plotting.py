from pathlib import Path

from pyaerocom_plotting.readers import AerovalJsonData, PyaModelData


class Plotting:
    """plotting class with methods for each supported plot"""

    __version__ = "0.0.2"
    DEFAULT_DPI = 300

    def __init__(self, plotdir: [str, Path]):
        self._plotdir = plotdir

    def plot_pixel_map(
        self,
        model_obj: PyaModelData,
    ):
        """method to plot pixelmaps

        due to lack of pyaerocom API documentation this uses the iris infrastructure which is also
        retained in pyaerocom's GriddedData object
        """

        import iris
        import iris.analysis.cartography
        import iris.plot as iplt
        import iris.quickplot as qplt
        import matplotlib.pyplot as plt

        # this will be a monthly plot for now
        # create monthly plot data
        mdata = {}
        ts_type = "monthly"
        for _model in model_obj.models:
            mdata[_model] = {}
            for _var in model_obj.variables:
                mdata[_model][_var] = model_obj.data[_model][_var].resample_time(
                    ts_type
                )
                # loop through the resulting time steps
                for _idx in range(mdata[_model][_var]["time"].points.size):
                    ts_data = mdata[_model][_var][_idx]
                    filename = f"{self._plotdir}/pixelmap_{_model}_{_var}_m{ts_data['time'].cell(0).point.month:02}{ts_data['time'].cell(0).point.year}_{ts_type}.png"
                    qplt.pcolormesh(ts_data.cube)
                    plt.gca().coastlines()
                    print(f"saving file: {filename}")
                    plt.savefig(filename, dpi=self.DEFAULT_DPI)
                    plt.close()

    def plot_weighted_means(self, model_obj: PyaModelData):
        """method to plot weighted means"""

        # this will be a monthly plot for now
        # create monthly plot data
        import iris.analysis.cartography
        from pyaerocom.helpers import cftime_to_datetime64
        import matplotlib.pyplot as plt
        from matplotlib.ticker import FuncFormatter
        from matplotlib.dates import MonthLocator, DateFormatter, YearLocator
        from datetime import datetime

        mdata = {}
        ts_type = "monthly"
        for _model in model_obj.models:
            mdata[_model] = {}
            fig = plt.figure(
                figsize=(21, 9),
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
                print("Anna start (one model / var at a time)")
                plots.append(ax.plot(time, mean.data, linewidth=2.0, marker="o", label=_var))

            plt.ylabel("weighted mean")
            ax.legend()
            #plt.xlabel("time")
            ax=plt.gca()
            ax.grid(color='#DDDDDD', linestyle='dashed')
            month_fmt = DateFormatter('%b')
            def m_fmt(x, pos=None):
                return month_fmt(x)[0]

            ax.xaxis.set_major_locator(MonthLocator(bymonth=[2,4,6,8,10,12]))
            ax.xaxis.set_major_formatter(FuncFormatter(m_fmt))
            # add second x-axis with Years
            sec_xaxis = ax.secondary_xaxis(-0.1)
            sec_xaxis.xaxis.set_major_locator(YearLocator(month=7))
            sec_xaxis.xaxis.set_major_formatter(DateFormatter('%Y'))
            # Hide the second x-axis spines and ticks
            sec_xaxis.spines['bottom'].set_visible(False)
            sec_xaxis.tick_params(length=0, labelsize=10, pad=-3)

            print(max(mean.data))
            ax.axvline(datetime(2023,6,27),color='black',linestyle='--')
            ax.text(datetime(2023,6,27), max(mean.data),'48r1', ha='center')
            ax.axvline(datetime(2021,10,13),color='black',linestyle='--')
            ax.text(datetime(2021,10,13), max(mean.data),'47r3', ha='center')
            ax.axvline(datetime(2021,5,19),color='black',linestyle='--')
            ax.text(datetime(2021,5,19), max(mean.data),'47r2', ha='center')
            ax.axvline(datetime(2020,10,6),color='black',linestyle='--')
            ax.text(datetime(2020,10,6), max(mean.data),'47r1', ha='center')
            ax.axvline(datetime(2019,7,9),color='black',linestyle='--')
            ax.text(datetime(2019,7,9), max(mean.data),'46r1', ha='center')
            ax.axvline(datetime(2018,6,26),color='black',linestyle='--')
            ax.text(datetime(2018,6,26), max(mean.data),'45r1', ha='center')
            ax.axvline(datetime(2017,9,26),color='black',linestyle='--')
            ax.text(datetime(2017,9,26), max(mean.data),'43r3', ha='center')
            ax.axvline(datetime(2017,1,24),color='black',linestyle='--')
            ax.text(datetime(2017,1,24), max(mean.data),'43r1', ha='center')
            ax.axvline(datetime(2016,6,21),color='black',linestyle='--')
            ax.text(datetime(2016,6,21), max(mean.data),'41r2', ha='center')
            ax.axvline(datetime(2015,9,3),color='black',linestyle='--')
            ax.text(datetime(2015,9,3), max(mean.data),'41r1', ha='center')          
            ax.axvline(datetime(2014,9,18),color='black',linestyle='--')
            ax.text(datetime(2014,9,18), max(mean.data),'40r2', ha='center')
            ax.axvline(datetime(2014,2,19),color='black',linestyle='--')
            ax.text(datetime(2014,2,19), max(mean.data),'40r1', ha='center')
            ax.axvline(datetime(2013,10,7),label='38r2',color='black',linestyle='--')
            ax.text(datetime(2013,10,7), max(mean.data),'38r2', ha='center')
            ax.axvline(datetime(2012,7,5),color='black',linestyle='--')
            ax.text(datetime(2012,7,5), max(mean.data),'37r3', ha='center')
            #ax.axvline(datetime(2009,9,1),color='black',linestyle='--')
            #ax.text(datetime(2009,9,1), max(mean.data),'36r1', ha='center')
            filename = f"{self._plotdir}/monthlyweightedmean_{_model}.png"
            print(f"saving file: {filename}")
            plt.savefig(filename, dpi=self.DEFAULT_DPI)
            plt.close()

    def plot_aeroval_overall_time_series_SU_Paper(
        self,
        json_data: AerovalJsonData,
        stat_prop: str = "data_mean",
        title: str = None,
    ):
        """method to plot the time series plot from aeroval's overall evaluation
        SPECIAL version for SU paper!!"""
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
                mdata[_model][json_data.modelvars[0]][json_data.regions[0]][x][
                    stat_prop
                ]
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
                mdata[_model][json_data.modelvars[0]][json_data.regions[0]][x][
                    stat_prop
                ]
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
