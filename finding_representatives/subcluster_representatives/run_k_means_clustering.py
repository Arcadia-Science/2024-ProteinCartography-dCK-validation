import argparse

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

"""
This script processes a similarity matrix file and a ProteinCartography cluster file to perform
k-means clustering on each cluster. The script identifies the protein with the highest average
TM-score for each k-means cluster. The cluster labels are provided with the leiden_features.tsv
file, which is an output of ProteinCartography. The comparison matrix is also an output file of
ProteinCartography called all_by_all_tmscore_pivoted.tsv. Both of these input files are provided
in this repository under the /subclustering/input_files/ folder.

The output consists of two TSV files:
1. A file displaying the protein with the highest average TM-score for each cluster.
2. A file organizing the proteins in each k-means cluster under their respective Leiden clusters
   and k-means clusters.

Usage:
cd finding_representatives/subcluster_representatives/
python run_k_means_clustering.py \
--matrix-tsv ../input_files/all_by_all_tmscore_pivoted.tsv \
--cluster-tsv ../input_files/leiden_features.tsv \
--output-file1 representatives.tsv \
--output-file2 kclusters.tsv
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
        "--output-file1",
        required=True,
        help="Path to output TSV file with highest average TM-scores and corresponding proteins.",
    )
    parser.add_argument(
        "-e",
        "--output-file2",
        required=True,
        help="Path to the output TSV file showing the proteins in each k-means cluster.",
    )
    args = parser.parse_args()
    return args


def run_kmeans_clustering(matrix_tsv, cluster_tsv, output_file1, output_file2):
    df_matrix = pd.read_csv(matrix_tsv, sep="\t", index_col=0)
    df_leiden = pd.read_csv(cluster_tsv, sep="\t")

    leiden_groups = df_leiden.groupby("LeidenCluster")
    output_columns = [
        "LeidenCluster",
        "KMeansCluster",
        "HighestProtein",
        "HighestScore",
    ]
    output_df = pd.DataFrame(columns=output_columns)

    headers_lc = []
    headers_kc = []
    data = []

    cluster_count = 3  # Number of k-means clusters

    for leiden_cluster, group in leiden_groups:
        protein_names = group["protid"].tolist()
        protein_df = df_matrix.loc[protein_names, protein_names]
        kmeans = KMeans(n_clusters=cluster_count, random_state=0)
        kmeans.fit(protein_df)
        clusters = kmeans.labels_

        rows_to_append = []

        for i in range(cluster_count):
            cluster_data = protein_df.iloc[clusters == i, :]
            mean_calc_df = cluster_data.replace([1.0, 0.0], np.nan)
            row_means = mean_calc_df.mean(axis=1)
            highest_score = row_means.max()
            highest_protein = row_means.idxmax()

            row = {
                "LeidenCluster": leiden_cluster,
                "KMeansCluster": f"KC{i}",
                "HighestProtein": highest_protein,
                "HighestScore": highest_score,
            }
            rows_to_append.append(row)
            headers_lc.extend([leiden_cluster])
            headers_kc.extend([f"KC{i}"])
            data.append([p for p in cluster_data.index])

        output_df = pd.concat([output_df, pd.DataFrame(rows_to_append)], ignore_index=True)

    output_df.to_csv(output_file1, sep="\t", index=False)

    with open(output_file2, "w") as f:
        f.write("\t".join(headers_lc) + "\n")
        f.write("\t".join(headers_kc) + "\n")
        max_len = max(len(d) for d in data)
        for i in range(max_len):
            row = [d[i] if i < len(d) else "" for d in data]
            f.write("\t".join(row) + "\n")


def main():
    args = parse_args()
    run_kmeans_clustering(args.matrix_tsv, args.cluster_tsv, args.output_file1, args.output_file2)


if __name__ == "__main__":
    main()
