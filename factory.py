"""Defines a factory object for a US supply chain"""

__author__ = "Matt Shields"
__copyright__ = "Copyright 2022, National Renewable Energy Laboratory"
__maintainer__ = "Matt Shields"
__email__ = "matt.shields@nrel.gov"

import numpy as np
import pandas as pd

class Factory():
    """ Define factory class """
    def __init__(self, filepath, component, years, generic, facility=None):
        self.read_attributes(filepath, component, generic, facility)
        self.define_schedule(years)
        self.outputs = {}

    def read_attributes(self, filepath, component, generic, facility):
        """Read in CSV and assign values to Factory object"""
        df = pd.read_excel(filepath, sheet_name=component, index_col=0)

        self.COD = self.define_COD(df, generic, facility)

        self.throughput = df.loc['Annual throughput', 'Value']
        self.investment = df.loc['Investment cost', 'Value']
        self.lead_time = df.loc['Lead time', 'Value']
        self.total_jobs = df.loc['Total Direct Jobs', 'Value']
        # TODO - break down into individual jobs

    def define_COD(self, df, generic, facility):
        """Either read COD for facility or calculate from annoucmentn"""
        if generic==False:
            COD = df.loc['Operational date', 'Value']
        else:
            COD = facility[0]
        return COD

    def define_schedule(self, years):
        """Define throughput per year"""
        _ind = np.where(years == self.COD)[0]
        self.annual_throughput = np.zeros(len(years))
        self.annual_throughput[_ind[0]:] = self.throughput
        self.annual_investment = np.zeros(len(years))
        self.annual_investment[_ind[0]:] = self.investment
        self.annual_jobs = np.zeros(len(years))
        self.annual_jobs[_ind[0]:] = self.total_jobs
