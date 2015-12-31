from flask import Flask, render_template, redirect, request, abort
from flask_bootstrap import Bootstrap
from helper import Helper
import os

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/countries/detail/<country_code>')
def countries_detail(country_code):
    data = Helper.get_country_detail(country_code)
    if data is None:
        abort(404)
    return render_template('countries/detail.html', data=data)


@app.route('/countries/all')
def countries_all():
    data = Helper.get_all_countries()
    title = 'All countries ({})'.format(len(data))
    return render_template('countries/list.html', data=data, title=title)


@app.route('/countries/region/<region_name>')
def countries_region(region_name):
    data = Helper.get_countries_by_region(region_name)
    if data is None:
        abort(404)
    title = '{} ({})'.format(region_name, len(data))
    return render_template('countries/list.html', data=data, title=title)


@app.route('/countries/regions')
def countries_regions():
    data = Helper.get_country_regions()
    return render_template('countries/regions.html', data=data)


@app.route('/countries/language/<language_name>')
def countries_language(language_name):
    data = Helper.get_countries_by_language(language_name)
    if data is None:
        abort(404)
    title = 'Language {} ({})'.format(language_name, len(data))
    return render_template('countries/list.html', data=data, title=title)


@app.route('/countries/languages')
def countries_languages():
    data = Helper.get_contry_languages()
    return render_template('countries/languages.html', data=data)


@app.route('/countries/top')
def countries_top():
    data = Helper.get_country_top()
    return render_template('countries/top.html', data=data)


@app.route('/schools/detail/<school_id>')
def schools_detail(school_id):
    data = Helper.get_school_detail(school_id)
    if data is None:
        abort(404)
    return render_template('schools/detail.html', data=data)


@app.route('/schools/top')
def schools_top():
    data = Helper.get_school_top()
    return render_template('schools/top.html', data=data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
