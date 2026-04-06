import os
import glob
import re
import shutil


# DELETA OS DIRETÓRIOS TEMPORÁRIOS DA CORRIDA PASSADA (CASO EXISTAM)

if os.path.exists("interm"):
    shutil.rmtree("interm")
    
if os.path.exists("ncbiDB"):
    shutil.rmtree("ncbiDB")
    
if os.path.exists("output_files"):
    shutil.rmtree("output_files")

os.mkdir("interm")
os.mkdir("ncbiDB")
os.mkdir("output_files")


# MKGFF3 PARA PYTHON

def mkGFF3(species):
    chrom_map = {}
    
    with open("input_files/" + species + "_genomic.gff") as opened_gff:
        for line in opened_gff:
            line = line.strip()
            if "chromosome=" not in line.lower() or "chromosome=unknown" in line.lower():
                continue
            parts = line.split("\t")
            seq_id = parts[0]
            if match := re.search(r"Name=([^;]+)", line):
                chrom = re.sub(r"\W+$", "", match.group(1))
                if seq_id in chrom_map:
                    raise ValueError(f"Duplicate sequence ID: {seq_id}")
                chrom_map[seq_id] = f"{species}{chrom}"
    
    with open("input_files/" + species + "_cds_from_genomic.fna") as opened_cds, open("interm/" + species + ".gff", "w") as out:
        for line in opened_cds:
            if not line.startswith(">") or "protein_id=" not in line:
                continue
            seq_id = line.split("_cds_", 1)[0].split("|")[-1]
            if not (prot_match := re.search(r"protein_id=([^\]]+)", line)):
                continue
            prot_id = prot_match.group(1).strip("]; ")
            if not (loc_match := re.search(r"location=([^\]]+)", line)):
                continue
            loc_str = loc_match.group(1)
            numbers = re.findall(r"\d+", loc_str)
            if not numbers:
                continue
            is_reverse = "complement" in loc_str or ">" in loc_str
            start = numbers[-1] if is_reverse else numbers[0]
            end = numbers[0] if is_reverse else numbers[-1]
            if seq_id in chrom_map:
                out.write(f"{chrom_map[seq_id]}\t{prot_id}\t{start}\t{end}\n")


# USA O MKGFF3 EM CADA ESPÉCIE E CONCATENA PARA O MASTER.GFF

species_list = [os.path.basename(i).split("_")[0] for i in glob.glob("input_files/*_genomic.gff")]

for species in species_list:
    mkGFF3(species)

os.system("cat interm/*.gff > output_files/master.gff")


# CRIA AS DATABASES

for species in species_list:
    os.system("makeblastdb -in input_files/" + species + "_protein.faa -out ncbiDB/" + species + " -dbtype prot")


# RODA O BLASTP ITERATIVAMENTE E CONCATENA PARA O MASTER.BLAST

for species1 in species_list:
    for species2 in species_list:
        if species1 == species2:
            continue
        print("-> Running BLASTP with " + species1 + " as database and " + species2 + " as query!")
        os.system("blastp -db ncbiDB/" + species1 + " -query input_files/" + species2 + "_protein.faa -evalue 1e-10 -num_alignments 5 -outfmt 6 -out interm/" + species1 + "-" + species2 + ".blast")

os.system("cat interm/*.blast > output_files/master.blast")
        

# RODA O MCSCANX

os.system("./bin/MCScanX output_files/master")
