def show():
    import duckdb
    import streamlit as st
    import altair as alt
    import pandas as pd

    con = duckdb.connect('data/stats.duckdb')

    st.markdown("""
    <div style="text-align: center"> 

    ## IQR - väli neljännespisteiden välillä

    </div>
    """, unsafe_allow_html=True)


    st.markdown("""

    ### Havaintoja Käyttäytymismalleista

    Tutkimusten alussa huomattiin, että jokainen datan piste vastaa käytännössä yhtä senttimetriä kartalla. 
    Tämän ansiosta liikkeiden analysointi on melko suoraviivaista, sillä X ja Y arvojen osalta meidän ei tarvitse 
    alkaa suorittamaan erillisiä konversioita. Alkuperäisissä tiedoissa mainittu "noin yhden senttimetrin etäisyyttä" 
    tuo kuitenkin mukanaan pienen haasteen - emme saa täysin tarkkaa kuvaa mittauksen tarkkuudesta. 
    Siitä huolimatta, tämä antaa meille mahdollisuuden tehdä varsin selkeitä havaintoja. 
    
    Huomasimme, että jotkin trendit ovat selvästi tunnistettavissa, ja vaikkapa kvartiiliväli 
    (IQR) ei yksinään tarjoa kaikkea tietoa, se paljastaa kuitenkin monia mielenkiintoisia yksityiskohtia.

    Analyysistä jouduttiin sulkemaan pois joitakin ostoskärryjä niiden puutteellisten tietojen vuoksi. 

    Jäljelle jääneistä 28 kärrystä valtaosa (20 kärryä) 
    mahtuu IQR-X-välille 5150-6190 ja IQR-Y-välille 1830-2270. Nämä alueet sijaitsevat keskeisellä 
    oikoreitillä kaupan sisällä, mikä saattaa selittää asiakasvirran keskittymisen juuri tähän kohtaan.

    ### Yksittäisten Kärryjen Käyttö

    Kahdeksan muuta kärryä poikkeavat merkittävästi lopuista. Tarkempi tutkimus, esimerkiksi  kärryjen
    kokonaismatkan analysoinnin kautta, paljastaa, että nämä kärryt ovat käytössä harvemmin. 
    Tämän voi olla syynä se, että ne ovat sijoitettu kärryasemaan viimeisiksi tai niissä on ollut joitakin teknisiä vikoja, mikä vaikuttaa niiden alhaiseen suosioon asiakkaiden keskuudessa.

    Lopullisessa analyysissä on tärkeää yhdistää IQR-arvot muihin tilastollisiin mittareihin, kuten keskiarvoon, mediaaniin, varianssiin ja keskihajontaan. Lisäksi kannattaa ottaa huomioon datan koko kirjo, 
    myös poikkeavat arvot ja ääripäät, saadaksemme kattavan kuvan liikemalleista ja datan levinnäisyydestä. 
    On myös oleellista tarkastella, miten ja missä kohtaa kaupan pohjapiirrosta nämä IQR-arvot ilmenevät, 
    jotta niiden merkitystä voidaan tulkita asianmukaisesti.

                """)

    query = "SELECT * FROM iqr"
    df = con.execute(query).fetch_df()

    df['x'] = df['x'].astype(int)
    df['y'] = df['y'].astype(int)

    df['combined_iqr'] = df['x'] + df['y']

    title_combined = alt.TitleParams('Combined Interquartile Range' , anchor='middle')

    chart_combined = alt.Chart(df).mark_bar().encode(
        x=alt.X('node_id:N', title=None),
        y=alt.Y('combined_iqr', title=None),
        color=alt.Color('node_id:N', scale=alt.Scale(scheme='turbo'), legend=None),
        tooltip='node_id:N'
    ).properties(
        title=title_combined
    )

    st.altair_chart(chart_combined)

    title_x = alt.TitleParams('Interquartile Range for X', anchor='middle')

    chart_x = alt.Chart(df).mark_bar().encode(
        x=alt.X('node_id:N', title=None),
        y=alt.Y('x', title=None),
        color=alt.Color('node_id:N', scale=alt.Scale(scheme='turbo'), legend=None),
        tooltip='node_id:N'
    ).properties(
        title=title_x
    )

    st.altair_chart(chart_x)

    title_y = alt.TitleParams('Interquartile Range for Y', anchor='middle')

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