"""Evaluate future supply chain scenarios"""

__author__ = "Matt Shields"
__copyright__ = "Copyright 2022, National Renewable Energy Laboratory"
__maintainer__ = "Matt Shields"
__email__ = "matt.shields@nrel.gov"

import numpy as np
import pandas as pd

from helpers import read_future_scenarios, read_pipeline, define_factories, sum_property, compute_utilization, color_list, job_breakdown, ymax_plots, label_map, announced_name_map
from plot_routines import plot_supply_demand, plot_diff, plot_total_diff,  plot_cumulative, plot_num_facilities, plot_gantt, lineplot_comp

# Input paramters
filepath_scenarios = "library/Generic_facilities.xlsx"
filepath_announced = "library/Announced_factories.xlsx"
filepath_pipeline = "library/total_demand.csv"
filepath_ports = "fabrication_ports/ports_scenario_max.xlsx"
filepath_deploy = "library/total_deployment.csv"

components = ['Blade', 'Nacelle', 'Tower','Monopile', 'Jacket', 'GBF', 'Transition piece', 'Array cable', 'Export cable', 'Semisubmersible', 'Mooring chain', 'Mooring rope', 'Steel plate', 'Flange', 'Casting']

if __name__ == "__main__":
    # Demand
    total_demand, years= read_pipeline(filepath_pipeline, cod_shift=2)
    _deploy = pd.read_csv(filepath_deploy)
    cod_years = _deploy['COD']
    total_deploy = _deploy['Cumulative deployment, MW']

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
    # Scenarios
    indiv_scenario = read_future_scenarios(filepath_ports, 'Avg Demand Scenario', header=9)


    announced = {}
    scenario = {}
    aggr_announced = {}
    aggr_scenario = {}
    announced_list = []
    scenario_list = []
    annual_diff_pos = {}
    annual_diff = {}
    average = {}

    total_announced_throughput = {}
    total_scenario_throughput = {}
    total_announced_investment = {}
    total_scenario_investment = {}
    total_announced_jobs = {}
    total_scenario_jobs = {}
    # Instantiate individual factories for all components in t
    for c in components:
        # Known facilities
        announced[c] = define_factories(filepath_announced,
                                        indiv_announced,
                                        c,
                                        years,
                                        generic=False, name_map = announced_name_map)
        # Scenario facilities
        scenario[c] = define_factories(filepath_scenarios,
                                        indiv_scenario,
                                        c,
                                        years,
                                        generic=True)

        announced_list += announced[c]
        scenario_list += scenario[c]
        # Construction Gantt charts
        fname_gantt = 'results/'+ c + '_gantt'
        plot_gantt(components, announced[c], scenario[c], color_list, single_component=True, fname=fname_gantt)

        # Sum up propeties of each facility
        total_announced_throughput[c] = sum_property(years, announced[c], 'annual_throughput')
        total_scenario_throughput[c] = sum_property(years, scenario[c], 'annual_throughput')
        total_announced_investment[c] = sum_property(years, announced[c], 'annual_investment')
        total_scenario_investment[c] = sum_property(years, scenario[c], 'annual_investment')
        total_announced_jobs[c] = sum_property(years, announced[c], 'annual_jobs')
        total_scenario_jobs[c] = sum_property(years, scenario[c], 'annual_jobs')

        # Compare with demand
        fname = 'results/'+ c + '_supply_demand'
        y_throughput = [total_announced_throughput[c], total_scenario_throughput[c] ]
        color_throughput = [color_list['Announced'], color_list['Scenario'], 'k']
        name_throughput = ['Announced','Additional required','Annual demand']
        hatch_throughput = [color_list['Announced_hatch'], color_list['Scenario_hatch'], None]

        if c == 'WTIV':
            ylabel = 'Cumulative wind turbine installation vessels'
            _plot_average = None
        elif c == 'Semisubmersible' or c == 'Mooring chain' or c == 'Mooring rope' or c == "Anchors":
            ylabel = 'Throughput (' + c + '/year)'
            _plot_average = [2028,2033]
        else:
            ylabel = 'Throughput (' + c + '/year)'
            _plot_average = [2026,2033]

        average[c] = plot_supply_demand(years, zip(y_throughput, color_throughput, name_throughput, hatch_throughput), color_list, c, ylabel, y2=total_demand[c], ylim=ymax_plots[c], fname=fname, plot_average=_plot_average)
        #
        # Plot difference between supply and demand
        fname_diff = 'results/' + c + 'diff'
        try:
            y_diff = total_announced_throughput[c] + total_scenario_throughput[c] - total_demand[c]
            y_prod = total_announced_throughput[c] + total_scenario_throughput[c]
        except ValueError:
            # No announced facilities
            y_diff = total_scenario_throughput[c] - total_demand[c]
            y_prod = total_scenario_throughput[c]

        ylabel_diff = 'Difference from annual demand (' + c + '/year)'
        annual_diff_pos[c] = plot_diff(years, y_diff, ylabel_diff, color_list, fname_diff)
        annual_diff[c] = y_prod / average[c]
        # annual_diff[c] = y_prod / total_demand[c]
        # Plot investment
        fname = 'results/'+ c + '_investment'
        y_investment = [total_announced_investment[c], total_scenario_investment[c] ]
        color_investment = [color_list['Announced'], color_list['Scenario']]
        name_investment = ['Announced','Additional required']
        hatch_investment = [color_list['Announced_hatch'], color_list['Scenario_hatch'], None]
        ylabel = 'Cumulative investment ($ million)'
        plot_supply_demand(years, zip(y_throughput, color_investment, name_investment, hatch_investment), color_list, c, ylabel, fname=fname)
        #
        # Plot jobs
        fname = 'results/'+ c + '_jobs'
        y_jobs = [total_announced_jobs[c], total_scenario_jobs[c] ]
        color_jobs = [color_list['Announced'], color_list['Scenario']]
        name_jobs = ['Announced','Additional required']
        hatch_jobs = [color_list['Announced_hatch'], color_list['Scenario_hatch'], None]
        ylabel = 'Cumulative jobs, FTEs'
        plot_supply_demand(years, zip(y_jobs, color_jobs, name_jobs, hatch_jobs), color_list, c, ylabel, fname=fname)

plot_cumulative(years, total_announced_investment, total_scenario_investment, components, color_list, ylabel = 'Investment, $ million', fname='results/total_investment')

plot_cumulative(years, total_announced_jobs, total_scenario_jobs, components, color_list, ylabel='Direct manufacturing jobs, FTEs', fname='results/total_jobs', alternate_breakdown=job_breakdown)

plot_num_facilities(components, indiv_announced, indiv_scenario, color_list, fname='results/num_facilities')

# Construction Gantt charts
fname_gantt2 = 'results/overall_gantt'
plot_gantt(components, announced_list, scenario_list, color_list, fname=fname_gantt2)
# plot_job_breakdown()

# Overall difference in component_list
fname_total_diff = 'results/total_diff'
domestic_sc_percent = plot_total_diff(years, annual_diff, total_demand, fname_total_diff)

# Plot percentage of deployment from domestic supply chain
fname_deploy_perc = 'results/deployment_impact'
scaled_deploy = [(i/100)*j for i,j in zip(domestic_sc_percent, total_deploy)]
deploy_scenarios = [total_deploy, scaled_deploy]
ylabels = ['Baseline deployment', 'Supply chain constraints']
linetype = ['-', '--']

lineplot_comp(cod_years, deploy_scenarios, ylabels, linetype,  fname=fname_deploy_perc)
