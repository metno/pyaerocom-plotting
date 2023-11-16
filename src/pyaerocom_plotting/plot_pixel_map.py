"""plot pixel maps"""

from pyaerocom_plotting.readers import PyaModelData


def plot_pixel_map(
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
    from pyaerocom.aeroval.glob_defaults import var_ranges_defaults

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
