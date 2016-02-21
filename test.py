import logging
from itertools import chain

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('secretome.database_operations').setLevel(logging.INFO)
logging.getLogger('sqlalchemy.engine.base').setLevel(logging.ERROR)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_structure import Base, Specie, Taxonomy, Genome, Protein, get_or_create, Cluster
 
# Create the engine.
engine = create_engine('postgresql://secretome:secretome@localhost/fun395')

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()

#species = session.query(Specie).filter(Specie.taxonomies.any(phylum='Ascomycota')).all()

#genomes = [g for g in chain(*[s.genomes for s in species])]

proteins = session.query(Protein).join(Genome).join(Specie). \
    filter(Specie.taxonomies.any(phylum='Ascomycota')). \
    filter(Protein.aminoacid_sequence.op('~')('L.FLAK'))


print(proteins.count())

#protein_names = [
# 'jgi|Antlo1|1000|2084', 
# 'jgi|Antlo1|1001|1076', 
# 'jgi|Antlo1|1002|2059', 
# 'jgi|Antlo1|100|2380',
# 'jgi|Antlo1|1003|2285', 
# 'jgi|Antlo1|1004|2286', 
# 'jgi|Antlo1|1005|2287', 
# 'jgi|Antlo1|1006|2045', 
# 'jgi|Antlo1|1007|2245', 
# 'jgi|Antlo1|1008|1990',
    #]

#proteins = session.query(Protein).filter(Protein.name.in_(protein_names))

#print(proteins.count())

#protein_data = session.query(Protein.id, Protein.name).all()

#species = session.query(Specie).filter(Specie.taxonomies.any(phylum='Ascomycota')).all()
