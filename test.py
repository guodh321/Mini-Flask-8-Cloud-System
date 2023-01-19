import process as p
from urllib.request import urlopen
import json
import matplotlib.pyplot as plt
import pandas as pd
import os
import io
import base64
import matplotlib.ticker as ticker

BASE_PATH = os.path.dirname(__file__)
filename = '/Users/michael/Documents/modern-programming-methods/mpm-assessment-2-edsml-dg321-main/tideReadings.csv'
# print(p.Reader(filename).data.loc[0].stationName)

reader = p.Reader(filename)
# # tides = reader.station_tides(["Newlyn", "Bangor"],"2021-09-20T00:00:00Z","2021-09-20T02:00:00Z")
# # print(tides)
# # print(tides.loc["2021-09-20T02:00:00Z", "Bangor"])   #有问题
#
# # tides = reader.max_tides("2021-09-20T00:00:00Z", "2021-09-20T02:00:00Z")
# # print(tides['Newlyn'])
# #
# #
# # # tides = reader.min_tides()
# # # print(tides["Newlyn"])
# #
# # # tides = reader.mean_tides()
# # # print(tides["Newlyn"])
# #
# # original_len = len(reader.data.index)
# # reader.add_data("2021-09-20T02:00:00Z","Newlyn", 1.465)
# # print(reader.data.iloc[-1])
# # print(len(reader.data.index) == original_len + 1)
# #
# # writefile = '/Users/michael/Documents/modern-programming-methods/mpm-assessment-2-edsml-dg321-main/result.csv'
# # reader.write_data
#
# # url = "http://environment.data.gov.uk/flood-monitoring/id/stations/E73839"
# #
# # station_i = json.loads(str(urlopen(url).read(), 'ascii'))
# #
# # print(station_i)
# #
# # short_info = {s['name']: s['lineStatuses'][0]['statusSeverityDescription'] for s in station_i}
# # print(short_info)
# #**********************************************************
# filename = '/Users/michael/Documents/modern-programming-methods/mpm-assessment-2-edsml-dg321-main/stations.csv'
# station_data = pd.read_csv(filename)
# #
# # # print(station_data)
# # # url = station_data.loc[station_data.stationName == stationName].iloc[:, 2]
# # # url = url[0]
# # #
# # # station_i = json.loads(str(urlopen(url).read(), 'ascii'))
# # #
# # # print(station_i)
# # #
# # # print(url)
# #
# # initial_data = '{"stationName" : "","from" : "", "to" : "", "tideValues": {"" : "", "" : ""}}'
# #
# # data = json.loads(initial_data)
# # data["stationName"] = station_data.stationName.loc[station_data.stationReference == 'E73839'].tolist()[0]
# # # data["stationName"] = "2332"
# # data["from"] = "2021-09-20T00:00:00Z"
# # data["to"] = "2021-09-26T06:00:00Z"
# # df = reader.station_tides([data["stationName"]],data["from"],data["to"])
# # print(df)
# # data["tideValues"] = df.to_dict()
# #
# # print(json.dumps(data))
# #
# # url = station_data.loc[station_data.stationReference == 'E73839'].iloc[:, 2]
# # url = url[0]
# #
# # station_i = json.loads(str(urlopen(url).read(), 'ascii'))
# # print(json.dumps(station_i))
# # print(json.dumps(station_i["northing"]))
#
# # stationName = ["Newlyn", "Bangor","Dover"]
# # df = reader.station_tides(stationName)
# # for i in stationName:
# #     df.loc[:,i].astype('float').plot(label=str(i))
# # plt.legend()
# # plt.savefig(os.sep.join((BASE_PATH, 'image.png')))
# # plt.show()
#
# # img = io.BytesIO()
# # y = [1,2,3,4,5]
# # x = [0,2,1,3,4]
# # plt.plot(x,y)
# # plt.savefig(img, format='png')
# # img.seek(0)
# #
# # plot_url = base64.b64encode(img.getvalue()).decode()
# # print(plot_url)
#
# station_ref = 'E71639'
# # station_ref = 'E73839'
#
# # if station_ref in station_data.stationReference.tolist():
# #     station_data = station_data.set_index('stationReference')
# #     url = station_data.loc[station_ref][1]
# #
# #     station_i = json.loads(str(urlopen(url).read(), 'ascii'))
# #
# #     initial_data = '{"stationName" : "","stationReference" : "", "northing" : "", "easting" : "", "latitude" : "", "longitude" : ""}'
# #     data = json.loads(initial_data)
# #     data["stationName"] = station_data.loc[station_ref][0]
# #     data["stationReference"] = station_ref
# #     data["northing"] = station_i["items"]["northing"]
# #     data["easting"] = station_i["items"]["easting"]
# #     data["latitude"] = station_i["items"]["lat"]
# #     data["longitude"] = station_i["items"]["long"]
#
# # f = "mean" + "_tides"
# #
# # r = getattr(reader, f)().loc['Whitby']
# # print(r)
#
# # dd = reader.data
# # dd = dd.sort_values('dateTime')
# #
# # dd = dd.set_index('dateTime')
# #
# # print(dd)
# # dd1 = dd.loc['2021-09-23T06:00:00Z':None]
# # print(dd1)
# # dd2 = dd.loc[None:None]
# # print(dd2)
#
# stationName = ["Bangor"]
# # img = io.BytesIO()
# # df = reader.station_tides(stationName)
# # for i in stationName:
# #     df.loc[:, i].astype('float').plot(label=str(i))
# # plt.legend()
# # plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(15))
# # plt.savefig(img, format='png')
# # img.seek(0)
# #
# # plot_url = base64.b64encode(img.getvalue()).decode()
# # r = reader.station_graph(stationName)
#
# input = '{"stationName": "Stornoway","dateTime": "2021-10-18T00:00:00Z","tideValue": 1.234}'
#
# input = json.loads(input)
# print(input)
# df = pd.DataFrame.from_dict(input, orient='index').T
# print(df)
# for i in df.index:
#     reader.add_data(df.loc[i, 'dateTime'], df.loc[i, 'stationName'], df.loc[i, 'tideValue'])
# reader.write_data('/Users/michael/Documents/modern-programming-methods/mpm-assessment-2-edsml-dg321-main/writed.csv')
#
# # @app.route('/test/', methods=['GET', 'POST'])
# # def data_test():
# #     if request.method == 'GET':
# #
# #         return render_template('P.html')

# statistic = 'min'
# str = statistic.split(',')
# statistic_fun = str[0] + "_tides"
# r = getattr(reader, statistic_fun)()
# r = r.to_frame()
# r = r.rename(columns={'tideValue': str[0]})
# if len(str)>1:
#     for i in  range(1, len(str)):
#         statistic_fun = str[i] + "_tides"
#         new_r = getattr(reader, statistic_fun)()
#         new_r = new_r.to_frame()
#         new_r = new_r.rename(columns={'tideValue':str[i]})
#         r = r.join(new_r)
# print(r)
# statistic_fun = statistic + "_tides"
# result = getattr(reader, statistic_fun)()
# print(result)

# tides = reader.station_tides(["Aberdeen", "Avonmouth+Portbury"])
# print(tides)
# tides1 = reader.station_tides(["Avonmouth+Portbury","Aberdeen"])
# print(tides1)


# tides4 = reader.station_tides(["Avonmouth+Portbury"])
# print(tides4)

# url =
# json_data =
#
# res = requests.post(url,data = )



tides3 = reader.station_tides("Dover")
print(tides3)