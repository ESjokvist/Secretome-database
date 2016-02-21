from sqlalchemy import create_engine
import contextlib

# Create the engine.
engine = create_engine('postgresql://secretome:secretome@localhost/fun395')

from db_structure import Base
meta = Base.metadata

with contextlib.closing(engine.connect()) as con:
    trans = con.begin()
    for table in reversed(meta.sorted_tables):
        con.execute(table.delete())
    trans.commit()



