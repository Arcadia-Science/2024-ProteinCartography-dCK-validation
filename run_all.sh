#!/usr/bin/env bash
set -euo pipefail

# Resolve repo root regardless of where the script is called from.
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

MATRIX_TSV="$REPO_DIR/finding_representatives/input_files/all_by_all_tmscore_pivoted.tsv"
CLUSTER_TSV="$REPO_DIR/finding_representatives/input_files/leiden_features.tsv"

# ── 1. Cluster representatives ────────────────────────────────────────────────
echo "==> find_cluster_representative.py"
python "$REPO_DIR/finding_representatives/cluster_representatives/find_cluster_representative.py" \
    -m "$MATRIX_TSV" \
    -c "$CLUSTER_TSV" \
    -o "$REPO_DIR/finding_representatives/cluster_representatives/output/"

# ── 2a. Elbow method (determines optimal k per Leiden cluster) ────────────────
echo "==> run_elbow_method.py"
python "$REPO_DIR/finding_representatives/subcluster_representatives/run_elbow_method.py" \
    -m "$MATRIX_TSV" \
    -c "$CLUSTER_TSV" \
    -p "$REPO_DIR/finding_representatives/subcluster_representatives/elbow_plots/" \
    -o "$REPO_DIR/finding_representatives/subcluster_representatives/elbow_data/"

# ── 2b. K-means clustering (reads per-cluster k from elbow output) ────────────
echo "==> run_k_means_clustering.py"
mkdir -p "$REPO_DIR/finding_representatives/subcluster_representatives/output"
python "$REPO_DIR/finding_representatives/subcluster_representatives/run_k_means_clustering.py" \
    -m "$MATRIX_TSV" \
    -c "$CLUSTER_TSV" \
    -k "$REPO_DIR/finding_representatives/subcluster_representatives/elbow_data/" \
    -o "$REPO_DIR/finding_representatives/subcluster_representatives/output/representatives.tsv" \
    -e "$REPO_DIR/finding_representatives/subcluster_representatives/output/kclusters.tsv"

# ── 3. FPLC traces ────────────────────────────────────────────────────────────
FPLC_DIR="$REPO_DIR/plotting/FPLC"
FPLC_OUT="$FPLC_DIR/output"
mkdir -p "$FPLC_OUT"

echo "==> prep_trace_graph.py (FPLC traces)"
python "$FPLC_DIR/prep_trace_graph.py" \
    -f "$FPLC_DIR/Standards/SEC_standards.tsv" \
    -o "$FPLC_OUT/SEC_standards.svg"
python "$FPLC_DIR/prep_trace_graph.py" \
    -f "$FPLC_DIR/human_dCK_P27707/P27707_SEC.tsv" \
    -o "$FPLC_OUT/P27707_SEC.svg"
python "$FPLC_DIR/prep_trace_graph.py" \
    -f "$FPLC_DIR/Antarctic_cod_A0A7J5YK87/A0A7J5YK87_SEC.tsv" \
    -o "$FPLC_OUT/A0A7J5YK87_SEC.svg"
python "$FPLC_DIR/prep_trace_graph.py" \
    -f "$FPLC_DIR/Almond_A0A4Y1QVV5/A0A4Y1QVV5_SEC.tsv" \
    -o "$FPLC_OUT/A0A4Y1QVV5_SEC.svg"
python "$FPLC_DIR/prep_trace_graph.py" \
    -f "$FPLC_DIR/Field_mustard_A0A3P6ASY1/A0A3P6ASY1_SEC.tsv" \
    -o "$FPLC_OUT/A0A3P6ASY1_SEC.svg"
python "$FPLC_DIR/prep_trace_graph.py" \
    -f "$FPLC_DIR/Rickettsiales_A0A2A5BCG8/A0A2A5BCG8_SEC.tsv" \
    -o "$FPLC_OUT/A0A2A5BCG8_SEC.svg"

# ── 4. Heatmap ────────────────────────────────────────────────────────────────
echo "==> prep_heatmap.py"
mkdir -p "$REPO_DIR/plotting/heatmap/output"
python "$REPO_DIR/plotting/heatmap/prep_heatmap.py" \
    -f "$REPO_DIR/plotting/heatmap/dNKs_activities.tsv" \
    -o "$REPO_DIR/plotting/heatmap/output/heatmap.svg"

# ── 5. Sankey plot ────────────────────────────────────────────────────────────
echo "==> prep_sankey_plot.py"
mkdir -p "$REPO_DIR/plotting/sankey_plot/output"
python "$REPO_DIR/plotting/sankey_plot/prep_sankey_plot.py" \
    -f "$REPO_DIR/plotting/sankey_plot/sankey_data.tsv" \
    -o "$REPO_DIR/plotting/sankey_plot/output/sankey_plot.svg"

echo ""
echo "Done. Outputs:"
echo "  finding_representatives/cluster_representatives/output/"
echo "  finding_representatives/subcluster_representatives/elbow_plots/"
echo "  finding_representatives/subcluster_representatives/elbow_data/"
echo "  finding_representatives/subcluster_representatives/output/"
echo "  plotting/FPLC/output/"
echo "  plotting/heatmap/output/"
echo "  plotting/sankey_plot/output/"
