import argparse
import os
import shutil
import subprocess

"""
This script processes a directory containing subdirectories, 
each with multiple PDB files using Foldseek. This script runs
Foldseek using the 3Di alphabet. The user needs to specify 
the input directory containing the subdirectories, and the 
output directory.

Note1: make sure to use the absolute paths when specifying the 
folder paths in the command below! The script will not work
if the relative folder paths are used instead of the absolute
folder paths!

Note2: Foldseek will not run if, in the input folder, there are 
output files that it has produced in a previous run. These are
the .fasta, .tsv files, and the tmp folder. If you wish
to re-run Foldseek multiple times on the same input folder, make
sure to delete the Foldseek output files/folder between each run.

To run the script, use the following command: 
python run_foldseek_clustering.py \
--input-folder /path/to/directory/with/PDBs/organized/in/subfolders/ \
--output-folder /path/to/directory/for/subfolders/with/clustered/PDBs/

The script was prepared with the assistance of ChatGPT.
"""

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--input-folder",
        required=True,
        help="Path to input folder containing subdirectories with PDB files.",
    )
    parser.add_argument(
        "-o",
        "--output-folder",
        required=True,
        help="Path to output folder for processed PDB files.",
    )
    args = parser.parse_args()
    return args

def run_foldseek(input_folder):
    """
    Changes the working directory to the specified input 
    folder and runs Foldseek. The function uses the subprocess 
    module to run the Foldseek command with specified parameters.
    It waits for the Foldseek process to complete before returning.
    """
    os.chdir(input_folder)
    command = "foldseek easy-cluster . res tmp -c 0.1"
    subprocess.run(command, shell=True, check=True)

def process_res_file(input_folder, output_folder):
    """
    Processes the "res_rep_seq.fasta" file to move selected PDB
    files to the output directory. The function reads the "res_rep_seq.fasta" 
    file line by line, and for each line that starts with ">", 
    it extracts the string between ">" and ".pdb", finds the 
    corresponding PDB file in the input folder, and copies it to 
    a newly created subfolder in the output folder (which has the 
    same name as the current subfolder).
    """
    current_working_dir = os.getcwd()
    res_file_path = os.path.join(current_working_dir, "res_rep_seq.fasta")
    with open(res_file_path, "r") as file:
        for line in file:
            if line.startswith(">"):
                pdb_name = line[1:line.index(".pdb")]
                pdb_file = f"{pdb_name}.pdb"
                source_path = os.path.join(input_folder, pdb_file)
                destination_subfolder = os.path.join(output_folder, os.path.basename(input_folder))
                os.makedirs(destination_subfolder, exist_ok=True)
                destination_path = os.path.join(destination_subfolder, pdb_file)
                shutil.copy(source_path, destination_path)

def main():
    args = parse_args()
    input_folder = args.input_folder
    output_folder = args.output_folder
    
    for subfolder in os.listdir(input_folder):
        subfolder_path = os.path.join(input_folder, subfolder)
        if os.path.isdir(subfolder_path):
            run_foldseek(subfolder_path)
            process_res_file(subfolder_path, output_folder)

if __name__ == "__main__":
    main()