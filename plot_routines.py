import pandas as pd
import math
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.cm as cm
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.text as txt
import matplotlib.patches as mpatches
import os

from helpers import label_map


def mysave(fig, froot, mode='png'):
    assert mode in ['png', 'eps', 'pdf', 'all']
    fileName, fileExtension = os.path.splitext(froot)
    padding = 0.1
    dpiVal = 200
    legs = []
    for a in fig.get_axes():
        addLeg = a.get_legend()
        if not addLeg is None: legs.append(a.get_legend())
    ext = []
    if mode == 'png' or mode == 'all':
        ext.append('png')
    if mode == 'eps':  # or mode == 'all':
        ext.append('eps')
    if mode == 'pdf' or mode == 'all':
        ext.append('pdf')

    for sfx in ext:
        fig.savefig(fileName + '.' + sfx, format=sfx, pad_inches=padding, bbox_inches='tight',
                    dpi=dpiVal, bbox_extra_artists=legs)


titleSize = 24  # 40 #38
axLabelSize = 20  # 38 #36
tickLabelSize = 18  # 30 #28
ganttTick = 18
legendSize = tickLabelSize + 2
textSize = legendSize - 2
deltaShow = 4
linewidth = 3


def myformat(ax, linewidth=linewidth, xticklabel=tickLabelSize, yticklabel=tickLabelSize, mode='save'):
    assert type(mode) == type('')
    assert mode.lower() in ['save', 'show'], 'Unknown mode'

    def myformat(myax, linewidth=linewidth, xticklabel=xticklabel, yticklabel=yticklabel):
        if mode.lower() == 'show':
            for i in myax.get_children():  # Gets EVERYTHING!
                if isinstance(i, txt.Text):
                    i.set_size(textSize + 3 * deltaShow)

            for i in myax.get_lines():
                if i.get_marker() == 'D': continue  # Don't modify baseline diamond
                i.set_linewidth(linewidth)
                # i.set_markeredgewidth(4)
                i.set_markersize(10)

            leg = myax.get_legend()
            if not leg is None:
                for t in leg.get_texts(): t.set_fontsize(legendSize + deltaShow + 6)
                th = leg.get_title()
                if not th is None:
                    th.set_fontsize(legendSize + deltaShow + 6)

            myax.set_title(myax.get_title(), size=titleSize + deltaShow, weight='bold')
            myax.set_xlabel(myax.get_xlabel(), size=axLabelSize + deltaShow, weight='bold')
            myax.set_ylabel(myax.get_ylabel(), size=axLabelSize + deltaShow, weight='bold')
            myax.tick_params(labelsize=tickLabelSize + deltaShow)
            myax.patch.set_linewidth(3)
            for i in myax.get_xticklabels():
                i.set_size(tickLabelSize + deltaShow)
            for i in myax.get_xticklines():
                i.set_linewidth(3)
            for i in myax.get_yticklabels():
                i.set_size(yticklabel + deltaShow)
            for i in myax.get_yticklines():
                i.set_linewidth(3)

        elif mode.lower() == 'save':
            for i in myax.get_children():  # Gets EVERYTHING!
                if isinstance(i, txt.Text):
                    i.set_size(textSize)

            for i in myax.get_lines():
                if i.get_marker() == 'D': continue  # Don't modify baseline diamond
                i.set_linewidth(linewidth)
                # i.set_markeredgewidth(4)
                i.set_markersize(10)

            leg = myax.get_legend()
            if not leg is None:
                for t in leg.get_texts(): t.set_fontsize(legendSize)
                th = leg.get_title()
                if not th is None:
                    th.set_fontsize(legendSize)

            myax.set_title(myax.get_title(), size=titleSize, weight='bold')
            myax.set_xlabel(myax.get_xlabel(), size=axLabelSize, weight='bold')
            myax.set_ylabel(myax.get_ylabel(), size=axLabelSize, weight='bold')
            myax.tick_params(labelsize=tickLabelSize)
            myax.patch.set_linewidth(3)
            for i in myax.get_xticklabels():
                i.set_size(xticklabel)
            for i in myax.get_xticklines():
                i.set_linewidth(3)
            for i in myax.get_yticklabels():
                i.set_size(yticklabel)
            for i in myax.get_yticklines():
                i.set_linewidth(3)

    if type(ax) == type([]):
        for i in ax: myformat(i)
    else:
        myformat(ax)

