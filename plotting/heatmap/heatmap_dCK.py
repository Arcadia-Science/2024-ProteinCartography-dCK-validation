import argparse

import arcadia_pycolor as apc
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib import gridspec

"""
This script reads a TSV file containing enzyme activity data, processes the data,
and generates a heatmap along with secondary labels. The script uses pandas to read
the data and seaborn to create the heatmap.

To run the script, use the command:
python heatmap_dCK.py -f input_file -o output_file.

The first draft of this script was prepared with ChatGPT.
"""

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--input-file",
        required=True,
        help="Path to input file.",
    )
    parser.add_argument(
        "-o",
        "--output-file",
        required=True,
        help="Path to output TSV file.",
    )
    args = parser.parse_args()
    return args

def create_heatmap(input_file, output_file):
    """
    This function reads the TSV file, processes the data, and creates a heatmap
    with secondary labels. It saves the heatmap as an SVG file at the specified
    output file path.
    """
    # Load the data from a TSV file
    data = pd.read_csv(input_file, sep='\t', encoding='utf-8')

    # Extract labels and data values
    secondary_labels = data.iloc[:, 1]
    primary_labels = data.iloc[:, 2]
    data_values = data.iloc[:, 3:]

    # Convert data to numeric type (float), if necessary
    data_values = data_values.apply(pd.to_numeric, errors='coerce')

    # Invert the data by subtracting each value from 100
    inverted_data_values = 100 - data_values

    # Create the figure and set up the layout
    fig = plt.figure(figsize=(12, 8))
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 5])

    # Create axes
    ax0 = fig.add_subplot(gs[0])
    ax1 = fig.add_subplot(gs[1])

    # Plotting the secondary labels
    ax0.axis('off')
    font_style = {'fontstyle': "italic", 'fontname': "Suisse Int'l"}
    for i, label in enumerate(secondary_labels):
        ax0.text(
            0.5,
            (len(secondary_labels) - i - 0.5) / len(secondary_labels),
            label,
            ha='right',
            va='center',
            fontdict=font_style
        )

    # Generate the heatmap
    heatmap = sns.heatmap(
        inverted_data_values,
        annot=False,
        fmt=".1f",
        cmap=apc.gradients.reds.to_mpl_cmap(),
        cbar_kws={'label': 'Normalized enzyme activity'},
        vmin=0,
        vmax=100,
        linewidths=1,
        linecolor='white',
        ax=ax1
    )
    heatmap.set_yticklabels(primary_labels, rotation=0)
    heatmap.set_xticklabels(heatmap.get_xticklabels(), rotation=45)
    heatmap.tick_params(axis='both', which='both', length=0)

    # Access and modify the color bar
    cbar = heatmap.collections[0].colorbar

    # Invert the color bar ticks and labels
    cbar.set_ticks([0, 20, 40, 60, 80, 100])
    cbar.set_ticklabels([100, 80, 60, 40, 20, 0])
    cbar.ax.tick_params(length=0)

    # Adjust subplot parameters
    plt.subplots_adjust(left=0.193, right=0.33, bottom=0.11, top=0.88, wspace=0.998, hspace=0.2)

    # Apply Arcadia figure formatting
    apc.mpl.setup()
    apc.mpl.style_plot(colorbar_exists=True)

    # Save the plot as an SVG file
    plt.savefig(output_file, format='svg')

def main():
    args = parse_args()
    create_heatmap(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
