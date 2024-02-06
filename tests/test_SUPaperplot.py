import unittest
import os

from pyaerocom_plotting.plotting import Plotting
from pyaerocom_plotting.readers import AerovalJsonData

SU_PAPER_PLOTNAME = "./overallts_od550aer_data_mean_Aeronet_Column.png"


class Testplots(unittest.TestCase):
    file = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "testdata",
        "ALL-Aeronet-od550aer-Column.json",
    )

    def json_read(self, options: dict) -> AerovalJsonData:
        """read model data using pyaerocom"""
        json_data = AerovalJsonData()
        json_data.read(options["file"])
        return json_data

    def test_su_paper_plot(self):
        options = {}
        options["plottype"] = "overall_ts_SU"
        options["outdir"] = "."
        options["file"] = self.file
        # read data
        json_data = self.json_read(options=options)
        plt_obj = Plotting(plotdir=options["outdir"])
        plt_obj.plot_aeroval_overall_time_series_SU_Paper(json_data)
        self.assertEqual(os.path.exists(SU_PAPER_PLOTNAME), True)
