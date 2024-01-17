from sqlalchemy import Integer, String, Table, Column  
from config.db import meta, engine

users = Table("users", meta, 
              Column("id", Integer, primary_key=True), 
              Column("name", String(255)), 
              Column("email", String(255)), 
              Column("password", String(255)))


# spotify_data = Table("albums", meta, 
#                     Column("id", Integer, primary_key=True), 
#                     Column("artist_id", String(255), index=True),
#                     Column("data", JSON))

meta.create_all(engine)
