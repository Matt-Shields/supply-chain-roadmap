import pandas as pd
import numpy as np
from plot_routines import stacked_bar_2ser, simple_bar

dir_ind_jobs = True
state_facilities = True

if __name__ == '__main__':
    ##### Gaps assessment slide deck



    # Direct vs indirect Jobs
    if dir_ind_jobs == True:
        component = ['Nacelle', 'Blade', 'Tower', 'Monopile', 'Transition \npiece', 'Jacket', 'Offshore \nsubstation', 'Cable']
        direct = np.array([35.6, 48.3, 43.7, 34.3, 34.3, 34.3, 71.3, 38.4])
        indirect = np.array([64.4, 51.9, 56.4, 65.7, 65.7, 65.7, 28.7, 61.6])
        dir_col = '#FF8500'
        indir_col = '#055B7C'
        n1 = 'Direct jobs'
        n2 = 'Indirect jobs'
        ylabel = 'Breakdown of direct and indirect jobs, %'
        fname = 'results/additional_plots/dir_ind_jobs.png'
        ymax=100

        stacked_bar_2ser(component, direct, indirect, dir_col, indir_col, n1, n2, ylabel, fname, ymax)


    if state_facilities == True:
        filepath = 'C:/Users/mshields/Documents/Projects/Supply Chain Roadmap/Analysis repos/Roadmap/fabrication_ports/ports_scenario_max.xlsx'
        scenario = pd.read_excel(filepath, header=9, usecols='A:P')
        state_ports = pd.pivot_table(scenario, index='State', values='Factory', aggfunc=len)
        states = np.array(state_ports.index)
        factories = np.array(state_ports['Factory'])

        factory_ind = np.argsort(factories)
        sort_states = [states[i] for i in factory_ind[::-1]]
        sort_factories = [factories[i] for i in factory_ind[::-1]]

        yticks = np.arange(0,max(factories)+1,1)
        ylabel = 'Number of factories'
        fname = 'results/state_factories'

        simple_bar(sort_states, sort_factories, yticks, ylabel=ylabel, fname=fname)
