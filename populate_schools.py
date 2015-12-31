"""
POPULATE DATABASE
"""
import sqlite3
import requests
import ipdb

DB_FILE = 'schools.db'
ALL_SCHOOLS_URL = 'https://api.data.gov/ed/collegescorecard/v1/schools'
DATA_COLUMNS = ['id', 'school.name', 'school.city', 'school.state', 'school.school_url', 'school.ownership',
                'school.region_id', 'school.operating', '2013.student.size', '2013.cost.tuition.program_year']
API_KEY = 'LJGH3f7uhvxRQBSrKApmMO7e3TeuNmEyblQpucG8'


def init_tables():
    """
    :return: Initialize tables
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    query = "DROP TABLE IF EXISTS school"
    cursor.execute(query)

    query = """
        CREATE TABLE IF NOT EXISTS school (
        id INTEGER PRIMARY KEY,
        name TEXT,
        city TEXT,
        state TEXT,
        url TEXT,
        ownership_id INTEGER,
        region_id INTEGER,
        operating_id INTEGER,
        size INTEGER,
        cost INTEGER
        )
    """
    cursor.execute(query)

    conn.close()


def populate_tables():
    """
    :return: Populate tables
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    school_query = """
        REPLACE INTO school
        (id, name, city, state, url, ownership_id, region_id, operating_id, size, cost) VALUES
        (:id, :name, :city, :state, :url, :ownership_id, :region_id, :operating_id, :size, :cost)
    """

    for page in range(79):
        print 'Page {}'.format(page)

        params = {
            'fields': ','.join(DATA_COLUMNS),
            'api_key': API_KEY,
            'per_page': 100,
            'page': page,
        }
        schools = requests.get(ALL_SCHOOLS_URL, params=params).json()['results']

        for school in schools:
            data = {
                'id': school.get('id'),
                'name': school.get('school.name'),
                'city': school.get('school.city'),
                'state': school.get('school.state'),
                'url': school.get('school.school_url'),
                'ownership_id': school.get('school.ownership'),
                'region_id': school.get('school.region_id'),
                'operating_id': school.get('school.operating'),
                'size': school.get('2013.student.size'),
                'cost': school.get('2013.cost.tuition.program_year'),
            }
            try:
                cursor.execute(school_query, data)
            except Exception as e:
                print e

        conn.commit()
    conn.close()


def extra_tables():
    """
    :return:
    """
    extra_table('ownership', [(1, 'Public'), (2, 'Private nonprofit'), (3, 'Private for-profit')])
    extra_table('region', [(0, 'Service'), (1, 'New England'), (2, 'Mid East'),
                           (3, 'Great Lakes'), (4, 'Plains'), (5, 'South East'),
                           (6, 'South West'), (7, 'Rocky Mountains'), (8, 'Far West'), (9, 'Outlying Areas')])
    extra_table('operating', [(0, 'close'), (1, 'operating')])


def extra_table(table_name, data):
    """
    :param table_name:
    :param data:
    :return:
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    query = "DROP TABLE IF EXISTS {}".format(table_name)
    cursor.execute(query)

    query = """
        CREATE TABLE IF NOT EXISTS {} (
        id INTEGER PRIMARY KEY,
        name TEXT
        )
    """.format(table_name)
    cursor.execute(query)

    query = "REPLACE INTO {} (id, name) VALUES (:id, :name)".format(table_name)

    for id, name in data:
        try:
            cursor.execute(query, {'id': id, 'name': name})
        except Exception as e:
            print e
    conn.commit()
    conn.close()


if __name__ == '__main__':
    # init_tables()
    # populate_tables()
    extra_tables()
