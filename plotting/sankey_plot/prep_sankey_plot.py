import argparse

import pandas as pd
import plotly.graph_objects as go

"""
This script reads a TSV file containing data for a Sankey diagram, processes the data,
and generates a Sankey diagram as a PNG file. The script uses pandas to read the data
and plotly to create the diagram.

To run the script, use the command:
python prep_sankey_plot.py -f input_file.tsv -o output_file.svg

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


def create_sankey_diagram(input_file, output_file):
    """
    This function reads the TSV file, processes the data, and creates a Sankey diagram.
    It saves the diagram as a PNG file at the specified output file path.
    """
    data = pd.read_csv(input_file, sep="\t")

    sources = data["Activity-based annotation"].tolist()
    targets = data["LeidenCluster"].tolist()
    sorted_targets = sorted(set(targets), reverse=False)
    unique_sources = list(set(sources))
    labels = unique_sources + sorted_targets
    label_index = {label: index for index, label in enumerate(labels)}
    source_indices = [label_index[source] for source in sources]
    target_indices = [label_index[target] for target in targets]
    values = [1] * len(sources)

    color_mapping = {
        "dNK": "#F28360",
        "TK": "#FFCFAF",
        "TK1": "#FFCFAF",
        "TK2": "#FFCFAF",
        "TK1a": "#FFCFAF",
        "TK1b": "#FFCFAF",
        "dCK": "#FFB883",
        "dCK2": "#FFB883",
        "dAK": "#C85152",
        "dGK": "#9E3F41",
        "LC00": "#635C5A",
        "LC02": "#8F8885",
        "LC03": "#B9AFA7",
        "LC05": "#DBD1C3",
        "LC06": "#EDE6DA",
        "LC07": "#FFFFFF",
    }
    colors = [color_mapping.get(label, "rgba(127, 127, 127, 0.8)") for label in labels]

    fig = go.Figure(
        data=[
            go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=labels,
                    color=colors,
                ),
                link=dict(source=source_indices, target=target_indices, value=values),
            )
        ]
    )
    fig.update_layout(
        title_text="Sankey Diagram",
        font=dict(family="Suisse Int'l Regular", size=15),
        width=1000,
        height=800,
    )

    fig.write_image(output_file, scale=10)


def main():
    args = parse_args()
    create_sankey_diagram(args.input_file, args.output_file)


if __name__ == "__main__":
    main()
