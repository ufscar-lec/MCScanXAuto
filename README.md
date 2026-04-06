# USAGE GUIDE

1- Preparing the Input Files

For each species, place the following three files inside the `input_files` directory.

Use a consistent identifier for your species by replacing `(species)` with a valid string identifier for your species (e.g., `gallusgallus` as an identifier for *Gallus gallus*):
	
	(species)_cds_from_genomic.fna
	(species)_genomic.gff
	(species)_protein.faa

2- Run the Script

Execute the script with:

	python McScanXAuto.py

3- Check the Results

All output files will be generated in the `output_files` directory.

!! IMPORTANT: THIS SCRIPT IS ONLY COMPATIBLE WITH LINUX SYSTEMS !!
