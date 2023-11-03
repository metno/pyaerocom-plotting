"""
reader classes of pyaerocom plotting

besides the current PyaModelData class there will be classes to read
- colocated data (netcdf files)
- aeroval json files
"""
from collections.abc import Iterable
from pathlib import Path

import pyaerocom.io as pio
from pyaerocom.exceptions import DataSearchError, VarNotAvailableError
from pyaerocom.griddeddata import GriddedData

from pyaerocom_plotting.const import DEFAULT_TS_TYPE


class PyaModelData:
    """data class for model data read by pyaerocom"""

    __version__ = "0.0.1"

    def __init__(
        self,
    ):
        self._models = []
        self._vars = []
        self._data = {}
        self._model_obj = {}

    def __getitem__(self, item):
        """x.__getitem__(y) <==> x[y]"""
        if len(item) == 1:
            model = item
            if model in self._data:
                return self._data[model]
            # else:
            #     raise NameError
        elif len(item) == 2:
            model, var = item
            if model in self._data:
                return self._data[model][var]
        else:
            pass

    def read(
        self,
        model: str,
        vars: Iterable[str],
        startyear: int,
        endyear: int,
        ts_type: str = DEFAULT_TS_TYPE,
        data_dir: str | Path = None,
    ):
        if model is not None:
            try:
                self._model_obj[model] = pio.ReadGridded(model)
            except DataSearchError:
                print(f"No model match found for model {model}.")
                return

            self._data[model] = {}
            self._models.append(model)
            for _var in vars:
                try:
                    dummy = self._model_obj[model].read_var(
                        var_name=_var,
                        start=startyear,
                        stop=endyear,
                        ts_type=ts_type,
                    )
                    # not entirely sure why this necessary
                    self._data[model][_var] = dummy
                    self._vars.append(_var)
                    # unique listy of variables
                    self._vars = list(set(self._vars))

                except VarNotAvailableError:
                    print(
                        "Error: variable {_var} not available in files and can also not be computed. Skipping..."
                    )

    @property
    def data(self):
        """data"""
        return self._data

    @data.setter
    def data(self, val: GriddedData):
        model = val.data_id
        var = val.var_name
        self._data[model] = {}
        self._data[model][var] = val

    def add_model_data(self, model: str, var_name: str, data: GriddedData):
        self._models.append(model)
        self._vars.append(var_name)
        if not model in self._data:
            self._data[model] = {}
        self._data[model][var_name] = data

    @property
    def models(self):
        return self._models

    @models.setter
    def models(self, val: str):
        self._models.append(val)

    @property
    def variables(self):
        return self._vars

    @variables.setter
    def variables(self, val: str):
        self._vars.append(val)


class PyaColocatedData:
    """class for pyaerocom colocated data objects stored in netcdf files"""

    pass


class AerovalJsonData:
    """class for aerovals' json files"""

    pass
