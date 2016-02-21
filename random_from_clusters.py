import logging
import random
from itertools import chain


logging.basicConfig(level=logging.DEBUG)
logging.getLogger('secretome.database_operations').setLevel(logging.INFO)
logging.getLogger('sqlalchemy.engine.base').setLevel(logging.ERROR)

from sqlalchemy.sql.expression import func, select
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, load_only, Load


from db_structure import Base, Specie, Taxonomy, Genome, Protein, get_or_create, Cluster
 
# Create the engine.
engine = create_engine('postgresql://secretome:secretome@localhost/fun395')

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()


# 1) how much of the protein families have been sampled in this dataset. Randomly select 10, 20, 40, 80, 160 taxa X times


ids=session.query(Specie.id)
#for sp_id in ids:
#    print sp_id


# Cluster where cluster__protein in genome in species.

random_sample=session.query(Specie).order_by(func.random()).limit(10)
for sp in random_sample:
    
    n_query = session.query(func.count(Cluster.id), func.count(Cluster.proteins)). \
        join(Protein, Cluster.proteins).join(Genome) .\
        filter(Genome.specie == sp)

    print(n_query)

    print("{0}: {1}".format(sp.name, n_query.all()))


n_cluster = session.query(func.count(Cluster.protein)).first()
print(n_cluster)


#random_species=select([Specie.name]).func.random().limit(10)

#for species in random_species:
#    print species.name


Ascomycete_one=session.query(Specie).filter(Specie.taxonomies.any(phylum="Ascomycota")).first()
#print Ascomycete_one.id

#Ascomycetes=session.query(Specie).filter(Specie.taxonomies.any(phylum="Ascomycota"))
#for species in Ascomycetes.all():
#    print species.name
#print(Ascomycetes.column_descriptions)

#Ascomycetes=select([Specie.name]).where(Specie.taxonomies.any(phylum="Ascomycota"))






#print(Ascomycetes.items())
#results=Ascomycetes.execute()

#for row in results:
#    print row 

#print(Ascomycetes.species_name())
#print(gene_families.count())

# 2) genes distributed in 10% of taxa and all over the kingdom
# which clusters contain taxa from > 1 Class + not all in any class.



      # 3) shape of gene family sizes
# print len(clusters) to table, then plot


#species = session.query(Specie).filter(Specie.taxonomies.any(phylum='Ascomycota')).all()

#genomes = [g for g in chain(*[s.genomes for s in species])]



#proteins = session.query(Protein).join(Genome).join(Specie). \
#    filter(Specie.taxonomies.any(phylum='Ascomycota')). \
#    filter(Protein.aminoacid_sequence.op('~')('L.FLAK'))


#print(proteins.count())

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
