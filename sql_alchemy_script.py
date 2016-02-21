import logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('sqlalchemy.engine.base').setLevel(logging.ERROR)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_structure import Specie, Genome, get_or_create
 
# Create the engine.
engine = create_engine('postgresql://secretome:secretome@localhost/fun395')

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()

# Add genomes and species names

def add_species_and_genomes():
    with open("list_of_used_proteomes_ensemble.txt") as ensembl_genomes:
        for row in ensembl_genomes:
            specie = get_or_create(session, Specie, name=row.split(".")[0])
            genome = get_or_create(session, Genome, genome_name=row)
            genome.specie = specie
            session.add(genome)
    session.commit()





