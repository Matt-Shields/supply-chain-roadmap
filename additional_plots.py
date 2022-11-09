import pandas as pd
import numpy as np
from plot_routines import stacked_bar_2ser, simple_bar, pie_plot, area_bar_chart, plot_multi_bar, plot_cumulative_jobs, plot_overlap_bar, plot_multi_line, plot_port_vessel_gantt
from helpers import color_list


dir_ind_jobs = False
workforce_plots = True
port_vessel_plots = True

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
        wf_filepath = 'workforce_plot_data/SC Report WF Charts_All_November FINAL.xlsx'

        workforce_plot_list = {
            'Figure 5': {'header': 3, 'index_col': 0, 'usecols': 'A:B', 'nrows': 5},
            'Figure 16 (top)': {'header': 5, 'index_col': 0, 'usecols': 'A:Q', 'nrows': 3},
            'Figure 16 (bottom)': {'header': 5, 'index_col': 0, 'usecols': 'A:Q', 'nrows': 3},
            'Figure 20': {'header': 3, 'index_col': 0, 'usecols': 'A:D', 'nrows': 50},
            'Figure 21': {'header': 3, 'index_col': 0, 'usecols': 'A:AY', 'nrows': 4},
            'Figure B1 (top)': {'header': 5, 'index_col': 0, 'usecols': 'B:R', 'nrows': 15},
            'Figure B1 (bottom)': {'header': 5, 'index_col': 0, 'usecols': 'B:R', 'nrows': 15},
            'Figure B2 (top)': {'header': 7, 'index_col': 0, 'usecols': 'A:Q', 'nrows': 14},
            'Figure B2 (bottom)': {'header': 6, 'index_col': 0, 'usecols': 'B:R', 'nrows': 14},
            'Figure B3': {'header': 5, 'index_col': 0, 'usecols': 'A:Y', 'nrows': 4},
        }

        for fig, data in workforce_plot_list.items():
            _df = pd.read_excel(wf_filepath, sheet_name=fig, header=data['header'], index_col=data['index_col'],    usecols=data['usecols'], nrows=data['nrows'])

            # Extract data and call plot routines
            if fig == 'Figure 5':
                names = _df.index.values
                values = _df.iloc[:,0].values
                colors = [color_list[n] for n in names]
                fname = 'results/workforce/worker_breakdown'
                pie_plot(values, colors, names, fname)

            elif "Figure 16" in fig:
                years = _df.columns.values
                direct = _df.loc['Major manufacturing jobs (prescribed)',:].values
                indirect_100 = _df.loc['Supplier jobs (100% domestic content)',:].values
                indirect_25 = _df.loc['Supplier jobs (25% domestic content)',:].values
                label = ['Major manufacturing jobs (prescribed)',
                        'Supplier jobs (25% domestic content)',
                        'Supplier jobs (100% domestic content)']

                kwargs = {'bar_width': 0.33,
                            'zorder1': 0,
                            'zorder2': 1,
                            'color1': color_list[label[0]],
                            'color2': color_list[label[1]],
                            'color3': color_list[label[2]],
                            'ylim': [0, 60000],
                            'ylabel': 'Job market opportunity, Potential FTEs',
                            'xlabel': 'Manufacturing date'
                            }

                # Different names and directories for accelerated and conservative scenarios
                if "top" in fig:
                    fname = 'results/Accelerated/workforce_rampup'
                elif "bottom" in fig:
                    fname = 'results/Conservative/workforce_rampup'
                area_bar_chart(years, direct, indirect_25, indirect_100, label, kwargs, fname)
                # Alternate plot
                kwargs['bar_width'] = 0.25
                if "top" in fig:
                    fname_alt = 'results/Accelerated/workforce_rampup_alt'
                elif "bottom" in fig:
                    fname_alt = 'results/Conservative/workforce_rampup_alt'
                plot_multi_bar(years, direct, indirect_25, indirect_100, label, kwargs, fname_alt)
            elif "Figure 20" in fig:
                states = _df.index.values

                label = ['Existing similar industries',
                            'Proximity to scenario facilities',
                            'Adjacent industry manufacturing scale ']

                y1 = _df.loc[:, label[0]].values
                y2 = _df.loc[:, label[1]].values
                y3 = _df.loc[:, label[2]].values

                kwargs = {'bar_width': 0.2,
                            'back_bar_zorder': 0,
                            'front_bar_zorder': 1,
                            'legend': label
                            }
                fname = 'results/workforce/state_scoring'

                plot_overlap_bar(states, y1, y2, y3, color_list, kwargs, fname)
            elif "Figure 21" in fig or "Figure B3" in fig:

                states = _df.columns.values
                y1 = _df.iloc[2,:].values
                y2_bottom = _df.iloc[0,:].values
                y2_top = _df.iloc[1,:].values

                # y2_height = [t-b for b,t in zip(y2_bottom, y2_top)]

                kwargs = {'width': 0.4,
                            'legend': ['Major manufacturing jobs (prescribed)', 'Supplier jobs'],
                            'ylabel': 'Job market opportunity, Potential FTEs',
                }

                if "21" in fig:
                    fname = 'results/state_job_opportunity'
                    kwargs['ylim'] = [0,50000]
                    kwargs['figx'] = 25
                    kwargs['rotation'] = 45
                elif 'B3' in fig:
                    fname = 'results/NC_job_opportunity'
                    kwargs['ylim'] = [0,14000]
                    kwargs['figx'] = 12
                    kwargs['rotation'] = 90

                plot_multi_line(states, y1, y2_top, y2_bottom, color_list, kwargs, fname)

            elif "B1" in fig or "B2" in fig:
                years = _df.columns.values
                components = _df.index.values

                kwargs = {'xlabel': 'Manufacturing date',
                            'ylabel': 'Potential Job Opportunities, FTEs',
                            'ylim': [0, 60000],
                        }
                if "top" in fig:
                    if "B1" in fig:
                        fname = 'results/Accelerated/direct_workforce_rampup'
                    elif "B2" in fig:
                        fname = 'results/Accelerated/indirect_workforce_rampup'
                elif "bottom" in fig:
                    if "B1" in fig:
                        fname = 'results/Conservative/direct_workforce_rampup'
                    elif "B2" in fig:
                        fname = 'results/Conservative/indirect_workforce_rampup'

                plot_cumulative_jobs(years, _df, components, color_list, kwargs, aggregate=True, fname=fname)

            else:
                print("Figure type not identified")

    if port_vessel_plots == True:
        port_vessel_scenario = {
            'US_wtivs': {
                'Ports': {
                    'Baseline': {
                        'NBMCT': {'start': 2023, 'end': 2030, 'invest': 150},
                        'NLSP': {'start': 2023, 'end': 2030, 'invest': 255},
                        'PMT': {'start': 2025, 'end': 2030, 'invest': 250},
                        'NJWP (Phase 1)': {'start': 2025, 'end': 2030, 'invest': 400},
                        'TPA': {'start': 2025, 'end': 2030, 'invest': 200},
                        'SBMT': {'start': 2027, 'end': 2030, 'invest': 260},
                    },
                    'Scenario': {
                        'Salem': {'start': 2027, 'end': 2030, 'invest': 200},
                        'AKT': {'start': 2027, 'end': 2030, 'invest': 400},
                        'NJWP (Phase 2)': {'start': 2028, 'end': 2030, 'invest': 200},
                    }
                    },
                'WTIVs': {
                    'Baseline': {
                        'Foreign-flagged WTIV #1': {'start': 2023, 'end': 2025, 'invest': 0},
                        'Foreign-flagged WTIV #2': {'start': 2023, 'end': 2024, 'invest': 0},
                        'Charybdis': {'start': 2024, 'end': 2030, 'invest': 500},
                        'Maersk': {'start': 2025, 'end': 2030, 'invest': 500},
                    },
                    'Scenario': {
                        'New U.S.-flagged WTIV (x4)': {'start': 2026, 'end': 2030, 'invest':500},
                        # 'New U.S.-flagged WTIV (x2)': {'start': 2028, 'end': 2030, 'invest':1000}
                    },
                },
                'HLVs': {
                    'Baseline': {'Foriegn-flagged HLV (x2)': {'start': 2023, 'end': 2030, 'invest': 0},},
                    'Scenario': {'U.S./foreign-flagged HLV (x4)': {'start': 2026, 'end': 2030, 'invest': 1050},
                        },},
                'Feeder barges':{
                    'Baseline': {'U.S. feeder (x4)': {'start': 2023, 'end': 2030, 'invest': 0},},
                    'Scenario': {'U.S. feeder (x4)': {'start': 2023, 'end': 2030, 'invest': 0},},
                    },
            },
            'US_feeders': {
                'Ports': {
                    'Baseline': {
                        'NBMCT': {'start': 2023, 'end': 2030, 'invest': 150},
                        'NLSP': {'start': 2023, 'end': 2030, 'invest': 255},
                        'PMT': {'start': 2025, 'end': 2030, 'invest': 250},
                        'NJWP (Phase 1)': {'start': 2025, 'end': 2030, 'invest': 400},
                        'TPA': {'start': 2025, 'end': 2030, 'invest': 200},
                        'SBMT': {'start': 2027, 'end': 2030, 'invest': 260},
                    },
                    'Scenario': {
                        'Salem': {'start': 2027, 'end': 2030, 'invest': 200},
                        'AKT': {'start': 2027, 'end': 2030, 'invest': 400},
                        'NJWP (Phase 2)': {'start': 2028, 'end': 2030, 'invest': 200},
                    }
                    },
                'WTIVs': {
                    'Baseline': {
                        'Foreign WTIV #1': {'start': 2023, 'end': 2025, 'invest': 0},
                        'Foreign WTIV #2': {'start': 2023, 'end': 2024, 'invest': 0},
                        'Charybdis': {'start': 2024, 'end': 2030, 'invest': 500},
                        'Maersk': {'start': 2025, 'end': 2030, 'invest': 500},
                    },
                    'Scenario': {
                        'U.S./foreign-flagged WTIV (x2)': {'start': 2026, 'end': 2030, 'invest':0},}
                    },
                'HLVs': {
                    'Baseline': {'Foriegn-flagged HLV (x2)': {'start': 2023, 'end': 2030, 'invest': 0},},
                    'Scenario': {'U.S./foreign-flagged HLV (x2)': {'start': 2026, 'end': 2030, 'invest': 1050},
                        },
                    },
                'Feeder barges':{
                    'Baseline': {'U.S. feeder (x4)': {'start': 2023, 'end': 2030, 'invest': 0},},
                    'Scenario': {'New U.S. feeder (x4)': {'start': 2026, 'end': 2030, 'invest': 0},}
                    },

                }
        }

        scenario_label = {
            'US_wtivs': 'U.S. WTIV scenario: Focused investment in U.S.-flagged WTIVs',
            'US_feeders': 'U.S. Feeder scenario: Focused investment in U.S. flagged feeder barges',
        }

        fname = 'results/port_vessel_scenario_gantt'
        plot_port_vessel_gantt(port_vessel_scenario, color_list, scenario_label, fname=fname)
