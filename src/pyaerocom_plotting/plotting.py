from pyaerocom.griddeddata import GriddedData


class Plotting:
    """plotting class with methods for each supported plot"""

    __version__ = "0.0.1"

    def __init__(self):
        self.models = []
        self.vars = []
        self.plotdata = {}

    def add_model_data(self, model: str, var_name: str, data: GriddedData):
        self.models.append(model)
        self.vars.append(var_name)
        if not model in self.plotdata:
            self.plotdata[model] = {}
        self.plotdata[model][var_name] = data

    # @property
    # def models(self):
    #     return self.models
    #
    # @models.setter
    # def models(self, val: str):
    #     self.models[val] = {}

    def plot_pixel_map(self, plotdata):
        """method to plot pixelmaps"""

    def plot_weighted_means(self, plotdata):
        """method to plot weighted means"""
