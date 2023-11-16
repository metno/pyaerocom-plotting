from pathlib import Path

from pyaerocom_plotting.readers import AerovalJsonData, PyaModelData
from pyaerocom_plotting.plot_pixel_map import plot_pixel_map as _plot_pixel_map


class Plotting:
    """plotting class with methods for each supported plot"""

    __version__ = "0.0.2"
    DEFAULT_DPI = 300

    def plot_pixel_map(self, model_obj: PyaModelData, ):
        _plot_pixel_map(model_obj, )

    def __init__(self, plotdir: [str, Path]):
        self._plotdir = plotdir

    def plot_weighted_means(self, model_obj: PyaModelData):
        """method to plot weighted means"""
        pass

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
