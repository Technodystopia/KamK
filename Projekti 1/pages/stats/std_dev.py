def show():
    import duckdb
    import streamlit as st
    import altair as alt
    import pandas as pd

    con = duckdb.connect('data/stats.duckdb')

    st.markdown("""
    <div style="text-align: center"> 

    ## STD-Dev - Keskihajonta

    </div>
    """, unsafe_allow_html=True)


    st.markdown("""
    Tämä kuvaa datanäytteiden hajontaa keskiarvon ympärillä.
                
    ## Havaintoja
                
    Keskihajonta voi auttaa arvioimaan, ovatko kärryt liikkuneet odotetusti koko kaupan alueella.
        
    Korkea keskihajonta X-suunnassa tarkoittaa, että kärryt liikkuvat enemmän vasen-oikea-suunnassa, 
    kun taas korkea Y-suunnan keskihajonta viittaa siihen, että ne liikkuvat enemmän ylös-alas-suuntaisesti. 
    Samankaltaiset keskihajonnat sekä X- että Y-suunnassa viittaavat siihen, että kärryt liikkuvat pyöreämmässä 
    kuviossa pohjakuvan päälle visualisoituna, eli eivät liiku vain edes takaisin yhdellä akselilla.

    Suuret vaihtelut voivat viitata esimerkiksi eri kokoisiin liikkumisalueisiin tai rikkoutuneeseen
    paikannuslaitteeseen.
    Johdonmukainen matala keskihajonta voi viitata siihen, että ne kulkevat rajoitetummalla alueella, kuten 
    vain muutamalla kaupan osastolla.

                """)

    query = "SELECT * FROM std_dev"
    df = con.execute(query).fetch_df()

    df['x'] = df['x'].astype(int)

    df['combined_std_dev'] = df['x'] + df['y']

    title_combined = alt.TitleParams('Combined Std Dev Range' , anchor='middle')

    chart_combined = alt.Chart(df).mark_bar().encode(
        x=alt.X('node_id:N', title=None),
        y=alt.Y('combined_std_dev', title=None),
        color=alt.Color('node_id:N', scale=alt.Scale(scheme='turbo'), legend=None),
        tooltip='node_id:N'
    ).properties(
        title=title_combined
    )

    st.altair_chart(chart_combined)

    title_x = alt.TitleParams('Std Dev Range for X', anchor='middle')

    chart_x = alt.Chart(df).mark_bar().encode(
        x=alt.X('node_id:N', title=None),
        y=alt.Y('x', title=None),
        color=alt.Color('node_id:N', scale=alt.Scale(scheme='turbo'), legend=None),
        tooltip='node_id:N'
    ).properties(
        title=title_x
    )

    st.altair_chart(chart_x)

    title_y = alt.TitleParams('Std Dev Range for Y', anchor='middle')

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
