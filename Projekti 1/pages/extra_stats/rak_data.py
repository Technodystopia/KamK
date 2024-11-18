def show():

    import streamlit as st
    import pandas as pd
    import altair as alt

    def load_data():
        data = pd.read_csv('data/muut/lampomuodot2.csv', header=None)
        total_rows = len(data)
        table_size = 20
        dataframes = []
        titles = []  
        for start in range(0, total_rows, table_size):
            end = start + 19
            df = data.iloc[start:end]
            if not df.empty:
                title = df.iloc[0, 0]
                titles.append(title)
                df.columns = df.iloc[0]
                df = df[1:]
                df.columns = df.columns.astype(str)  
                df.columns = [col.split('.')[0] for col in df.columns]
                df.set_index(df.columns[0], inplace=True)
                df = df.apply(pd.to_numeric, errors='coerce')
                dataframes.append(df)
        return dataframes, titles

    def create_chart(df, color_scheme):
        df_reset = df.reset_index() 
        df_melted = df_reset.melt(id_vars=df_reset.columns[0], var_name='Year', value_name='Value')
        chart = alt.Chart(df_melted).mark_bar().encode(
            x='Year:N',
            y='Value:Q',
            color=alt.Color('Year:N', scale=alt.Scale(scheme=color_scheme)),
            tooltip=[
                alt.Tooltip(field=df_reset.columns[0], type='nominal', title='Rakennustyyppi'),
                'Value',
                'Year'
            ]
        ).properties(
            width=700,
            height=400
        )
        return chart



    def main():
        dataframes, titles = load_data()
        st.title('Lämmitysmuotojen kehitys Järvenpäässä 2010-2020')

        df_index = st.selectbox("Valitse taulukko:", titles)

        selected_df = dataframes[titles.index(df_index)] if df_index in titles else dataframes[0]

        st.write(f"Taulukko: {df_index}")
        st.dataframe(selected_df)

        chart = create_chart(selected_df, color_scheme= 'turbo')
        st.altair_chart(chart, use_container_width=True)


    main()

    st.markdown("""
## Yleiskatsaus

### Rakennusdatan trendianalyysi
Tämä visualisointi tarjoaa kattavan kuvan siitä, miten eri lämmitysmuodot ovat kehittyneet tietyllä alueella tietyllä aikavälillä. Kauppiaat, jotka myyvät lämmityslaitteita tai tarjoavat lämmitykseen liittyviä palveluja, voivat hyödyntää näitä tietoja monin tavoin.

### Hyödyntäminen: Kuinka kauppias voi hyötyä rakennusdatan trendeistä

**Markkinoiden ymmärtäminen:** Ymmärrys siitä, mitkä lämmitysmuodot ovat yleistymässä tai vähenemässä, auttaa kauppiaita suuntaamaan markkinointiponnistelunsa ja varastonsa vastaavasti.

**Kohdennetut tarjoukset:** Tiedot eri rakennustyyppien suosimista lämmitysmuodoista mahdollistavat kohdennettujen tarjousten luomisen, jotka vastaavat asiakkaiden todellisia tarpeita.

**Investointipäätökset:** Trenditieto auttaa kauppiaita tekemään perusteltuja päätöksiä esimerkiksi uusien tuotteiden varastointiin tai vanhojen tuotteiden poistoon liittyen.

**Asiakassuhdemarkkinointi:** Tietämys asiakasalueen suosituista lämmitystavoista mahdollistaa räätälöityjen ylläpitopalveluiden ja huoltosopimusten tarjoamisen.

Näin ollen, tämän sovelluksen avulla kauppias voi ei ainoastaan nähdä historiallisia muutoksia, vaan myös ennakoida tulevia markkinatrendejä ja säätää toimintaansa vastaavasti.

""")

    
    st.markdown("""
### Tietosisältö
- **Sisältää tietoa**: Rakennuksista (lukumäärä, kerrosala) käyttötarkoituksen, lämmitysaineen ja -tavan mukaan 31.12.

### Aluerajat
- **Tilastossa käytetään**: 1.1.2021 aluejakoa.
- **Helsingin seutu**: Neljä pääkaupunkiseudun kuntaa (Helsinki, Espoo, Vantaa, Kauniainen) ja kymmenen kehyskuntaa (Hyvinkää, Järvenpää, Kerava, Kirkkonummi, Mäntsälä, Nurmijärvi, Pornainen, Sipoo, Tuusula, Vihti).
- **Uudenmaan maakunta**: Sisältää Helsingin, Raaseporin, Loviisan ja Porvoon seutukunnat. Kuuluu EU-alueluokituksessa NUTS-3-luokkaan.

### Luokitukset
- **Tilastovuodesta 2020**: Käytössä on Rakennusluokitus 2018. Kaikkia rakennusluokituksen luokkia ei ole luettu mukaan Tilastokeskuksen rakennuskantaan. Lisätietoja [rakennusluokituksesta](https://www2.stat.fi/fi/luokitukset/rakennus/).
- **Rakennuskanta**: Ei pääsääntöisesti sisälly kesämökit eikä maatalousrakennukset. Rakennuksen käyttötarkoituksen luokittelu perustuu pääasiassa siihen, mihin suurinta osaa rakennuksen kerrosalasta käytetään.

### Kohdejoukko ja rajaus
- **Rakennus**: Tarkoittaa erillistä, sijaintipaikalleen kiinteästi rakennettua tai pystytettyä, omalla sisäänkäynnillä varustettua rakennelmaa, joka sisältää eri toimintoihin tarkoitettua katettua ja yleensä ulkoseinien tai muista rakennelmista (rakennuksista) erottavien seinien rajoittamaa tilaa.

### Tietolähde
- **Tilastokeskus**

### Päivitystiheys
- **Vuosittain**

### Päivitetty viimeksi
- **Rakennuksia (lkm)**: 20230801 08:00
- **Kerrosala (m2)**: 20230801 08:00

""")