def initFigAxis(figx=12, figy=9):
    fig = plt.figure(figsize=(figx, figy))
    ax = fig.add_subplot(111)
    return fig, ax

def plot_supply_demand(x, y_zip, color_list, component, ylabel, y2=None, ylim=None, fname=None, plot_average=None):
    fig, ax = initFigAxis()
    y_total = np.zeros(len(x))
    color=color_list['Announced']

    for y, c, n, h in y_zip:
        ax.bar(x, y, color=color, edgecolor='k',  label=n, bottom=y_total)
        y_total += y
        color=color_list['Scenario']

    line = 'k'
    if y2 is not None:
        ax.plot(x, y2, line, label='Annual demand')
        if plot_average is not None:
            _ind_i = np.where(x == plot_average[0])[0][0]
            _ind_f = np.where(x == plot_average[1])[0][0]
            x_average = x[_ind_i:_ind_f+1]
            _y_avg = np.mean(y2[_ind_i:_ind_f+1])
            y_average = np.ones(len(x_average)) * _y_avg
            label_avg = 'Average demand between ' + str(x[_ind_i]) + ' and ' + str(x[_ind_f])
            ax.plot(x_average, y_average, c=line, linestyle='--', label=label_avg)
        else:
            _y_avg = -999
    else:
        _y_avg = -999
    # else:
    #     # ax.plot(x, y2, 'k', label='Total demand')
    ax.set_xticks(x)
    ax.set_xticklabels(ax.get_xticks(), rotation=45)
    ax.set_xlabel('Manufacturing date')

    if ylim is not None:
        ax.set_ylim([0, ylim])
    ax.set_ylabel(ylabel)
    ax.get_yaxis().set_major_formatter(
        mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    ax.legend(loc='upper left')

    if fname is not None:
        myformat(ax)
        mysave(fig, fname)
        plt.close()

    return _y_avg

def plot_diff(x, y, ylabel, color, fname):
    fig, ax = initFigAxis()
    # Separate into positive and negative
    yneg = [i if i<0 else 0 for i in y]
    ypos = [i if i>0 else 0 for i in y]

    ax.bar(x, yneg, color=color['Deficit'], edgecolor='k', label='Production deficit')
    ax.bar(x, ypos, color=color['Surplus'], edgecolor='k', alpha=0.75, label='Production surplus')

    ax.set_xticks(x)
    ax.set_xticklabels(ax.get_xticks(), rotation=45)
    ax.set_xlabel('Manufacturing date')

    ax.set_ylabel(ylabel)

    ax.legend(loc='upper left')

    if fname is not None:
        myformat(ax)
        mysave(fig, fname)
        plt.close()

    return ypos

def plot_total_diff(x, y, demand, fname):
    fig, ax = initFigAxis()
    # Loop through all components
    num_components = [0] * len(x)
    sum_percent = [0] * len(x)
    for k, v in y.items():
        v = [0 if math.isnan(x) else x for x in v]
        v = [1 if x > 1 else x for x in v]
        sum_percent = [i[0] + i[1] for i in zip(sum_percent, v)]

        annual_components  = [1 if x!=0 else 0 for x in demand[k]]
        num_components = [i[0] + i[1] for i in zip(annual_components, num_components)]

    total_percent = [100*x[0] / x[1] if x[1] != 0 else 0 for x in zip(sum_percent, num_components)]
    ax.plot(x, total_percent, 'k')
    plt.fill_between(x, total_percent)

    ax.set_xlabel('Manufacturing date')
    ax.set_ylabel('Percent of component demand met by domestic supply chain')
    ax.grid()

    if fname is not None:
        myformat(ax)
        mysave(fig, fname)
        plt.close()

    return total_percent

def plot_cumulative(x, y1, y2, y3, y4, components, color_list, ylabel, fname=None, alternate_breakdown=None, ymax=None):
    """ PLot the cumulative investment or jobs in the overall supply chain"""
    fig, ax = initFigAxis()

    yBase = np.zeros(len(x))
    for c in components:
        yPlot = yBase + y1[c] + y2[c]
        ax.plot(x, yPlot, 'k')
        ax.fill_between(x, list(yBase), list(yPlot), color=color_list[c], label=c)
        yBase = yPlot

    # Add ports
    yPorts = yBase + y3
    ax.fill_between(x, list(yBase), list(yPorts), color=color_list['Ports'], alpha=0.5, label='Ports')
    ax.plot(x, yPorts, 'k')
    # Add vessels
    yVessels = yPorts + y4
    ax.fill_between(x, list(yPorts), list(yVessels), color=color_list['WTIV'], label='WTIVs and HLVs')
    ax.plot(x, yVessels, 'w')

    total_inv = pd.DataFrame({'Year': x, 'Investment': yVessels})
    print('Cumulative supply chain investment is: ', total_inv)

    if ymax is not None:
        ax.set_ylim([0,ymax])

    ax.set_xlabel('Manufacturing date')
    ax.set_ylabel(ylabel)
    ax.get_yaxis().set_major_formatter(
        mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], loc='upper left')
    # ax.legend(loc='upper left')

    if fname is not None:
        myformat(ax, linewidth=2)
        mysave(fig, fname)
        plt.close()

    if alternate_breakdown is not None:
        fig_alt, ax_alt = initFigAxis()

        yBase_total = yBase
        yBase_alt = np.zeros(len(x))
        for k, v in alternate_breakdown.items():
            yPlot_alt = yBase_alt + v * yBase_total
            ax_alt.plot(x, yPlot_alt, 'k')
            ax_alt.fill_between(x, list(yBase_alt), list(yPlot_alt), color=color_list[k], label=k)
            yBase_alt = yPlot_alt

        ax_alt.set_xlabel('Manufacturing date')
        ax_alt.set_ylabel(ylabel)
        ax_alt.get_yaxis().set_major_formatter(
            mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

        handles, labels = ax_alt.get_legend_handles_labels()
        ax_alt.legend(handles[::-1], labels[::-1], loc='upper left')

        if fname is not None:
            myformat(ax_alt)
            mysave(fig_alt, fname+'_alt')
            plt.close()



def plot_num_facilities(components, y1, y2, color_list, fname=None):
    """Plot the total number of required facilities per component"""

    announced = {}
    scenario = {}
    bar_color = []

    for c in components:
        count1 = 0
        count2 = 0
        for f1 in y1:
            if c in f1:
                count1 += len(y1[f1])
        for f2 in y2:
            if c in f2:
                count2 += len(y2[f2])
        announced[c] = count1
        scenario[c] = count2

    fig, ax = initFigAxis()
    announced_vals = list(announced.values())
    scenario_vals = list(scenario.values())

    ax.bar(components, announced_vals, color=color_list['Announced'], edgecolor='k', linewidth=2, label='Announced')
    ax.bar(components, scenario_vals, color=color_list['Scenario'],  edgecolor='k', linewidth=2, bottom=announced_vals, label='Additional required')

    xlabels = [label_map[c] for c in components]

    ax.set_xticklabels(components, rotation=90)
    ax.set_ylabel('Number of facilities')

    ax.legend(loc='upper left')

    if fname is not None:
        myformat(ax)
        mysave(fig, fname)
        plt.close()

def stacked_bar_2ser(x, y1, y2, c1, c2, n1, n2, ylabel, fname=None, ymax=None):
    """ Simple stacked bar chart for 2 series"""
    fig, ax = initFigAxis()
    ax.bar(x, y1, color=c1, edgecolor='k', label=n1)
    ax.bar(x, y2, color=c2, edgecolor='k', label=n2, bottom=y1)

    if ymax is not None:
        ax.set_ylim([0, ymax])

    ax.set_xticklabels(x, rotation=45)
    ax.set_ylabel(ylabel)

    ax.legend(loc='upper left', bbox_to_anchor=(1.01, 1))

    if fname:
        myformat(ax)
        mysave(fig, fname)
        plt.close()

def plot_gantt(components, announced, scenario, color_list, single_component=False, fname=None):
    """Gantt chart showing announced and scenario construction times"""

    # Extract information from each list of Facilities
    names = []
    start_date = []
    duration = []
    color = []
    facility_ind = {}
    for c in components:
        facility_ind[c] = 1

    for a in announced:
        if single_component == False:
            fi = facility_ind[a.component]
            names.append(a.component + '#' + str(fi) + ' (' + a.name.split(', ')[1] + ')')
        else:
            names.append(a.name)
        start_date.append(a.announced_date)
        duration.append(a.construction_time)
        color.append(color_list['Announced'])
        facility_ind[a.component] += 1

    for s in scenario:
        # _name = s.name + str(s_ind)
        fi = facility_ind[s.component]
        _name = s.component + '#' + str(fi) + ' (' + s.name.split(', ')[1] + ')'
        names.append(_name)
        start_date.append(s.announced_date)
        duration.append(s.construction_time)
        color.append(color_list['Scenario'])
        facility_ind[s.component] += 1

    # Sort by start data
    start_ind = np.argsort(start_date)
    sort_names = [names[i] for i in start_ind]
    sort_duration = [duration[i] for i in start_ind]
    sort_start = [start_date[i] for i in start_ind]
    sort_color = [color[i] for i in start_ind]

    # Make horizontal bar (Gantt)charts
    fig, ax = initFigAxis(figy=12)
    bar_height = 0.4
    ax.barh(sort_names[::-1], width=sort_duration[::-1], height=bar_height, left=sort_start[::-1], color=sort_color[::-1])
    ax.set_xticks(list(np.arange(2018, 2033+1, 1)))
    ax.set_xticklabels(ax.get_xticks(), rotation=45)
    ax.grid(alpha=0.5)

    if fname:
        if single_component == False:
            myformat(ax, xticklabel=ganttTick, yticklabel=ganttTick)
        else:
            myformat(ax)
        mysave(fig, fname)
        plt.close()

def lineplot_comp(x, y, legend, linetype, xlabel, ylabel, xlim, ylim, fname):
    fig, ax = initFigAxis()

    # Write data out
    _df_out = pd.DataFrame({
        'Year': x
    })

    for y, l, t in zip(y, legend, linetype):
        ax.plot(x, y, t, label=l)
        _df_out[l] = y
    print(_df_out)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_ylim(ylim)
    ax.set_xlim(xlim)
    ax.legend(loc='upper left')
    ax.grid()
    if fname:
        myformat(ax)
        mysave(fig, fname)
        plt.close()

def simple_bar(x, y, yticks, xlabel=None, ylabel=None, fname=None):
    fig, ax = initFigAxis()

    ax.bar(x, y)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_yticks(yticks)

    ax.set_xticklabels(x, rotation=45)

    if fname:
        myformat(ax)
        mysave(fig, fname)
        plt.close()

def pie_plot(y, c, n, fname=None):
    fig, ax = initFigAxis()

    y_pie = y / np.sum(y)
    _dict = {}
    _c_dict={}
    for name, val, col in zip(n, y_pie, c):
        _val = np.round(100*val, 1)
        _leg = (name + ' (' + str(_val) + '%)')
        _dict[_leg] = _val
        _c_dict[col] = _val

    sort_dict = {k: v for k, v in sorted(_dict.items(), key=lambda item: item[1])}
    sort_c_dict = {k: v for k, v in sorted(_c_dict.items(), key=lambda item: item[1])}

    wedges, texts = ax.pie(sort_dict.values(), colors=sort_c_dict.keys())
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    ax.legend(wedges[::-1], list(sort_dict.keys())[::-1],
              loc='center left',
              bbox_to_anchor=(0.9, 0, 0.5, 1))

    # handles, labels = ax.get_legend_handles_labels()
    # ax.legend(handles=handles[::-1],
    #            labels=labels[::-1])


    if fname:
        myformat(ax)
        mysave(fig, fname)
        plt.close()

def area_bar_chart(x, y1, y2, l, kwargs, fname=None):
    fig, ax = initFigAxis()

    # Area plot
    y0 = np.zeros(len(x))
    ax.fill_between(x, list(y0), y1, color=kwargs['color1'], label=l[0], zorder=kwargs['zorder1'])
    ax.plot(x,y1, 'k', zorder=kwargs['zorder1'])

    # Bar plot
    ax.bar(x, y2, width=kwargs['bar_width'], color=kwargs['color2'], label=l[1], zorder=kwargs['zorder2'])

    ax.set_xlabel(kwargs['xlabel'])
    ax.set_ylabel(kwargs['ylabel'])
    ax.set_xlim(x[0], x[-1]+1)
    ax.set_ylim(kwargs['ylim'])
    ax.legend(loc='upper left')
    ax.get_yaxis().set_major_formatter(
        mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    if fname:
        myformat(ax)
        mysave(fig, fname)
        plt.close()

def plot_cumulative_jobs(x, y, components, color_list, kwargs, fname=None):
    """ PLot the cumulative jobs in the overall supply chain"""
    fig, ax = initFigAxis()

    yBase = np.zeros(len(x))
    for c in components:
        yPlot = y.loc[c,:].values + yBase
        ax.plot(x, yPlot, 'k')
        ax.fill_between(x, list(yBase), list(yPlot), color=color_list[c], label=c)
        yBase = yPlot

    ax.set_xlabel(kwargs['xlabel'])
    ax.set_ylabel(kwargs['ylabel'])
    ax.set_ylim(kwargs['ylim'])
    ax.get_yaxis().set_major_formatter(
        mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], loc='upper left')
    # ax.legend(loc='upper left')

    if fname is not None:
        myformat(ax, linewidth=2)
        mysave(fig, fname)
        plt.close()

def plot_overlap_bar(x, y1, y2, y3, color_list, kwargs, fname=None):
    """y1 and y2 are side-by-side vertical bars; y3 is a vertical bar overlapping these two"""

    fig, ax = initFigAxis(figx=30)

    # x =  np.arange(len(x_name))

    y_avg = [(i+j+k)/3 for i,j,k in zip(y1, y2, y3)]
    y_avg_sort = [y_avg[i] for i in np.argsort(y_avg)]
    x_sort = [x[i] for i in np.argsort(y_avg)]
    # x1_sort = [x[i] - kwargs['bar_width'] for i in np.argsort(y_avg)]
    # x2_sort = [x[i] + kwargs['bar_width'] for i in np.argsort(y_avg)]
    # x_name_sort = [x_name[i] for i in np.argsort(y_avg)]
    y1_sort = [y1[i] for i in np.argsort(y_avg)]
    y2_sort = [y2[i] for i in np.argsort(y_avg)]
    y3_sort = [y3[i] for i in np.argsort(y_avg)]

    x_tick = np.arange(len(x_sort))

    ax.bar(x_tick - kwargs['bar_width'], y1_sort[::-1], width=kwargs['bar_width'],  label=kwargs['legend'][0], edgecolor='k', color=color_list[kwargs['legend'][0]])
    ax.bar(x_tick, y2_sort[::-1], width=kwargs['bar_width'], label=kwargs['legend'][1], edgecolor='k', color=color_list[kwargs['legend'][1]])
    ax.bar(x_tick + kwargs['bar_width'], y3_sort[::-1], kwargs['bar_width'],   label=kwargs['legend'][2], edgecolor='k', color=color_list[kwargs['legend'][2]])

    ax.plot(x_sort[::-1], y_avg_sort[::-1],'k', label='Average score')

    ax.set_xticks(x_tick)
    ax.set_xticklabels(x_sort[::-1], rotation=45)
    ax.legend()
    frame = plt.gca()
    frame.axes.get_yaxis().set_visible(False)

    if fname is not None:
        myformat(ax)
        mysave(fig, fname)
        plt.close()

def plot_multi_bars(x, y1, y2, y2_bottom, y2_height, color_list, kwargs, fname=None):
    """y1 is a bar starting at the x axis, y2 is a range bar above"""

    fig, ax = initFigAxis(figx=kwargs['figx'])

    ind_label = 'Range of indirect job potential'

    ymin = [y2_bottom[i] for i in np.argsort(y2)]
    xsort = [x[i] for i in np.argsort(y2)]
    y2sort = [y2_height[i] for i in np.argsort(y2)]
    y1sort = [y1[i] for i in np.argsort(y2)]


    ax.bar(xsort[::-1], y1sort[::-1], width=kwargs['width'], label=kwargs['legend'][0], color=color_list[kwargs['legend'][0]], edgecolor='k')
    ax.bar(xsort[::-1], y2sort[::-1], width=kwargs['width'], bottom=ymin[::-1], label=ind_label, color=color_list[kwargs['legend'][1]], edgecolor='k')

    ax.set_xticklabels(xsort[::-1], rotation=kwargs['rotation'])
    ax.set_ylabel(kwargs['ylabel'])
    ax.set_ylim(kwargs['ylim'])
    ax.legend(loc='upper left')
    ax.get_yaxis().set_major_formatter(
        mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    if fname is not None:
        myformat(ax)
        mysave(fig, fname)
        plt.close()

def plot_port_vessel_gantt(data, color_list, fname):

        # Select all cases
        ports = []
        wtivs = []
        hlvs = []
        ports_start = []
        wtivs_start = []
        hlvs_start = []
        ports_end = []
        wtivs_end = []
        hlvs_end = []


        y_existing = []

        existing_start = []
        existing_end = []
        # expanded_start = []

        # end_date = 2030

        for k, v in data.items():
            # Define all assets
            ports += [i for i, j in data[k]['Ports'].items()]
            wtivs += [i for i, j in data[k]['WTIVs'].items()]
            hlvs += [i for i, j in data[k]['HLVs'].items()]

            ports_start += [j['start'] for i, j in data[k]['Ports'].items()]
            wtivs_start += [j['start'] for i, j in data[k]['WTIVs'].items()]
            hlvs_start += [j['start'] for i, j in data[k]['HLVs'].items()]

            ports_end += [j['end'] for i, j in data[k]['Ports'].items()]
            wtivs_end += [j['end'] for i, j in data[k]['WTIVs'].items()]
            hlvs_end += [j['end'] for i, j in data[k]['HLVs'].items()]

            if k == 'Existing':
                y_existing += [i for i, j in data[k]['Ports'].items()] + [i for i, j in data[k]['WTIVs'].items()] + [i for i, j in data[k]['HLVs'].items()]
                existing_start += [j['start'] for i, j in data[k]['Ports'].items()] + [j['start'] for i, j in data[k]['WTIVs'].items()] + [j['start'] for i, j in data[k]['HLVs'].items()]
                existing_end += [j['end'] for i, j in data[k]['Ports'].items()] + [j['end'] for i, j in data[k]['WTIVs'].items()] + [j['end'] for i, j in data[k]['HLVs'].items()]
                existing_width = [e-s for s,e in zip(existing_start, existing_end)]

        yvals = ports +  wtivs +  hlvs
        ypos = np.arange(len(yvals))

        expanded_start = ports_start + wtivs_start + hlvs_start
        expanded_end= ports_end + wtivs_end + hlvs_end
        expanded_width = [e-s for s,e in zip(expanded_start, expanded_end)]

        # Make horizontal bar (Gantt)charts
        fig, ax = initFigAxis()
        bar_height = 0.5

        ax.set_yticks(ypos)

        ax.barh(yvals[::-1], left=expanded_start[::-1], width=expanded_width[::-1], height=bar_height, color=color_list['Expanded'], label='Expanded infrastructure scenario only')
        ax.barh(y_existing[::-1], left=existing_start[::-1], width=existing_width[::-1], height=bar_height, color=color_list['Existing'], label='Existing and expanded infrastructure scenarios')

        y1_line = len(yvals) - ( len(ports) + 0.5)
        y2_line = len(yvals) - ( len(ports) + len(wtivs) + 0.5)


        label_space = .075
        y1_label = y1_line / len(yvals) + label_space
        y2_label = y2_line / len(yvals) + label_space
        y3_label = label_space

        plt.axhline(y1_line, color='k', linestyle='--')
        plt.axhline(y2_line, color='k', linestyle='--')

        ax.set_xticks(list(np.arange(2023, 2029+2, 1)))
        ax.set_xticklabels(ax.get_xticks(), rotation=45)
        ax.grid(alpha=0.5)

        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1], loc='upper center', bbox_to_anchor=(0.5, -0.12))

        ax.text(.02, y1_label, 'Ports', transform=ax.transAxes, bbox=dict(facecolor='tab:gray', alpha=0.5))
        ax.text(.02, y2_label, 'WTIVs', transform=ax.transAxes, bbox=dict(facecolor='tab:gray', alpha=0.5))
        ax.text(.02, y3_label, 'HLVs', transform=ax.transAxes, bbox=dict(facecolor='tab:gray', alpha=0.5))


        if fname is not None:
            myformat(ax)
            mysave(fig, fname)
            plt.close()
