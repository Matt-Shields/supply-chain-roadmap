import pandas as pd
import numpy as np
from plot_routines import stacked_bar_2ser, simple_bar, pie_plot
from helpers import color_list


dir_ind_jobs = False
workforce_plots = True

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

    if workforce_plots == True:
        wf_filepath = 'workforce_plot_data/SC Report WF Charts_All.xlsx'

        workforce_plot_list = {
            'Figure 5': {'header': 3, 'index_col': 0, 'usecols': 'A:B', 'nrows': 5},
            'Figure 16 (top)': {'header': 5, 'index_col': 0, 'usecols': 'A:Q', 'nrows': 3},
        }

        for fig, data in workforce_plot_list.items():
            # print(fig, df)
            _df = pd.read_excel(wf_filepath, sheet_name=fig, header=data['header'], index_col=data['index_col'],    usecols=data['usecols'], nrows=data['nrows'])

            # Extract data and call plot routines
            if fig == 'Figure 5':
                names = _df.index.values
                values = _df.iloc[:,0].values
                colors = [color_list[n] for n in names]
                fname = 'results/workforce/worker_breakdown'
                pie_plot(values, colors, names, fname)
