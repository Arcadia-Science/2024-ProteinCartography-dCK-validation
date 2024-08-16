import argparse

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

"""
This script processes a TM-score matrix and a Leiden cluster data file to perform k-means
clustering on the matrix rows. It groups proteins based on Leiden clusters, calculates
centroids, and identifies the closest and farthest proteins to each centroid for every
k-means cluster. The proteins are identified based on the calculated Euclidean distances
to the k-means cluster centroid.

Outputs:
1. A TSV file listing centroids and representative proteins for each centroid.
2. A TSV file categorizing proteins in each k-means cluster under their respective Leiden and
   k-means clusters.

Functions:
- find_representatives(protein_df, centroid): Finds the closest and farthest proteins
  from the centroid.
- run_kmeans_clustering(matrix_tsv, cluster_tsv, output_file1, output_file2): Performs
  k-means clustering and generates output files.

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

def find_representatives(protein_df, centroid):
    # Calculate Euclidean distances from the centroid to each protein
    distances = np.linalg.norm(protein_df.values - centroid, axis=1)
    closest_index = np.argmin(distances)
    farthest_index = np.argmax(distances)

    closest_values = protein_df.iloc[closest_index].tolist()
    farthest_values = protein_df.iloc[farthest_index].tolist()

    closest_protein = (
        protein_df.index[closest_index],
        closest_values,
        distances[closest_index]
    )
    farthest_protein = (
        protein_df.index[farthest_index],
        farthest_values,
        distances[farthest_index]
    )
    return closest_protein, farthest_protein

def run_kmeans_clustering(matrix_tsv, cluster_tsv, output_file1, output_file2):
    df_matrix = pd.read_csv(matrix_tsv, sep='\t', index_col=0)
    df_leiden = pd.read_csv(cluster_tsv, sep='\t')
    leiden_groups = df_leiden.groupby('LeidenCluster')
    output_columns = [
        'LeidenCluster', 'KMeansCluster', 'ClusterCentroid',
        'ClosestKmeans', 'ClosestKmeansValue', 'ClosestKmeansMean',
        'FarthestKmeans', 'FarthestKmeansValue', 'FarthestKmeansMean'
    ]
    output_df = pd.DataFrame(columns=output_columns)
    headers_lc = []
    headers_kc = []
    data = []

    for leiden_cluster, group in leiden_groups:
        protein_names = group['protid'].tolist()
        protein_df = df_matrix.loc[protein_names, protein_names]
        kmeans = KMeans(n_clusters=3, random_state=0)
        kmeans.fit(protein_df)
        clusters = kmeans.labels_

        for i in range(3):
            cluster_data = protein_df.iloc[clusters == i]
            filtered_data = cluster_data[cluster_data.index]
            kmeans_centroid = kmeans.cluster_centers_[i]
            closest_kmeans, farthest_kmeans = find_representatives(cluster_data, kmeans_centroid)

            closest_kmeans_formatted = ', '.join(map(str, closest_kmeans[1]))
            farthest_kmeans_formatted = ', '.join(map(str, farthest_kmeans[1]))

            row = {
                'LeidenCluster': leiden_cluster,
                'KMeansCluster': f'KC{i}',
                'ClusterCentroid': ', '.join(f"{x:.3f}" for x in kmeans_centroid),
                'ClosestKmeans': closest_kmeans[0],
                'ClosestKmeansValue': closest_kmeans_formatted,
                'ClosestKmeansMean': f"{closest_kmeans[2]:.3f}",
                'FarthestKmeans': farthest_kmeans[0],
                'FarthestKmeansValue': farthest_kmeans_formatted,
                'FarthestKmeansMean': f"{farthest_kmeans[2]:.3f}"
            }

            new_row_df = pd.DataFrame([row])
            output_df = pd.concat([output_df, new_row_df], ignore_index=True)

            # Collect data for output file 2
            headers_lc.append(leiden_cluster)
            headers_kc.append(f'KC{i}')
            data.append([p for p in filtered_data.index])

    output_df.to_csv(output_file1, sep='\t', index=False)

    with open(output_file2, 'w') as f:
        f.write('\t'.join(headers_lc) + '\n')
        f.write('\t'.join(headers_kc) + '\n')
        max_len = max(len(d) for d in data)
        for i in range(max_len):
            row = [d[i] if i < len(d) else '' for d in data]
            f.write('\t'.join(row) + '\n')

def main():
    args = parse_args()
    run_kmeans_clustering(args.matrix_tsv, args.cluster_tsv, args.output_file1, args.output_file2)

if __name__ == "__main__":
    main()
