from pyaerocom.griddeddata import GriddedData


class Plotting:
    """plotting class with methods for each supported plot"""

    __version__ = "0.0.1"

    def __init__(self):
        self._models = []
        self._vars = []
        self._plotdata = {}

    @property
    def plotdata(self):
        """plotdata"""
        return self._plotdata

    @plotdata.setter
    def plotdata(self, val: GriddedData):
        model = val.data_id
        var = val.var_name
        self._plotdata[model] = {}
        self._plotdata[model][var] = val

    def add_model_data(self, model: str, var_name: str, data: GriddedData):
        self._models.append(model)
        self._vars.append(var_name)
        if not model in self.plotdata:
            self._plotdata[model] = {}
        self._plotdata[model][var_name] = data

    @property
    def models(self):
        return self._models

    @models.setter
    def models(self, val: str):
        self._models.append(val)

    @property
    def variables(self):
        return self._vars

    @models.setter
    def variables(self, val: str):
        self._vars.append(val)

    def plot_pixel_map(
        self,
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

        for _model in self.models:
            for _var in self.variables:
                print(self.plotdata[_model][_var].cube.var_name)
                self.plotdata[_model][_var].cube.coord("latitude").guess_bounds()
                self.plotdata[_model][_var].cube.coord("longitude").guess_bounds()
                weights = iris.analysis.cartography.area_weights(
                    self.plotdata[_model][_var].cube
                )
                self.plotdata[_model][_var].cube.coord("longitude").guess_bounds()

    def plot_weighted_means(self, plotdata):
        """method to plot weighted means"""
