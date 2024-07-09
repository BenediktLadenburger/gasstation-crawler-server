import sqlite3
import os


create_table_gasstation = """
    CREATE TABLE IF NOT EXISTS gasstation (
        id           integer primary key autoincrement,
        name         varchar(255) not null,
        url          varchar(255) not null,
        time_created default current_timestamp,
        postal_id    varchar(255),
        city         varchar(255),
        street       varchar(255),
        is_active    boolean default true
    );
"""

create_table_price = """
    CREATE TABLE IF NOT EXISTS price (
        id            integer primary key autoincrement,
        fk_gasstation integer not null,
        fk_fueltype   varchar(255) not null,
        price         real,
        time_created  default current_timestamp,

        foreign key (fk_gasstation)
            references gasstation (id),
        foreign key (fk_fueltype)
            references fueltype (name)
    );
"""

create_table_fueltype = """
    CREATE TABLE IF NOT EXISTS fueltype (
        name varchar(255) primary key
    );
"""

create_table_fuelavailability = """
    CREATE TABLE IF NOT EXISTS fuelavailability (
        fk_gasstation integer,
        fk_fueltype   varchar(255),

        primary key (fk_gasstation, fk_fueltype),

        foreign key (fk_gasstation)
            references gasstation (id),
        foreign key (fk_fueltype)
            references fueltype (name)
    );
"""

create_table_log = """
    CREATE TABLE IF NOT EXISTS log (
        id            integer primary key autoincrement,
        error_message BLOB,
        time_created  default current_timestamp
    );
"""

create_table_secret = """
    CREATE TABLE IF NOT EXISTS secret (
        id    integer primary key autoincrement,
        name  varchar(255),
        value varchar(255) not null
    );
"""

con = sqlite3.connect(os.getenv('DATABASE_PATH'))
cur = con.cursor()
try:
    cur.execute(create_table_gasstation)
    cur.execute(create_table_price)
    cur.execute(create_table_fueltype)
    cur.execute(create_table_fuelavailability)
    cur.execute(create_table_log)
    cur.execute(create_table_secret)
    con.commit()
except Exception as e:
    print(e)
    con.rollback()
