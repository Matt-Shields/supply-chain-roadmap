import pandas as pd
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.cm as cm
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.text as txt
import os


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
linewidth = 4


def myformat(ax, mode='save'):
    assert type(mode) == type('')
    assert mode.lower() in ['save', 'show'], 'Unknown mode'

    def myformat(myax):
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

def plot_supply_demand(x, y_zip, y2, ylabel, fname=None, plot_average=None):
    fig, ax = initFigAxis()
    y_total = np.zeros(len(x))
    for y, c, n in y_zip:
        ax.bar(x, y, color=c, edgecolor='k', label=n, bottom=y_total)
        y_total += y
    if plot_average is not None:
        _ind_i = np.where(x == plot_average[0])[0][0]
        _ind_f = np.where(x == plot_average[1])[0][0]
        x_average = x[_ind_i:_ind_f+1]
        y_average = np.ones(len(x_average)) * np.mean(y2[_ind_i:_ind_f+1])
        label_avg = 'Average demand between ' + str(x[_ind_i]) + ' and ' + str(x[_ind_f])
        ax.plot(x_average, y_average, c='k', linestyle='--', label=label_avg)
        ax.plot(x, y2, 'k', label='Annual demand', alpha=0.5)
    # else:
    #     # ax.plot(x, y2, 'k', label='Total demand')
    ax.set_xticks(x)
    ax.set_xticklabels(ax.get_xticks(), rotation=45)
    ax.set_xlabel('Manufacturing date')

    ax.set_ylabel(ylabel)

    ax.legend(loc='upper left')

    if fname is not None:
        myformat(ax)
        mysave(fig, fname)
        plt.close()

def plot_diff(x, y, ylabel, fname):
    fig, ax = initFigAxis()
    ax.bar(x, y)

    ax.set_xticks(x)
    ax.set_xticklabels(ax.get_xticks(), rotation=45)
    ax.set_xlabel('Manufacturing date')

    ax.set_ylabel(ylabel)

    # ax.legend(loc='upper left')

    if fname is not None:
        myformat(ax)
        mysave(fig, fname)
        plt.close()
