""" Module containing a class to process tidal data."""

import pandas as pd
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import matplotlib.ticker as ticker



class Reader:
    """
    Class to process tidal data.

    data : pandas.DataFrame
        The underlying tide data.
    """

    def __init__(self, filename):
        """Read in the rainfall data from a named ``.csv``
           file using ``pandas``.

        The DataFrame data is stored in a class instance variable ``data``
        indexed by entry.

        Parameters
        ----------

        filename: str
            The file to be read

        Examples
        --------

        >>> Reader("tidalReadings.csv").data.loc[0].stationName
        'Bangor'
        """

        df = pd.read_csv(filename)
        self.data = df


    def station_tides(self, station_name, time_from=None, time_to=None):
        """Return the tide data at a named station as an ordered pandas Series,
         indexed by the dateTime data.

        Parameters
        ----------

        station_name: str or list of strs
            Station Name(s) to return
        time_from: str or None
            Time from which to report (ISO 8601 format)
        time_to: str or None
            Time up to which to report (ISO 8601 format)

        Returns
        -------

        pandas.DataFrame
            The relevant tide data indexed by dateTime and with columns the stationName(s)

        Examples
        --------

        >>> reader = Reader("tideReadings.csv")
        >>> tides = reader.station_tides(["Newlyn", "Bangor"])
        >>> tides.loc["2021-09-20T02:00:00Z", "Newlyn"]
        0.937

        """

        sd = self.data
        sd.loc[sd.tideValue == 'dd', 'tideValue'] = None
        sd.loc[sd.tideValue == '\{}', 'tideValue'] = None
        sd = sd.sort_values('dateTime')

        sd = sd.set_index('dateTime')
        sd = sd.loc[time_from:time_to]

        r = pd.DataFrame()

        r = sd.loc[sd.stationName == station_name[0]]
        r = r.iloc[:, [1]]
        # r = r.set_index('dateTime')
        r = r.rename(columns={'tideValue': station_name[0]})

        l = len(station_name)
        if l > 1:
            for i in range(1, l):
                new_c = sd.loc[sd.stationName == station_name[i]]
                new_c = new_c.iloc[:, [1]]
                # new_c = new_c.set_index('dateTime')
                new_c = new_c.rename(columns={'tideValue': station_name[i]})
                r = r.merge(new_c, on='dateTime', how='outer')

        return r


    def max_tides(self, time_from=None, time_to=None):
        """Return the high tide data as an ordered pandas Series,
         indexed by station name data.

        Parameters
        ----------

        time_from: str or None
            Time from which to report (ISO 8601 format).
            If ``None``, then earliest value used.
        time_to: str or None
            Time up to which to report (ISO 8601 format)
            If ``None``, then latest value used.

        Returns
        -------

        pandas.Series
            The relevant tide data indexed by stationName.

        Examples
        --------

        >>> reader = Reader("tideReadings.csv")
        >>> tides = reader.max_tides()
        >>> tides["Newlyn"]
        2.376
        """
        # self.data.groupby
        # initial_df = self.station_tides()

        sd = self.data
        sd = sd.sort_values('dateTime')
        sd = sd.set_index('dateTime')
        sd = sd.loc[time_from:time_to]

        sd.loc[sd.tideValue == 'dd', 'tideValue'] = None
        sd.loc[sd.tideValue == '\{}', 'tideValue'] = None

        float_tv = sd.iloc[:, 1].astype('float')
        sd.iloc[:, 1] = float_tv

        r = pd.Series()
        r = sd.groupby("stationName").tideValue.max()

        return r


    def min_tides(self, time_from=None, time_to=None):
        """Return the low tide data as an ordered pandas Series,
         indexed by station name data.

        Parameters
        ----------

        time_from: str or None
            Time from which to report (ISO 8601 format)
            If ``None``, then earliest value used.
        time_to: str or None
            Time up to which to report (ISO 8601 format)
            If ``None``, then latest value used.

        Returns
        -------

        pandas.Series
            The relevant tide data indexed by stationName.

        Examples
        --------

        >>> reader = Reader("tideReadings.csv")
        >>> tides = reader.min_tides()
        >>> tides["Newlyn"]
        -2.231
        """

        sd = self.data
        sd = sd.sort_values('dateTime')
        sd = sd.set_index('dateTime')
        sd = sd.loc[time_from:time_to]

        sd.loc[sd.tideValue == 'dd', 'tideValue'] = None
        sd.loc[sd.tideValue == '\{}', 'tideValue'] = None

        float_tv = sd.iloc[:, 1].astype('float')
        sd.iloc[:, 1] = float_tv

        r = pd.Series()
        r = sd.groupby("stationName").tideValue.min()

        return r


    def mean_tides(self, time_from=None, time_to=None):  # 和结果有点不同
        """Return the mean tide data as an ordered pandas Series,
         indexed by station name data.

        Parameters
        ----------

        time_from: str or None
            Time from which to report (ISO 8601 format)
        time_to: str or None
            Time up to which to report (ISO 8601 format)

        Returns
        -------

        pandas.Series
            The relevant tide data indexed by stationName.

        Examples
        --------

        >>> reader = Reader("tideReadings.csv")
        >>> tides = reader.mean_tides()
        >>> tides["Newlyn"]
        0.19242285714285723
        """

        sd = self.data
        sd = sd.sort_values('dateTime')
        sd = sd.set_index('dateTime')
        sd = sd.loc[time_from:time_to]

        sd.loc[sd.tideValue == 'dd', 'tideValue'] = None
        sd.loc[sd.tideValue == '\{}', 'tideValue'] = None

        float_tv = sd.iloc[:, 1].astype('float')
        sd.iloc[:, 1] = float_tv

        r = pd.Series()
        r = sd.groupby("stationName").tideValue.mean()
        return r


    def station_graph(self, station_name, time_from=None, time_to=None):
        """Return a matplotlib graph of the tide data at a named station,
        indexed by the dateTime data.

        Parameters
        ----------

        station_name: str
            Station Name
        time_from: str or None
            Time from which to report (ISO 8601 format)
        time_to: str or None
            Time up to which to report (ISO 8601 format)

        Returns
        -------

        matplotlib.figure.Figure
            Labelled graph of station tide data.
        """

        df = self.station_tides(station_name, time_from, time_to)
        df.loc[:, station_name[0]].astype('float').plot(label=str(station_name[0]))
        plt.xlabel('dateTime')
        plt.ylabel('tideValue')
        plt.legend()
        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(15))


        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)

        plot_url = base64.b64encode(img.getvalue())
        plot_url = str(plot_url, "utf-8")
        plt.clf()

        return plot_url


    def add_data(self, date_time, station_name, tide_value):
        """Add data to the reader DataFrame.

        Parameters
        ----------
        date_time: str
            Time of reading in ISO 8601 format
        station_name: str
            Station Name
        time_value: float
            Observed tide in m

        Examples
        --------

        >>> reader = Reader("tideReadings.csv")
        >>> original_len = len(reader.data.index)
        >>> reader.add_data("2021-09-20T02:00:00Z",
                            "Newlyn", 1.465)
        >>> len(reader.data.index) = original_len + 1
        True
        """

        sd = self.data
        sd = sd.append({'dateTime': date_time, 'stationName': station_name, 'tideValue': tide_value}, ignore_index=True)
        self.data = sd
        return sd


    def write_data(self, filename):
        """Write data to disk in .csv format.

        Parameters
        ----------

        filename: str
            filename to write to.
        """

        self.data.to_csv(filename, index=False)

        return NotImplemented


if __name__ == "__main__":
    reader = Reader("tideReadings.csv")
    try:
        print(len(reader.data.index))
    except TypeError:
        print("No data loaded.")
