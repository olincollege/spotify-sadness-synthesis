"""
Functions related to plotting spotify data. 
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
import data_collector


def make_levels(names):
    """
    Create levels for the graph_songs_percentile function

    Levels are essentially the y axis height of an annotation,
    we need to create the levels slightly dispersed so that
    annotations wont overlap. This function is made to be a helper
    function for graph_songs_percentile

    Args: names, a list of song names that are going to be used
    as annotations in graph_songs_percentile

    Return: levels, a list of ints, representing the yaxis height
    for the annotations
    """

    # create equal spacing of levels so song names overlap less
    levels = list(range(int(-len(names) / 2), int(len(names) / 2)))
    # add an extra level if the amount of songs is odd (because level
    # amounts were determined by diving by 2)
    if len(names) % 2 != 0:
        levels.append(10)
        print("appended")
    # spreads levels out across negative and positive side of line to avoid overlap
    for i in range(len(levels)):
        if levels[i] % 2 == 1:
            levels[i] = levels[i] * -1

    return levels


def shorten_names_for_display(names, length=20):
    """ """
    shortened = []
    for i in names:
        if len(i) > length:
            shortened.append(i[0:7] + "..." + i[len(i) - 3 : len(i)])
        else:
            shortened.append(i)

    return shortened


def graph_songs_percentile(rank, graph_title, song_length=20, x=30, y=15):

    # separate dictionary into x value and lables
    percentile = [*rank.values()]
    names = [*rank.keys()]
    short_names = shorten_names_for_display(names, song_length)
    levels = make_levels(names)

    # Create figure and plot a stem plot with the date
    fig, ax = plt.subplots(figsize=(x, y), layout="constrained")
    ax.set_title(label=graph_title, fontsize=20)

    ax.vlines(percentile, 0, levels, color="tab:red")  # The vertical stems.
    ax.plot(
        percentile, np.zeros_like(percentile), "-o", color="k", markerfacecolor="w"
    )  # Baseline and markers on it.
    colors = create_box_colors(names)

    i = 0
    # annotate lines
    for d, l, r in zip(percentile, levels, short_names):
        ax.annotate(
            r,
            xy=(d, l),
            xytext=(-3, np.sign(l) * 3),
            textcoords="offset points",
            horizontalalignment="right",
            verticalalignment="bottom" if l > 0 else "top",
            fontsize=17,
            bbox=dict(boxstyle="round,pad=0.2", fc=colors[i], alpha=0.5),
        )
        i += 1

    plt.setp(ax.get_xticklabels(), rotation=30, fontsize=17, ha="right")

    # remove y-axis and spines
    ax.yaxis.set_visible(False)
    ax.spines[["left", "top", "right"]].set_visible(False)
    plt.xlabel("Average percentile", fontsize=20)

    ax.margins(y=0.1)

    return plt.show()


def make_boxplot_songs(
    rank, graph_title, x_label="Songs", y_label="Percentiles", x=10, y=6
):
    # rank is dictionary with just the songs to rank
    "This is a whole mess, i need to edit it to take a dictionary as a parameter - Kelsey"
    names = [*rank.keys()]
    percentile = [*rank.values()]

    data = percentile

    fig, ax1 = plt.subplots(figsize=(x, y))
    fig.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)

    boxplt = ax1.boxplot(data, notch=False, sym="+", vert=True, whis=1.5)
    plt.setp(boxplt["boxes"], color="black")
    plt.setp(boxplt["whiskers"], color="black")
    plt.setp(boxplt["fliers"], color="red", marker="+")

    ax1.yaxis.grid(True, linestyle="-", which="major", color="lightgrey", alpha=0.5)

    ax1.set(
        axisbelow=True,  # Hide the grid behind plot objects
        title=graph_title,
        xlabel=x_label,
        ylabel=y_label,
    )

    # Now fill the boxes with desired colors
    box_colors = create_box_colors(names)
    num_boxes = len(data)
    medians = np.empty(num_boxes)
    for i in range(num_boxes):
        box = boxplt["boxes"][i]
        box_x = []
        box_y = []
        for j in range(5):
            box_x.append(box.get_xdata()[j])
            box_y.append(box.get_ydata()[j])
        box_coords = np.column_stack([box_x, box_y])
        # Alternate between Dark Khaki and Royal Blue
        ax1.add_patch(Polygon(box_coords, facecolor=box_colors[i]))
        # Now draw the median lines back over what we just filled in
        med = boxplt["medians"][i]
        median_x = []
        median_y = []
        for j in range(2):
            median_x.append(med.get_xdata()[j])
            median_y.append(med.get_ydata()[j])
            ax1.plot(median_x, median_y, "k")
        medians[i] = median_y[0]
        # Finally, overplot the sample averages, with horizontal alignment
        # in the center of each box

        ax1.plot(
            np.average(med.get_xdata()),
            np.average(data[i]),
            color="w",
            marker="*",
            markeredgecolor="k",
        )

    # Set the axes ranges and axes labels
    ax1.set_xlim(0.5, num_boxes + 0.5)
    top = 1
    bottom = 0
    ax1.set_ylim(bottom, top)
    ax1.set_xticklabels(np.repeat(names, 1), rotation=90, fontsize=8)

    # Due to the Y-axis scale being different across samples, it can be
    # hard to compare differences in medians across the samples. Add upper
    # X-axis tick labels with the sample medians to aid in comparison
    # (just use two decimal places of precision)
    pos = np.arange(num_boxes) + 1
    upper_labels = [str(round(s, 2)) for s in medians]
    weights = ["bold", "semibold"]
    for tick, label in zip(range(num_boxes), ax1.get_xticklabels()):
        k = tick % 2
        ax1.text(
            pos[tick],
            0.95,
            upper_labels[tick],
            transform=ax1.get_xaxis_transform(),
            horizontalalignment="center",
            size="x-small",
            weight=weights[k],
            color=box_colors[k],
        )

    plt.show()


def create_box_colors(data):
    colors = []
    (
        lh,
        btc,
        p2,
        bmamc,
        rfsncib,
        lush,
        sita,
        punisher,
        boygenius,
    ) = data_collector.get_all_albums()
    for i in data:
        if i in lh:
            colors.append("darkred")
        elif i in btc:
            colors.append("silver")
        elif i in p2:
            colors.append("yellowgreen")
        elif i in bmamc:
            colors.append("slategrey")
        elif i in rfsncib:
            colors.append("teal")
        elif i in lush:
            colors.append("darkolivegreen")
        elif i in sita:
            colors.append("paleturquoise")
        elif i in punisher:
            colors.append("mediumblue")
        elif i in boygenius:
            colors.append("dimgrey")
        else:
            colors.append("gold")
    return colors


# LEGEND EXAMPLE CODE
# fig.text(0.80, 0.08, f'{N} Random Numbers',
#          backgroundcolor=box_colors[0], color='black', weight='roman',
#          size='x-small')
# fig.text(0.80, 0.045, 'IID Bootstrap Resample',
#          backgroundcolor=box_colors[1],
#          color='white', weight='roman', size='x-small')
# fig.text(0.80, 0.015, '*', color='white', backgroundcolor='silver',
#          weight='roman', size='medium')
# fig.text(0.815, 0.013, ' Average Value', color='black', weight='roman',
#          size='x-small')
