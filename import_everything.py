import logging
import os
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('secretome.database_operations').setLevel(logging.INFO)
logging.getLogger('sqlalchemy.engine.base').setLevel(logging.ERROR)


from database_operations import (
    clear_database, 
    add_proteins,
    add_single_protein_file,
    add_species, 
    add_taxonomy,
    add_clusters
)

#print("Clearing the database")
#clear_database()
#add_species("/mnt/cluster_ramularia/endophyte/manuscript/all_genomes_species_edited2.txt")
#add_taxonomy("/mnt/cluster_ramularia/endophyte/manuscript/")

#print("Adding species and genomes")
#add_species_and_genomes()

#print("Parsing proteins")
#add_proteins("/mnt/cluster_ramularia/endophyte/orthofinder_all/all_sp", ["DK05_all_proteins_1_2.fasta"], True)

add_clusters("/mnt/cluster_ramularia/endophyte/orthofinder_all/orthofinder_results_run_symlink_dir1_395species/OrthologousGroups.txt")

#add_single_protein_file("/mnt/cluster_ramularia/endophyte/orthofinder_all/all_sp", "Alternaria_brassicicola_proteins.fasta", False)

