import flask
from flask import jsonify, request, render_template
import pandas as pd
import locale
import datetime

locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

years = range(2007,2015)

def collect_data(years):
    list_of_dfs = []
    for i in years:
        file = str(i) + '-PIT-Counts-by-State.csv'
        df = pd.read_csv(file)
        list_of_dfs.append(df)
    return list_of_dfs

list_of_dfs = collect_data(years)

def get_homeless_types(df):
    headers = df.columns
    homeless_types = []
    for i in range(1,len(headers)):
        name = headers[i].split(',')[0]
        homeless_types.append(name)
    return homeless_types

def get_states(df):
    states = list(df['State'])
    return states

homeless_types = get_homeless_types(list_of_dfs[0])
states = get_states(list_of_dfs[0])

def get_timeseries(state_selected, homeless_selected, list_of_dfs):
    all_ts = []
    year = 2007
    for homeless in homeless_selected:
        ts = []
        for df in list_of_dfs:
            new_time = (datetime.datetime(year,1,1)-datetime.datetime(1970,1,1)).total_seconds()*1e3
            key = homeless + ', '+str(year)
            a = df[key].loc[df['State'] == state_selected].values[0]
            value = locale.atof(a)
            ts.append(value)
            year = year+1
        all_ts.append({'name': homeless, 'data': ts})
    return all_ts


application = flask.Flask(__name__)

@application.route('/', methods=['GET', 'POST'])
def run_job():
    if request.method == 'GET':
        homeless_types_selected = ['Total Homeless']
        state_selected = 'Total'
    else:
        homeless_types_selected = request.form.getlist('homeless_types_selected')
        state_selected = request.form['state_selected']
    all_ts = get_timeseries(state_selected, homeless_types_selected, list_of_dfs)
    #return jsonify(items=[years,all_ts])
    return render_template('homeless.html', states = states, homeless_types = homeless_types, state_selected = state_selected, homeless_types_selected = homeless_types_selected, years = years, all_ts = all_ts)

if __name__ == '__main__':
    application.run()
