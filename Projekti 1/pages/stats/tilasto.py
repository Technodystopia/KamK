def show():
    import duckdb
    import streamlit as st
    import pandas as pd
    import plotly.express as px

    conn = duckdb.connect(database="data/ultimate.duckdb")

    query = """
    SELECT node_id, 
        DATE_TRUNC('month', timestamp) as month, 
        COUNT(*) as count
    FROM tokmanni2
    GROUP BY node_id, month
    ORDER BY node_id, month
    """

    df = pd.read_sql_query(query, conn)

    figs = []

    unique_node_ids = df['node_id'].unique()

    for node_id in unique_node_ids:
        node_data = df[df['node_id'] == node_id]
        fig = px.line(node_data, x='month', y='count', title=f'Node ID: {node_id}')
        fig.update_xaxes(title_text="Month")
        fig.update_yaxes(title_text="Count")
        figs.append(fig)

    st.markdown('Kuukausittainen datapisteiden määrä kärrykohtaisesti')

    for fig in figs:
        st.plotly_chart(fig)

