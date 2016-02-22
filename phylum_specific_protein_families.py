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


species_phylums = session.query(Taxonomy.phylum, func.count(Taxonomy.id)).group_by(Taxonomy.phylum)
print(species_phylums.all())

cluster_phylums = session.query(Cluster.id, Taxonomy.phylum, func.count(Taxonomy.phylum)).join(Cluster.proteins).join(Genome).join(Specie).join(Specie.taxonomies).group_by(Cluster.id, Taxonomy.phylum)
#
print(cluster_phylums)
#
#
print(cluster_phylums.first())
