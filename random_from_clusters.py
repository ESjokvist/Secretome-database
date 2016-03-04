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


# 1) how much of the protein families have been sampled in this dataset. Randomly select 10, 20, 40, 80, 160 taxa X times


ids=session.query(Specie.id)
#for sp_id in ids:
#    print sp_id


# Cluster where cluster__protein in genome in species.

def mean(values):
    return sum(values)/len(values)

def std(values):
    m = mean(values)
    var = 1/(len(values) - 1)*sum((x-m)*(x-m) for x in values)
    return math.sqrt(var) 

def clusters_for_random_species_optimized(limit, distinct=True):
    random_sample=session.query(Specie.id).order_by(func.random()).limit(limit)
    
    cluster_ids = session.query(Cluster.id, func.count(Cluster.id)). \
    join(Cluster.proteins).join(Genome) .\
    filter(Genome.specie_id.in_(random_sample)).group_by(Cluster.id)
    if distinct:
        cluster_ids=cluster_ids.distinct()
    
    print(cluster_ids)

    return {c[0]: c[1] for c in cluster_ids.all()}


def clusters_for_random_species(limit, distinct=True):
    random_sample=session.query(Specie).order_by(func.random()).limit(limit)
    protein_families={}
    for sp in random_sample:    
        cluster_ids = session.query(Cluster.id). \
        join(Cluster.proteins).join(Genome) .\
        filter(Genome.specie == sp)
        if distinct:
            cluster_ids=cluster_ids.distinct()
        
        for cluster in cluster_ids.all():
            n = protein_families.get(cluster[0], 0)
            protein_families[cluster[0]] = n + 1 
    return protein_families

print clusters_for_random_species



gene_families_from_species=[]
for i in range(300, 400, 20):
    print("Calculating for i={}".format(i))
    values = [len(clusters_for_random_species_optimized(i)) for j in range(0,20)]
    gene_families_from_species.append({
        'mean': mean(values), 
        'std': std(values),
        'n_species': i,
        'samples': values
    })

print(gene_families_from_species)
#with open("number_of_clusters_for_random_species.json", "w") as f:
#    json.dump(gene_families_from_species, f)


