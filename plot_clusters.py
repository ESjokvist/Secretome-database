import logging
import random
from itertools import chain
import matplotlib.pyplot as pyplot
import math

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

proteins_per_cluster = session.query(Cluster.id, func.count(Protein.id)).\
    join(Protein, Cluster.proteins).group_by(Cluster.id).all()

print(proteins_per_cluster[:20])

x=[i[1] for i in proteins_per_cluster]# if i[1] > 1000]

pyplot.hist(x, 100, log=True)
pyplot.axis([0, 40000, -1000, 1e6])
pyplot.show()
