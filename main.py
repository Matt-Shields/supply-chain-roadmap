"""Evaluate future supply chain scenarios"""

__author__ = "Matt Shields"
__copyright__ = "Copyright 2022, National Renewable Energy Laboratory"
__maintainer__ = "Matt Shields"
__email__ = "matt.shields@nrel.gov"

import numpy as np
import pandas as pd

from helpers import read_future_scenarios, read_pipeline, define_factories, sum_property, compute_utilization, color_list
from plot_routines import plot_supply_demand, plot_diff, plot_investment, plot_num_facilities

# Input paramters
filepath_scenarios = "library/Generic_facilities.xlsx"
filepath_announced = "library/Announced_factories.xlsx"
filepath_pipeline = "library/total_demand.csv"

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
    total_announced_investment = {}
    total_scenario_investment = {}

    # Instantiate individual factories for all components in t
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
        total_announced_throughput[c] = sum_property(years, announced[c], 'annual_throughput')
        total_scenario_throughput[c] = sum_property(years, scenario[c], 'annual_throughput')
        total_announced_investment[c] = sum_property(years, announced[c], 'annual_investment')
        total_scenario_investment[c] = sum_property(years, scenario[c], 'annual_investment')

        # print(total_scenario_investment)

        # Compare with demand
        fname = 'results/'+ c + '_supply_demand'
        y_throughput = [total_announced_throughput[c], total_scenario_throughput[c] ]
        color_throughput = ['r', 'b', 'k']
        name_throughput = ['Announced','Scenario','Annual demand']
        ylabel = 'Throughput (' + c + '/year)'
        plot_supply_demand(years, zip(y_throughput, color_throughput, name_throughput), ylabel, y2=total_demand[c], fname=fname, plot_average=[2023,2033])
        #
        # Plot difference between supply and demand
        # TODO: Figure cleanup, different bars colors
        fname_diff = 'results/' + c + 'diff'
        y_diff = total_announced_throughput[c] + total_scenario_throughput[c] - total_demand[c]
        ylabel_diff = 'Difference from annual demand (' + c + '/year)'
        plot_diff(years, y_diff, ylabel_diff, fname_diff)
        #
        # Plot investment
        fname = 'results/'+ c + '_investment'
        y_investment = [total_announced_investment[c], total_scenario_investment[c] ]
        color_investment = ['r', 'b']
        name_investment = ['Announced','Scenario']
        ylabel = 'Cumulative investment ($ million)'
        plot_supply_demand(years, zip(y_throughput, color_investment, name_investment), ylabel, fname=fname)
        #

plot_investment(years, total_announced_investment, total_scenario_investment, components, color_list, fname='results/total_investment')

plot_num_facilities(components, indiv_announced, indiv_scenario, fname='results/num_facilities')
