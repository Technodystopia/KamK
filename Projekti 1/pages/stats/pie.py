def show():
    import duckdb
    import plotly.express as px
    import streamlit as st
    import calendar

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

    conn = duckdb.connect('data/ultimate.duckdb')
    year = st.selectbox('Vuosi', [2019, 2020])

    query_week = f'''
    SELECT EXTRACT(YEAR FROM timestamp) as year, EXTRACT(MONTH FROM timestamp) as month, EXTRACT(WEEK FROM timestamp) as week, COUNT(*) as count
    FROM tokmanni2
    WHERE EXTRACT(YEAR FROM timestamp) = {year}
    GROUP BY year, month, week
    '''

    df_week = conn.execute(query_week).fetchdf()
    df_week['month'] = df_week['month'].apply(lambda x: month_translation[calendar.month_name[int(x)]])
    df_week['month_week'] = df_week['month'] + ' - Viikko ' + df_week['week'].astype(str)

    fig = px.sunburst(df_week, path=['year', 'month', 'month_week'], values='count')
    fig.update_traces(branchvalues='total')
    fig.update_layout(height=800, width=800)

    st.markdown('''
    ## Suodatettujen mittauspisteiden määrä
    
    Tässä visualisoinnissa on esitetty filtteröidyn mittauspisteiden määrä mittausajankohdan aikana.
    ''')

    st.plotly_chart(fig)
