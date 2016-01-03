from flask.ext.wtf import Form
from wtforms import StringField, SelectField
import sqlite3

SCHOOL_DB = 'schools.db'
ENERGY_DB = 'energy.db'

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


def get_energy(table_name):
    conn = sqlite3.connect(ENERGY_DB)
    cursor = conn.cursor()

    query = """
        SELECT code, name
        FROM {}
        ORDER BY name
    """.format(table_name)

    cursor.execute(query)
    return cursor.fetchall()


# Country form
COUNTRY_CHOICES = get_energy('country')
COUNTRY_LOOKUP = {k: v for k, v in COUNTRY_CHOICES}

COUNTRY_METRIC_CHOICES = [
    ('INTL.44-8-{}-MMTCD.A', 'CO2 Emissions'),
    ('INTL.44-1-{}-QBTU.A', 'Energy Production'),
    ('INTL.44-2-{}-QBTU.A', 'Energy Consumption'),
    ('INTL.44-33-{}-MM.A', 'Population'),
    ('INTL.45-2-{}-MBTUPP.A', 'Energy Consumption per capita'),
    ('INTL.45-8-{}-MTCDPP.A', 'CO2 Emissions per capita')
]
COUNTRY_METRIC_LOOKUP = {k: v for k, v in COUNTRY_METRIC_CHOICES}


class WorldEnergyForm(Form):
    metric = SelectField('Metric', choices=COUNTRY_METRIC_CHOICES)
    country = SelectField('Country', choices=COUNTRY_CHOICES)


# State form
STATE_CHOICES = get_energy('state')
STATE_LOOKUP = {k: v for k, v in STATE_CHOICES}

STATE_METRIC_CHOICES = [
    ('SEDS.TETCB.{}.A', 'Energy Consumption'),
    ('SEDS.TEPRB.{}.A', 'Energy Production'),
    ('SEDS.TETCD.{}.A', 'Price'),
    ('SEDS.TETCV.{}.A', 'Expenditure'),
    ('SEDS.TPOPP.{}.A', 'Population'),
    ('SEDS.GDPRX.{}.A', 'Real GDP'),
    ('SEDS.GDPRV.{}.A', 'Current Dollar GDP'),
]
STATE_METRIC_LOOKUP = {k: v for k, v in STATE_METRIC_CHOICES}


class StateEnergyForm(Form):
    metric = SelectField('Metric', choices=STATE_METRIC_CHOICES)
    state = SelectField('State', choices=STATE_CHOICES)


