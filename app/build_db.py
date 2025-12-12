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


DROP TABLE IF EXISTS clues;
CREATE TABLE clues (
    clue_id INTEGER PRIMARY KEY,
    clue_description TEXT,
    clue_name TEXT,
    clue_found INTEGER
);
INSERT INTO clues VALUES (1, "insert clue description here", "insert name of clue if needed", 0);
INSERT INTO clues VALUES (2, "insert clue description here", "insert name of clue if needed", 0);
INSERT INTO clues VALUES (3, "insert clue description here", "insert name of clue if needed", 0);
INSERT INTO clues VALUES (4, "insert clue description here", "insert name of clue if needed", 0);
""")

db.commit()
db.close()
