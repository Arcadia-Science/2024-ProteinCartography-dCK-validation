import argparse

import arcadia_pycolor as apc
import matplotlib.pyplot as plt
import pandas as pd
from kneed import KneeLocator
from sklearn.cluster import KMeans

"""
This script performs k-means clustering on a TM-score matrix using the Elbow method
to determine the optimal number of clusters. It reads the matrix from a TSV file
and plots the Elbow curve to visualize the optimal number of clusters.
The optimal number of clusters is saved to a text file.

Usage:
python run_elbow_method.py \
--matrix-tsv /path/to/matrix.tsv \
--plot-file /path/to/output/elbow_plot.png \
--output-file /path/to/output/optimal_clusters.txt \
--max-k 10

The first draft of this script was prepared with chatGPT.
"""


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--matrix-tsv",
        required=True,
        help="Path to the TSV file containing the TM-score matrix.",
    )
    parser.add_argument(
        "-p", "--plot-file", required=True, help="Path to the output PNG file for the Elbow plot."
    )
    parser.add_argument(
        "-o",
        "--output-file",
        required=True,
        help="Path to the output text file for the optimal number of clusters.",
    )
    parser.add_argument(
        "-k",
        "--max-k",
        type=int,
        default=10,
        help="Maximum number of clusters to test (default: 10).",
    )
    args = parser.parse_args()
    return args


def read_matrix_from_tsv(file_path):
    df = pd.read_csv(file_path, sep="\t", index_col=0)
    return df.values


def elbow_method(matrix, max_k, plot_file, output_file):
    distortions = []
    K = range(1, max_k + 1)

    for k in K:
        kmeans = KMeans(n_clusters=k, random_state=0)
        kmeans.fit(matrix)
        distortions.append(kmeans.inertia_)

    kneedle = KneeLocator(K, distortions, curve="convex", direction="decreasing")
    optimal_k = kneedle.elbow

    if optimal_k is None:
        optimal_k = 1

    plt.figure(figsize=(8, 6))
    plt.plot(K, distortions, "bx-")
    plt.xlabel("Number of clusters (k)")
    plt.ylabel("Distortion")
    plt.title("The Elbow Method showing the optimal k")
    plt.vlines(optimal_k, plt.ylim()[0], plt.ylim()[1], linestyles="dashed", colors="r")

    # Apply Arcadia figure formatting
    apc.mpl.style_plot()

    plt.savefig(plot_file, format="svg")

    with open(output_file, "w") as f:
        f.write(f"The optimal number of clusters is: {optimal_k}\n")

    return optimal_k


if __name__ == "__main__":
    args = parse_args()
    matrix = read_matrix_from_tsv(args.matrix_tsv)
    elbow_method(matrix, args.max_k, args.plot_file, args.output_file)
