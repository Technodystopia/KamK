def show():
    import duckdb
    import streamlit as st
    import altair as alt
    import pandas as pd

    con = duckdb.connect('data/stats.duckdb')

    st.markdown("""
    <div style="text-align: center"> 

    ## Max

    </div>
    """, unsafe_allow_html=True)


    st.markdown("""
    # Tämä on suurin arvo datassa.
                
    ## Johdanto
                
    Maksimimäärä tässä datassa kertoo vain, onko kärry käynyt x- tai y-koordinaatin 
    maksimikohdassa. 
                
    - Maksimikohta on x-arvolla on karttakuvan oikean puoleinen seinä, eli arvo 10406 alla olevan taulukon mukaisesti. 
    - Y-arvolla maksimikohta on saman pohjapiirroksen yläosan seinä ja taulukon mukaisesti 5220. 
        
    ## Havaintoja
                
    - Paikannuksen tarkkuus on noin +/- 10 senttimetriä, joten voidaan päätellä että myös lähellä maksimiarvoa käyneet kärryt ovat käytännössä käyneet oikean- ja ylimmän seinän luona.
    - Datasetin aikaväli on maaliskuun alusta 2019 tammikuun loppuun 2020.
        
    Taulukkoa ja kuvaajia tutkimalla voidaan todeta, että lähes kaikki ostoskärryjen kanssa
    liikkuvat asiakkaat ovat käyneet liikkeen perällä, vastakkaisilla seinillä sisäänkäyntiin nähden.
        
    Myymäläsuunnittelu on siltä osin onnistunutta, koska asiakkaan tulee niihin päästäkseen kävellä 
    kaikkien muidenkin osastojen läpi ja todennäköisyys heräteostoksille kasvaa.
    X-arvon maksimissa on käynyt 25 ostoskärryä ja Y-arvon maksimissa 24 kärryä kaikista 31 paikannetusta
    ostoskärrystä. 
        
    ## Datan luotettavuus
                
    Dataa tulkitessa tulee ottaa huomioon, että tämä datasetti ei huomioi kuinka monesti yksittäinen kärry on 
    paikannettu maksimikohdista. Kärryn mukaan järjestetty data kertoo vain, että se on vuoden aikana käynyt
    ainakin kerran liikkeen sisäänkäynnistä katsottuna perimmäisillä seinillä.

                """)

    query = "SELECT * FROM max"
    df = con.execute(query).fetch_df()

    df['x'] = df['x'].astype(int)

    df['combined_max'] = df['x'] + df['y']

    title_combined = alt.TitleParams('Combined Max Range' , anchor='middle')

    chart_combined = alt.Chart(df).mark_bar().encode(
        x=alt.X('node_id:N', title=None),
        y=alt.Y('combined_max', title=None),
        color=alt.Color('node_id:N', scale=alt.Scale(scheme='turbo'), legend=None),
        tooltip='node_id:N'
    ).properties(
        title=title_combined
    )

    st.altair_chart(chart_combined)

    title_x = alt.TitleParams('Max Range for X', anchor='middle')

    chart_x = alt.Chart(df).mark_bar().encode(
        x=alt.X('node_id:N', title=None),
        y=alt.Y('x', title=None),
        color=alt.Color('node_id:N', scale=alt.Scale(scheme='turbo'), legend=None),
        tooltip='node_id:N'
    ).properties(
        title=title_x
    )

    st.altair_chart(chart_x)

    title_y = alt.TitleParams('Max Range for Y', anchor='middle')

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
