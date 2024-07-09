import sqlite3
import os
import error_logger


def write(gasstation_id, fuel_type_prices):
    if not gasstation_id or not fuel_type_prices:
        error_logger.log('Not able to write None values to database')
        return

    con = sqlite3.connect(os.getenv('DATABASE_PATH'))
    sql_select = '''
        SELECT price
        FROM price
        WHERE fk_gasstation = ?
        AND fk_fueltype = ?
        AND time_created = (
            SELECT MAX(time_created)
            FROM price
            WHERE fk_gasstation = ?
            AND fk_fueltype = ?
        );
    '''

    sql_insert = '''
        INSERT INTO price
            (fk_gasstation, fk_fueltype, price)
        VALUES
            (?, ?, ?)
    '''
    try:
        cur = con.cursor()
        for fueltype, price in fuel_type_prices.items():
            res = cur.execute(sql_select, (
                    gasstation_id, fueltype,
                    gasstation_id, fueltype
                )).fetchone()

            # if the price didn't change
            if str(res[0]) == str(price):
                continue
            cur.execute(sql_insert, (gasstation_id, fueltype, price))
            con.commit()
    except Exception as e:
        error_logger.log('failed to write result')
        print(e)
        con.rollback()
    finally:
        con.close()
