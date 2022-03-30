"""Evaluate future supply chain scenarios"""

__author__ = "Matt Shields"
__copyright__ = "Copyright 2022, National Renewable Energy Laboratory"
__maintainer__ = "Matt Shields"
__email__ = "matt.shields@nrel.gov"

import numpy as np
import pandas as pd

from helpers import read_future_scenarios, read_pipeline, define_factories, sum_property, compute_utilization
from plot_routines import plot_supply_demand, plot_diff

# Input paramters
filepath_scenarios = "library/Generic_facilities.xlsx"
filepath_announced = "library/Announced_factories.xlsx"
filepath_pipeline = "library/total_demand.csv"
# years = np.arange(2020,2034)
components = ['Monopile', 'Blade', 'Nacelle', 'Tower', 'Transition piece', 'Array cable', 'Export cable']

if __name__ == "__main__":
    # Demand
    total_demand, years= read_pipeline(filepath_pipeline)

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
        'Hellenic - Array cable'
    ]
    # Scenarios
    indiv_scenario = read_future_scenarios(filepath_scenarios, 'Avg Demand Scenario')


    announced = {}
    scenario = {}
    aggr_announced = {}
    aggr_scenario = {}

    total_announced_throughput = {}
    total_scenario_throughput = {}

    # Instantiate individual factories for all components in teh scenario and compute the total characteristics of the supply chain
    for c in components:
        # Known facilities
        announced[c] = define_factories(filepath_announced,
                                        indiv_announced,
                                        c,
                                        years,
                                        generic=False)
        # Scenario facilities
        scenario[c] = define_factories(filepath_scenarios,
                                        indiv_scenario,
                                        c,
                                        years,
                                        generic=True)

        # Sum up propeties of each facility
        # _total_throughput = [0] * len(years)
        # for f in announced[c]+scenario[c]:
        #     # print(getattr(f, 'annual_throughput'))
        #     _total_throughput =[sum(x) for x in zip(_total_throughput, f.annual_throughput)]
        total_announced_throughput[c] = sum_property(years, announced[c], 'annual_throughput')
        total_scenario_throughput[c] = sum_property(years, scenario[c], 'annual_throughput')

        # Compare with demand
        fname = 'results/'+ c + '_supply_demand'
        y_throughput = [total_announced_throughput[c], total_scenario_throughput[c] ]
        color_throughput = ['r', 'b', 'k']
        name_throughput = ['Announced','Scenario','Annual demand']
        ylabel = 'Throughput (' + c + '/year)'
        plot_supply_demand(years, zip(y_throughput, color_throughput, name_throughput), total_demand[c], ylabel, fname, plot_average=[2023,2033])
        #
        fname_diff = 'results/' + c + 'diff'
        y_diff = total_announced_throughput[c] + total_scenario_throughput[c] - total_demand[c]
        ylabel_diff = 'Difference from annual demand (' + c + '/year)'
        plot_diff(years, y_diff, ylabel_diff, fname_diff)
