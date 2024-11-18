def show():
    import streamlit as st
    import pandas as pd
    import altair as alt
    import duckdb
    import os


    conn = duckdb.connect(database=':memory:', read_only=False)

    def load_data_to_duckdb(data_path):
        data = pd.read_csv(data_path, on_bad_lines='skip')
        data['StartDate'] = pd.to_datetime(data['StartDate'].str.strip(), errors='coerce', dayfirst=True)
        data['EndDate'] = pd.to_datetime(data['EndDate'].str.strip(), errors='coerce', dayfirst=True)
        conn.register('events', data)
        conn.execute("CREATE VIEW IF NOT EXISTS event_view AS SELECT * FROM events")

    def create_events_chart(start_date, end_date, aggregation, color_scheme):
        date_trunc_arg = {
            'Päivittäin': 'day',
            'Viikoittain': 'week',
            'Kuukausittain': 'month'
        }[aggregation]
        query = f"""
        SELECT DATE_TRUNC('{date_trunc_arg}', StartDate) AS period, COUNT(*) AS event_count
        FROM event_view
        WHERE StartDate >= '{start_date}' AND EndDate <= '{end_date}'
        GROUP BY DATE_TRUNC('{date_trunc_arg}', StartDate)
        ORDER BY period
        """
        result = conn.execute(query).df()
        chart = alt.Chart(result).mark_bar().encode(
            x=alt.X('period:T', title=f'{aggregation} alkaen'),
            y=alt.Y('event_count:Q', title='Tapahtumien määrä'),
            color=alt.Color('event_count:Q', scale=alt.Scale(scheme=color_scheme)),
            tooltip=[alt.Tooltip('period:T', title='Ajanjakso'), 'event_count']
        ).properties(
            title=f'Tapahtumat {aggregation.lower()} valitulla aikavälillä',
            width=700,
            height=400
        )
        return chart

    def main():
        data_path = os.path.abspath('data/muut/jarvenpaa_events.csv')
        load_data_to_duckdb(data_path)

        st.title('Järvenpään Tapahtumat')

        start_date = st.date_input("Aloitus päivämäärä", value=pd.Timestamp('2019-01-01'))
        end_date = st.date_input("Lopetus päivämäärä", value=pd.Timestamp('2020-03-01'))
        aggregation = st.selectbox("Valitse aggregointitapa:", ["Päivittäin", "Viikoittain", "Kuukausittain"])

        if start_date > end_date:
            st.error('Aloituspäivämäärä ei voi olla suurempi kuin lopetuspäivämäärä. Säädä päivämäärät.')
            st.stop()

        chart = create_events_chart(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), aggregation, color_scheme='turbo')
        st.altair_chart(chart, use_container_width=True)

        event_query = f"""
        SELECT * FROM event_view
        WHERE StartDate >= '{start_date.strftime('%Y-%m-%d')}' AND EndDate <= '{end_date.strftime('%Y-%m-%d')}'
        ORDER BY StartDate
        """
        events_df = conn.execute(event_query).df()
        st.write("Valitun aikavälin tapahtumat:")
        st.dataframe(events_df)

    main()

    st.markdown("""
## Yleiskatsaus

### Tapahtumien trendianalyysi
Kauppiaat voivat tarkastella tapahtumien määrän muutoksia päivittäin, viikoittain tai kuukausittain. Tämä auttaa ymmärtämään asiakasvirtojen muutoksia eri aikoina ja suunnittelemaan tarjouksia sekä kampanjoita, jotka ajoitetaan yhteen suosittujen tapahtumien kanssa.

### Hyödyntäminen

- **Varastonhallinta:** Tapahtumien aikataulutiedot auttavat kauppiaita optimoimaan varastonsa, jotta suosituimpien tuotteiden saatavuus on taattu tapahtumien aikana.

- **Markkinointitoimenpiteet:** Kauppiaat voivat kohdentaa mainontaansa ja markkinointitoimensa niin, että ne osuvat yhteen suurten tapahtumien kanssa, jolloin potentiaalinen asiakaskunta on suurimmillaan.

- **Henkilöstöresurssien suunnittelu:** Tieto tapahtumapäivien ja -jaksojen asiakasvirroista auttaa kauppiaita suunnittelemaan työvuorot ja henkilöstöresurssit tehokkaasti.

- **Asiakaskokemuksen parantaminen:** Ymmärtämällä, milloin liikkeellä on eniten asiakkaita, kauppiaat voivat suunnitella parempia asiakaskokemuksia, kuten nopeampaa palvelua tai lisäaktiviteetteja.

- **Strategiset päätökset:** Pitkän aikavälin datan analysointi auttaa tunnistamaan trendejä ja kausivaihteluita, mikä puolestaan auttaa strategisessa suunnittelussa ja päätöksenteossa.

- [Lähde](https://www.menoinfo.fi/jarvenpaa) Menoinfo.fi
""")

