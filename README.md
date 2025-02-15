# 2024-ProteinCartography-dCK-validation

[![run with conda](http://img.shields.io/badge/run%20with-conda-3EB049?labelColor=000000&logo=anaconda)](https://docs.conda.io/projects/miniconda/en/latest/)

## Purpose

This repo accompanies the pub on [ProteinCartography validation using the Deoxycytidine Kinase protein family](https://doi.org/10.57844/arcadia-a757-3651). ProteinCartography is a bioinformatics pipeline that groups proteins based on their predicted structures. It searches for proteins that are similar to an input structure and prepares an interactive map with the clustering information. For more information on this pipeline, check out the pub describing the capabilities of [ProteinCartography](https://doi.org/10.57844/ARCADIA-A5A6-1068) and the [ProteinCartography GitHub repo](https://github.com/Arcadia-Science/ProteinCartography/releases/tag/v0.5.0). 

In our [previous pub](https://doi.org/10.57844/arcadia-1e5d-e272) on the Deoxycytidine Kinase (dCK) protein family, we outlined a plan for using dCKs to validate the results of ProteinCartography, and we described in detail why we chose to use this family for our analysis. As part of this pub, we analyzed the resulting clusters and proposed a tentative strategy for selecting individual clusters and proteins to bring into the lab to study their biochemical function.

In the [current pub](https://doi.org/10.57844/arcadia-a757-3651) that accompanies this repo, we selected proteins from two ProteinCartography clusters to bring into the lab. Our goal is to biochemically characterize the enzymatic activity of these proteins and understand how their activity profiles correlate with the structural groupings produced by ProteinCartography. Our findings could help us better understand the relationship between protein structure and function. Additionally, we could use the results to optimize and improve the performance of ProteinCartography. 

The scripts in this pub helped us identify the proteins to bring into the lab for our empirical studies. Additionally, we have also included the scripts used to prepare the plots in the pub.

The analysis scripts include subclustering of ProteinCartography clusters to identify representative proteins for biochemical validation in the lab. These scripts are under the `finding_representatives` folder. 

There are also additional scripts included that were used to prepare the figures in the publication. These scripts are under the `plotting` folder.

## Installation and Setup

This repository uses conda to manage software environments and installations. You can find operating system-specific instructions for installing miniconda [here](https://docs.conda.io/projects/miniconda/en/latest/). After installing conda and [mamba](https://mamba.readthedocs.io/en/latest/), run the following command to create the pipeline run environment.

```{bash}
mamba env create -n dev --file envs/dev.yml
conda activate dev
```

<details><summary>Developer Notes (click to expand/collapse)</summary>

1. Install your pre-commit hooks:

    ```{bash}
    pre-commit install
    ```

    This installs the pre-commit hooks defined in your config (`./.pre-commit-config.yaml`).

2. Export your conda environment before sharing:

    As your project develops, the number of dependencies in your environment may increase. Whenever you install new dependencies (using either `pip install` or `mamba install`), you should update the environment file using the following command.

    ```{bash}
    conda env export --from-history --no-builds > envs/dev.yml
    ```

    `--from-history` only exports packages that were explicitly added by you (e.g., the packages you installed with `pip` or `mamba`) and `--no-builds` removes build specification from the exported packages to increase portability between different platforms.
</details>

## Data

The scripts in this repo can be run with the included data files under each of the analysis folders to reproduce the results. For the `finding_representatives` folder, these can be found in the `input_files` directory. These data files were generated in our ProteinCartography run and can also be found in this [Zenodo repository](https://doi.org/10.5281/zenodo.11288250).

The plots can also be produced using the provided data files for each type of plot under the `plotting` folder. The data under the `FPLC` subfolder were generated in our lab during the biochemical characterization of our selected proteins. The data under the remaining two folders, `heatmap` and `sankey_plot`, were generated through a literature search for biochemically characterized proteins in the Deoxycytidine Kinase protein family. Specifically, we extracted these data from the review article [“Non-Viral Deoxyribonucleoside Kinases – Diversity and Practical Use”](https://doi.org/10.1016/j.jgg.2015.01.003).

## Overview

### Description of the folder structure

There are two main folders with scripts and input files. The `finding_representatives` folder contains the scripts for identifying representative proteins from each ProteinCartography cluster or subcluster. The `plotting` folder contains the scripts used to prepare any plots and graphs.

The `envs` folder contains the environment packages that were used for our analyses. To be able to run the scripts, follow the instructions above to create your `conda` environment using the `dev.yml` file in this directory.

Below we have provided a directory map, the scripts and data files, as well as the commands to run each script.

## Directory Map

```
├── 2024-ProteinCartography-dCK-validation
│   ├── envs
|   ├── finding_representatives
|   |   ├── cluster_representatives
|   |   ├── input_files
|   |   └── subcluster_representatives
|   ├── plotting
|   |   ├── FPLC
|   |   ├── heatmap
|   |   └── sankey_plot

```

- **finding_representatives**
  - *cluster_representatives*
    - Script: `find_cluster_representatives.py`
    - Purpose: The scripts in this folder find the representatives from the overall ProteinCartography clusters. 
    - Usage:
      ```{bash}
      cd finding_representatives/cluster_representatives/
      python find_cluster_representatives.py -m ../input_files/all_by_all_tmscore_pivoted.tsv -c ../input_files/leiden_features.tsv -o data_folder/
      ```
  - *subcluster_representatives*
    - Scripts: `run_elbow_method.py`, `run_k_means_clustering.py`
    - Purpose: The scripts in this folder break the ProteinCartography clusters into subclusters using K-Means. First, run the `run_elbow_method.py` script to identify the number of K-Means clusters to allow. Then run the `run_k_means_clustering.py` script to perform K-Means clustering and identify representative proteins for each subcluster.
    - Usage:
      ```{bash}
      cd finding_representatives/subcluster_representatives/
      python run_elbow_method.py -m ../input_files/all_by_all_tmscore_pivoted.tsv -c ../input_files/leiden_features.tsv -p plots_folder/ -o data_folder/
      ```
      ```{bash}
      cd finding_representatives/subcluster_representatives/
      python run_k_means_clustering.py -m ../input_files/all_by_all_tmscore_pivoted.tsv -c ../input_files/leiden_features.tsv -o representatives.tsv -e kclusters.tsv
      ```
  - *input_files*
    - Purpose: Input files used by the scripts in the `finding_representatives` directory can be found here. 
      - These files are produced by the ProteinCartography pipeline and can also be found in this [Zenodo repository](https://doi.org/10.5281/zenodo.11288250).
      - They include: 
        - `all_by_all_tmscore_pivoted.tsv`
        - `leiden_features.tsv`
- **plotting**
  - *FPLC*
    - Script: `prep_trace_graph.py`
    - Purpose: This folder contains a script to create FPLC traces and all of the necessary input data. 
    - Sub-directories containing input data files generated with an FPLC instrument as part of size exclusion chromatography analyses.
      - `Standards/`
          File: `SEC_standards.tsv`
      - `human_dCK_P27707/`
        - File: `P27707_SEC.tsv`
      - `Antarctic_cod_A0A7J5YK87/`
        - File: `A0A7J5YK87_SEC.tsv`
      - `Almond_A0A4Y1QVV5/`
        - File: `A0A4Y1QVV5_SEC.tsv`
      - `Field_mustard_A0A3P6ASY1/`
        - File: `A0A3P6ASY1_SEC.tsv`
      - `Rickettsiales_A0A2A5BCG8/`
        - File: `A0A2A5BCG8_SEC.tsv`
    - Usage:
      ```{bash}
      cd plotting/FPLC/
      python prep_trace_graph.py -f Standards/SEC_standards.tsv -o plot_stadards.svg
      python prep_trace_graph.py -f human_dCK_P27707/P27707_SEC.tsv -o plot_P27707.svg
      python prep_trace_graph.py -f Antarctic_cod_A0A7J5YK87/A0A7J5YK87_SEC.tsv -o plot_A0A7J5YK87.svg
      python prep_trace_graph.py -f Almond_A0A4Y1QVV5/A0A4Y1QVV5_SEC.tsv -o plot_A0A4Y1QVV5.svg
      python prep_trace_graph.py -f Field_mustard_A0A3P6ASY1/A0A3P6ASY1_SEC.tsv -o plot_A0A3P6ASY1.svg
      python prep_trace_graph.py -f Rickettsiales_A0A2A5BCG8/A0A2A5BCG8_SEC.tsv -o plot_A0A2A5BCG8.svg
      ```
  - *heatmap*
    - Script: `prep_heatmap.py`
    - Purpose: This folder contains a script to create a heatmap as well as all of the necessary input files.
    - Input data file: `dNKs_activities.tsv`
      - Data sourced from the review article [Non-Viral Deoxyribonucleoside Kinases – Diversity and Practical Use](https://doi.org/10.1016/j.jgg.2015.01.003).
      - Represents activities of biochemically characterized enzymes in the Deoxynucleoside Kinase family.
    - Usage:
      ```{bash}
      cd plotting/heatmap/
      python prep_heatmap.py -f dNKs_activities.tsv -o heatmap.svg
      ```
  - *sankey_plot*
    - Script: `prep_sankey_plot.py`
    - Purpose: This folder contains a script to create a Sankey plot and the input data.
    - Input data file: `sankey_data.tsv`
      - Data are a combination of the enzyme activity data from the `heatmap` directory and the clustering results from our ProteinCartography analysis.
    - Usage:
      ```{bash}
      cd plotting/sankey_plot/
      python prep_sankey_plot.py -f sankey_data.tsv -o sankey_plot.svg
      ```
- **envs**
  - Purpose: This folder contains files to set up the compute environment for this analysis.
    - `dev.yml`

### Methods

To select individual proteins, we identified a single representative for each cluster. We calculated the the protein that was the most similar to all other proteins in each cluster based on the all-vs-all similarity matrix generated by ProteinCartography. To do this, we used the `find_cluster_representative.py` and both of the files in the `input_files` directory.

Following this, we subclustered the ProteinCartography clusters and selected representatives from each subcluster. To determine the optimal number of clusters, we used the Elbow method with the `run_elbow_method.py` script found in the `subcluster_representatives` folder. We then applied Scikit-Learn’s K-Means clustering algorithm using the `run_k_means_clustering.py` script. To select the representative for each subcluster, we found the protein that was the most similar to all other proteins in each subcluster as we did for the ProteinCartography clusters.

Lastly, there are three subfolders with scripts in the `plotting` folder. Under `heatmap` is the script we used to prepare an enzyme activity heatmap plot that is shown in Figure 1 of our pub. The `sankey_plot` folder contains the script we used to prepare the Sankey plot that is also shown in Figure 1. And in the `FPLC` folder is the script that we used to generate the FPLC traces shown in Figures 2 and 3 of the pub. Each of these folders also contain the corresponding input `TSV` files that were used to run the scripts and produce the plots.

Check out the [accompanying pub](https://doi.org/10.57844/arcadia-a757-3651) to learn more about our findings.

### Compute Specifications

Computer model: MacBook Pro, 13-inch, 2020, Four Thunderbolt 3 ports

Processor: 2GHz Quad-Core Intel Core i5

Graphics: Intel Iris Plus Graphics 1536 MB

Memory: 16GB 3733 MNz LPDDR4X

macOS: Sonoma 14.4.1

## Contributing

See how we recognize [feedback and contributions to our code](https://github.com/Arcadia-Science/arcadia-software-handbook/blob/main/guides-and-standards/guide-credit-for-contributions.md).

---
## For Developers

This section contains information for developers who are working off of this template. Please adjust or edit this section as appropriate when you're ready to share your repo.

### GitHub templates
This template uses GitHub templates to provide checklists when making new pull requests. These templates are stored in the [.github/](./.github/) directory.

### VSCode
This template includes recommendations to VSCode users for extensions, particularly the `ruff` linter. These recommendations are stored in `.vscode/extensions.json`. When you open the repository in VSCode, you should see a prompt to install the recommended extensions.

### `.gitignore`
This template uses a `.gitignore` file to prevent certain files from being committed to the repository.

### `pyproject.toml`
`pyproject.toml` is a configuration file to specify your project's metadata and to set the behavior of other tools such as linters, type checkers etc. You can learn more [here](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)

### Linting
This template automates linting and formatting using GitHub Actions and the `ruff` linter. When you push changes to your repository, GitHub will automatically run the linter and report any errors, blocking merges until they are resolved.
