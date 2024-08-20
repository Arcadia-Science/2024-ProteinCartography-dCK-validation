import argparse

import arcadia_pycolor as apc
import matplotlib.pyplot as plt
import pandas as pd

"""
This script reads a TSV file containing two columns, processes the data,
and generates a simple line plot. The script uses pandas to read the data
and matplotlib to create the plot.

To run the script, use the command:
python prep_trace_graph.py -f input_file.tsv -o output_file.svg

The first draft of this script was prepared with ChatGPT.
"""


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--input-file",
        required=True,
        help="Path to input TSV file.",
    )
    parser.add_argument(
        "-o",
        "--output-file",
        required=True,
        help="Path to output SVG file.",
    )
    args = parser.parse_args()
    return args


def create_plot(input_file, output_file):
    """
    This function reads the TSV file, processes the data, and creates a simple
    line plot. It saves the plot as an SVG file at the specified output file path.
    """
    # Load the data from the TSV file
    data = pd.read_csv(input_file, sep="\t", encoding="utf-8")

    # Create a simple line plot of the data
    plt.figure()
    plt.plot(data.iloc[:, 0], data.iloc[:, 1], linestyle="-")

    # Apply x-axis and y-axis labels
    plt.xlabel("Elution volume (ml)", fontsize=15, fontname="Suisse Int'l")
    plt.ylabel("Relative absorbance units", fontsize=15, fontname="Suisse Int'l")

    # Get the current axis
    ax = plt.gca()

    # Remove the top and right spines (frame lines)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Apply Arcadia figure formatting
    apc.mpl.setup()
    apc.mpl.style_plot(monospaced_axes="both")

    # Save the plot as an SVG file
    plt.savefig(output_file, format="svg")


def main():
    args = parse_args()
    create_plot(args.input_file, args.output_file)


if __name__ == "__main__":
    main()
