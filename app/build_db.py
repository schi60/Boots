import sqlite3

DB_FILE = "data.db"

def create_tbs():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    tb_names = ["USER", "API_CACHE"]
    for tb in tb_names:
        c.execute(f"DROP TABLE IF EXISTS {tb}")

    c.execute(f"CREATE TABLE USER(user_id TEXT PRIMARY KEY, password TEXT)")
    c.execute(f"CREATE TABLE API_CACHE(id TEXT PRIMARY KEY, user_id TEXT, name TEXT, path TEXT)")
    db.commit()
    db.close()

if __name__ == "__main__":
    create_tbs()
    print("Database created successfully.")
