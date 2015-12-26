from flask import Flask, render_template, redirect, request, abort
from flask_bootstrap import Bootstrap
from helper import Helper

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/country/<country_code>')
def country(country_code):
    data = Helper.get_country_detail(country_code)
    if data is None:
        abort(404)
    return render_template('country_detail.html', data=data)


@app.route('/all')
def all():
    data = Helper.get_all_countries()
    title = 'All countries ({})'.format(len(data))
    return render_template('country_list.html', data=data, title=title)


@app.route('/region/<region_name>')
def region(region_name):
    data = Helper.get_countries_by_region(region_name)
    if data is None:
        abort(404)
    title = '{} ({})'.format(region_name, len(data))
    return render_template('country_list.html', data=data, title=title)


@app.route('/regions')
def regions():
    data = Helper.get_regions()
    return render_template('regions.html', data=data)


@app.route('/language/<language_name>')
def language(language_name):
    data = Helper.get_countries_by_language(language_name)
    if data is None:
        abort(404)
    title = 'Language {} ({})'.format(language_name, len(data))
    return render_template('country_list.html', data=data, title=title)


@app.route('/languages')
def languages():
    data = Helper.get_languages()
    return render_template('languages.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
