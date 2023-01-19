from flask import Flask, request, render_template
import pandas as pd
import json

import os
from urllib.request import urlopen

import process

app = Flask(__name__)

BASE_PATH = os.path.dirname(__file__)
reader = process.Reader('tideReadings.csv')
stations = pd.read_csv('stations.csv')


@app.route('/station/json')
def station_info():
    """Return station info.

    The endpoint accepts query parameters:
    * stationName
    * stationRef

    At least one must be present.
    """

    station_data = stations
    station_name = request.args.get('stationName', default=None)
    if station_name != None:
        station_name = station_name.strip().replace(' ', '+')
    station_ref = request.args.get('stationReference', default=None)
    initial_data = '{"stationName" : "","stationReference" : "", "northing" : "", "easting" : "", "latitude" : "", "longitude" : ""}'
    data = json.loads(initial_data)

    if station_name in stations.stationName.tolist():
        station_data = station_data.set_index('stationName')
        url = station_data.loc[station_name][1]
        data["stationName"] = station_name
        data["stationReference"] = station_data.loc[station_name][0]
    elif station_ref in stations.stationReference.tolist():
        station_data = station_data.set_index('stationReference')
        url = station_data.loc[station_ref][1]
        data["stationName"] = station_data.loc[station_ref][0]
        data["stationReference"] = station_ref
    else:
        return f"Did you type the right station Name/Reference?"

    station_i = json.loads(str(urlopen(url).read(), 'ascii'))

    data["northing"] = station_i["items"]["northing"]
    data["easting"] = station_i["items"]["easting"]
    data["latitude"] = station_i["items"]["lat"]
    data["longitude"] = station_i["items"]["long"]

    return json.dumps(data)


@app.route('/data/graph')
def data_graph():
    """Return a graph of station data.

    The endpoint accepts query parameters:
    * stationName
    * stationRef
    * from
    * to
    """

    station_data = stations

    station_name = request.args.get('stationName', default=None)
    if station_name != None:
        station_name = station_name.strip().replace(' ', '+')
    station_ref = request.args.get('stationReference', default=None)

    time_from = request.args.get('from', default=None)
    time_to = request.args.get('to', default=None)

    if station_name in stations.stationName.tolist():
        stationName = [station_name]
    elif station_ref in stations.stationReference.tolist():
        station_data = station_data.set_index('stationReference')
        stationName = [station_data.loc[station_ref][0]]
    else:
        return f"Did you type the right station Name/Reference?"

    plot_url = reader.station_graph(stationName, time_from, time_to)

    return render_template('plot.html', plot_url=plot_url)


@app.route('/data/json', methods=['GET', 'POST'])
def data_data():
    """Return related data as well as can write data.

        The endpoint accepts query parameters:
        * stationName
        * stationRef
        * statistic
        * from
        * to
        *write
        """

    write = request.args.get('write', default=None)
    if (write == None) and (request.method != 'POST'):

        station_data = stations

        station_name = request.args.get('stationName', default=None)
        if station_name != None:
            station_name = station_name.strip().replace(' ', '+')
        station_ref = request.args.get('stationReference', default=None)
        statistic = request.args.get('statistic', default=None)

        time_from = request.args.get('from', default=None)
        time_to = request.args.get('to', default=None)

        initial_data = '{"stationName" : "", "stationReference" : "", "from" : "", "to" : ""}'
        data = json.loads(initial_data)
        if station_name in stations.stationName.tolist():
            station_data = station_data.set_index('stationName')
            data["stationName"] = station_name
            data["stationReference"] = station_data.loc[station_name][0]
        elif station_ref in stations.stationReference.tolist():
            station_data = station_data.set_index('stationReference')
            data["stationName"] = station_data.loc[station_ref][0]
            data["stationReference"] = station_ref
        else:
            return f"Did you type the right station Name/Reference?"

        data["from"] = "2021-09-20T00:00:00Z"
        data["to"] = "2021-09-26T06:00:00Z"
        if time_from:
            data["from"] = time_from
        if time_to:
            data["to"] = time_to

        if statistic:
            statistic_fun = statistic + "_tides"
            data[statistic] = getattr(reader, statistic_fun)(data["from"], data["to"]).loc[data["stationName"]]
        else:
            df = reader.station_tides([data["stationName"]], data["from"], data["to"])
            df = df.rename(columns={data["stationName"]:'tideValue'})
            data.update(df.to_dict())

        return json.dumps(data)

    else:

        if request.method == 'GET':
            return render_template('Post.html')
        else:
            input = request.form.get('inputData')
            if input == None:
                input = request.get_json(force=True)
            input = json.loads(input)
            for i in input:
                reader.add_data(i['dateTime'], i['stationName'], i['tideValue'])
            reader.write_data('tideReadings.csv')
            return f"Data got added and file got written successfully!"


@app.route('/data/json1', methods=['GET', 'POST'])
def data_data1():
    if request.method == 'POST':
        input = request.get_json(force=True)
        input = json.loads(input)
        for i in input:
            reader.add_data(i['dateTime'], i['stationName'], i['tideValue'])
        reader.write_data('tideReadings.csv')
        return f"Data got added and file got written successfully!"



@app.route('/data/html')
def data_html():
    """Return related html table.

    The endpoint accepts query parameters:
    * stationName
    * stationRef
    * statistic
    * from
    * to
    """

    station_name = request.args.get('stationName', default=None)
    if station_name != None:
        station_name = station_name.strip().replace(' ', '+')
    station_ref = request.args.get('stationReference', default=None)
    statistic = request.args.get('statistic', default=None)

    time_from = request.args.get('from', default=None)
    time_to = request.args.get('to', default=None)

    if time_from != None:
        time_from = time_from
    if time_to != None:
        time_to = time_to

    if statistic != None:

        str = statistic.split(',')
        statistic_fun = str[0] + "_tides"
        r = getattr(reader, statistic_fun)(time_from, time_to)
        r = r.to_frame()
        r = r.rename(columns={'tideValue': str[0]})
        if len(str) > 1:
            for i in range(1, len(str)):
                statistic_fun = str[i] + "_tides"
                new_r = getattr(reader, statistic_fun)()
                new_r = new_r.to_frame()
                new_r = new_r.rename(columns={'tideValue': str[i]})
                r = r.join(new_r)
        htm_result = r.to_html(header="true", table_id="table")
        return htm_result
    else:
        station_data = stations
        if station_name in stations.stationName.tolist():
            station_name = [station_name]
        elif station_ref in stations.stationReference.tolist():
            station_data = station_data.set_index('stationReference')
            station_name = [station_data.loc[station_ref][0]]
        else:
            return f"Did you type the right station Name/Reference?"

        result = reader.station_tides(station_name, time_from, time_to)
        htm_result = result.to_html(header="true", table_id="table")
        return htm_result


@app.errorhandler(404)
def errorurl(e):
    return 'Your input url is wrong. Please rewirte!'

@app.errorhandler(500)
def errorurl1(e):
    return 'Your input url is wrong. Please rewirte and think your input parameter value carefully!!!'




