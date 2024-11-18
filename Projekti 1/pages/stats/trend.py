def show():
    import streamlit as st
    import plotly.express as px
    import duckdb
    import pandas as pd

    month_translation = {
        "January": "Tammikuu",
        "February": "Helmikuu",
        "March": "Maaliskuu",
        "April": "Huhtikuu",
        "May": "Toukokuu",
        "June": "Kesäkuu",
        "July": "Heinäkuu",
        "August": "Elokuu",
        "September": "Syyskuu",
        "October": "Lokakuu",
        "November": "Marraskuu",
        "December": "Joulukuu"
    }

    def get_data():
        conn = duckdb.connect('data/ultimate.duckdb')
        query = "SELECT * FROM tokmanni"
        df = conn.execute(query).fetchdf()
        return df

    df = get_data()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['year'] = df['timestamp'].dt.year
    df['month'] = df['timestamp'].dt.month_name()

    selected_year = st.selectbox('Select Year', sorted(df['year'].unique()))
    selected_month = st.selectbox('Select Month', sorted(df['month'].unique()))

    filtered_df = df[(df['year'] == selected_year) & (df['month'] == selected_month)]

    daily_counts = filtered_df.groupby(['node_id', 'timestamp']).size().reset_index(name='count')

    fig = px.line(daily_counts, x='timestamp', y='count', color='node_id', title='Trend over time')
    st.plotly_chart(fig, use_container_width=True)
