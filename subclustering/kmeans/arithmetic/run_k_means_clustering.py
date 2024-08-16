import argparse

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

"""
This script processes a TM-score matrix file and a Leiden cluster
data file to perform k-means clustering directly on matrix rows. The
script groups proteins based on Leiden clusters, calculates the centroid,
and finds the closest, farthest above, and farthest below proteins to
the centroid for each k-means cluster.

The output consists of two TSV files:
1. A file displaying centroids and representative proteins for each centroid.
2. A file organizing the proteins in each k-means cluster under their respective
   Leiden clusters and k-means clusters.

Usage:
python run_k_means_clustering.py \
--matrix-tsv /path/to/matrix.tsv \
--cluster-tsv /path/to/leiden/clusters.tsv \
--output-file1 /path/to/output/showing/centroids/and/representative/proteins/file.tsv \
--output-file2 /path/to/output/showing/the/proteins/in/each/kmeans/cluster/file.tsv

The first draft of this script was prepared with chatGPT.
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
        "--output-file1",
        required=True,
        help="Path to the output TSV file showing centroids and representative proteins."
    )
    parser.add_argument(
        "-e",
        "--output-file2",
        required=True,
        help="Path to the output TSV file showing the proteins in each kmeans cluster."
    )
    args = parser.parse_args()
    return args

def find_representatives(protein_means, centroid):
    closest_protein = min(protein_means, key=lambda x: abs(x[1] - centroid))
    farthest_above_protein = max(
        protein_means,
        key=lambda x: x[1] - centroid if x[1] > centroid else float("-inf")
    )
    farthest_below_protein = min(
        protein_means,
        key=lambda x: x[1] - centroid if x[1] < centroid else float("inf")
    )
    return closest_protein, farthest_above_protein, farthest_below_protein

def run_kmeans_clustering(matrix_tsv, cluster_tsv, output_file1, output_file2):
    df_matrix = pd.read_csv(matrix_tsv, sep="\t", index_col=0)
    df_leiden = pd.read_csv(cluster_tsv, sep="\t")

    leiden_groups = df_leiden.groupby("LeidenCluster")
    output_columns = [
        "LeidenCluster", "KMeansCluster", "Centroid", "ClosestProtein", "ClosestValue",
        "FarthestAboveProtein", "FarthestAboveValue", "FarthestBelowProtein", "FarthestBelowValue"
    ]
    output_df = pd.DataFrame(columns=output_columns)

    # Prepare headers and data storage for output file 2
    headers_lc = []
    headers_kc = []
    data = []

    for leiden_cluster, group in leiden_groups:
        protein_names = group["protid"].tolist()

        protein_df = df_matrix.loc[protein_names, protein_names]
        kmeans = KMeans(n_clusters=3, random_state=0)
        kmeans.fit(protein_df)
        clusters = kmeans.labels_

        rows_to_append = []

        for i in range(3):
            cluster_data = protein_df.iloc[clusters == i, :]
            mean_calc_df = cluster_data.replace([1.0, 0.0], np.nan)

            # Filter mean_calc_df to include the relevant columns for the specific kmeans cluster
            mean_calc_df = mean_calc_df[mean_calc_df.index]

            row_means = mean_calc_df.mean(axis=1)
            cluster_centroid = row_means.mean()
            protein_means = list(zip(cluster_data.index, row_means, strict=False))

            closest, farthest_above, farthest_below = \
                find_representatives(protein_means, cluster_centroid)
            row = {
                "LeidenCluster": leiden_cluster,
                "KMeansCluster": f"KC{i}",
                "Centroid": cluster_centroid,
                "ClosestProtein": closest[0], "ClosestValue": closest[1],
                "FarthestBelowProtein": farthest_below[0], "FarthestBelowValue": farthest_below[1],
                "FarthestAboveProtein": farthest_above[0], "FarthestAboveValue": farthest_above[1]
            }
            rows_to_append.append(row)

            # Organizing headers and data for output file 2
            headers_lc.extend([leiden_cluster])
            headers_kc.extend([f"KC{i}"])
            data.append([p[0] for p in protein_means])

        if rows_to_append:
            rows_df = pd.DataFrame(rows_to_append).dropna(how="all")
            if not rows_df.empty:
                if output_df.empty:
                    output_df = rows_df
                else:
                    output_df = pd.concat([output_df, rows_df], ignore_index=True)
        output_df.to_csv(output_file1, sep="\t", index=False)

    with open(output_file2, "w") as f:
        f.write("\t".join(headers_lc) + "\n")
        f.write("\t".join(headers_kc) + "\n")
        max_len = max(len(d) for d in data)
        for i in range(max_len):
            row = [d[i] if i < len(d) else '' for d in data]
            f.write("\t".join(row) + "\n")

def main():
    args = parse_args()
    run_kmeans_clustering(args.matrix_tsv, args.cluster_tsv, args.output_file1, args.output_file2)

if __name__ == "__main__":
    main()
