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

components = ['Monopile', 'Blade', 'Nacelle', 'Tower', 'Transition piece', 'Array cable', 'Export cable', 'WTIV']

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
        'Hellenic - Array cable',
        'Keppel AmFELS - WTIV',
        'Sembcorp - WTIV'
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
        color_throughput = [color_list['Announced'], color_list['Scenario'], 'k']
        name_throughput = ['Announced','Additional required','Annual demand']
        hatch_throughput = [color_list['Announced_hatch'], color_list['Scenario_hatch'], None]
        if c == 'WTIV':
            ylabel = 'Cumulative wind turbine installation vessels'
            _plot_average = None
        else:
            ylabel = 'Throughput (' + c + '/year)'
            _plot_average = [2023,2033]

        plot_supply_demand(years, zip(y_throughput, color_throughput, name_throughput, hatch_throughput), color_list, c, ylabel, y2=total_demand[c], fname=fname, plot_average=_plot_average)
        #
        # Plot difference between supply and demand
        # TODO: Figure cleanup, different bars colors
        fname_diff = 'results/' + c + 'diff'
        y_diff = total_announced_throughput[c] + total_scenario_throughput[c] - total_demand[c]
        ylabel_diff = 'Difference from annual demand (' + c + '/year)'
        plot_diff(years, y_diff, ylabel_diff, color_list[c], fname_diff)
        #
        # Plot investment
        fname = 'results/'+ c + '_investment'
        y_investment = [total_announced_investment[c], total_scenario_investment[c] ]
        color_investment = [color_list['Announced'], color_list['Scenario']]
        name_investment = ['Announced','Additional required']
        hatch_throughput = [color_list['Announced_hatch'], color_list['Scenario_hatch'], None]
        ylabel = 'Cumulative investment ($ million)'
        plot_supply_demand(years, zip(y_throughput, color_investment, name_investment, hatch_throughput), color_list, c, ylabel, fname=fname)
        #

plot_investment(years, total_announced_investment, total_scenario_investment, components, color_list, fname='results/total_investment')

plot_num_facilities(components, indiv_announced, indiv_scenario, color_list, fname='results/num_facilities')
