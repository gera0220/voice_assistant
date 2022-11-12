import sqlite3
import numpy as np

db = sqlite3.connect("db/test.db")
cur = db.cursor()

#features = np.load('data/features/features.npy')

#cur.executemany("""INSERT INTO audio_features VALUES(NULL, ?,
#?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
#?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#""", features)

#db.commit()

#people = np.load('data/features/people.npy')

#cur.executemany("""INSERT OR IGNORE INTO personas VALUES(?, ?)""", people)

cur.execute("""
    UPDATE personas_verdad
    SET nombre = 'Gerardo'
    WHERE id_persona = 2;
""")

db.commit()
