def show():
    import duckdb
    import streamlit as st
    import altair as alt
    import pandas as pd

    con = duckdb.connect('data/stats.duckdb')

    st.markdown("""
    <div style="text-align: center"> 

    ## Min

    </div>
    """, unsafe_allow_html=True)


    st.markdown("""
    # Tämä on pienin arvo datassa.
                
    ## Johdanto
                
    Minimmäärä tässä datasetissä kertoo, onko paikannettu kärry käynyt koordinaattien
    minimiarvossa (0). 
                
    - Minimiarvo pohjakuvaan suhteutettuna on x-arvolla kassalinjojen keskipiste 
    - y-arvolla pohjakuvan alin seinä.
        
    ## Havaintoja
                
    - Paikannuksen tarkkuus on noin +/- 10 senttimetriä, joten voidaan päätellä että myös lähellä maksimiarvoa käyneet kärryt ovat käytännössä käyneet oikean- ja ylimmän seinän luona.
    - Datasetin aikaväli on maaliskuun alusta 2019 tammikuun loppuun 2020.
        
    ## Datan luotettavuus
                
    Dataa tulkitessa tulee ottaa huomioon, että tämä datasetti ei huomioi kuinka monesti yksittäinen kärry on 
    paikannettu minimikohdasta. Kärryn mukaan järjestetty data kertoo vain, että se on vuoden aikana käynyt
    ainakin kerran liikkeen sisäänkäynnistä katsottuna perimmäisillä seinillä.

                """)

    query = "SELECT * FROM min"
    df = con.execute(query).fetch_df()

    df['x'] = df['x'].astype(int)

    df['combined_min'] = df['x'] + df['y']

    title_combined = alt.TitleParams('Combined Min Range' , anchor='middle')

    chart_combined = alt.Chart(df).mark_bar().encode(
        x=alt.X('node_id:N', title=None),
        y=alt.Y('combined_min', title=None),
        color=alt.Color('node_id:N', scale=alt.Scale(scheme='turbo'), legend=None),
        tooltip='x'
    ).properties(
        title=title_combined
    )

    st.altair_chart(chart_combined)

    title_x = alt.TitleParams('Min Range for X', anchor='middle')

    chart_x = alt.Chart(df).mark_bar().encode(
        x=alt.X('node_id:N', title=None),
        y=alt.Y('x', title=None),
        color=alt.Color('node_id:N', scale=alt.Scale(scheme='turbo'), legend=None),
        tooltip='x'
    ).properties(
        title=title_x
    )

    st.altair_chart(chart_x)

    title_y = alt.TitleParams('Min Range for Y', anchor='middle')

    chart_y = alt.Chart(df).mark_bar().encode(
        x=alt.X('node_id:N', title=None),
        y=alt.Y('y', title=None),
        color=alt.Color('node_id:N', scale=alt.Scale(scheme='turbo'), legend=None),
        tooltip='x'
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
