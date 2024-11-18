def show():
    import duckdb
    import streamlit as st
    import altair as alt
    import pandas as pd

    con = duckdb.connect('data/stats.duckdb')

    st.markdown("""
    <div style="text-align: center"> 

    ## Skew - Vinous

    </div>
    """, unsafe_allow_html=True)


    st.markdown("""
    Tämä kuvaa datanäytteiden jakauman symmetriaa. Positiivinen vino tarkoittaa, 
    että data on painottunut vasemmalle, kun taas negatiivinen vino tarkoittaa, 
    että data on painottunut oikealle.
                
    ## Havainto
                 
    Keskiarvoisen vinouden perusteella enemmistö antureista osoittaa melko symmetristä jakaumaa, sillä vinouden 
    arvo on lähes nolla. Vinouden arvojen vaihteluväli on kohtalainen, ja joillakin antureilla havaitaan sekä 
    positiivista että negatiivista vinoutta. Negatiivinen vinous voi osoittaa fyysisen esteen rajoittavan 
    datan keruuta tai kärryn toimintahäiriötä.
        
                """)

    query = "SELECT * FROM skew"
    df = con.execute(query).fetch_df()

    df['x'] = df['x'].astype(int)

    df['combined_skew'] = df['x'] + df['y']

    title_combined = alt.TitleParams('Combined Skew Range' , anchor='middle')

    chart_combined = alt.Chart(df).mark_bar().encode(
        x=alt.X('node_id:N', title=None),
        y=alt.Y('combined_skew', title=None),
        color=alt.Color('node_id:N', scale=alt.Scale(scheme='turbo'), legend=None),
        tooltip='node_id:N'
    ).properties(
        title=title_combined
    )

    st.altair_chart(chart_combined)

    title_x = alt.TitleParams('Skew Range for X', anchor='middle')

    chart_x = alt.Chart(df).mark_bar().encode(
        x=alt.X('node_id:N', title=None),
        y=alt.Y('x', title=None),
        color=alt.Color('node_id:N', scale=alt.Scale(scheme='turbo'), legend=None),
        tooltip='node_id:N'
    ).properties(
        title=title_x
    )

    st.altair_chart(chart_x)

    title_y = alt.TitleParams('Skew Range for Y', anchor='middle')

    chart_y = alt.Chart(df).mark_bar().encode(
        x=alt.X('node_id:N', title=None),
        y=alt.Y('y', title=None),
        color=alt.Color('node_id:N', scale=alt.Scale(scheme='turbo'), legend=None),
        tooltip='node_id:N'
    ).properties(
        title=title_y
    )

    st.altair_chart(chart_y)

    st.markdown("""
    <div style="text-align: center"> 

    ##  Taulukko arvoista

    </div>
    """, unsafe_allow_html=True)

    st.table(df[['node_id', 'x', 'y']])
