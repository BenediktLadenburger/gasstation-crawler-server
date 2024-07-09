import sqlite3
import os


def get(sql, arguments):
    con = sqlite3.connect(os.getenv('DATABASE_PATH'))
    cur = con.cursor()
    rows = cur.execute(sql, arguments).fetchall()
    columns = [description[0] for description in cur.description]
    return [dict(zip(columns, row)) for row in rows]
