"""Defines a factory object for a US supply chain"""

__author__ = "Matt Shields"
__copyright__ = "Copyright 2022, National Renewable Energy Laboratory"
__maintainer__ = "Matt Shields"
__email__ = "matt.shields@nrel.gov"

import numpy as np
import pandas as pd

# Standard inputs
port_time = 3
port_overlap_time = 0.25
learning_curve = {0: 0.5, 1: 0.75}

class Factory():
    """ Define factory class """
    def __init__(self, facility_specs, component, years, name_map=None):
        self.assign_attributes(facility_specs, component, years, name_map)
        self.define_schedule(years)
        self.outputs = {}

    def assign_attributes(self, facility_specs, component, years, name_map):
        """Assign values to Factory object from input CSV"""

        self.COD = facility_specs['Operational date']
        self.announced_date = facility_specs['Announcement date']
        self.throughput = facility_specs['Production capacity']
        self.investment = facility_specs['Facility cost']
        self.fab_port_investment = facility_specs['Port cost']
        self.lead_time = facility_specs['Facility construction time']
        self.facility_type = facility_specs['Type']
        self.name = facility_specs['Name']
        self.component = component
        self.construction_time = self.COD - self.announced_date

    def define_schedule(self, years):
        """Define throughput per year"""

        _ind = np.where(years == self.COD)[0][0]

        self.annual_throughput = np.zeros(len(years))
        self.annual_throughput[_ind:] = self.throughput

        # Correct for learning curve in early years
        for yr,perc in learning_curve.items():
            _yr_ind = _ind + yr
            try:
                self.annual_throughput[_yr_ind] = perc * self.throughput
            except IndexError:
                # TODO: Fix
                print('index error - learning rate applied at end of array in factory.py')
        # Cumulative values
        self.annual_investment = np.zeros(len(years))
        self.annual_investment[_ind:] = self.investment
        self.annual_fab_port_investment = np.zeros(len(years))
        self.annual_fab_port_investment[_ind:] = self.fab_port_investment
        # self.annual_jobs = np.zeros(len(years))
        # self.annual_jobs[_ind[0]:] = self.total_jobs
