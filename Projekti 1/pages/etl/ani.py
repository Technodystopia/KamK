def show():
    import streamlit as st
    import pandas as pd
    import altair as alt

    csv_file_path = 'data/muut/etl.csv'

    data = pd.read_csv(csv_file_path)
    data.columns = data.columns.str.strip()

    column_order = ['Node_id', 'Original', 'Step0', 'Step1', 'Step2', 'Step3', 'Step4', 'Step5', 'Step6', 'Time', 'Speed']

    data = data[column_order]

    data_melted = data.melt(id_vars='Node_id', var_name='Step', value_name='Value')

    step_order = ['Original', 'Step0', 'Step1', 'Step2', 'Step3', 'Step4', 'Step5', 'Step6', 'Time', 'Speed']
    data_melted['Step'] = pd.Categorical(data_melted['Step'], categories=step_order, ordered=True)

    chart = alt.Chart(data_melted).mark_line().encode(
        x=alt.X('Step', title='Filtter stepit'),
        y=alt.Y('Value', title='Datapisteiden määrä'),
        color=alt.Color('Node_id:N', scale=alt.Scale(scheme='turbo'), legend=alt.Legend(orient='bottom', columns=4))
    )

    chart = chart.properties(width=800, height=1000)


    st.markdown("ETL-putken modulaarinen rakenne auttaa visualisoimaan datan kulkua ja muutoksia eri vaiheissa. Tässä visualisoinnissa on esitetty datan määrä eri vaiheissa.")

    st.markdown("Datasta suurin osa on irrelevanttia, joten sitä suodatetaan pois alkuperäisestä datasta. Dataa on käsitelty useissa eri vaiheissa, kunnes lopulta on saatu haluttu lopputulos. ")

    st.altair_chart(chart)

    st.markdown("Osa ostoskärryistä (Node_id) on selvästi käyttämättömiä, näiden kärryjen osalta missä dataa on todella vähän, ne ovat poistettu tilastollisista laskelmista. Tämä on tehty, jotta datasta saadaan mahdollisimman puhdasta ja relevanttia.")

    st.table(data)

    st.markdown("""
                
    # Filtterit
                
    - Original = Alkuperäinen data mistä on poistettu sarakkeet q ja z turhana
    - Step0 = Kaupan koordinaattien ulkopuolinen data on poistettu
    - Step1 = Kaupan oikean yläkulman seinien ulkopuolinen data on poistettu
    - Step2 = Kaupan oikean alakulman seinien ulkopuolinen data on poistettu
    - Step3 = Kaupan vasemman alakulman seinien ulkopuolinen data on poistettu
    - Step4 = Kaupan vasemman alakulman sisemmän neliön seinien ulkopuolinen data on poistettu
    - Step5 = Isomman Latausaseman data on poistettu
    - Step6 = Pienemmän Latausaseman data on poistettu          
    - Time  = Kaupan aukioloaikojen ulkopuolinen data on poistettu         
    - Speed = Liian nopeasti liikkuvat datapisteet on poistettu          
""")

