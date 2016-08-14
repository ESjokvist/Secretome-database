# Script for creating database structure in postgres
import contextlib
import os
import logging
import json
from settings import DATABASE_URL

logger = logging.getLogger('secretome.database_operations')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, load_only

from db_structure import Base, Specie, Taxonomy, Genome, Protein, get_or_create, Cluster, cluster_protein_table
 
# Create the engine.
engine = create_engine(DATABASE_URL)

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()

# Util functions
def find_gene_name(line):
    for item in line.split():
        if item.startswith("gene"):
            return item.split(":")[1]


# Add genomes and species names
def add_species_and_genomes():
    with open("list_of_used_proteomes_ensemble.txt") as ensembl_genomes:
        for row in ensembl_genomes:
            specie = get_or_create(session, Specie, name=row.split(".")[0])
            genome = get_or_create(session, Genome, genome_name=row)
            genome.specie = specie
            session.add(genome)
    session.commit()

def add_proteins(path_to_proteinfolder, exclude_list=[], skip_existing=False):
    files = [
        f for f in os.listdir(path_to_proteinfolder) 
        if os.path.isfile(os.path.join(path_to_proteinfolder, f)) and
        f not in exclude_list
        and session.query(Genome).filter_by(genome_name=f).count()
    ]

    for file in files:
        logger.info("Parsing file {}".format(file))
        genome = session.query(Genome).filter_by(genome_name=file).one()
        existing_proteins = {
            p.name: p 
            for p in session.query(Protein).filter_by(genome=genome).all()
        }
        
        file_type = file.split(".")[-1]
        
        with open(os.path.join(path_to_proteinfolder, file)) as f:
            for i, line in enumerate(f):
                try:
                    if line.startswith(">"):
                        if file_type == "fa":
                            name = line.split()[0][1:] 
                            gene_name = find_gene_name(line)
                        elif file_type == "faa":
                            name = line.split()[0][1:]
                            gene_name = ""
                        elif file == "DK05_all_proteins_1_2.fasta":
                            name = line[1:]
                            gene_name = line[1:]
                        elif file == "Alternaria_brassicicola_proteins.fasta":
                            name = line[1:].strip()
                            gene_name = line[1:].strip()
                        elif file_type == "fasta":
                            name = line[1:].split()[0]
                            gene_name = line.split("|")[2]
                    else:
                        name = name.strip()
                        gene_name = gene_name.strip()
                        aminoacid_sequence = line.strip()
                        
                        if name in existing_proteins:
                            if skip_existing:
                                continue
                            protein = existing_proteins[name]
                        else:
                            protein = Protein(name=name)
                            
                        protein.gene_name = gene_name
                        protein.aminoacid_sequence = aminoacid_sequence
                        protein.genome = genome
                        session.add(protein)
                        logger.debug("Saving protein {}".format(name))
                except Exception as e:
                    logger.error("Error during parsing at line {0}: {1}".format(i, e))
                    exit(1)

                if i % 2000 == 0:
                    logger.info("Parsed {} proteins".format(i/2))
        logger.info("Commiting.")
        session.commit()


def add_single_protein_file(path_to_proteinfolder, file, skip_existing=False):
    files = [
        f for f in os.listdir(path_to_proteinfolder) 
        if os.path.isfile(os.path.join(path_to_proteinfolder, f))
    ]

    files_to_ignore = set(files)
    files_to_ignore.remove(file)
    add_proteins(path_to_proteinfolder, files_to_ignore, skip_existing)
        

def add_taxonomy(path):
    with open(os.path.join(path,"lineages.json")) as f:
        lineages = json.load(f)
    with open(os.path.join(path,"taxon_taxid.json")) as f:
        taxid_taxon_map = json.load(f)
        taxid_taxon_map = {value: key for key, value in taxid_taxon_map.items()}
    for taxid, lineage in lineages.items():
        taxon = taxid_taxon_map[taxid]
        
        species = session.query(Specie).filter_by(taxon=taxon).all()
        if species is None or len(species) == 0:
            logger.warn("Taxon {} didn't match any species.".format(taxon))
        
        taxa = get_or_create(session, Taxonomy, id = taxid)
        taxa.species = species
        taxa.no_rank = lineage["no rank"]
        taxa.varietas= lineage["varietas"]
        taxa.db_species=lineage["species"]
    	taxa.genus=lineage["genus"]
    	taxa.family=lineage["family"]
    	taxa.order=lineage["order"]
    	taxa.t_class=lineage["order"]
    	taxa.phylum=lineage["phylum"]
        session.add(taxa)
    session.commit()


def add_species(path, SpeciesIds):
    with open(SpeciesIds) as Specieslist:
        specieslist=[line.split(": ")[1].rstrip() for line in Specieslist if line[0].isdigit()]
    with open(path) as f:
        taxon_dict = {}
        for line in f:
            columns = line.split("\t")
            if columns[0] in specieslist:
                taxon_dict[columns[0]]=[c.strip() for c in columns if c != ""]
    for genome_name, specie_info in taxon_dict.items():
        specie = get_or_create(session, Specie, name=specie_info[1])
        specie.current_name = specie_info[2]
        specie.taxon = specie_info[3]
        genome = get_or_create(session, Genome, genome_name=specie_info[0])
        genome.specie = specie
        session.add(genome)
        session.add(specie)
    session.commit()

def add_clusters(path, i_value):
    """ Function to add cluster names and respective protein  names to Cluster table in database
    
    :param path: path to file with orthofinder clusters, in txt format
    """ 
    logger.info("Loading proteins from database")
#    existing_proteins = {
#        p.name: p 
#        for p in session.query(Protein).options(load_only('name', 'id')).all()
#    }
    with open(path) as f:
        for i, line in enumerate(f):
            cluster_data = line.strip().split(" ")
            name=cluster_data[0][:-1]
            cluster = get_or_create(session, Cluster, name=name)
            # proteins = [p for p in cluster_data[1:] if p in existing_proteins]
            proteins = session.query(Protein). \
                       filter(Protein.name.in_(cluster_data[1:])). \
                       options(load_only('name', 'id')).all()

            if len(proteins) != len(cluster_data) - 1:
                #diff = set(cluster_data[1:]) - set(p.name for p in proteins)
                logger.warn("Cluster {} contains missing proteins".format(name))
                logger.warn("Cluster n={0}, database n={1}".format(
                    len(cluster_data)-1, 
                    len(proteins)
                ))
                #logger.debug("Protein diff: {}".format(diff))
            
            cluster.proteins = proteins
            cluster.clustering_inflation_value=i_value
            session.add(cluster)
            
            if (i < 100 and i % 10 == 0) or i % 1000 == 0:
                logger.info("parsed {}, committing".format(i))
                session.commit()
        
        session.commit()

def clear_database():
    with contextlib.closing(engine.connect()) as con:
        trans = con.begin()
        for table in reversed(Base.metadata.sorted_tables):
            con.execute(table.delete())
        trans.commit()
