from __future__ import division
import logging
import random
from itertools import chain
import math
import json

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


#species_phylums = session.query(Taxonomy.phylum, func.count(Taxonomy.id)).group_by(Taxonomy.phylum)
#print(species_phylums.all())

cluster_phylums = session.query(Cluster.id, Taxonomy.phylum, func.count(Taxonomy.phylum)).join(Cluster.proteins).join(Genome).join(Specie).join(Specie.taxonomies).group_by(Cluster.id, Taxonomy.phylum)

phylum_annotated_clusters={}
for i,j,k in cluster_phylums.all():
    my_dict = phylum_annotated_clusters.get(i, {})
    my_dict[j] = k
    phylum_annotated_clusters[i]=my_dict
#print(cluster_phylums[:10000])

with open("cluster_by_phylum.json", "w") as f:
    json.dump(phylum_annotated_clusters, f)

