"""
POPULATE DATABASE
"""
import sqlite3
import requests
import ipdb

DB_FILE = 'energy.db'
ENERGY_URL = 'http://api.eia.gov/category'
API_KEY = 'E9693F9C41C748460B05C0DBEB9DACEA'


def init_tables():
    """
    :return: Initialize tables
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    query = "DROP TABLE IF EXISTS country"
    cursor.execute(query)

    query = """
        CREATE TABLE IF NOT EXISTS country (
        code TEXT PRIMARY KEY,
        name TEXT
        )
    """
    cursor.execute(query)
    conn.close()


def populate_tables():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    eneregy_query = """
        REPLACE INTO country
        (code, name) VALUES
        (:code, :name)
    """
    params = {'api_key': API_KEY,
              'category_id': 1741131}
    records = requests.get(ENERGY_URL, params=params).json()['category']['childseries']
    for record in records:
        if record['units'] != "Tera Joules":
            continue
        data = {
            'code': record['series_id'].split('-')[2],
            'name': ', '.join(record['name'].split(', ')[1:-1])
        }
        cursor.execute(eneregy_query, data)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_tables()
    populate_tables()
