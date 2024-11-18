def show():
    import duckdb
    import streamlit as st
    import altair as alt
    import pandas as pd

    con = duckdb.connect('data/stats.duckdb')

    st.markdown("""
    <div style="text-align: center"> 

    ## Kurtosis - Huipukkuus

    </div>
    """, unsafe_allow_html=True)


    st.markdown("""
    Tämä kuvaa jakauman huipukkuutta. Suurempi kurtosis tarkoittaa, että data on enemmän keskittynyt keskiarvon ympärille, kun taas pienempi kurtosis tarkoittaa, että data on enemmän hajallaan.
                

    ### Havaintoja Kurtosis-arvoista
                
    - Yhteensä kärryjä: 28
    - Platykurtiset kärryt (litteä huipukkuus):23 kärryä
    - Leptokurtiset kärryt (terävä huipukkuus): 5 kärryä
    - Erityisesti huomioitava: Kärry 53027, joka on merkittävästi leptokurtinen ja omaa myös lievästi leptokurtisen y-koordinaatin.
                
    ### Huipukkuuden ja käytön suhde
                
    Kurtosis-arvojen suuret poikkeamat korreloivat suoraan kärryjen käytön vähyyteen. Paljon käytetyt kärryt näyttävät tasaantuvan seuraaviin arvoihin

    - Kurtosis_X: -1.34
    - Kurtosis_Y: -0.69

    Nämä arvot ovat keskiarvot useimmiten käytettyjen kärryjen Kurtosis-arvoista.
                
    ### Odotukset liikehdinnästä
                
    Kärryjen tasainen liikehdinta ympäri kauppaa ja erilaisten ihmisten käyttö tasoittavat huipukkuutta, johtaen jakaumaan, jossa ei ilmaannu selkeitä huippuarvoja tietyssä kohdassa.
                """)

    query = "SELECT * FROM kurtosis"
    df = con.execute(query).fetch_df()

    df['x'] = df['x'].astype(int)
    df['y'] = df['y'].astype(int)

    df['combined_kurtosis'] = df['x'] + df['y']

    title_combined = alt.TitleParams('Combined Kurtosis Range' , anchor='middle')

    chart_combined = alt.Chart(df).mark_bar().encode(
        x=alt.X('node_id:N', title=None),
        y=alt.Y('combined_kurtosis', title=None),
        color=alt.Color('node_id:N', scale=alt.Scale(scheme='turbo'), legend=None),
        tooltip='node_id:N'
    ).properties(
        title=title_combined
    )

    st.altair_chart(chart_combined)

    title_x = alt.TitleParams('Kurtosis Range for X', anchor='middle')

    chart_x = alt.Chart(df).mark_bar().encode(
        x=alt.X('node_id:N', title=None),
        y=alt.Y('x', title=None),
        color=alt.Color('node_id:N', scale=alt.Scale(scheme='turbo'), legend=None),
        tooltip='node_id:N'
    ).properties(
        title=title_x
    )

    st.altair_chart(chart_x)

    title_y = alt.TitleParams('Kurtosis Range for Y', anchor='middle')

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
