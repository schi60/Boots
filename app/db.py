# Sophia Chi, Emaan Asif, Jun Jie Li
# SoftDev
# P00
# Dec 2025

import sqlite3

DB_FILE="data.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False)

def select_query(query_string, parameters=()):
    c = db.cursor()
    c.execute(query_string, parameters)
    out_array = []
    column_names = c.description
    for row in c.fetchall():
        item_dict = dict()
        for col in range(len(row)):
             item_dict.update({column_names[col][0]: row[col]})
        out_array.append(item_dict)
    c.close()
    db.commit()
    return out_array
    
def insert_query(table, data):
    c = db.cursor()
    keys = ", ".join(data.keys())
    placeholders = ", ".join(["?"] * len(data))
    values = tuple(data.values())
    c.execute(f"INSERT INTO {table} ({keys}) VALUES ({placeholders})", values)
    
    # Return inserted data as dict
    output = {k: v for k, v in data.items()}
    
    c.close()
    db.commit()
    return output


def general_query(query_string, parameters=()):
    c = db.cursor()
    c.execute(query_string, parameters)
    c.close()
    db.commit()