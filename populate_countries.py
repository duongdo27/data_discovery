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

    query = "DROP TABLE IF EXISTS language"
    cursor.execute(query)

    query = """
        CREATE TABLE IF NOT EXISTS language (
        alpha3Code TEXT,
        language TEXT,
        UNIQUE (alpha3Code, language)
        )
    """
    cursor.execute(query)

    query = "DROP TABLE IF EXISTS border"
    cursor.execute(query)

    query = """
        CREATE TABLE IF NOT EXISTS border (
        alpha3Code TEXT,
        border TEXT,
        UNIQUE (alpha3Code, border)
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

    country_query = """
        REPLACE INTO country
        (alpha3Code, name, capital, area, population, region, subregion) VALUES
        (:alpha3Code, :name, :capital, :area, :population, :region, :subregion)
    """

    language_query = """
        REPLACE INTO language
        (alpha3Code, language) VALUES
        (:alpha3Code, :language)
    """

    border_query = """
        REPLACE INTO border
        (alpha3Code, border) VALUES
        (:alpha3Code, :border)
    """

    for country in countries:
        try:
            cursor.execute(country_query, country)
        except Exception as e:
            print e

        for language in country['languages']:
            try:
                cursor.execute(language_query, {'alpha3Code': country['alpha3Code'], 'language': language})
            except Exception as e:
                print e

        for border in country['borders']:
            try:
                cursor.execute(border_query, {'alpha3Code': country['alpha3Code'], 'border': border})
            except Exception as e:
                print e

    conn.commit()
    conn.close()

if __name__ == '__main__':
    #init_tables()
    populate_tables()
