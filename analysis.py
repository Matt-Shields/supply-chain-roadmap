""" Run through all analysis and plotting routines for each scenario"""
import numpy as np
import pandas as pd

from helpers import read_future_scenarios, read_pipeline, define_factories, sum_property, compute_utilization, color_list, job_breakdown, ymax_plots, label_map, announced_name_map, ports_inv, vessel_inv
from plot_routines import plot_supply_demand, plot_diff, plot_total_diff,  plot_cumulative, plot_num_facilities, plot_gantt, lineplot_comp

def scenario_analysis(filepath_pipeline, filepath_ports, filepath_deploy, components, indiv_announced, plot_dir):
    # Demand
    total_demand, years= read_pipeline(filepath_pipeline, cod_shift=2)
    _deploy = pd.read_csv(filepath_deploy)
    cod_years = _deploy['COD']
    annual_deploy = _deploy['Annual deployment, MW']
    total_deploy = _deploy['Cumulative deployment, MW']

    # Scenarios
    all_factories = read_future_scenarios(filepath_ports, 'Avg Demand Scenario', header=9)

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
    total_announced_fab_port_investment = {}
    total_scenario_fab_port_investment = {}
    # Instantiate individual factories for all components in t
    for c in components:
        # Known facilities
        announced[c], scenario[c] = define_factories(all_factories, c, years, announced_name_map
        )

        announced_list += announced[c]
        scenario_list += scenario[c]

        # Construction Gantt charts
        fname_gantt = 'results/'+ plot_dir + '/' + c + '_gantt'
        plot_gantt(components, announced[c], scenario[c], color_list, single_component=True, fname=fname_gantt)

        # Sum up propeties of each facility
        total_announced_throughput[c] = sum_property(years, announced[c], 'annual_throughput')
        total_scenario_throughput[c] = sum_property(years, scenario[c], 'annual_throughput')
        total_announced_investment[c] = sum_property(years, announced[c], 'annual_investment')
        total_scenario_investment[c] = sum_property(years, scenario[c], 'annual_investment')
        total_announced_fab_port_investment[c] = sum_property(years, announced[c], 'annual_fab_port_investment')
        total_scenario_fab_port_investment[c] = sum_property(years, scenario[c], 'annual_fab_port_investment')

        # Compare with demand
        fname = 'results/'+ plot_dir + '/' + c + '_supply_demand'
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
        fname_diff = 'results/' + plot_dir + '/' + c + 'diff'
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
        fname = 'results/'+ plot_dir + '/' + c + '_investment'
        y_investment = [total_announced_investment[c], total_scenario_investment[c] ]
        color_investment = [color_list['Announced'], color_list['Scenario']]
        name_investment = ['Announced','Additional required']
        hatch_investment = [color_list['Announced_hatch'], color_list['Scenario_hatch'], None]
        ylabel = 'Cumulative investment ($ million)'
        plot_supply_demand(years, zip(y_throughput, color_investment, name_investment, hatch_investment), color_list, c, ylabel, fname=fname)
        #
        # # Plot jobs
        # fname = 'results/'+ plot_dir + '/' + c + '_jobs'
        # y_jobs = [total_announced_jobs[c], total_scenario_jobs[c] ]
        # color_jobs = [color_list['Announced'], color_list['Scenario']]
        # name_jobs = ['Announced','Additional required']
        # hatch_jobs = [color_list['Announced_hatch'], color_list['Scenario_hatch'], None]
        # ylabel = 'Cumulative jobs, FTEs'
        # plot_supply_demand(years, zip(y_jobs, color_jobs, name_jobs, hatch_jobs), color_list, c, ylabel, fname=fname)

    ### total_announced_investment = arrays
    ### announced = dict
    fab_port_inv = [0] * len(years)
    for c in components:
            _a = total_announced_fab_port_investment[c]
            _s = total_scenario_fab_port_investment[c]
            fab_port_inv = np.array([sum(x) for x in zip(_a, _s, fab_port_inv)])
    total_ports = np.add(ports_inv, fab_port_inv)
    total_vessels = vessel_inv

    plot_cumulative(years, total_announced_investment, total_scenario_investment, total_ports, total_vessels, components, color_list, ylabel = 'Investment, $ million', fname='results/total_investment', ymax=25000)
    #
    # plot_cumulative(years, total_announced_jobs, total_scenario_jobs, components, color_list, ylabel='Direct manufacturing jobs, FTEs', fname='results/total_jobs', alternate_breakdown=job_breakdown)
    #
    plot_num_facilities(components, announced, scenario, color_list, fname='results/num_facilities')
    #
    # Construction Gantt charts
    fname_gantt2 = 'results/' + plot_dir + '/overall_gantt'
    plot_gantt(components, announced_list, scenario_list, color_list, fname=fname_gantt2)
    # # plot_job_breakdown()
    #
    # Overall difference in component_list
    fname_total_diff = 'results/' + plot_dir + '/total_diff'
    domestic_sc_percent = plot_total_diff(years, annual_diff, total_demand, fname_total_diff)

    return years, cod_years, total_demand, domestic_sc_percent, total_deploy, annual_deploy
    #
    # # Plot percentage of deployment from domestic supply chain
    # fname_deploy_perc = 'results/deployment_impact'
    # scaled_deploy = [(i/100)*j for i,j in zip(domestic_sc_percent, total_deploy)]
    # deploy_scenarios = [total_deploy, scaled_deploy]
    # ylabels = ['Baseline deployment', 'Supply chain constraints']
    # linetype = ['-', '--']
    #
    # lineplot_comp(cod_years, deploy_scenarios, ylabels, linetype,  fname=fname_deploy_perc)
