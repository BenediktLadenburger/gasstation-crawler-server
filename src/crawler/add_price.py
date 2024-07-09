import sqlite3
import os


def add_price(id, new_price):
    sql = '''
        INSERT INTO price
            (fk_gasstation, price)
        VALUES
            (?, ?);
    '''
    con = sqlite3.connect(os.getenv('DATABASE_PATH'))
    con.execute(sql, (id, new_price))
    con.commit()
    con.close()


add_price(1, 2.44)
