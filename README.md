# MCScanXAuto

## Usage Guide

1- Install NCBI BLAST+

This script requires NCBI BLAST+ to be installed. Here are some ways you can install it based on your Linux distribution:

For Ubuntu-based distributions
    sudo apt install ncbi-blast+

For Arch-based distributions
    yay -S blast+-bin


2- Preparing the Input Files

For each species, place the following three files inside the `input_files` directory.

Use a consistent identifier for your species by replacing `(species)` with a valid string identifier for your species (e.g., `gallusgallus` as an identifier for *Gallus gallus*):
	
	(species)_cds_from_genomic.fna
	(species)_genomic.gff
	(species)_protein.faa


3- Run the Script

Execute the script with:

	python McScanXAuto.py


4- Check the Results

All output files will be generated in the `output_files` directory.


**!! IMPORTANT: THIS SCRIPT IS ONLY COMPATIBLE WITH LINUX SYSTEMS !!**
