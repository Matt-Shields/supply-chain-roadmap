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
moor_chain = 600/1000
moor_rope = 1000/1000
tier23_scaling = {'Flange': ['Tower', 1],
    'Generator': ['Nacelle', 1],
    'Gearbox': ['Nacelle', 0.33],  # 1/3 market share (Vestas only)
    'Mooring chain': ['Semisubmersible', 3*moor_chain],
    'Mooring rope': ['Semisubmersible', 3*moor_rope],
    'Anchor': ['Semisubmersible', 3],
    'Suction caisson': ['Semisubmersible', 3],
    'Bearing': ['Nacelle', 4],  # yaw, 3xpitch,
    'Hub': ['Nacelle', 1],
    'Bedplate': ['Nacelle', 1],
    'Steel plate': [['Monopile', 2500], ['Tower', 900], ['Semisubmersible', 3000]],
    'Casting': [['Nacelle', 2]]
}

job_breakdown = {'Design and engineering': .03,
    'Quality and safety': .05,
    'Factory-level management': .12,
    'Factory-level worker': .65,
    'Facilities maintenance': .15
}

# Copy vessel/port investment schedule from CORAL/investment_schedule.CSV
# TODO: make this dynamic
ports_inv = np.cumsum([770, 0, 0, 0, 0, 387, 0, 860, 200, 0, 1400, 200, 200, 0])
vessel_inv = np.cumsum([0, 500, 0, 0, 0, 500, 500, 1050, 1000, 0, 0, 0, 0, 0])


ymax_plots = {'Monopile': 350,
    'Jacket': 120,
    'GBF': 120,
    'Semisubmersible': 300,
    'Blade': 1600,
    'Nacelle': 800,
    'Tower': 600,
    'Transition piece': 350 ,
    'Array cable': 2000,
    'Export cable': 2000,
    'WTIV': 6,
    'Steel plate': 1200000,
    'Casting': 1000,
    'Flange': 5000,
    'Mooring chain': 2500,
    'Mooring rope': 2500,
    'Anchor': 3000

}

color_list = {
    # Color scheme for components: https://paletton.com/#uid=70m0P1kuovZh9G7nlz8xWp1E7j0kHlz6lxHTsYGtJjpEN5j5kLGs1q7F9IcGrO+m8T6fxkmuEKatTJhdM3rQzhvZqJ
    'Monopile': '#FF670D',
    'Jacket': '#C74A00',
    'GBF': '#973800',
    'Semisubmersible': '#FF8518',
    'Mooring chain': '#0F378E',
    'Mooring rope': '#2753B3',
    'Mooring Chain': '#0F378E',
    'Mooring Rope': '#2753B3',
    'Mooring System': '#2753B3',
    'Anchor': 'k',
    'Blade': '#698FE8',
    'Nacelle': '#7679DB',
    'Tower': '#ABADED',
    'Transition piece': '#FFA976' ,
    'Array cable': '#008564',
    'Export cable': '#00AE83',
    'WTIV': '#FF4545',
    'Ports': '#970000',
    'Steel plate': '#FFBE00',
    'Steel plates':  '#FFBE00',
    'Flange': '#B08300',
    'Casting': '#FFCA2F',
    # Color schem for announced/scneario:
    'Announced': '#5D63AA',
    'Scenario': '#2F8B6F',
    'Deficit': '#801515',
    'Surplus': 'k',
    # Color scheme for jobs: Hue 278, RBG 4D249B Dist 159
    'Design and Engineering': '#29086B',
    'Quality and Safety': '#8D76B9',
    'Factory-Level Management': '#E3B521',
    'Factory-Level Worker': '#FFE699',
    'Facilities Maintenance': '#9C7700',
    # Other Jobs color
    'Component (Direct jobs)': '#FF8500',
    'Direct jobs': '#FF8500',
    'Suppliers (Indirect jobs, 100% domestic content)': '#055B7C',
    'Indirect jobs': '#055B7C',
    'Similar industries capacity': '#70AD47',
    'Proximity to conceptual facilities': '#FFC000',
    'Offshore specific capability ': '#5B9BD5',
    #
    'Announced_hatch': '\\\\',
    'Scenario_hatch': '...',
    # Color scheme for port and vessel scenarios
    'Existing': '#C64D13',
    'Expanded': '#0D855A',

}

