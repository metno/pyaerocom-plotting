"""plot pixel maps"""
import numpy as np

from pyaerocom_plotting.readers import PyaModelData
from pathlib import Path
import iris
import iris.analysis.cartography
import iris.plot as iplt
import iris.quickplot as qplt
import matplotlib.pyplot as plt

# from pyaerocom.aeroval.glob_defaults import var_ranges_defaults

import cartopy.crs as ccrs
from cartopy.mpl.geoaxes import GeoAxes
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter
from matplotlib.colors import BoundaryNorm, LogNorm, Normalize
from pyaerocom.region import Region
from pyaerocom_plotting.const import DEFAULT_DPI, FIGSIZE_DEFAULT

from matplotlib.ticker import MaxNLocator


def plot_pixel_map(
    model_obj: PyaModelData,
    plotdir: [str, Path],
    dpi: int = DEFAULT_DPI,
    projection: GeoAxes = ccrs.PlateCarree(),
):
    """method to plot pixelmaps

    due to lack of pyaerocom API documentation this uses the iris infrastructure which is also
    retained in pyaerocom's GriddedData object
    """

    # this will be a monthly plot for now
    # create monthly plot data
    mdata = {}
    ts_type = "monthly"
    iris_flag = False
    # two implementations for now: within iris, or all by hand

    for _model in model_obj.models:
        mdata[_model] = {}
        for _var in model_obj.variables:
            mdata[_model][_var] = model_obj.data[_model][_var].resample_time(ts_type)
            # get aeroval mapping info
            # keys: dict_keys(['scale', 'colmap'])
            plotinfo = get_aeroval_plot_info(_var)

            lat_name = mdata[_model][_var].dimcoord_names[1]
            lon_name = mdata[_model][_var].dimcoord_names[2]
            if str(mdata[_model][_var].units) == "1":
                unit_text = f"{_var}"
            else:
                unit_text = f"{_var} [{mdata[_model][_var].units}]"

            # prep discrete mapping levels according to aeroval
            npscale = np.array(plotinfo["scale"])
            levels = MaxNLocator(nbins=npscale.size).tick_values(
                npscale.min(), npscale.max()
            )
            cmap = plt.colormaps[plotinfo["colmap"]]
            norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
            # loop through the resulting time steps

            for _idx in range(mdata[_model][_var]["time"].points.size):
                ts_data = mdata[_model][_var][_idx]
                filename = f"{plotdir}/pixelmap_{_model}_{_var}_m{ts_data['time'].cell(0).point.month:02}{ts_data['time'].cell(0).point.year}_{ts_type}.png"
                title = f"{_model} {_var} {ts_data['time'].cell(0).point.month:02}/{ts_data['time'].cell(0).point.year} "
                if iris_flag:
                    qplt.pcolormesh(ts_data.cube)
                    plt.gca().coastlines()
                    print(f"saving file: {filename}")
                    plt.savefig(filename, dpi=dpi)
                    plt.close()
                else:
                    # manual matlotlib plotting
                    fig = plt.figure(
                        figsize=FIGSIZE_DEFAULT,
                    )
                    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
                    ax.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree())

                    ax.set_global()
                    ax.set_xticks(
                        [-180, -120, -60, 0, 60, 120, 180], crs=ccrs.PlateCarree()
                    )
                    ax.set_yticks(
                        [-90, -60, -30, 0, 30, 60, 90], crs=ccrs.PlateCarree()
                    )
                    lon_formatter = LongitudeFormatter()
                    lat_formatter = LatitudeFormatter()
                    ax.xaxis.set_major_formatter(lon_formatter)
                    ax.yaxis.set_major_formatter(lat_formatter)
                    ax.coastlines(resolution="auto", color="k")
                    plot = ax.pcolormesh(
                        mdata[_model][_var][lon_name].points,
                        mdata[_model][_var][lat_name].points,
                        ts_data.data,
                        shading="nearest",
                        cmap=plotinfo["colmap"],
                        norm=norm,
                    )
                    ax.set_title(title)
                    fig.colorbar(plot, ax=ax, aspect=10, shrink=0.7)
                    fig.text(
                        0.86,
                        0.45,
                        unit_text,
                        fontsize="medium",
                        rotation=90,
                        ha="center",
                    )

                    print(f"saving file: {filename}")
                    plt.savefig(filename, dpi=dpi)
                    plt.close()


def get_aeroval_plot_info(var: str):
    """get aeroval's plot info from aeroval"""
    from pyaerocom.aeroval.glob_defaults import var_ranges_defaults

    try:
        return var_ranges_defaults[var]
    except NameError:
        pass
