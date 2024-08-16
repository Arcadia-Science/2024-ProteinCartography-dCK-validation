import argparse
from pathlib import Path

import numpy as np
import pandas as pd

"""
This script calculates the centroid TM-score for given groups of proteins
based on their comparison matrix provided in a TSV file. It then identifies
the protein that is closest to this centroid TM-score, as well as
the TM-scores that are farthest below and above the centroid. The script outputs the
results to two TSV files grouped by clusters specified in an additional TSV file.

Usage:
python calculate_centroid.py \
--matrix-tsv /path/to/tm_scores/matrix/file.tsv \
--cluster-tsv /path/to/LC/labels/file.tsv \
--output-folder /path/to/output/folder/for/TSV/files/

Arguments:
-m, --matrix-tsv: Path to the input TSV file containing the TM-score matrix.
-c, --cluster-tsv: Path to the TSV file with the LC labels (columns "protid" and "LeidenCluster").
-o, --output-folder: Path to the output folder where the results will be written.
"""

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--matrix-tsv",
        required=True,
        help="Path to the TSV file containing the TM-score matrix."
    )
    parser.add_argument(
        "-c",
        "--cluster-tsv",
        required=True,
        help="Path to the TSV file containing protein clusters."
    )
    parser.add_argument(
        "-o",
        "--output-folder",
        required=True,
        help="Path to the folder for the output TSV files."
    )
    args = parser.parse_args()
    return args

def calculate_arithmetic_mean(tm_scores, protein_names):
    row_means = [np.mean(scores) if scores else np.nan for scores in tm_scores]
    centroid = np.mean(row_means)
    closest_index, closest_score = find_closest_to_centroid(row_means, centroid)
    lowest_index, lowest_score = find_lowest(row_means)
    highest_index, highest_score = find_highest(row_means)
    results = [[
        centroid,
        protein_names[closest_index],
        closest_score,
        protein_names[lowest_index],
        lowest_score,
        protein_names[highest_index],
        highest_score
    ]]
    return results

def find_closest_to_centroid(row_means, centroid):
    valid_indices = [i for i, score in enumerate(row_means) if not np.isnan(score)]
    closest_index = min(valid_indices, key=lambda i: abs(row_means[i] - centroid))
    closest_score = row_means[closest_index]
    return closest_index, closest_score

def find_lowest(row_means):
    valid_indices = [i for i, score in enumerate(row_means) if not np.isnan(score)]
    lowest_index = min(valid_indices, key=lambda i: row_means[i])
    lowest_score = row_means[lowest_index]
    return lowest_index, lowest_score

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
        clusters[cluster] = cluster_df[cluster_df["LeidenCluster"] == cluster]["protid"].tolist()
    return clusters

def write_tsv(output_folder, filename, data, columns):
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(output_folder / filename, sep="\t", index=False)

def compute_results(args):
    tm_scores_df = read_matrix(args.matrix_tsv)
    clusters = read_clusters(args.cluster_tsv)

    combined_data = []
    arithmetic_mean_data = []

    for cluster in sorted(clusters.keys()):
        proteins = clusters[cluster]
        valid_proteins = [protein for protein in proteins if protein in tm_scores_df.index]

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
        arithmetic_results = calculate_arithmetic_mean(cluster_tm_scores, valid_proteins)
        arithmetic_mean_data.extend([[cluster] + res[1:] for res in arithmetic_results])

        combined_data.append([
            cluster,
            arithmetic_results[0][0]
        ])

    output_folder = Path(args.output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    write_tsv(
        output_folder,
        "combined.tsv",
        combined_data,
        ["Cluster", "Arithmetic Mean"]
    )

    write_tsv(
        output_folder,
        "arithmetic_mean.tsv",
        arithmetic_mean_data,
        ["Cluster",
         "Closest Protein",
         "TM-score",
         "Lowest Protein",
         "TM-score",
         "Highest Protein",
         "TM-score"]
    )

def main():
    args = parse_args()
    compute_results(args)

if __name__ == "__main__":
    main()
