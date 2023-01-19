# Mini Flask 8 Cloud System for Tide gauge data processing development project

## Description

Used Pandas, Flask and Docker to create a tool to process tide gauge data in `.csv` format into a cloud compatible form.

The `tideReadings.csv` file contains sea level readings (in m) recorded over 15 minute windows at tide gauges around the UK for the week of Monday 20th September 2021. The columns are:

- `dateTime`: The date and time for which the reading is valid.
- `stationName`: The human readable tide gauge name.
- `tideValue`: the tide gauge reading in metres (relative to mean sea level at Newlyn).

The `stations.csv` file contains some relevant information on the tide gauge stations. The columns are:

- `stationName`: The human readable tide gauge name.
- `stationReference` The Environment Agency short code for the station
- `stationURL` the Environment Agency REST API URL for the station, which can be called to access more information if needed.

1. Wrote appropriate Python code to complete the methods of class `Reader` in `process.py`. See the docstrings in each method for details of key functionality required, although other methods or functions can be added if appropriate. This 
2. Wrote Python code in `app.py` to serve a REST API for the data in the two `.csv` files. See the `API.rst` file for a description of required paths and responses. You may either use Flask, or builtin Python modules, and may add additional classes or functions as needed, to the `process.py` and `app.py` files, or to new Python files.
3. Updated the `Dockerfile` to correctly serve your `app.py` on the container's port 80, so that the command sequence
```bash
  docker build --tag tides:latest
  docker run -it -p8888:80 tides:latest
```
  allows a user to connect to `http://localhost:8888/station/json?stationName=Newlyn` and see a response listing the tide data for the Newlyn station.





