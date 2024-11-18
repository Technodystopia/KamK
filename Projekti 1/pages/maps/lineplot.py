def show():
    """
    This module provides a Streamlit application for visualizing data from a DuckDB database.

    The application allows the user to select a time zone, specific shopping carts (identified by node IDs), 
    and a date and time range. It then queries the database for data within the selected parameters and 
    plots the usage of the shopping carts over the selected date range.

    Functions:
        generate_extract(field, start, end): Generate the EXTRACT part of the SQL query.
        plot_data(start_year, start_month, start_day, end_year, end_month, end_day, start_hour, end_hour, selected_nodes): Query the database and plot the data.

    Constants:
        UNIQUE_NODE_IDS: A list of unique node IDs representing different shopping carts.
        TABLE_OPTIONS: A dictionary mapping time zone options to table names in the database.

    Example:
        To run the application, simply execute the script in a Streamlit-compatible environment:
            $ streamlit run script.py
    """
    import plotly.graph_objects as go
    import datetime
    import streamlit as st
    import duckdb

    UNIQUE_NODE_IDS = [3200, 3224, 3240, 42787, 45300, 51719, 51720, 51735, 51751, 51850, 51866, 51889, 
                    51968, 51976, 51992, 52003, 52008, 52023, 52099, 52535, 53000, 53011, 53027, 53130,
                    53768, 53795, 53888, 53924, 53936, 54016, 64458]
    TABLE_OPTIONS = {"EET Aika": "tokmanni2", "UTC Aika": "tokmanni"}

    conn = duckdb.connect('data/ultimate.duckdb')

    selected_table = st.selectbox('Aikavyöhyke:', options=list(TABLE_OPTIONS.keys()))
    selected_nodes = st.multiselect('Ostoskärry(t):', options=list(UNIQUE_NODE_IDS))

    def generate_extract(field, start, end):
        """
        Function to generate EXTRACT part of the query based on the parameters.
        """
        if start == "All" and end == "All":
            return ""
        else:
            return f"AND EXTRACT({field} FROM timestamp) BETWEEN {start} AND {end} "

    def plot_data(start_year, start_month, start_day, end_year, end_month, end_day, start_hour, end_hour, selected_nodes=None):
        """
        Function to plot data based on the selected parameters.
        """
        query = f"SELECT * FROM {TABLE_OPTIONS[selected_table]} WHERE 1=1"
        query += generate_extract("YEAR", start_year, end_year)
        query += generate_extract("MONTH", start_month, end_month)
        query += generate_extract("DAY", start_day, end_day)
        query += generate_extract("HOUR", start_hour, end_hour)
        if selected_nodes:
            query += f"AND node_id IN ({','.join(map(str, selected_nodes))})"
        query += " ORDER BY timestamp"

        result = conn.execute(query)
        df = result.fetchdf()

        df['date'] = df['timestamp'].dt.date
        df_grouped = df.groupby(['date', 'node_id']).size().reset_index(name='count')

        fig = go.Figure()
        for node_id in df_grouped['node_id'].unique():
            df_node = df_grouped[df_grouped['node_id'] == node_id]
            fig.add_trace(go.Scatter(x=df_node['date'], y=df_node['count'], mode='lines', name=str(node_id)))

        fig.update_layout(
            title='Ostoskärryjen käyttö',
            xaxis_title='Date',
            yaxis_title='Count',
            legend=dict(
                y=-0.1,
                traceorder='reversed',
                font=dict(
                    size=10,
                )
            ),
            legend_orientation="h"
        )

        st.plotly_chart(fig)

    start_date = datetime.datetime(2019, 3, 1)
    end_date = datetime.datetime(2020, 1, 31)

    start_date_selected = st.date_input('Ensimmäinen päivämäärä:', start_date, min_value=start_date, max_value=end_date)
    end_date_selected = st.date_input('Viimeinen päivämäärä:', end_date, min_value=start_date, max_value=end_date)

    start_year = start_date_selected.year
    start_month = start_date_selected.month
    start_day = start_date_selected.day

    end_year = end_date_selected.year
    end_month = end_date_selected.month
    end_day = end_date_selected.day

    start_hour, end_hour = st.slider('Aikaväli:', 7, 23, (7, 23), 1)

    plot_data(start_year, start_month, start_day, end_year, end_month, end_day, start_hour, end_hour, selected_nodes)
