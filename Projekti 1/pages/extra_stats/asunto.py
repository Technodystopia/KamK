def show():
    import pandas as pd
    import streamlit as st
    import plotly.express as px

    st.title("Asuntokunnat Järvenpäässä")

    df = pd.read_csv("data/muut/asuntokunnat/asuntokunnat0.csv", sep=";")
    df1 = pd.read_csv("data/muut/asuntokunnat/asuntokunnat1.csv", sep=";")
    df2 = pd.read_csv("data/muut/asuntokunnat/asuntokunnat2.csv", sep=";")
    df3 = pd.read_csv("data/muut/asuntokunnat/asuntokunnat3.csv", sep=";")
    df4 = pd.read_csv("data/muut/asuntokunnat/asuntokunnat4.csv", sep=";")

    df_melted = df.melt(id_vars=df.columns[0], var_name="Vuosi", value_name="Arvo")

    fig_line = px.line(df_melted, x="Vuosi", y="Arvo", color=df.columns[0], title="Asuntokuntien määrä Järvenpäässä vuosittain")

    st.plotly_chart(fig_line)

    st.markdown("""
    - Asukaslukumäärän kasvu: Järvenpään asukasluku on kasvanut vuodesta 1985 lähtien, mikä voi olla positiivinen merkki kauppiaille. Kasvava väestö tarkoittaa yleensä kasvavaa potentiaalista asiakaskuntaa, mikä voi lisätä kauppojen asiakasmääriä ja liikevaihtoa.
    - Asuntokuntien määrän kasvu: Asuntokuntien määrän kasvu viittaa siihen, että alueella on enemmän perheitä ja kotitalouksia, mikä voi lisätä kaupankäyntiä ja kulutusta. Perheillä on yleensä enemmän tarpeita ja ostovoimaa kuin yksin asuvilla.
    - Henkilölukujen jakautuminen: Tarkastelemalla henkilölukujen jakautumista eri kategorioiden (1, 2, 3, jne.) mukaan voidaan saada tarkempaa tietoa asiakasprofiileista ja heidän mahdollisista tarpeistaan. Esimerkiksi suuri määrä 1-2 hengen kotitalouksia voi viitata siihen, että kaupan kannattaa panostaa pienempiin tuotepakkauksiin ja yksilöllisiin tarpeisiin vastaaviin tuotteisiin.
    - Vuotuisten vaihteluiden huomioiminen: On tärkeää ottaa huomioon, että vuosittaiset vaihtelut voivat vaikuttaa kaupankäyntiin. Esimerkiksi taloudelliset tekijät, kuten työllisyystilanne, voivat vaikuttaa asiakkaiden ostovoimaan ja siten myös kaupan suorituskykyyn.
    - Tulevaisuuden ennustaminen: Analysoimalla menneitä trendejä kauppias voi yrittää ennustaa tulevia muutoksia ja valmistautua niihin. Esimerkiksi väestönkasvun hidastuminen voi vaikuttaa kaupan kasvuun, kun taas odotettavissa oleva väestön ikääntyminen voi merkitä kysynnän muutoksia tietyille tuoteryhmille.
    """)

    selected_year = st.selectbox("Valikoi vuosi", df.columns[1:])

    fig_pie0 = px.pie(df, values=selected_year, names=df.columns[0], title=f"Vuoden {selected_year} prosentuaalinen data")

    fig_pie1 = px.pie(df1, values=selected_year, names=df1.columns[0], title=f"Vuoden {selected_year} Erillinen pientalo")

    fig_pie2 = px.pie(df2, values=selected_year, names=df2.columns[0], title=f"Vuoden {selected_year} Rivi- tai ketjutalo")

    fig_pie3 = px.pie(df3, values=selected_year, names=df3.columns[0], title=f"Vuoden {selected_year} Asuinkerrostalo")

    fig_pie4 = px.pie(df4, values=selected_year, names=df4.columns[0], title=f"Vuoden {selected_year} Muu tai tuntematon")

    fig_bar = px.bar(df, x=df.columns[0], y=selected_year, title=f"Vuoden {selected_year} asuntokuntien määrä")

    st.markdown("## Asuntokuntien määrä eri asuntotyypeissä")

    st.markdown("""Kauppiaan kannattaa tarkastella näitä tietoja yhdessä muiden paikallisten taloudellisten ja demografisten indikaattoreiden kanssa saadakseen kokonaiskuvan markkinatilanteesta ja suunnitellessaan liiketoiminnan kehitystä ja markkinointistrategioita.""")

    st.plotly_chart(fig_pie0)

    st.plotly_chart(fig_pie1)

    st.plotly_chart(fig_pie2)

    st.plotly_chart(fig_pie3)

    st.plotly_chart(fig_pie4)

    df = pd.read_csv("data/muut/asuntokunnat/asuntokunnat.csv", sep=";")

    st.markdown("## Järvenpään asuntokunnat henkilöluvun ja vanhimman iän mukaan")

    fig_bar = px.bar(df, x=df.columns[0], y=df.columns[1:], title="Järvenpään asuntokuntien määrä")

    st.plotly_chart(fig_bar)

    st.markdown("""
    - Tietosisältö - Sisältää tietoja asuntokuntien määrästä henkilöluvun mukaan.
    - Tietolähde - Tilastokeskus.
    - Kohdejoukko ja rajaus
        - Asuntokunnan muodostavat kaikki samassa asuinhuoneistossa vakinaisesti asuvat henkilöt.
        - Asuntokuntia ei muodosteta henkilöistä, jotka ovat väestötietojärjestelmän mukaan vakinaisesti kirjoilla laitoksissa, asunnottomia, ulkomailla tai tietymättömissä.
        - Henkilöt, joiden asunto ei täytä asuinhuoneisto määritelmää, eivät myöskään muodosta asuntokuntia.
    - Tietojen luotettavuus - Tiedot henkilöiden asuinpaikasta saadaan väestötietojärjestelmään muuttoilmoituksen kautta. Väestö yhdistetään asuntokunniksi asuinpaikkatunnuksen mukaan ohjelmallisesti.
    - Päivitystiheys- Vuosittain
    - Päivitetty viimeksi - 20230705 09:00
    """)
