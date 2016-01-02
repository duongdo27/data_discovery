from flask.ext.wtf import Form
from wtforms import StringField, SelectField
import sqlite3

SCHOOL_DB = 'schools.db'
ENERGY_DB = 'energy.db'
METRIC_CHOICES = [
    ('INTL.44-8-{}-MMTCD.A', 'CO2 Emissions'),
    ('INTL.44-1-{}-TJ.A', 'Energy Production'),
    ('INTL.44-2-{}-TJ.A', 'Energy Consumption'),
]
METRIC_LOOKUP = {k: v for k, v in METRIC_CHOICES}


def get_school_choices(field):
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
    state = SelectField('State', choices=get_school_choices('state'))
    ownership = SelectField('Ownership', choices=get_school_choices('ownership'))
    operating = SelectField('Operating', choices=get_school_choices('operating'))
    region = SelectField('Region', choices=get_school_choices('region'))


def get_energy_countries():
    conn = sqlite3.connect(ENERGY_DB)
    cursor = conn.cursor()

    query = """
        SELECT code, name
        FROM country
        ORDER BY name
    """

    cursor.execute(query)
    return cursor.fetchall()

COUNTRY_CHOICES = get_energy_countries()
COUNTRY_LOOKUP = {k: v for k, v in COUNTRY_CHOICES}


class WorldEnergyForm(Form):
    metric = SelectField('Metric', choices=METRIC_CHOICES)
    country = SelectField('Country', choices=COUNTRY_CHOICES)

