from sqlalchemy import Table, Column, Integer, ForeignKey, String, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
Base=declarative_base()

specie_taxonomy_table=Table(
    'specie_taxonomy', 
    Base.metadata,
    Column("specie_id", Integer, ForeignKey("species.id")),
    Column("taxonomy_id", Integer, ForeignKey("taxonomies.id"))
)

class Specie(Base):
    __tablename__ = "species"
    id = Column(Integer,primary_key=True)
    name = Column(String)
    current_name = Column(String)
    taxon=Column(String)
    
    genomes = relationship("Genome", back_populates='specie')
    taxonomies = relationship(
        "Taxonomy", 
        secondary=specie_taxonomy_table, 
        back_populates='species'
    )

class Taxonomy(Base):
    __tablename__ = "taxonomies"
    id = Column(Integer,primary_key=True, autoincrement=False, index=True)
    
    species = relationship(
        "Specie", 
        secondary=specie_taxonomy_table,
        back_populates="taxonomies"
    )

    no_rank=Column(String)
    varietas=Column(String)
    db_species=Column(String)
    genus=Column(String)
    family=Column(String)
    order=Column(String)
    t_class=Column(String)
    phylum=Column(String, index=True)

    
class Genome(Base):
    __tablename__ = "genomes"
    id = Column(Integer,primary_key=True)
    genome_name = Column(String)
    specie_id=Column(Integer, ForeignKey('species.id'))
    specie = relationship("Specie", back_populates='genomes')
    proteins = relationship("Protein", back_populates='genome')

cluster_protein_table=Table(
    'cluster_protein', 
    Base.metadata,
    Column("protein_id", Integer, ForeignKey("proteins.id"), index=True),
    Column("cluster_id", Integer, ForeignKey("clusters.id"), index=True)
)


class Protein(Base):
    __tablename__= "proteins"
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String, index=True)
    gene_name = Column(String)
    aminoacid_sequence = Column(Text)
    functional_annotations=relationship("FunctionalAnnotation")

    genome_id=Column(Integer, ForeignKey('genomes.id'), index=True)
    genome = relationship("Genome", back_populates='proteins')


class FunctionalAnnotation(Base):
    __tablename__="functional_annotations"
    id=Column(Integer, primary_key=True)
    go_term=Column(String)
    signalp=Column(String)
    tmhmm=Column(String)
    pfam=Column(String)
    KEGG=Column(String)
    KOG=Column(String)
    protein_id=Column(Integer, ForeignKey("proteins.id"))

class Cluster(Base):
    __tablename__="clusters"
    id=Column(Integer, primary_key=True, index=True)
    name=Column(String)
    proteins=relationship("Protein", secondary=cluster_protein_table, backref="clusters", cascade_backrefs=False)
    clustering_inflation_value=Column(Float)


# Can be used to get or create a model.
def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance
