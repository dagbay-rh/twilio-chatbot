import sqlite3 as sl
import sql

def db_connect():
    return sl.connect(sql.db_name)

def query_execute(conn: sl.Connection, query: str, params: tuple = []):
    with conn:
        data = conn.execute(query, params)
    return data.fetchall()