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
legendSize = tickLabelSize + 2
textSize = legendSize - 2
deltaShow = 4
linewidth = 3


def myformat(ax, linewidth=linewidth, yticklabel=tickLabelSize, mode='save'):
    assert type(mode) == type('')
    assert mode.lower() in ['save', 'show'], 'Unknown mode'

    def myformat(myax, linewidth=linewidth, yticklabel=tickLabelSize,):
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
                i.set_size(tickLabelSize)
            for i in myax.get_xticklines():
                i.set_linewidth(3)
            for i in myax.get_yticklabels():
                i.set_size(tickLabelSize)
            for i in myax.get_yticklines():
                i.set_linewidth(3)

    if type(ax) == type([]):
        for i in ax: myformat(i)
    else:
        myformat(ax)

def initFigAxis():
    fig = plt.figure(figsize=(12, 9))
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

def plot_cumulative(x, y1, y2, components, color_list, ylabel, fname=None, alternate_breakdown=None):
    """ PLot the cumulative investment or jobs in the overall supply chain"""
    fig, ax = initFigAxis()

    yBase = np.zeros(len(x))
    for c in components:
        yPlot = yBase + y1[c] + y2[c]
        ax.plot(x, yPlot, 'k')
        ax.fill_between(x, list(yBase), list(yPlot), color=color_list[c], label=c)
        yBase = yPlot

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
                count1 += 1
        for f2 in y2:
            if c in f2:
                count2 += 1
        announced[c] = count1
        scenario[c] = count2

    fig, ax = initFigAxis()
    announced_vals = list(announced.values())
    scenario_vals = list(scenario.values())

    ax.bar(components, announced_vals, color=color_list['Announced'], edgecolor='k', label='Announced')
    ax.bar(components, scenario_vals, color=color_list['Scenario'],  edgecolor='k', bottom=announced_vals, label='Additional required')

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
    fig, ax = initFigAxis()
    bar_height = 0.4
    ax.barh(sort_names[::-1], width=sort_duration[::-1], height=bar_height, left=sort_start[::-1], color=sort_color[::-1])
    ax.tick_params(axis='y', which='major', labelsize=5)
    ax.grid()

    if fname:
        if single_component == False:
            myformat(ax, yticklabel=5)
        else:
            myformat(ax)
        mysave(fig, fname)
        plt.close()

def lineplot_comp(x, y, legend, linetype, xlabel, ylabel, fname):
    fig, ax = initFigAxis()
    for y, l, t in zip(y, legend, linetype):
        ax.plot(x, y, t, label=l)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()
    ax.grid()
    if fname:
        myformat(ax)
        mysave(fig, fname)
        plt.close()
