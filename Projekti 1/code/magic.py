"""
This module contains the DataAnalyzer class which provides various statistical and analytical
methods to analyze data from a database. The class uses pandas for data manipulation, numpy 
for numerical operations, sklearn's KMeans for clustering, and scipy's mode for mode calculation.

Imports:
- pandas (pd): A library providing high-performance, easy-to-use data structures and data 
  analysis tools.
- numpy (np): A library for the Python programming language, adding support for large,
  multi-dimensional arrays and matrices, along with a large collection of high-level 
  mathematical functions to operate on these arrays.
- KMeans from sklearn.cluster: A clustering method that divides a set of samples into 
  disjoint clusters, each described by the mean of the samples in the cluster.
- mode from scipy.stats: A function that returns an array of the modal (most common) 
  value in the passed array.
"""
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

class DataAnalyzer:
    """
    A class used to analyze data from a database.

    ...

    Attributes
    ----------
    conn : DuckDb.Connection
        a SQL connection object to the database

    Methods
    -------
    get_table_data(table_name)
        Retrieves all data from a specified table in the database and returns it 
        as a pandas DataFrame.
    
    count(table_name)
        Counts the number of non-NA cells for 'x' and 'y' columns in the specified 
        table and returns the count.
    
    median(table_name)
        Calculates the median of 'x' and 'y' columns in the specified table and 
        returns the median.
    
    kurtosis(table_name)
        Calculates the kurtosis of 'x' and 'y' columns in the specified table and 
        returns the kurtosis.
    
    skew(table_name)
        Calculates the skewness of 'x' and 'y' columns in the specified table and 
        returns the skewness.
    
    iqr(table_name)
        Calculates the interquartile range (IQR) of 'x' and 'y' columns in the 
        specified table and returns the IQR.
    
    min_value(table_name)
        Calculates the minimum value of 'x' and 'y' columns in the specified table 
        and returns the minimum values.
    
    max_value(table_name)
        Calculates the maximum value of 'x' and 'y' columns in the specified table 
        and returns the maximum values.
    
    sample_mean(table_name)
        Calculates the sample mean of 'x' and 'y' columns in the specified table and 
        returns the mean values.
    
    sample_std_dev(table_name)
        Calculates the sample standard deviation of 'x' and 'y' columns in the 
        specified table and returns the standard deviation values.
    
    outlier_frequency(table_name)
        Calculates the frequency of outliers in 'x' and 'y' columns in the specified 
        table and returns the frequency.
    
    location_noise(table_name)
        Calculates the location noise of 'x' and 'y' columns in the specified table 
        and returns the noise.
    
    trend_over_time(table_name, resample_period='D')
        Calculates the trend over time of 'x' and 'y' columns in the specified table 
        and returns the trend.
    
    daily_seasonality(table_name)
        Calculates the daily seasonality of 'x' and 'y' columns in the specified table 
        and returns the seasonality.
    
    total_distance(table_name)
        Calculates the total distance traveled based on 'x' and 'y' columns in the 
        specified table and returns the distance.
    
    average_speed(table_name)
        Calculates the average speed based on the total distance traveled and the time 
        duration in the specified table and returns the average speed.
    
    correlation(table_name)
        Calculates the correlation between 'x' and 'y' columns in the specified table 
        and returns the correlation.
    
    kmeans_clustering(table_name, n_clusters=2)
        Performs KMeans clustering on 'x' and 'y' columns in the specified table and 
        returns the DataFrame with an additional column 'cluster_label' representing 
        the cluster each row belongs to.
    
    mode(table_name)
        Calculates the mode of 'x' and 'y' columns in the specified table and returns 
        the mode.
    
    variance(table_name)
        Calculates the variance of 'x' and 'y' columns in the specified table and returns 
        the variance.
    
    covariance(table_name)
        Calculates the covariance between 'x' and 'y' columns in the specified table 
        and returns the covariance.
    
    quantile(table_name, quantile=0.5)
        Calculates the specified quantile of 'x' and 'y' columns in the specified table 
        and returns the quantile values.
    
    histogram(table_name, bins=10)
        Generates a histogram of 'x' and 'y' columns in the specified table.
    
    first_last_timestamp(table_name)
        Retrieves the first and last timestamp from the 'timestamp' column in 
        the specified table.
    
    days_between_timestamps(table_name)
        Calculates the number of days between the first and last timestamp in 
        the 'timestamp' column of the specified table.
    """
    def __init__(self, conn):
        """
        Constructs all the necessary attributes for the DataAnalyzer object.

        Parameters:
            conn : DuckDb.Connection
                a SQL connection object to the database
        """
        self.conn = conn

    def get_table_data(self, table_name, node_id):
        """
        Retrieves all data from a specified table in the database and returns 
        it as a pandas DataFrame.

        Parameters:
        table_name (str): The name of the table from which to retrieve data.

        Returns:
        df (pd.DataFrame): A DataFrame containing the data from the table. 
        The DataFrame has the following columns:
            - 'node_id': The ID of the node.
            - 'timestamp': The timestamp of the data entry, converted 
               to a datetime object.
            - 'x': The x-coordinate of the node.
            - 'y': The y-coordinate of the node.
        """
        query = f"SELECT * FROM {table_name} WHERE node_id={node_id}"
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=['node_id', 'timestamp', 'x', 'y'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        return df

    def count(self, table_name, node_id):
        """
        Counts the number of non-NA cells for 'x' and 'y' columns in the 
        specified table and returns the count.

        Parameters:
        table_name (str): The name of the table from which to retrieve 
        and count data.

        Returns:
        count (pd.Series): A Series containing the count of non-NA cells 
        for 'x' and 'y' columns.
        """
        df = self.get_table_data(table_name, node_id)
        count = df[['x', 'y']].count()
        return count

    def median(self, table_name, node_id):
        """
        Calculates the median of 'x' and 'y' columns in the specified 
        table and returns the median.

        Parameters:
        table_name (str): The name of the table from which to retrieve 
        and calculate the median.

        Returns:
        median (pd.Series): A Series containing the median of 'x' 
        and 'y' columns.
        """
        df = self.get_table_data(table_name, node_id)
        median = df[['x', 'y']].median()
        return median

    def kurtosis(self, table_name, node_id):
        """
        Calculates the kurtosis of 'x' and 'y' columns in the specified 
        table and returns the kurtosis.

        Parameters:
        table_name (str): The name of the table from which to retrieve 
        and calculate the kurtosis.

        Returns:
        kurtosis (pd.Series): A Series containing the kurtosis of 'x' 
        and 'y' columns.
        """
        df = self.get_table_data(table_name, node_id)
        kurtosis = df[['x', 'y']].kurtosis()
        return kurtosis

    def skew(self, table_name, node_id):
        """
        Calculates the skewness of 'x' and 'y' columns in the specified 
        table and returns the skewness.

        Parameters:
        table_name (str): The name of the table from which to retrieve 
        and calculate the skewness.

        Returns:
        skew (pd.Series): A Series containing the skewness of 'x' 
        and 'y' columns.
        """
        df = self.get_table_data(table_name, node_id)
        skew = df[['x', 'y']].skew()
        return skew

    def iqr(self, table_name, node_id):
        """
        Calculates the interquartile range (IQR) of 'x' and 'y' columns 
        in the specified table and returns the IQR.

        Parameters:
        table_name (str): The name of the table from which to retrieve 
        and calculate the IQR.

        Returns:
        iqr (pd.Series): A Series containing the IQR of 'x' and 'y' columns. 
        The IQR is calculated as the difference between the 75th percentile 
        (Q3) and the 25th percentile (Q1).
        """
        df = self.get_table_data(table_name, node_id)
        q1 = df[['x', 'y']].quantile(0.25)
        q3 = df[['x', 'y']].quantile(0.75)
        iqr = q3 - q1
        return iqr

    def min_value(self, table_name, node_id):
        """
        Calculates the minimum value of 'x' and 'y' columns in the specified 
        table and returns the minimum values.

        Parameters:
        table_name (str): The name of the table from which to retrieve and 
        calculate the minimum values.

        Returns:
        min (pd.Series): A Series containing the minimum values of 'x' 
        and 'y' columns.
        """
        df = self.get_table_data(table_name, node_id)
        min = df[['x', 'y']].min()
        return min

    def max_value(self, table_name, node_id):
        """
        Calculates the maximum value of 'x' and 'y' columns in the specified 
        table and returns the maximum values.

        Parameters:
        table_name (str): The name of the table from which to retrieve 
        and calculate the maximum values.

        Returns:
        max (pd.Series): A Series containing the maximum values of 'x' 
        and 'y' columns.
        """
        df = self.get_table_data(table_name, node_id)
        max = df[['x', 'y']].max()
        return max

    def sample_mean(self, table_name, node_id):
        """
        Calculates the sample mean of 'x' and 'y' columns in the specified 
        table and returns the mean values.

        Parameters:
        table_name (str): The name of the table from which to retrieve and 
        calculate the mean values.

        Returns:
        mean (pd.Series): A Series containing the mean values of 'x' 
        and 'y' columns.
        """
        df = self.get_table_data(table_name, node_id)
        mean = df[['x', 'y']].mean()
        return mean

    def sample_std_dev(self, table_name, node_id):
        """
        Calculates the sample standard deviation of 'x' and 'y' columns 
        in the specified table and returns the standard deviation values.

        Parameters:
        table_name (str): The name of the table from which to retrieve 
        and calculate the standard deviation values.

        Returns:
        std_dev (pd.Series): A Series containing the standard deviation 
        values of 'x' and 'y' columns.
        """
        df = self.get_table_data(table_name, node_id)
        std_dev = df[['x', 'y']].std()
        return std_dev

    def outlier_frequency(self, table_name, node_id):
        """
        Calculates the frequency of outliers in 'x' and 'y' columns in the 
        specified table and returns the frequency. Outliers are defined as 
        values that fall below Q1 - 1.5 * IQR or above Q3 + 1.5 * IQR.

        Parameters:
        table_name (str): The name of the table from which to retrieve and 
        calculate the outlier frequency.

        Returns:
        freq (float): The frequency of outliers in 'x' and 'y' columns. 
        If the DataFrame is empty, returns None.
        """
        df = self.get_table_data(table_name, node_id)
        if df.empty:
            return None
        q1_x, q1_y = df['x'].quantile(0.25), df['y'].quantile(0.25)
        q3_x, q3_y = df['x'].quantile(0.75), df['y'].quantile(0.75)
        iqr_x, iqr_y = q3_x - q1_x, q3_y - q1_y
        outliers = df[
            ((df['x'] < (q1_x - 1.5 * iqr_x)) | (df['x'] > (q3_x + 1.5 * iqr_x))) |
            ((df['y'] < (q1_y - 1.5 * iqr_y)) | (df['y'] > (q3_y + 1.5 * iqr_y)))
        ]

        freq = len(outliers) / len(df)
        return freq

    def location_noise(self, table_name, node_id):
        """
        Calculates the location noise of 'x' and 'y' columns in the specified 
        table and returns the noise. The location noise is defined as the absolute 
        difference between each value and the mean, divided by the standard deviation.

        Parameters:
        table_name (str): The name of the table from which to retrieve and calculate 
        the location noise.

        Returns:
        noise (pd.DataFrame): A DataFrame containing the location noise of 'x' 
        and 'y' columns.
        """
        df = self.get_table_data(table_name, node_id)
        noise = df[['x', 'y']].apply(lambda x: np.abs(x - x.mean()) / x.std())
        return noise

    def trend_over_time(self, table_name, node_id, resample_period='D'):
        """
        Calculates the trend over time of 'x' and 'y' columns in the specified 
        table and returns the trend. The trend is defined as the mean value 
        of 'x' and 'y' columns resampled over a specified period.

        Parameters:
        table_name (str): The name of the table from which to retrieve and 
        calculate the trend.
        resample_period (str): The period over which to resample the data. 
        Defaults to 'D' (daily).

        Returns:
        resampled_df (pd.DataFrame): A DataFrame containing the trend 
        of 'x' and 'y' columns over time.
        """
        df = self.get_table_data(table_name, node_id)
        df.set_index('timestamp', inplace=True)
        resampled_df = df.resample(resample_period).mean().ffill()
        return resampled_df

    def daily_seasonality(self, table_name, node_id):
        """
        Calculates the daily seasonality of 'x' and 'y' columns in the specified 
        table and returns the seasonality. The daily seasonality is defined as 
        the mean value of 'x' and 'y' columns grouped by hour of the day.

        Parameters:
        table_name (str): The name of the table from which to retrieve and 
        calculate the daily seasonality.

        Returns:
        hourly_means (pd.DataFrame): A DataFrame containing the mean values 
        of 'x' and 'y' columns grouped by hour of the day.
        """
        df = self.get_table_data(table_name, node_id)
        df['hour'] = df['timestamp'].dt.hour
        hourly_means = df.groupby('hour').mean()
        return hourly_means

    def total_distance(self, table_name, node_id):
        """
        Calculates the total distance traveled based on 'x' and 'y' columns 
        in the specified table and returns the distance. The distance is 
        calculated as the sum of the Euclidean distance between consecutive points.

        Parameters:
        table_name (str): The name of the table from which to retrieve 
        and calculate the total distance.

        Returns:
        distance (float): The total distance traveled.
        """
        df = self.get_table_data(table_name, node_id)
        df = df.dropna(subset=['x', 'y'])
        dx = np.diff(df['x'])
        dy = np.diff(df['y'])
        distance = np.sqrt(dx**2 + dy**2).sum()
        return distance


    def average_speed(self, table_name, node_id):
        """
        Calculates the average speed based on the total distance traveled and the 
        time duration in the specified table and returns the average speed. 
        The average speed is defined as the total distance divided by 
        the time duration.

        Parameters:
        table_name (str): The name of the table from which to retrieve 
        and calculate the average speed.

        Returns:
        average_speed (float): The average speed. If the time duration 
        is zero, returns NaN.
        """
        total_distance = self.total_distance(table_name, node_id)
        df = self.get_table_data(table_name, node_id)
        first_timestamp = df['timestamp'].iloc[0]
        last_timestamp = df['timestamp'].iloc[-1]
        time_delta = last_timestamp - first_timestamp
        if time_delta.total_seconds() == 0:
            return np.nan
        average_speed = total_distance / time_delta.total_seconds()
        return average_speed

    def correlation(self, table_name, node_id):
        """
        Calculates the correlation between 'x' and 'y' columns in 
        the specified table and returns the correlation. 
        The correlation is calculated using the Pearson correlation 
        coefficient.

        Parameters:
        table_name (str): The name of the table from which to retrieve 
        and calculate the correlation.

        Returns:
        x_y_correlation (float): The correlation between 'x' 
        and 'y' columns.
        """
        df = self.get_table_data(table_name, node_id)
        correlation_matrix = df[['x', 'y']].corr()
        x_y_correlation = correlation_matrix.loc['x', 'y']
        return x_y_correlation

    def kmeans_clustering(self, table_name, node_id, n_clusters=2):
        """
        Performs KMeans clustering on 'x' and 'y' columns in the specified 
        table and returns the DataFrame with an additional column 
        'cluster_label' representing the cluster each row belongs to.

        Parameters:
        table_name (str): The name of the table from which to retrieve 
        data for clustering.
        n_clusters (int): The number of clusters to form. 
        Defaults to 2.

        Returns:
        df (pd.DataFrame): The DataFrame with an additional column 
        'cluster_label' representing the cluster each row belongs to.
        """
        df = self.get_table_data(table_name, node_id)
        df = df.fillna(df.mean())
        kmeans = KMeans(n_clusters=n_clusters, random_state=0)
        kmeans.fit(df[['x', 'y']])
        df['cluster_label'] = kmeans.labels_
        return df

    def variance(self, table_name, node_id):
        """
        Calculates the variance of 'x' and 'y' columns in the specified 
        table and returns the variance. The variance is a measure of 
        the variability or spread in a set of data.

        Parameters:
        table_name (str): The name of the table from which to retrieve 
        and calculate the variance.

        Returns:
        variance (pd.Series): A Series containing the variance 
        of 'x' and 'y' columns.
        """
        df = self.get_table_data(table_name, node_id)
        variance = df[['x', 'y']].var()
        return variance

    def covariance(self, table_name, node_id):
        """
        Calculates the covariance between 'x' and 'y' columns in the specified 
        table and returns the covariance. Covariance is a measure of how 
        much two random variables vary together.

        Parameters:
        table_name (str): The name of the table from which to retrieve 
        and calculate the covariance.

        Returns:
        covariance (float): The covariance between 'x' 
        and 'y' columns.
        """
        df = self.get_table_data(table_name, node_id)
        covariance = df['x'].cov(df['y'])
        return covariance

    def quantile(self, table_name, node_id, quantile=0.5):
        """
        Calculates the specified quantile of 'x' and 'y' columns 
        in the specified table and returns the quantile values.

        Parameters:
        table_name (str): The name of the table from which to 
        retrieve and calculate the quantile.
        quantile (float): The quantile to compute, which must 
        be between 0 and 1 inclusive. Defaults to 0.5.

        Returns:
        quantile_value (pd.Series): A Series containing the 
        quantile values of 'x' and 'y' columns.
        """
        df = self.get_table_data(table_name, node_id)
        quantile_value = df[['x', 'y']].quantile(quantile)
        return quantile_value

    def histogram(self, table_name, node_id, bins=10):
        """
        Generates a histogram of 'x' and 'y' columns in 
        the specified table.

        Parameters:
        table_name (str): The name of the table from which to 
        retrieve data for the histogram.
        bins (int): The number of bins to use for the histogram. 
        Defaults to 10.

        Returns:
        hist (matplotlib.AxesSubplot): A histogram plot object.
        """
        df = self.get_table_data(table_name, node_id)
        hist = df[['x', 'y']].hist(bins=bins)
        return hist

    def first_last_timestamp(self, table_name, node_id):
        """
        Retrieves the first and last timestamp from the 'timestamp' 
        column in the specified table.

        Parameters:
        table_name (str): The name of the table from which to 
        retrieve the timestamps.

        Returns:
        first_timestamp (datetime): The earliest timestamp 
        in the 'timestamp' column.
        last_timestamp (datetime): The latest timestamp 
        in the 'timestamp' column.
        """
        df = self.get_table_data(table_name, node_id)
        first_timestamp = df['timestamp'].min()
        last_timestamp = df['timestamp'].max()
        return first_timestamp, last_timestamp

    def days_between_timestamps(self, table_name, node_id):
        """
        Calculates the number of days between the first and last 
        timestamp in the 'timestamp' column of the specified table.

        Parameters:
        table_name (str): The name of the table from which to 
        retrieve the timestamps.

        Returns:
        days (int): The number of days between the first and 
        last timestamp.
        """
        first_timestamp, last_timestamp = self.first_last_timestamp(table_name, node_id)
        time_delta = last_timestamp - first_timestamp
        return time_delta.days
