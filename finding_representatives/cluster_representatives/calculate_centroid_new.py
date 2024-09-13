import argparse
from pathlib import Path

import numpy as np
import pandas as pd

"""
This script identifies representative proteins for each cluster by 
finding the protein that has the highest TM-score average in each cluster,
or the protein in the cluster that is the most similar to all other proteins.
The cluster labels are in the leiden_features.tsv file, which is an output
of ProteinCartography. The similarity matrix is also an output file of
ProteinCartography called all_by_all_tmscore_pivoted.tsv. Both of these
input files for this analysis are provided in this repository under the
/subclustering/input_files/ folder.

Usage:
cd subclustering/centroid/
python calculate_centroid.py \
--matrix-tsv ../input_files/all_by_all_tmscore_pivoted.tsv \
--cluster-tsv ../input_files/leiden_features.tsv \
--output-folder data_folder/

The first draft of this script was prepared with chatGPT.
"""


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--matrix-tsv",
        required=True,
        help="Path to the TSV file containing the comparison matrix.",
    )
    parser.add_argument(
        "-c",
        "--cluster-tsv",
        required=True,
        help="Path to the TSV file containing the cluster labels.",
    )
    parser.add_argument(
        "-o",
        "--output-folder",
        required=True,
        help="Path to the folder for the output TSV files.",
    )
    args = parser.parse_args()
    return args


def calculate_arithmetic_mean(tm_scores, protein_names):
    row_means = [np.mean(scores) if scores else np.nan for scores in tm_scores]
    highest_index, highest_score = find_highest(row_means)
    results = [
        [
            protein_names[highest_index],
            highest_score,
        ]
    ]
    return results


def find_highest(row_means):
    valid_indices = [i for i, score in enumerate(row_means) if not np.isnan(score)]
    highest_index = max(valid_indices, key=lambda i: row_means[i])
    highest_score = row_means[highest_index]
    return highest_index, highest_score


def read_matrix(matrix_tsv):
    df = pd.read_csv(matrix_tsv, sep="\t", index_col=0)
    return df


def read_clusters(cluster_tsv):
    cluster_df = pd.read_csv(cluster_tsv, sep="\t")
    clusters = {}
    for cluster in sorted(cluster_df["LeidenCluster"].unique()):
        clusters[cluster] = cluster_df[cluster_df["LeidenCluster"] == cluster][
            "protid"
        ].tolist()
    return clusters


def write_tsv(output_folder, filename, data, columns):
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(output_folder / filename, sep="\t", index=False)


def compute_results(args):
    tm_scores_df = read_matrix(args.matrix_tsv)
    clusters = read_clusters(args.cluster_tsv)

    combined_data = []
    # arithmetic_mean_data = []

    for cluster in sorted(clusters.keys()):
        proteins = clusters[cluster]
        valid_proteins = [
            protein for protein in proteins if protein in tm_scores_df.index
        ]

        # Step 1: Filter the columns based on the valid proteins
        filtered_tm_scores_df_columns = tm_scores_df[valid_proteins]

        # Step 2: Filter the rows based on the valid proteins
        filtered_tm_scores_df = filtered_tm_scores_df_columns.loc[valid_proteins]

        # Convert the DataFrame to a NumPy array for further processing
        filtered_tm_scores = filtered_tm_scores_df.values

        # Extract TM-scores for each protein in a cluster against other proteins in the same cluster
        cluster_tm_scores = []
        for idx in range(len(valid_proteins)):
            row_scores = filtered_tm_scores[idx, :]
            row_scores = row_scores[(row_scores != 1.0) & (row_scores != 0.0)].tolist()
            cluster_tm_scores.append(row_scores)

        # Calculate means without converting to a single numpy array
        arithmetic_results = calculate_arithmetic_mean(
            cluster_tm_scores, valid_proteins
        )
        highest_protein, highest_score = arithmetic_results[0]

        combined_data.append([cluster, highest_protein, highest_score])

    output_folder = Path(args.output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    write_tsv(
        output_folder,
        "cluster_representatives.tsv",
        combined_data,
        [
            "Cluster",
            "Highest Protein",
            "TM-score",
        ],
    )


def main():
    args = parse_args()
    compute_results(args)


if __name__ == "__main__":
    main()
