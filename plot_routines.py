import pandas as pd
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


def myformat(ax, linewidth=linewidth, mode='save'):
    assert type(mode) == type('')
    assert mode.lower() in ['save', 'show'], 'Unknown mode'

    def myformat(myax, linewidth=linewidth):
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
                i.set_size(tickLabelSize + deltaShow)
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
            y_average = np.ones(len(x_average)) * np.mean(y2[_ind_i:_ind_f+1])
            label_avg = 'Average demand between ' + str(x[_ind_i]) + ' and ' + str(x[_ind_f])
            ax.plot(x_average, y_average, c=line, linestyle='--', label=label_avg)
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

def plot_gantt(announced, scenario, color_list, fname=None):
    """Gantt chart showing announced and scenario construction times"""

    # Extract information from each list of Facilities
    names = []
    start_date = []
    duration = []
    color = []
    for a in announced:
        names.append(a.name)
        start_date.append(a.announced_date)
        duration.append(a.construction_time)
        color.append(color_list['Announced'])
    s_ind = 0
    for s in scenario:
        _name = s.name + str(s_ind)
        names.append(_name)
        start_date.append(s.announced_date)
        duration.append(s.construction_time)
        color.append(color_list['Scenario'])
        s_ind += 1
    print(names, start_date, duration, color)

    # Make horizontal bar (Gantt)charts
    fig, ax = initFigAxis()
    bar_height = 0.4
    ax.barh(names[::-1], width=duration[::-1], height=bar_height, left=start_date[::-1], color=color[::-1])

    if fname:
        myformat(ax)
        mysave(fig, fname)
        plt.close()
