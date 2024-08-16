import argparse
from pathlib import Path

import pandas as pd

"""
This script splits a matrix into sub-matrices based on unique cluster labels from a cluster
information file. Each sub-matrix is saved as a separate TSV file named with the cluster label
in a specified output directory.

Usage:
python prep_submatrices.py \
--matrix-file /path/to/all_by_all_tmscore_pivoted.tsv \
--cluster-file /path/to/leiden_features.tsv \
--output-dir /path/to/sub_matrices/

The first draft of this script was prepared with chatGPT.
"""

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--matrix-file",
        required=True,
        help="Path to the TSV file containing the main matrix."
    )
    parser.add_argument(
        "-c",
        "--cluster-file",
        required=True,
        help="Path to the TSV file containing the cluster information."
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        required=True,
        help="Directory where the sub-matrices will be saved."
    )
    args = parser.parse_args()
    return args

def load_tsv(file_path, index_col=None):
    return pd.read_csv(file_path, sep='\t', index_col=index_col)

def split_matrix_by_cluster(matrix_file, cluster_file, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    matrix_df = load_tsv(matrix_file, index_col=0)
    cluster_df = load_tsv(cluster_file, index_col=0)

    matrix_df.index.name = None
    matrix_df.columns.name = None

    unique_clusters = cluster_df['LeidenCluster'].unique()

    for cluster in unique_clusters:
        proteins_in_cluster = cluster_df[cluster_df['LeidenCluster'] == cluster].index
        sub_matrix = matrix_df.loc[proteins_in_cluster, proteins_in_cluster]
        sub_matrix.to_csv(output_dir / f'{cluster}.tsv', sep='\t')

if __name__ == "__main__":
    args = parse_args()
    split_matrix_by_cluster(args.matrix_file, args.cluster_file, args.output_dir)
