"""Helper functions"""

__author__ = "Matt Shields"
__copyright__ = "Copyright 2022, National Renewable Energy Laboratory"
__maintainer__ = "Matt Shields"
__email__ = "matt.shields@nrel.gov"

import numpy as np
import pandas as pd

from factory import Factory

# Define scaling from Tier 1 to Tier 2 and 3.  Format:
#  {"new component": ["original component', scaling factor"]}
moor_chain = 100
moor_rope = 800
tier23_scaling = {'Flange': ['Tower', 1],
    'Generator': ['Nacelle', 1],
    'Gearbox': ['Nacelle', 0.33],  # 1/3 market share (Vestas only)
    'Mooring chain': ['Semisubmersibles', 3*moor_chain],
    'Mooring rope': ['Semisubmersibles', 3*moor_rope],
    'Anchor': ['Semisubmersibles', 3],
    'Suction caisson': ['Semisubmersibles', 3],
    'Bearing': ['Nacelle', 4],  # yaw, 3xpitch,
    'Hub': ['Nacelle', 1],
    'Bedplate': ['Nacelle', 1],
    'Steel plate': ['Monopile', 45]
}

color_list = {'Monopile': '#282D30',
    'Blade': '#00FFFF',
    'Nacelle': '#7FFFD4',
    'Tower': '#008000',
    'Transition piece': '#D2691E' ,
    'Array cable': '#FFA500',
    'Export cable': '#FF4500',
}

def read_future_scenarios(file, sheet):
    """Read in factory deployment for given scenario"""
    df = pd.read_excel(file, sheet_name=sheet)
    dict = {}
    for index, row in df.iterrows():
        dict[row['Factory']] = [row['COD'], row['Location']]
    return dict

def read_pipeline(file):
    """Read in summary of deploymnet pipeline from Phase 1 report"""
    df = pd.read_csv(file)

    cod = df['COD']
    manf_date = cod - 2  # TODO - input?

    dict = {}
    for col, vals in df.items():
        dict[col] = vals
    for t, scale in tier23_scaling.items():
        dict[t] = dict[scale[0]] * scale[1]
    return dict, manf_date


def define_factories(file, facility_list, component, years, generic):
    """Instantiate Factory objects for each facility in pipeline"""
    _factories = []
    for fi in facility_list:
        if component in fi:
            if generic == False:
                f = Factory(file, fi, years, generic)
            else:
                f = Factory(file, component, years, generic, facility_list[fi])
            _factories.append(f)
    return _factories

def sum_property(years, factory_list, property):
    """Sum factory properties for Factory objects in a list"""
    _total = [0] * len(years)
    for f in factory_list:
        # print(_total, getattr(f,property))
        _total = np.array([sum(x) for x in zip(_total, getattr(f, property))])
    return _total


def compute_utilization(supply, demand):
    _diff = demand - supply
    _perc_diff = 100 * (demand - supply).divide(demand)
