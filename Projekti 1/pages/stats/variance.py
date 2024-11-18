def show():
    import duckdb
    import streamlit as st
    import altair as alt
    import pandas as pd

    con = duckdb.connect('data/stats.duckdb')

    st.markdown("""
    <div style="text-align: center"> 

    ## Variance - Varianssi

    </div>
    """, unsafe_allow_html=True)


    st.markdown("""
    Tämä on keskihajonnan neliö ja se kuvaa datanäytteiden hajontaa.
                
    ## Alustavat huomiot varianssista

    Varianssiarvoja tutkittaessa, samat "huonot kärryt", jotka nousivat esiin myös jo mm. IQR-analyysissä, osoittavat jälleen, etteivät tietyt kärryt vedä asiakkaita puoleensa. Syynä voi olla kärryn sijainti kärryrivin lopussa tai jonkinlaiset mekaaniset viat, jotka vaikuttavat käyttöön.
    Korkeat arvot X-muuttujassa ovat realistisia, ottaen huomioon tietokannan laajuuden. Nämä suuret luvut kertovat laajasta liikkumisalueesta kaupassa, mikä  itsessään on jo mielenkiintoinen havainto.
    Varianssianalyysi paljastaa, että suurimmalla osalla kärryistä (21 kärryllä) on huomattavan suuri varianssi, mikä viittaa erittäin "sekavaan" liikkumiskäyttäytymiseen kaupan sisällä.
    Seitsemän kärryä osoittaa pienempää varianssia, jotka ovat tuttuja myös muista havainnoista. Niiden vähäisempi käyttö voi kertoa pienemmästä suosiosta tai tietyntyyppisistä ostoskäyttäytymisistä.

     ## Lisähuomautukset

    On olennaista tunnistaa kohinan lähteet ja ymmärtää niiden vaikutukset varianssiin, jotta voimme saada tarkemman kuvan datan todellisesta luonteesta. ETL-prosessi filtteröi suurimman osan kohinasta, mutta yksittäiset ja pienemmät staattiset virheet voivat olla mahdollisia.
    Kaupan layoutilla ja tuotejärjestyksellä on merkittävä vaikutus siihen, miten asiakkaat liikkuvat tilassa, ja se voi osaltaan selittää havaittua varianssia.

    Nämä havainnot tuovat esiin arvokkaita alustavia oivalluksia ostoskärryjen liikkeistä ja asiakaskäyttäytymisestä, auttaen meitä parantamaan kaupan järjestelyjä ja asiakaskokemusta.

                """)

    query = "SELECT * FROM variance"
    df = con.execute(query).fetch_df()

    df['x'] = df['x'].astype(int)
    df['y'] = df['y'].astype(int)

    df['combined_variance'] = df['x'] + df['y']

    title_combined = alt.TitleParams('Combined Variance Range' , anchor='middle')

    chart_combined = alt.Chart(df).mark_bar().encode(
        x=alt.X('node_id:N', title=None),
        y=alt.Y('combined_variance', title=None),
        color=alt.Color('node_id:N', scale=alt.Scale(scheme='turbo'), legend=None),
        tooltip='node_id:N'
    ).properties(
        title=title_combined
    )

    st.altair_chart(chart_combined)

    title_x = alt.TitleParams('Variance Range for X', anchor='middle')

    chart_x = alt.Chart(df).mark_bar().encode(
        x=alt.X('node_id:N', title=None),
        y=alt.Y('x', title=None),
        color=alt.Color('node_id:N', scale=alt.Scale(scheme='turbo'), legend=None),
        tooltip='node_id:N'
    ).properties(
        title=title_x
    )

    st.altair_chart(chart_x)

    title_y = alt.TitleParams('Variance Range for Y', anchor='middle')

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
