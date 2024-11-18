def show():
    import pandas as pd
    import streamlit as st
    import plotly.express as px
    import duckdb

    conn = duckdb.connect('data/stats.duckdb')
    query = "SELECT * FROM daily_seasonality"
    df = conn.execute(query).fetch_df()

    node_id = st.selectbox('Valikoi ostoskärry', options=df['node_id'].unique())

    df_node = df[df['node_id'] == node_id]

    fig = px.line(df_node, x='hour', y=['x_mean', 'y_mean'], title='Tuntikohtainen kausiluonne ostoskärrylle {}'.format(node_id))

    st.markdown("""
    <div style="text-align: center"> 

    ## Datan tuntikohtainen kausiluonne viittaa säännöllisiin malleihin, jotka toistuvat tietyin väliajoin ajan kuluessa.

    </div>
    """, unsafe_allow_html=True)

    st.plotly_chart(fig)
