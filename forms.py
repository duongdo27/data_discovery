from flask.ext.wtf import Form
from wtforms import StringField, SelectField
import sqlite3

SCHOOL_DB = 'schools.db'


def get_choices(field):
    conn = sqlite3.connect(SCHOOL_DB)
    cursor = conn.cursor()

    if field == 'state':
        query = """
            SELECT DISTINCT state, state
            FROM school
            ORDER BY state
        """
    elif field == 'ownership':
        query = """
            SELECT id, name
            FROM ownership
            ORDER BY id
        """
    elif field == 'operating':
        query = """
            SELECT id, name
            FROM operating
            ORDER BY id
        """
    elif field == 'region':
        query = """
            SELECT id, name
            FROM region
            ORDER BY id
        """
    else:
        raise Exception('Invalid field')
    cursor.execute(query)
    data = [('--', '--')] + cursor.fetchall()
    return data


class SchoolSearchForm(Form):
    name = StringField('School name')
    state = SelectField('State', choices=get_choices('state'))
    ownership = SelectField('Ownership', choices=get_choices('ownership'))
    operating = SelectField('Operating', choices=get_choices('operating'))
    region = SelectField('Region', choices=get_choices('region'))

