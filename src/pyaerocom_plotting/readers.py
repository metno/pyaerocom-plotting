"""
reader classes of pyaerocom plotting

besides the current PyaModelData class there will be classes to read
- colocated data (netcdf files)
- aeroval json files
"""
from collections.abc import Iterable
from pathlib import Path

import pyaerocom.io as pio
import simplejson as json
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

    __version__ = "0.0.1"

    def __init__(
        self,
    ):
        self._models = []
        self._vars = []
        self._modelvars = []
        self._regions = []
        self._data = {}
        self._files = []
        self._obsnetworks = []
        self._code = []  # e.g. "Column"

    def __getitem__(self, item):
        """x.__getitem__(y) <==> x[y]"""
        if len(item) == 1:
            file = item
            if file in self._data:
                return self._data[file]
            else:
                raise NameError
        else:
            pass

    def read(
        self,
        file: [str, Path],
    ):
        if file is not None:
            self._data[file] = None
            try:
                with open(file) as fh:
                    self._data[file] = json.load(fh)
            except FileNotFoundError:
                print(f"file not found {file}.")
                return

            # probably fill out some helping vars
            self.files.append(file)
            for _var in self._data[file]:
                self.vars.append(_var)
                for _obsnetwork in self._data[file][_var]:
                    self.obsnetworks.append(_obsnetwork)
                    for _code in self._data[file][_var][_obsnetwork]:
                        self.code.append(_code)
                        for _model in self._data[file][_var][_obsnetwork][_code]:
                            self.models.append(_model)
                            for _modelvar in self._data[file][_var][_obsnetwork][_code][
                                _model
                            ]:
                                self.modelvars.append(_modelvar)
                                for _region in self._data[file][_var][_obsnetwork][
                                    _code
                                ][_model][_modelvar]:
                                    self.regions.append(_region)

    @property
    def data(self):
        """data"""
        return self._data

    @data.setter
    def data(self, val: dict):
        model = val.data_id
        var = val.var_name
        self._data[model] = {}
        self._data[model][var] = val

    def add_json_data(self, file: str, data: dict):
        self._data[file] = data

    @property
    def models(self):
        return self._models

    @models.setter
    def models(self, val: str):
        self._models.append(val)

    @property
    def files(self):
        return self._files

    @files.setter
    def files(self, val: str):
        self._files.append(val)

    @property
    def vars(self):
        return self._vars

    @vars.setter
    def vars(self, val: str):
        self._vars.append(val)

    @property
    def modelvars(self):
        return self._modelvars

    @modelvars.setter
    def modelvars(self, val: str):
        self._modelvars.append(val)

    @property
    def regions(self):
        return self._regions

    @regions.setter
    def regions(self, val: str):
        self._regions.append(val)

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, val: str):
        self._code.append(val)

    @property
    def obsnetworks(self):
        return self._obsnetworks

    @obsnetworks.setter
    def obsnetworks(self, val: str):
        self._obsnetworks.append(val)
