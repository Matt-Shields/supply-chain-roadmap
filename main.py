"""Evaluate future supply chain scenarios"""
__author__ = "Matt Shields"
__copyright__ = "Copyright 2022, National Renewable Energy Laboratory"
__maintainer__ = "Matt Shields"
__email__ = "matt.shields@nrel.gov"

from analysis import scenario_analysis as sa
from plot_routines import lineplot_comp

scenarios = {
'Early': {
'filepath_ports': "fabrication_ports/ports_scenario_min.xlsx",
'legend': 'Early investment',
'linetype': '--'
},
'Late': {
'filepath_ports': "fabrication_ports/ports_scenario_max.xlsx",
'legend': 'Delayed investment',
'linetype': '.-'
}
}

# Common paramters
filepath_scenarios = "library/Generic_facilities.xlsx"
filepath_announced = "library/Announced_factories.xlsx"
filepath_pipeline = "library/total_demand.csv"
filepath_deploy = "library/total_deployment.csv"

components = ['Blade', 'Nacelle', 'Tower','Monopile', 'Jacket', 'GBF', 'Transition piece', 'Array cable', 'Export cable', 'Semisubmersible', 'Mooring chain', 'Mooring rope', 'Steel plate', 'Flange', 'Casting']

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
    domestic_sc_percent = []
    deploy_scenarios = []
    legend = []
    linetype = []
    ind = 1
    for k, v in scenarios.items():
        cod_years, total_demand, domestic_sc_percent, total_deploy = sa(filepath_scenarios,
                filepath_announced,
                filepath_pipeline,
                v['filepath_ports'],
                filepath_deploy,
                components,
                indiv_announced,
                k)

        scaled_deploy = [(i/100)*j for i,j in zip(domestic_sc_percent, total_deploy)]

        if ind==1:
            deploy_scenarios += [total_deploy, scaled_deploy]
            legend += ['No constraints', v['legend']]
            linetype += ['-', v['linetype']]
        else:
            deploy_scenarios += [scaled_deploy]
            legend += [v['legend']]
            linetype += [v['linetype']]
        ind += 1

    print(cod_years, deploy_scenarios)
    lineplot_comp(cod_years, deploy_scenarios, legend, linetype, fname='results/deployment_impact')
