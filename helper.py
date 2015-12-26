import sqlite3
import ipdb

DB_FILE = 'countries.db'


class Helper(object):
    @staticmethod
    def get_country_detail(country_code):
        """
        :param country_code:
        :return:
        """
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        query = "SELECT * FROM country WHERE alpha3Code = :alpha3Code"
        cursor.execute(query, {'alpha3Code': country_code})

        result = cursor.fetchone()
        columns = [x[0] for x in cursor.description]

        if result is None:
            return
        data = {key: value for key, value in zip(columns, result)}

        query = "SELECT language FROM language WHERE alpha3COde = :alpha3Code"
        cursor.execute(query, {'alpha3Code': country_code})
        data['languages'] = [x[0] for x in cursor.fetchall()]

        conn.close()
        return data

    @staticmethod
    def get_all_countries():
        """
        :return:
        """
        conn = sqlite3.connect(DB_FILE)
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
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        query = "SELECT alpha3Code, name FROM country WHERE region = :region ORDER BY name"
        cursor.execute(query, {'region': region_name})

        result = cursor.fetchall()
        conn.close()

        if len(result) == 0:
            return
        return result

    @staticmethod
    def get_regions():
        """
        :return:
        """
        conn = sqlite3.connect(DB_FILE)
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
        conn = sqlite3.connect(DB_FILE)
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
    def get_languages():
        """
        :return:
        """
        conn = sqlite3.connect(DB_FILE)
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

if __name__ == '__main__':
    Helper.get_countries_by_language("uz")

