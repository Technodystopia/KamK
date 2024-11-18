def show():
    import streamlit as st
    import pandas as pd
    import altair as alt
    import duckdb
    import datetime

    
    unique_node_ids = [3200, 3224, 3240, 42787, 45300, 51719, 51720, 51735, 51751, 51850, 51866, 51889,
                    51968, 51976, 51992, 52003, 52008, 52023, 52099, 52535, 53000, 53011, 53027, 53130,
                    53768, 53795, 53888, 53924, 53936, 54016, 64458]

    st.title("Ostoskärrydata visualisointi")
    node_ids_selected = st.multiselect("Ostoskärry(t): (valitse 'Kaikki' jos haluat kaikki):", ['Kaikki'] + unique_node_ids, default=['Kaikki'])
    start_date = st.date_input("Aloitus päivämäärä", value=datetime.datetime(2019, 3, 1))
    end_date = st.date_input("Lopetus päivämäärä", value=datetime.datetime(2020, 1, 31))
    aggregation = st.selectbox("Valitse aggregointitapa:", ["Tunnit", "Päivät", "Viikot", "Kuukaudet"])


    def get_transitions(start_date, end_date, aggregation, node_ids):
        conn = duckdb.connect('data/ultimate.duckdb', read_only=True)
        date_trunc_arg = {'Tunnit': 'hour', 'Päivät': 'day', 'Viikot': 'week', 'Kuukaudet': 'month'}[aggregation]
        if 'Kaikki' in node_ids:
            node_ids_filter = ""
        else:
            node_ids_filter = f"AND node_id IN ({','.join([str(nid) for nid in node_ids])})"
        
        query = f"""
        WITH TransitionData AS (
            SELECT node_id, timestamp,
                CASE WHEN (x BETWEEN 600 AND 900 AND y BETWEEN 2350 AND 2965) THEN 'start'
                        WHEN (x BETWEEN 0 AND 200 AND y BETWEEN 0 AND 2100) THEN 'end'
                END AS area
            FROM tokmanni2
            WHERE timestamp BETWEEN '{start_date}' AND '{end_date}' {node_ids_filter}
        ),
        Transitions AS (
            SELECT node_id, timestamp,
                LAG(area) OVER (PARTITION BY node_id ORDER BY timestamp) AS prev_area,
                area
            FROM TransitionData
            WHERE area IS NOT NULL
        )
        SELECT DATE_TRUNC('{date_trunc_arg}', timestamp) AS date,
            COUNT(*) AS transitions
        FROM Transitions
        WHERE prev_area = 'start' AND area = 'end'
        GROUP BY DATE_TRUNC('{date_trunc_arg}', timestamp)
        ORDER BY date;
        """
        df = conn.execute(query).fetchdf()
        conn.close()
        return df

    def get_total_distance_and_time(start_date, end_date, aggregation, node_ids):
        conn = duckdb.connect('data/ultimate.duckdb', read_only=True)
        date_trunc_arg = {'Tunnit': 'hour', 'Päivät': 'day', 'Viikot': 'week', 'Kuukaudet': 'month'}[aggregation]
        if 'Kaikki' in node_ids:
            node_ids_filter = ""
        else:
            node_ids_filter = f"AND node_id IN ({','.join([str(nid) for nid in node_ids])})"
        
        query = f"""
        WITH DistanceData AS (
            SELECT node_id, timestamp, x, y,
                LAG(x) OVER(PARTITION BY node_id ORDER BY timestamp) AS prev_x,
                LAG(y) OVER(PARTITION BY node_id ORDER BY timestamp) AS prev_y,
                LAG(timestamp) OVER(PARTITION BY node_id ORDER BY timestamp) AS prev_timestamp
            FROM tokmanni2
            WHERE timestamp BETWEEN '{start_date}' AND '{end_date}' {node_ids_filter}
        ),
        FilteredDistances AS (
            SELECT node_id, timestamp, x, y, prev_x, prev_y, prev_timestamp,
                CASE 
                    WHEN prev_x IS NOT NULL AND prev_y IS NOT NULL AND
                            ((prev_x BETWEEN 600 AND 900 AND prev_y BETWEEN 2350 AND 2965) AND
                            (x BETWEEN 0 AND 200 AND y BETWEEN 0 AND 2100))
                    THEN SQRT(POWER(x - prev_x, 2) + POWER(y - prev_y, 2))
                    ELSE 0
                END AS distance,
                CASE
                    WHEN prev_x IS NOT NULL AND prev_y IS NOT NULL AND
                            ((prev_x BETWEEN 600 AND 900 AND prev_y BETWEEN 2350 AND 2965) AND
                            (x BETWEEN 0 AND 200 AND y BETWEEN 0 AND 2100))
                    THEN EXTRACT(EPOCH FROM (timestamp - prev_timestamp)) / 60
                    ELSE 0
                END AS time_minutes
            FROM DistanceData
        )
        SELECT DATE_TRUNC('{date_trunc_arg}', timestamp) AS date, 
            SUM(distance) AS total_distance_m,
            SUM(time_minutes) AS total_time_minutes
        FROM FilteredDistances
        WHERE distance > 0
        GROUP BY DATE_TRUNC('{date_trunc_arg}', timestamp)
        ORDER BY date;
        """
        df = conn.execute(query).fetchdf()
        conn.close()
        return df

    if st.button('Lataa ja visualisoi tiedot'):
        if 'Kaikki' in node_ids_selected:
            node_ids_selected = unique_node_ids
        df_transitions = get_transitions(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), aggregation, node_ids_selected)
        df_distance_time = get_total_distance_and_time(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), aggregation, node_ids_selected)

        if not df_transitions.empty:
            chart_transitions = alt.Chart(df_transitions).mark_bar().encode(
                x='date:T',
                y='transitions:Q',
                color=alt.Color('transitions:Q', scale=alt.Scale(scheme='turbo')),
                tooltip=['date:T', 'transitions:Q']
            ).properties(title=f"Number of Transitions ({aggregation})", width=700, height=400)
            st.altair_chart(chart_transitions, use_container_width=True)
        else:
            st.write("No transitions found for the selected period or parameters.")

        if not df_distance_time.empty:
            total_distance_chart = alt.Chart(df_distance_time).mark_bar().encode(
                x='date:T',
                y=alt.Y('total_distance_m:Q', title='Total Distance (meters)'),
                color=alt.Color('total_distance_m:Q', scale=alt.Scale(scheme='turbo')),
                tooltip=['date:T', 'total_distance_m:Q']
            ).properties(title=f"Total Distance ({aggregation})", width=700, height=400)
            st.altair_chart(total_distance_chart, use_container_width=True)

            total_time_chart = alt.Chart(df_distance_time).mark_bar().encode(
                x='date:T',
                y=alt.Y('total_time_minutes:Q', title='Total Time (minutes)'),
                color=alt.Color('total_time_minutes:Q', scale=alt.Scale(scheme='turbo')),
                tooltip=['date:T', 'total_time_minutes:Q']
            ).properties(title=f"Total Time ({aggregation})", width=700, height=400)
            st.altair_chart(total_time_chart, use_container_width=True)
        else:
            st.write("No data found for total distance or time for the selected period or parameters.")




    st.markdown("""
## Yleiskatsaus
Tämä sovellus visualisoi ostoskärryjen käyttöä valitulla aikavälillä. Käyttäjä voi valita tarkasteluun tietyt ostoskärryt (node_id) ja aikavälin. Visualisointi sisältää tietoja siirtymien määrästä, kokonaismatkasta ja käytetystä ajasta, mikä auttaa ymmärtämään, kuinka ostoskärryt liikkuvat myymälässä.

## Hyödyntäminen
**Varastonhallinta:** 
- Kauppiaat voivat optimoida varastonsa ja tuotteiden saatavuutta käyttäen hyväkseen tietoa ostoskärryjen liikkeistä.

**Markkinointitoimenpiteet:** 
- Analysoidut liikkumistiedot auttavat kauppiaita sijoittamaan tuotteita ja kampanjoita strategisesti, mikä mahdollistaa paremman näkyvyyden ja myynnin.

**Henkilöstöresurssit:** 
- Tieto myymälän vilkkaimmista ajoista auttaa optimoimaan henkilökunnan käyttöä, varmistaen, että asiakaspalvelu on tehokasta kiireisimpinä aikoina.

**Asiakaskokemuksen parantaminen:** 
- Ymmärtämällä, milloin ja missä myymälässä on eniten asiakasliikennettä, kauppiaat voivat suunnitella tehokkaampia palvelukokemuksia ja vähentää ruuhkia.

**Strategiset päätökset:** 
- Pitkäaikainen datan analyysi auttaa tunnistamaan liikennetrendit ja kausivaihtelut, mikä tukee parempaa päätöksentekoa ja strategista suunnittelua.
""")

