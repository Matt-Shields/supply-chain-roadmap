""" Screen port database for fabrication ports """
import pandas as pd
import numpy as np

from openpyxl import load_workbook

from helpers import criteria, upgrade_costs, upgrade_time, exceptions, scenario

if __name__ == '__main__':
    # Read in database
    ports = pd.read_csv('ports_database.csv', header=8,  usecols=list(np.arange(0,12))).drop('Notes', axis=1)
    output_cols = list(ports.columns)

    # Number of components to screen for
    component_list = ['Blade', 'Nacelle', 'Tower', 'Monopile', 'Jacket', 'GBF', 'Cable', 'Transition piece', 'Steel plate', 'Flange', 'Bedplate']

    # How flexible are we in looking at ports
    scale_factor = 0.75

    # Preferred values for state goals and existing commtiemtns
    state_osw_goals = 1
    commitments = 0

    # Number of conditoins that need to be met during downselection
    min_conditions_met = 4
    min_criteria_met = 1

    # How to sort output dataframes
    sort_criteria = ['Region', 'Laydown area (acres)']
    sort_vals = [False, False]

    def apply_filter(x, c):
        """ Filter each port based on component specificatons"""
        _laydown = False
        _quayside = False
        _draft = False
        _air_draft = False
        _state_goals = False
        _commitments = False

        conditions_met = 0
        criteria_met = 0
        failed_conditions = []

        if x['Laydown area (acres)'] > scale_factor * c['Area']:
            conditions_met += 1
            # ASsign upgrade costs if port condition doesn't quite meet criteria
            if x['Laydown area (acres)'] > c['Area']:
                _laydown_cost = 0
            else:
                failed_conditions.append('laydown area')
                _laydown_cost = upgrade_costs['laydown']
        elif x['Port'] in exceptions['Laydown']:
            conditions_met += 1
            failed_conditions.append('laydown area')
            _laydown_cost = upgrade_costs['laydown']
        else:
            failed_conditions.append('laydown area')
            _laydown_cost = upgrade_costs['laydown']

        if x['Quayside length (m)'] > scale_factor * c['Quayside']:
            conditions_met += 1
            # ASsign upgrade costs if port condition doesn't quite meet criteria
            if x['Quayside length (m)'] > c['Quayside']:
                _quayside_cost = 0
            else:
                failed_conditions.append('quayside length')
                _quayside_cost = upgrade_costs['quayside']
        elif x['Port'] in exceptions['Quayside']:
            conditions_met += 1
            failed_conditions.append('quayside length')
            _quayside_cost = upgrade_costs['quayside']
        else:
            failed_conditions.append('quayside length')
            _quayside_cost = upgrade_costs['quayside']

        if x['Channel depth (m)'] > scale_factor * c['Draft']:
            conditions_met += 1
            if x['Channel depth (m)'] > c['Draft']:
                _dredge_cost = 0
            else:
                failed_conditions.append('channel depth')
                _dredge_cost = upgrade_costs['dredge']
        else:
            failed_conditions.append('channel depth')
            _dredge_cost = upgrade_costs['dredge']

        if x['Air draft restriction (m)'] > c['Air Draft']:
            conditions_met += 1
        else:
            # Force a failing condition if air draft restructions aren't met
            failed_conditions.append('air draft')
            conditions_met -= 10

        if x['Bearing capacity (t/m2)'] > scale_factor * c['Bearing']:
            conditions_met += 1
            if x['Bearing capacity (t/m2)'] >  c['Bearing']:
                _bearing_cost = 0
            else:
                failed_conditions.append('bearing capacity')
                _bearing_cost = upgrade_costs['bearing']
        else:
            failed_conditions.append('bearing capacity')
            _bearing_cost = upgrade_costs['bearing']

        if x['State OSW goals'] == state_osw_goals:
            criteria_met += 1

        if x['Existing commitments'] == commitments:
            criteria_met += 1


        _cost = upgrade_costs['permit_design'] + _laydown_cost + _quayside_cost + _dredge_cost + _bearing_cost
        _time = upgrade_time

        if conditions_met >= min_conditions_met and criteria_met >= min_criteria_met:
            _decision = 'Yes'
        else:
            _decision = 'No'

        return _decision, _cost, _time, failed_conditions


    filtered_ports = {}
    decision = []
    for c in component_list:
        c_decision = c + '_decision'
        c_cost = c + '_upgrade_cost'
        c_time = c + '_upgrade_time'
        c_fails = c + '_fails'
        decision.append(c_decision)

        _cols = output_cols + [c_decision, c_cost, c_time, c_fails]

        ports[c_decision], ports[c_cost], ports[c_time], ports[c_fails] = zip(*ports.apply(lambda x: apply_filter(x, criteria[c]), axis=1))
        filtered_ports[c] = ports.loc[ports[c_decision]=='Yes'].sort_values(by=sort_criteria, ascending=sort_vals)[_cols]

    with pd.ExcelWriter("filtered_component_ports.xlsx") as writer:
        for df_name, df in filtered_ports.items():
            df.to_excel(writer, sheet_name=df_name, index=False)


    # Summarize scenarios
    # df_scenario = pd.DataFrame()
    # for port, vals in scenario.items():
    #     print(vals)
    #     df_scenario['Component'] = vals['Component']
    #     df_scenario['Factory'] = vals['Factory']
    # print(df_scenario)
