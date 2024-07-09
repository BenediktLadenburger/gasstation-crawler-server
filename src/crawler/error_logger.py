import sqlite3
import os


def log(error):
    sql = '''
        INSERT INTO log (error_message) VALUES (?)
    '''
    con = sqlite3.connect(os.getenv('DATABASE_PATH'))
    con.execute(sql, (error,))
    con.commit()
    con.close()
