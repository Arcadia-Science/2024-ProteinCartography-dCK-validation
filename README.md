# 2024-ProteinCartography-dCK-validation

[![run with conda](http://img.shields.io/badge/run%20with-conda-3EB049?labelColor=000000&logo=anaconda)](https://docs.conda.io/projects/miniconda/en/latest/)

## Purpose

This repo accompanies the pub on ProteinCartography validation using the dCK protein family (DOI: https://doi.org/10.57844/arcadia-a757-3651)

The analyses include Leiden Cluster subclustering to identify representative proteins for biochemicaly validation in the lab. These scripts are under the `subclustering` folder. 

There are also additional scripts included that were used to prepare the figures in the publication. These scripts are under the `plotting` folder

## Installation and Setup

This repository uses conda to manage software environments and installations. You can find operating system-specific instructions for installing miniconda [here](https://docs.conda.io/projects/miniconda/en/latest/). After installing conda and [mamba](https://mamba.readthedocs.io/en/latest/), run the following command to create the pipeline run environment.

```{bash}
mamba env create -n PC_validation --file envs/dev.yml
conda activate PC_validation
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

The scripts could be run with the included data files under each of the analysis folders. These can be found under the `subclustering` folder. The plots can also be produced using the provided data files for each type of plot under the `plotting` folder. 

We have all of our data that was part of this pub on Zenodo here - LINK TO ZENODO DATABASE

## Overview

### Description of the folder structure

There are two main folders with scripts and input files. The `subclustering` folder which contains the scripts for our analysis to choose representative proteins from each Leiden Cluster. And there is the `plotting` folder that contains the scripts we used to prepare any plots and graphs.

### Methods

The scripts in the repo are relatively easy to use with sufficient level of comments. 

There are three sets of scripts in the `subclustering` folder. 

Under each of the `centroid`, `kmeans`, and `foldseek` folders are the scripts used to run each subclustering method. For the K-Means and the Foldseek subclustering methods, there are two separate scripts that use slightly different methodologies to subcluster and select representative proteins. For example, we have one script that uses Euclidean distances and a second script that uses arithmetic mean distances to perform the K-Means analysis. Similarly, we have one script that uses the 3Di alphabet and a second script that uses the typical amino acid letters to perform the Foldseek analysis. Each of these scripts is provided under appropriately named folders.

Under the `kmeans` folder, there is also the `elbow_method` folder that has the `run_elbow_method.py` script. We used this script to determine the number of optimal k-clusters for running the K-Means clustering algorithm. There is also an additional script called `prep_submatrices.py` that helps prepare the input file for the elbow method script.

In addition to the scripts, there are the input files that we used for each analysis. This includes the elbow method, as well as each of our subclusering approaches. These files are in the `input_files` folder. Please check out the accompanying pub for more details about the scripts and their outputs.

Lastly, there are three sets of scripts in the `plotting` folder. 

Under `heatmap` is the script we used to prepare an enzyme activity heatmap plot that is shown in Figure 1 of our pub. The `sankey_plot` folder contains the script we used to prepare the Sankey plot that is also shown in Figure 1. And in the `FPLC` folder is the script that we used to generate the FPLC traces shown in Figures 2 and 3 of the pub. Each of these folders also contain the corresponding input `TSV` files that were used to run the scripts and produce the plots.

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