label_map = {'Monopile': 'Monopile',
            'Jacket': 'Jacket',
            'GBF': 'Gravity-based \nfoundation',
            'Semisubmersible': 'Semisub-\nmersible',
            'Blade': 'Blade',
            'Nacelle': 'Nacelle',
            'Tower': 'Tower',
            'Transition piece': 'Transition \npiece',
            'Array cable': 'Array \ncable',
            'Export cable': 'Export \ncable',
            'WTIV': 'WTIV',
            'Steel plate': 'Steel \nplate',
            'Casting': 'Casting',
            'Flange': 'Flange',
            'Mooring chain': 'Mooring \nchain',
            'Mooring rope': 'Mooring \nrope',
            'Anchor': 'Anchor'
}

announced_name_map= {'EEW - Monopile': 'Port of Paulsboro, NJ',
    'USWind - Monopile': 'Tradepoint Atlantic, MD',
    'SGRE - Blade': 'Portsmouth Marine Terminal, VA',
    'ASOW - Nacelle': 'New Jersey Wind Port, NJ',
    'GE - Nacelle': 'New Jersey Wind Port, NJ',
    'MarWel - Tower': 'Port of Albany, NY',
    'Smulders - Transition piece': 'Port of Albany, NY',
    'Nexans - Export cable': 'Goose Creek, SC',
    'Prysmian - Export cable': 'Brayton Point, MA',
    'Hellenic - Array cable': 'Tradepoint Atlantic, MD',
    'Keppel AmFELS - WTIV': 'Brownsville, TX',
    'Sembcorp - WTIV': 'International',
    'Nucor - Steel plate': 'Brandenburg, KY'
}

# port_vessel_scenario = {
#     'Existing': {
#
#     },
#     'Expanded':
#
# }

def read_future_scenarios(file, sheet, header):
    """Read in factory deployment for given scenario"""
    df = pd.read_excel(file, sheet_name=sheet, header=header, keep_default_na=False)
    dict = {}
    for index, row in df.iterrows():
        dict[row['Factory']] = {'Operational date': row['Operational date'],
                                'State': row['State'],
                                'Name': row['Name'],
                                'Type': row['Type'],
                                'Announcement date': row['Announcement date'],
                                'Port cost': row['Port upgrade cost'],
                                'Component': row['Component'],
                                'Production capacity': row['Production capacity'],
                                'Facility cost': row['Facility cost'],
                                'Facility construction time': row['Facility construction (yrs)']
                                }
    return dict

def read_pipeline(file, cod_shift):
    """Read in summary of deploymnet pipeline from Phase 1 report"""
    df = pd.read_csv(file)

    cod = df['COD']
    manf_date = cod - cod_shift

    dict = {}
    for col, vals in df.items():
        dict[col] = vals
    for t, scale in tier23_scaling.items():
        try:
            dict[t] = dict[scale[0]] * scale[1]
        except TypeError:
            # List of multiple components
            _amt = 0
            for s in scale:
                _amt += dict[s[0]] * s[1]
            dict[t] = _amt
    return dict, manf_date


def define_factories(facility_list, component, years, name_map):
    """Instantiate Factory objects for each facility in pipeline"""
    _announced_factories = []
    _scenario_factories = []
    for fi in facility_list:
        if component in facility_list[fi]['Component']:
            f = Factory(facility_list[fi], component, years, name_map)
            if f.facility_type == 'Announced':
                _announced_factories.append(f)
            elif f.facility_type == 'Scenario':
                _scenario_factories.append(f)
            else:
                print('Unknown facility type in ports_scenario spreadsheet')
    return _announced_factories, _scenario_factories

def sum_property(years, factory_list, property):
    """Sum factory properties for Factory objects in a list"""
    _total = [0] * len(years)
    for f in factory_list:
        _total = np.array([sum(x) for x in zip(_total, getattr(f, property))])
    return _total


def compute_utilization(supply, demand):
    _diff = demand - supply
    _perc_diff = 100 * (demand - supply).divide(demand)
