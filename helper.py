import sqlite3
import requests
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool
from forms import COUNTRY_METRIC_LOOKUP, COUNTRY_LOOKUP, STATE_METRIC_LOOKUP, STATE_LOOKUP, ECONOMIC_METRIC_LOOKUP
from collections import OrderedDict

COUNTRY_DB = 'countries.db'
SCHOOL_DB = 'schools.db'
ENERGY_URL = 'http://api.eia.gov/series'
DATAGOV_API_KEY = 'LJGH3f7uhvxRQBSrKApmMO7e3TeuNmEyblQpucG8'
EIA_API_KEY = 'E9693F9C41C748460B05C0DBEB9DACEA'
NUTRITION_URL = 'http://api.nal.usda.gov/ndb/reports/'


class Helper(object):
    @staticmethod
    def get_country_detail(country_code):
        """
        :param country_code:
        :return:
        """
        conn = sqlite3.connect(COUNTRY_DB)
        cursor = conn.cursor()

        query = "SELECT * FROM country WHERE alpha3Code = :alpha3Code"
        cursor.execute(query, {'alpha3Code': country_code})

        result = cursor.fetchone()
        columns = [x[0] for x in cursor.description]

        if result is None:
            return
        data = {key: value for key, value in zip(columns, result)}
        data['area'] = Helper.numeric_string(data['area'])
        data['population'] = Helper.numeric_string(data['population'])

        query = "SELECT language FROM language WHERE alpha3COde = :alpha3Code"
        cursor.execute(query, {'alpha3Code': country_code})
        data['languages'] = [x[0] for x in cursor.fetchall()]

        query = """
            SELECT border.border, country.name
            FROM border
            JOIN country ON border.border = country.alpha3Code
            WHERE border.alpha3Code = :alpha3Code
        """
        cursor.execute(query, {'alpha3Code': country_code})
        data['borders'] = cursor.fetchall()

        conn.close()
        return data

    @staticmethod
    def get_all_countries():
        """
        :return:
        """
        conn = sqlite3.connect(COUNTRY_DB)
        cursor = conn.cursor()

        query = "SELECT alpha3Code, name FROM country ORDER BY name"
        cursor.execute(query)

        result = cursor.fetchall()
        conn.close()
        return result

    @staticmethod
    def get_countries_by_region(region_name):
        """
        :param region_name:
        :return:
        """
        conn = sqlite3.connect(COUNTRY_DB)
        cursor = conn.cursor()

        query = "SELECT alpha3Code, name FROM country WHERE region = :region ORDER BY name"
        cursor.execute(query, {'region': region_name})

        result = cursor.fetchall()
        conn.close()

        if len(result) == 0:
            return
        return result

    @staticmethod
    def get_country_regions():
        """
        :return:
        """
        conn = sqlite3.connect(COUNTRY_DB)
        cursor = conn.cursor()

        query = "SELECT DISTINCT region FROM country WHERE region != '' ORDER BY region"
        cursor.execute(query)

        result = cursor.fetchall()
        conn.close()

        data = [x[0] for x in result]
        return data

    @staticmethod
    def get_countries_by_language(language_name):
        """
        :param language_name:
        :return:
        """
        conn = sqlite3.connect(COUNTRY_DB)
        cursor = conn.cursor()

        query = """
            SELECT country.alpha3Code, country.name
            FROM country
            JOIN language ON country.alpha3Code = language.alpha3Code
            WHERE language.language = :language
            ORDER BY country.name
        """
        cursor.execute(query, {'language': language_name})

        result = cursor.fetchall()
        conn.close()

        if len(result) == 0:
            return
        return result

    @staticmethod
    def get_contry_languages():
        """
        :return:
        """
        conn = sqlite3.connect(COUNTRY_DB)
        cursor = conn.cursor()

        query = """
            SELECT language, count(*) AS cnt
            FROM language
            GROUP BY language
            ORDER BY cnt DESC
        """
        cursor.execute(query)

        result = cursor.fetchall()
        conn.close()

        data = [x[0] for x in result]
        return data

    @staticmethod
    def numeric_string(num):
        """
        :param num:
        :return:
        """
        raw_string = str(num)
        if '.' in raw_string:
            integer, decimal = raw_string.split('.')
        else:
            integer, decimal = raw_string, None

        offset = len(integer) % 3
        ls = [integer[i:i+3] for i in range(offset, len(integer), 3)]
        if offset > 0:
            ls = [raw_string[:offset]] + ls
        combine = ','.join(ls)
        if decimal:
            combine += "." + decimal
        return combine

    @staticmethod
    def get_country_top():
        data = {}
        conn = sqlite3.connect(COUNTRY_DB)
        cursor = conn.cursor()

        query = """
            SELECT alpha3Code, name, population
            FROM country
            ORDER by population DESC
            LIMIT 10
        """
        cursor.execute(query)
        data['top10population'] = [(alpha3Code, name, Helper.numeric_string(population))
                                   for alpha3Code, name, population in cursor.fetchall()]

        query = """
            SELECT alpha3Code, name, area
            FROM country
            ORDER by area DESC
            LIMIT 10
        """
        cursor.execute(query)
        data['top10area'] = [(alpha3Code, name, Helper.numeric_string(area))
                             for alpha3Code, name, area in cursor.fetchall()]

        query = """
            SELECT alpha3Code, name, population/area AS density
            FROM country
            ORDER by density DESC
            LIMIT 10
        """
        cursor.execute(query)
        data['top10density'] = [(alpha3Code, name, Helper.numeric_string(int(density)))
                                for alpha3Code, name, density in cursor.fetchall()]

        conn.close()
        return data

    @staticmethod
    def get_school_detail(school_id):
        conn = sqlite3.connect(SCHOOL_DB)
        cursor = conn.cursor()

        query = """
            SELECT school.name, school.city, school.state, school.url, school.size, school.cost,
            ownership.name as ownership, region.name as region, operating.name as operating
            FROM school
            JOIN ownership on school.ownership_id = ownership.id
            JOIN region on school.region_id = region.id
            JOIN operating on school.operating_id = operating.id
            Where school.id = :id
        """
        cursor.execute(query, {'id': school_id})

        result = cursor.fetchone()
        columns = [x[0] for x in cursor.description]

        if result is None:
            return
        data = {key: value for key, value in zip(columns, result)}
        data['size'] = Helper.numeric_string(data['size']) if data['size'] else None
        data['cost'] = "$" + Helper.numeric_string(data['cost']) if data['cost'] else None
        return data

    @staticmethod
    def get_school_top():
        data = {}
        conn = sqlite3.connect(SCHOOL_DB)
        cursor = conn.cursor()

        query = """
            SELECT id, name, size
            FROM school
            ORDER by size DESC
            LIMIT 10
        """
        cursor.execute(query)
        data['top10size'] = [(id, name, Helper.numeric_string(size))
                             for id, name, size in cursor.fetchall()]

        query = """
            SELECT id, name, cost
            FROM school
            ORDER by cost DESC
            LIMIT 10
        """
        cursor.execute(query)
        data['top10cost'] = [(id, name, Helper.numeric_string(cost))
                             for id, name, cost in cursor.fetchall()]

        conn.close()
        return data

    @staticmethod
    def search_schools(form):
        conn = sqlite3.connect(SCHOOL_DB)
        cursor = conn.cursor()

        query = """
            SELECT id, name
            FROM school
            WHERE name LIKE :name
        """
        if form.state.data != "--":
            query += "AND state = :state\n"
        if form.ownership.data != "--":
            query += "AND ownership_id = :ownership\n"
        if form.operating.data != "--":
            query += "AND operating_id = :operating\n"
        if form.region.data != "--":
            query += "AND region_id = :region\n"

        cursor.execute(query, {'name': form.name.data + "%",
                               'state': form.state.data,
                               'ownership': form.ownership.data,
                               'region': form.region.data})
        data = cursor.fetchall()

        conn.close()
        return data

    @staticmethod
    def get_world_energy(form):
        """
        :param form:
        :return:
        """
        series_id = form.metric.data.format(form.country.data)
        params = {'api_key': EIA_API_KEY,
                  'series_id': series_id}
        raw_data = requests.get(ENERGY_URL, params=params).json()['series'][0]
        x_data = [x[0] for x in raw_data['data']]
        y_data = [x[1] for x in raw_data['data']]

        title = '{}, {}, Annual'.format(COUNTRY_METRIC_LOOKUP[form.metric.data], COUNTRY_LOOKUP[form.country.data])

        fig = figure(title=title, plot_width=1000, plot_height=500,
                     tools='pan,box_zoom,reset,resize,save,hover')
        hover = fig.select(dict(type=HoverTool))
        hover.tooltips = OrderedDict([
            ("Value", "@y"),
            ("Year", "@x")
        ])

        fig.line(x_data, y_data)
        fig.circle(x_data, y_data)
        fig.yaxis.axis_label = 'Amount [{}]'.format(raw_data['units'])
        fig.xaxis.axis_label = 'Year'

        fig_js, fig_div = components(fig)
        return fig_js, fig_div

    @staticmethod
    def get_state_energy(form):
        """
        :param form:
        :return:
        """
        series_id = form.metric.data.format(form.state.data)
        params = {'api_key': EIA_API_KEY,
                  'series_id': series_id}
        raw_data = requests.get(ENERGY_URL, params=params).json()['series'][0]
        x_data = [x[0] for x in raw_data['data']]
        y_data = [x[1] for x in raw_data['data']]

        title = '{}, {}, Annual'.format(STATE_METRIC_LOOKUP[form.metric.data], STATE_LOOKUP[form.state.data])

        fig = figure(title=title, plot_width=1000, plot_height=500,
                     tools='pan,box_zoom,reset,resize,save,hover')
        hover = fig.select(dict(type=HoverTool))
        hover.tooltips = OrderedDict([
            ("Value", "@y"),
            ("Year", "@x")
        ])

        fig.line(x_data, y_data)
        fig.circle(x_data, y_data)
        fig.yaxis.axis_label = 'Amount [{}]'.format(raw_data['units'])
        fig.xaxis.axis_label = 'Year'

        fig_js, fig_div = components(fig)
        return fig_js, fig_div

    @staticmethod
    def get_economy(form):
        """
        :param form:
        :return:
        """
        series_id = form.metric.data
        params = {'api_key': EIA_API_KEY,
                  'series_id': series_id}
        raw_data = requests.get(ENERGY_URL, params=params).json()['series'][0]
        x_data = [x[0] for x in raw_data['data']]
        y_data = [x[1] for x in raw_data['data']]

        title = '{}, Annual'.format(ECONOMIC_METRIC_LOOKUP[form.metric.data])

        fig = figure(title=title, plot_width=1000, plot_height=500,
                     tools='pan,box_zoom,reset,resize,save,hover')
        hover = fig.select(dict(type=HoverTool))
        hover.tooltips = OrderedDict([
            ("Value", "@y"),
            ("Year", "@x")
        ])

        fig.line(x_data, y_data)
        fig.circle(x_data, y_data)
        fig.yaxis.axis_label = 'Amount [{}]'.format(raw_data['units'])
        fig.xaxis.axis_label = 'Year'

        fig_js, fig_div = components(fig)
        return fig_js, fig_div

    @staticmethod
    def get_nutrition_detail(ndbno):
        params = {
            'ndbno': ndbno,
            'format': 'json',
            'api_key': DATAGOV_API_KEY,
        }
        raw_data = requests.get(NUTRITION_URL, params=params).json()['report']['food']

        data = {
            'name': raw_data['name'],
            'nutrients': OrderedDict(),
        }

        for record in raw_data['nutrients']:
            clean_record = {
                'name': record['name'],
                'unit': record['unit'],
                'value': float(record['value']),
            }
            if record['group'] in data['nutrients']:
                data['nutrients'][record['group']].append(clean_record)
            else:
                data['nutrients'][record['group']] = [clean_record]
        return data


if __name__ == '__main__':
    Helper.get_nutrition_detail(19303)


