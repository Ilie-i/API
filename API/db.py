import sqlite3
conn = sqlite3.connect("Movies.db")
curs = conn.cursor()

# Creating the DB
curs.execute("""CREATE TABLE Movies(
    id integer PRIMARY KEY,
    title text NOT NULL,
    year integer NOT NULL,
    score float NOT NULL)
    """)

#Inserting Values into the DB
curs.execute("""INSERT INTO Movies VALUES
             (1, 'Interstellar', 2014, 8.6),
             (2, 'The Pianist', 2002, 8.5),
             (3, 'Once Upon a Time in Hollywood', 2019, 7.6),
             (4, 'Life Of Pi', 2012, 7.9)""")
conn.commit()
conn.close()

#Creating a backup for Movies.db

src = sqlite3.connect("Movies.db")
dst = sqlite3.connect("Movies backup.db")
with dst:
    src.backup(dst, pages=1)
dst.close()
src.close()
