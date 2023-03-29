from data_helpers import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon


def make_levels(names):
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
    names = shorten_names_for_display([*rank.keys()], song_length)

    levels = make_levels(names)

    # Create figure and plot a stem plot with the date
    fig, ax = plt.subplots(figsize=(x, y), layout="constrained")
    ax.set_title(label=graph_title, fontsize=20)

    ax.vlines(percentile, 0, levels, color="tab:red")  # The vertical stems.
    ax.plot(
        percentile, np.zeros_like(percentile), "-o", color="k", markerfacecolor="w"
    )  # Baseline and markers on it.

    # annotate lines
    for d, l, r in zip(percentile, levels, names):
        ax.annotate(
            r,
            xy=(d, l),
            xytext=(-3, np.sign(l) * 3),
            textcoords="offset points",
            horizontalalignment="right",
            verticalalignment="bottom" if l > 0 else "top",
            fontsize=12,
        )

    plt.setp(ax.get_xticklabels(), rotation=30, fontsize=15, ha="right")

    # remove y-axis and spines
    ax.yaxis.set_visible(False)
    ax.spines[["left", "top", "right"]].set_visible(False)
    plt.xlabel("Average percentile", fontsize=20)

    ax.margins(y=0.1)

    return plt.show()


def make_boxplot_songs(rank, graph_title):
    # rank is dictionary with just the songs to rank
    "This is a whole mess, i need to edit it to take a dictionary as a parameter - Kelsey"
    random_dists = [*rank.keys()]
    percentile = [*rank.values()]

    N = 500

    Lush_data = [0.34, 0.56, 0.89, 0.45, 0.28, 0.40]
    rfsncb = [0.78, 0.54, 0.23, 0.68]
    bmamc = [0.34, 0.56, 0.89, 0.45, 0.28, 0.40]
    p2 = [0.89, 0.45, 0.28, 0.40, 0.78, 0.54]
    btc = [0.76, 0.45, 0.3, 0.78, 0.54]

    # norm = np.random.normal(1, 1, N)
    # logn = np.random.lognormal(1, 1, N)
    # expo = np.random.exponential(1, N)
    # gumb = np.random.gumbel(6, 4, N)
    # tria = np.random.triangular(2, 9, 11, N)

    # Generate some random indices that we'll use to resample the original data
    # arrays. For code brevity, just use the same random indices for each array
    # bootstrap_indices = np.random.randint(0, N, N)
    # data = [
    #     norm, norm[bootstrap_indices],
    #     logn, logn[bootstrap_indices],
    #     expo, expo[bootstrap_indices],
    #     gumb, gumb[bootstrap_indices],
    #     tria, tria[bootstrap_indices],
    # ]

    data = percentile

    fig, ax1 = plt.subplots(figsize=(10, 6))
    fig.canvas.manager.set_window_title("Mitski Songs By Album and Others")
    fig.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)

    bp = ax1.boxplot(data, notch=False, sym="+", vert=True, whis=1.5)
    plt.setp(bp["boxes"], color="black")
    plt.setp(bp["whiskers"], color="black")
    plt.setp(bp["fliers"], color="red", marker="+")

    # Add a horizontal grid to the plot, but make it very light in color
    # so we can use it for reading data values but not be distracting
    ax1.yaxis.grid(True, linestyle="-", which="major", color="lightgrey", alpha=0.5)

    ax1.set(
        axisbelow=True,  # Hide the grid behind plot objects
        title="Comparison of IID Bootstrap Resampling Across Five Distributions",
        xlabel="Distribution",
        ylabel="Value",
    )

    # Now fill the boxes with desired colors
    box_colors = ["darkolivegreen", "royalblue", "slategrey", "lightgreen", "grey"]
    num_boxes = len(data)
    medians = np.empty(num_boxes)
    for i in range(num_boxes):
        box = bp["boxes"][i]
        box_x = []
        box_y = []
        for j in range(5):
            box_x.append(box.get_xdata()[j])
            box_y.append(box.get_ydata()[j])
        box_coords = np.column_stack([box_x, box_y])
        # Alternate between Dark Khaki and Royal Blue
        ax1.add_patch(Polygon(box_coords, facecolor=box_colors[i]))
        # Now draw the median lines back over what we just filled in
        med = bp["medians"][i]
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
    ax1.set_xticklabels(np.repeat(random_dists, 1), rotation=45, fontsize=8)

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

    # Finally, add a basic legend
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

    plt.show()
