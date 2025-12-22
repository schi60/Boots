# Sophia Chi, Emaan Asif, Jun Jie Li
# SoftDev
# P01
# Dec 2025

import sqlite3

DB_FILE="data.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor()

c.executescript("""
DROP TABLE IF EXISTS profiles;
CREATE TABLE profiles (
    username TEXT PRIMARY KEY,
    password TEXT
);

CREATE TABLE IF NOT EXISTS clues (
    username TEXT,
    clueID TEXT,
    PRIMARY KEY (username, clueID)
);

INSERT INTO clues VALUES (1, "insert clue description here", "Recipe", 0);
INSERT INTO clues VALUES (2, "insert clue description here", "Joke", 0);
INSERT INTO clues VALUES (3, "insert clue description here", "Museum", 0);
INSERT INTO clues VALUES (4, "insert clue description here", "Movie", 0);
INSERT INTO clues VALUES (5, "insert clue description here", "Holiday", 0);
INSERT INTO clues VALUES (6, "insert clue description here", "CatOfDay", 0);
""")

db.commit()
db.close()
