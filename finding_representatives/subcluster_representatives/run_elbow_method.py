import argparse
from pathlib import Path

import arcadia_pycolor as apc
import matplotlib.pyplot as plt
import pandas as pd
from kneed import KneeLocator
from sklearn.cluster import KMeans

"""
This script splits a similarity matrix into sub-matrices based on cluster labels from
the ProteinCartography output file, leiden_features.tsv. The similarity matrix is also an
output file of ProteinCartography called all_by_all_tmscore_pivoted.tsv. Both of these
input files are provided in this repository under the /subclustering/input_files/ folder.

The script also passes each sub-matrix through a k-means clustering algorithm to determine the
optimal number of clusters using the Elbow method. The Elbow plot and the optimal number of
clusters for each sub-matrix are saved as output files.

Usage:
cd finding_representatives/subcluster_representatives/
python run_elbow_method.py \
--matrix-tsv ../input_files/all_by_all_tmscore_pivoted.tsv \
--cluster-tsv ../input_files/leiden_features.tsv \
--plot-folder plots_folder/ \
--output-folder data_folder/

The first draft of this script was prepared with chatGPT.
"""


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--matrix-tsv",
        required=True,
        help="Path to the TSV file containing the similarity matrix.",
    )
    parser.add_argument(
        "-c",
        "--cluster-tsv",
        required=True,
        help="Path to the TSV file containing the cluster labels.",
    )
    parser.add_argument(
        "-p",
        "--plot-folder",
        required=True,
        help="Folder where the Elbow plots will be saved.",
    )
    parser.add_argument(
        "-o",
        "--output-folder",
        required=True,
        help="Folder where text files with the optimal number of clusters will be saved.",
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


def load_tsv(file_path, index_col=None):
    return pd.read_csv(file_path, sep="\t", index_col=index_col)


def split_matrix_by_cluster(matrix_df, cluster_df):
    unique_clusters = cluster_df["LeidenCluster"].unique()
    sub_matrices = {}

    for cluster in unique_clusters:
        proteins_in_cluster = cluster_df[cluster_df["LeidenCluster"] == cluster].index
        sub_matrix = matrix_df.loc[proteins_in_cluster, proteins_in_cluster]
        sub_matrices[cluster] = sub_matrix.values

    return sub_matrices


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


def process_sub_matrices(matrix_tsv, cluster_tsv, plot_folder, output_folder, max_k):
    matrix_df = load_tsv(matrix_tsv, index_col=0)
    cluster_df = load_tsv(cluster_tsv, index_col=0)

    matrix_df.index.name = None
    matrix_df.columns.name = None

    sub_matrices = split_matrix_by_cluster(matrix_df, cluster_df)

    Path(plot_folder).mkdir(parents=True, exist_ok=True)
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    for cluster, sub_matrix in sub_matrices.items():
        plot_file = Path(plot_folder) / f"{cluster}.svg"
        output_file = Path(output_folder) / f"{cluster}.txt"
        elbow_method(sub_matrix, max_k, plot_file, output_file)


if __name__ == "__main__":
    args = parse_args()
    process_sub_matrices(
        args.matrix_tsv,
        args.cluster_tsv,
        args.plot_folder,
        args.output_folder,
        args.max_k,
    )
