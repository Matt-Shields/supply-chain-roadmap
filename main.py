"""Evaluate future supply chain scenarios"""
__author__ = "Matt Shields"
__copyright__ = "Copyright 2022, National Renewable Energy Laboratory"
__maintainer__ = "Matt Shields"
__email__ = "matt.shields@nrel.gov"

import numpy as np

from analysis import scenario_analysis as sa
from plot_routines import lineplot_comp

scenarios = {
'Conservative': {
'filepath_ports': "fabrication_ports/ports_scenario_max.xlsx",
'legend': 'Conservative supply chain growth',
'linetype': '.-'
},
'Accelerated': {
'filepath_ports': "fabrication_ports/ports_scenario_min.xlsx",
'legend': 'Accelerated supply chain growth',
'linetype': '--'
},
# 'Aggressive': {
# 'filepath_ports': "fabrication_ports/ports_scenario_aggressive.xlsx",
# 'legend': 'Aggressive supply chain growth',
# 'linetype': ':'
# }
}

# Common paramters
filepath_pipeline = "library/total_demand.csv"
filepath_deploy = "library/total_deployment.csv"

components = ['Blade', 'Nacelle', 'Tower','Monopile', 'Jacket', 'GBF', 'Transition piece', 'Array cable', 'Export cable', 'Floating platform', 'Mooring chain', 'Mooring rope', 'Steel plate', 'Flange', 'Casting']

# Known facilities
indiv_announced = ['EEW - Monopile',
    'USWind - Monopile',
    'SGRE - Blade',
    'ASOW - Nacelle',
    'GE - Nacelle',
    'MarWel - Tower',
    'Smulders - Transition piece',
    'Nexans - Export cable',
    'Prysmian - Export cable',
    'Hellenic - Array cable',
    'Keppel AmFELS - WTIV',
    'Sembcorp - WTIV',
    'Nucor - Steel plate'
]

if __name__ == "__main__":
    domestic_sc_percent_scenarios = []
    deploy_scenarios = []
    legend = []
    linetype = []
    ind = 1
    for k, v in scenarios.items():
        # Individual scenario results and plots
        mnf_years, cod_years, total_demand, domestic_sc_percent, total_deploy, annual_deploy = sa(
                filepath_pipeline,
                v['filepath_ports'],
                filepath_deploy,
                components,
                indiv_announced,
                k)

        # Define parameters for inter-scenario compariosn
        domestic_cod = 2025
        scaled_deploy = [(perc/100)*deploy if cod > domestic_cod else deploy for perc, deploy, cod in zip(domestic_sc_percent, annual_deploy, cod_years)]

        if ind==1:
            deploy_scenarios += [np.cumsum(annual_deploy) / 1000,
                                 np.cumsum(scaled_deploy) / 1000]
            legend += ['Deployment with no supply chain constraints', v['legend']]
            linetype += ['-', v['linetype']]
        else:
            deploy_scenarios += [np.cumsum(scaled_deploy) / 1000]
            legend += [v['legend']]
            linetype += [v['linetype']]

        domestic_sc_percent_scenarios += [domestic_sc_percent]

        ind += 1

    # Inter-scenario results and plots
    lineplot_comp(mnf_years, domestic_sc_percent_scenarios, legend[1:], linetype[1:], xlabel='Manufacturing date', ylabel='Manufacturing capacity (% of demand)', xlim = [2020, 2034], ylim = [0, 110], fname='results/domestic_percent')
    lineplot_comp(cod_years, deploy_scenarios, legend, linetype, xlabel='Commercial operation date', ylabel='Installed capacity from \ndomestic supply chain, GW', xlim = [2025, 2035], ylim = [0, 70], fname='results/deployment_impact', title='Offshore wind projects will need to import components \nwhile the domestic supply chain develops. Global supply \nbottlenecks could limit deployment if U.S. projects can \nnot source a sufficient number of these components.')
