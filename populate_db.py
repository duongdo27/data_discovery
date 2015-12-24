"""
POPULATE DATABASE
"""
import sqlite3
import requests
import ipdb

DB_FILE = 'countries.db'
ALL_COUNTRIES_URL = 'https://restcountries.eu/rest/v1/all'


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
        alpha3Code TEXT PRIMARY KEY,
        name TEXT,
        capital TEXT,
        area REAL,
        population INTEGER,
        region TEXT,
        subregion TEXT
        )
    """
    cursor.execute(query)
    conn.close()


def populate_tables():
    """
    :return: Populate tables
    """
    countries = requests.get(ALL_COUNTRIES_URL).json()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    base_query = """
        INSERT INTO country
        (alpha3Code, name, capital, area, population, region, subregion) VALUES
        (:alpha3Code, :name, :capital, :area, :population, :region, :subregion)
    """

    for country in countries:
        try:
            cursor.execute(base_query, country)
        except Exception as e:
            print e
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_tables()
    populate_tables()
