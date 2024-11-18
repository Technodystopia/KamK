import streamlit as st
import pandas as pd
import duckdb
import datetime
import calendar
import plotly.express as px
import matplotlib.pyplot as plt


def show():
    db_file = "../data/stats.duckdb"
    tok_db = "data/ultimate.duckdb"
    con = duckdb.connect(db_file)
    con2 = duckdb.connect(tok_db)

    start_date = datetime.datetime(2019, 3, 1)
    end_date = datetime.datetime(2020, 1, 31)

    st.markdown("# Valitse tarkkailtava ajanjakso:")
    start_date_selected = st.date_input('Ensimmäinen päivämäärä:', start_date, min_value=start_date, max_value=end_date)
    end_date_selected = st.date_input('Viimeinen päivämäärä:', end_date, min_value=start_date, max_value=end_date)

    start_year = start_date_selected.year
    start_month = start_date_selected.month
    start_day = start_date_selected.day

    end_year = end_date_selected.year
    end_month = end_date_selected.month
    end_day = end_date_selected.day

    start_hour, end_hour = st.slider('Aikaväli:', 7, 23, (7, 23), 1)

    if start_date_selected > end_date_selected:
                # Special logic for not using BETWEEN
                query_part1 = f"SELECT timestamp, COUNT(x) FROM tokmanni2 WHERE timestamp >= '{start_date_selected}' AND timestamp <= '{start_date_selected.replace(day=calendar.monthrange(start_date_selected.year, start_date_selected.month)[1])}'"
                query_part2 = f"SELECT timestamp, COUNT(x) FROM tokmanni2 WHERE timestamp >= '{end_date_selected.replace(day=1)}' AND timestamp <= '{end_date_selected}'"
                query = f"({query_part1}) UNION ALL ({query_part2}) ORDER BY timestamp"
    else:
        # Safe to use BETWEEN
        query = f"SELECT timestamp, COUNT(x) FROM tokmanni2 WHERE timestamp BETWEEN '{start_date_selected}' AND '{end_date_selected}' GROUP BY timestamp ORDER BY timestamp"
    result = con2.execute(query)
    df = result.fetchdf()
    df = df.resample('h', on='timestamp').count()


    if start_date_selected > end_date_selected:
                # Special logic for not using BETWEEN
                query_part1 = f"SELECT * FROM weather WHERE Time >= '{start_date_selected}' AND Time <= '{start_date_selected.replace(day=calendar.monthrange(start_date_selected.year, start_date_selected.month)[1])}'"
                query_part2 = f"SELECT * FROM weather WHERE Time >= '{end_date_selected.replace(day=1)}' AND Time <= '{end_date_selected}'"
                query = f"({query_part1}) UNION ALL ({query_part2}) ORDER BY Time"
    else:
        # Safe to use BETWEEN
        query = f"SELECT * FROM weather WHERE Time BETWEEN '{start_date_selected}' AND '{end_date_selected}' ORDER BY Time"
    result2 = con.execute(query)
    df1 = result2.fetchdf()
    df1 = df1.sort_values(['Time'], ascending =[True]).drop_duplicates(['Time']).reset_index(drop=True)
    df1.set_index("Time", inplace=True)

    #TODO diagrammit: päivä x-akselille, y-akselille tokmannidata ja toiselle y-akselille sää, vaikka lämpötila
    # Search criteria
    start_hour1 = datetime.time(start_hour)
    end_hour1 = datetime.time(end_hour)
    search = datetime.datetime.combine(start_date_selected, start_hour1)
    end_search = datetime.datetime.combine(end_date_selected, end_hour1)

    weather_df = df1[(df1.index >= search) & (df1.index <= end_search)]
    tokmanni_df = df[(df.index >= search) & (df.index <= end_search)]
    search_df = pd.concat([tokmanni_df, weather_df], axis=1)
    # print(search_df.columns)
    # print(search_df.head(20))


    ###! Matplotlib, lämpötilan vaikutus ostoskärryasiakkaiden määrään
    st.markdown("### Lämpötilan vaikutus ostoskärryasiakkaiden määrään")
    test, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel("Päivämäärä")
    ax1.set_ylabel("Lämpötila (°C)")
    ax1.plot(search_df.index, search_df['Temperature'], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()

    color = 'tab:green'
    ax2.set_ylabel("Määrä (pistettä)", color=color)
    ax2.plot(search_df.index, search_df['count(x)'], color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    st.pyplot(test)

    column_to_normalize = 'count(x)'
    search_df[column_to_normalize] = (search_df[column_to_normalize] - search_df[column_to_normalize].min()) / (search_df[column_to_normalize].max() - search_df[column_to_normalize].min())

    ###! Plotly normalisoitu graafi, sateen voimakkuus verrattuna normalisoituun kärryjen käyttöasteeseen
    st.markdown("### Sateen voimakkuus verrattuna normalisoituun kärryjen käyttöasteeseen")
    fig1 = px.line(search_df, x=search_df.index, y=[search_df['Rain intensity'], search_df['count(x)']])
    fig1.update_xaxes(title="Päivämäärä")
    fig1.update_yaxes(title="Sademäärä (mm), käyttöaste (0-1)")
    st.plotly_chart(fig1)
    
    ###! Plotly graafi, yleisiä säähommia
    st.markdown("### Yleistä säädataa")
    tab1, tab2, tab3 = st.tabs(["Lämpötila, kosteus, kastepiste", "Tuulen ja puuskien nopeus", "Pilvipeite ja lumen syvyys"])
    with tab1:
        fig = px.line(search_df, x=search_df.index, y=[search_df['Temperature'], search_df['Humidity']])
        fig.update_xaxes(title="Päivämäärä")
        st.plotly_chart(fig)
    with tab2:
        fig = px.bar(search_df, x=search_df.index, y=[search_df['Wind speed'], search_df['Gust speed']])
        fig.update_xaxes(title="Päivämäärä")
        st.plotly_chart(fig)
    with tab3:
        fig = px.bar(search_df, x=search_df.index, y=[search_df['Cloud cover'], search_df['Snow depth']])
        fig.update_xaxes(title="Päivämäärä")
        st.plotly_chart(fig)

    st.markdown("""
                ### Arvojen selitykset
                * Temperature / Lämpötila = Ilman lämpötila kahden metrin korkeudella.
                * Wind speed / Tuulen nopeus = Tuulen nopeuden keskiarvo 10 minuutin aikana, yksikkö m/s.
                * Gust speed / Puuskanopeus = Suurin kolmen sekunnin tuulen nopeuden keskiarvo edeltävän 10 minuutin aikana, yksikkö m/s.
                * Wind direction / Tuulen suunta = Ilmaistaan asteina, joissa 0 tarkoittaa tyyntä ja 360, että tuuli puhaltaa pohjoisesta etelään.
                * Cloud cover / Pilvisyys = Ottaa huomioon kaikki pilvikerrokset. 0 on täysin pilvetön ja 8 täysin pilvinen. 9 kertoo, ettei pilvisyyttä voitu määrittää.
                * Humidity / Kosteus = Ilman suhteellinen kosteusarvo, välillä 0-100%.
                * Dew point / Kastepistelämpötila = Lämpötila, jossa ilman kosteus tiivistyy vedeksi tai jääksi.
                * Rain amount / Sademäärä = Yksikkönä millimetri, joka vastaa yhtä litraa vettä neliömetriä kohti. Laskettu alkuperäisestä sateen intensiteetistä kymmenen minuutin aikana.
                * Rain intensity / Sateen voimakkuus = Jos sataa vähän, sademäärä on 0,3-0,9 millimetriä. Runsasta sade on puolestaan silloin, kun sademäärä on vähintään 4,5 millimetriä.
                * Snow depth / Lumen syvyys = Mittaa lumen syvyyttä automaattiasemilla, tarkkuus noin +- 2cm.
                * Air pressure / Ilmanpaine = Ilmoittaa ilmanpaineen merenpinnan tasolle reduktoituna.

                Lähde: [Ilmatieteen laitos](https://www.ilmatieteenlaitos.fi/lisatietoa-havaintosuureista)
                """)
    st.markdown("""
                Kauppias voi hyötyä visualisoidusta säädatasta yhdistettynä ostoskärryjen käyttömääriin monin eri tavoin:
                1. **Kysynnän ennustaminen:** Kun kauppias yhdistää säädatan ostoskärryjen käyttöön, hän voi paremmin ennustaa asiakkaiden 
                ostokäyttäytymistä eri sääolosuhteissa. Esimerkiksi sateisella säällä ihmiset saattavat tehdä enemmän verkko-ostoksia tai 
                suosia tietyntyyppisiä tuotteita, kuten sateenvarjoja tai sadesään vaatteita.
                2. **Varastonhallinta:** Tarkkailemalla ostoskärryjen käyttöä ja yhdistämällä sen sääolosuhteisiin, kauppias voi 
                hallita varastotasoaan tehokkaammin. Esimerkiksi lämpimänä päivänä saattaa olla enemmän kysyntää grillihiilille 
                ja virvoitusjuomille, kun taas kylmänä päivänä kysyntä voi keskittyä lämpimiin juomiin ja kauden mukaisiin vaatteisiin.
                3. **Markkinointikampanjoiden suunnittelu:** Visualisoitu säädata yhdistettynä ostoskärryjen käyttöön voi auttaa kauppiasta 
                suunnittelemaan markkinointikampanjoita, jotka kohdistuvat tietyntyyppisiin sääolosuhteisiin. Esimerkiksi aurinkoisena 
                päivänä kauppias voi mainostaa ulkoilma-aktiviteetteihin sopivia tuotteita, kun taas kylminä päivinä hän voi korostaa 
                lämpimiä ruokia tai kotiin sopivia tuotteita.
                4. **Asiakaskokemuksen parantaminen:** Seuraamalla ostoskärryjen käyttöä sään mukaan kauppias voi tarjota asiakkailleen 
                paremman ostokokemuksen. Esimerkiksi hän voi varautua lisäämään henkilökuntaa kassojen läheisyyteen ruuhka-aikoina 
                tai tarjota sääolosuhteisiin sopivia tuotteita esillepanolla ja tarjouksilla.

                Yhdistämällä visualisoitu säädata ostoskärryjen käyttöön, kauppias voi siis parantaa liiketoiminnan tehokkuutta, 
                varastonhallintaa, markkinointikampanjoiden suunnittelua ja asiakaskokemusta. 
                (Lähde: [ChatGPT 3.5](https://chatgpt.com/))
                """)

    st.markdown("""
                Tästä datasta ei voida kuitenkaan päätellä asiakkaiden kokonaismäärää, sillä sijaintidata koskee vain ostoskärryjen kanssa
                kulkevia asiakkaita. Häilyviä päätelmiä voidaan kuitenkin tehdä. Näiden päätelmien laatua voisi parantaa hankkimalla 
                sijantidataa esimerkiksi myös ostoskorien osalta tai asettamalla oviaukoille automaattinen kävijälaskuri ja 
                keräämällä siitä dataa.
                """)

    con.close()
    con2.close()
