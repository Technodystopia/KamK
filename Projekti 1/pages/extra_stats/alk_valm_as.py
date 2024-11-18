def show():
    import streamlit as st
    import pandas as pd
    import plotly.express as px

    def load_data():
        df_started = pd.read_csv('data/muut/alkaneetasunnotmal2016_2019.csv')
        df_completed = pd.read_csv('data/muut/valmistuneetasunnotmal2016_2019.csv')
        df_started['alkvuosi'] = pd.to_numeric(df_started['alkvuosi'], errors='coerce')
        df_completed['valmvuosi'] = pd.to_numeric(df_completed['valmvuosi'], errors='coerce')
        return df_started, df_completed

    def create_pie_charts(df, year, municipality, column_year, column_housing, column_funding):
        filtered_df = df[(df[column_year] == year) & (df['kuntanimi'] == municipality)]
        pie_chart_housing = px.pie(filtered_df, values='asuntolkm', names=column_housing, title=f"Asuntomäärät talotyypeittäin, {year}")
        pie_chart_funding = px.pie(filtered_df, values='asuntolkm', names=column_funding, title=f"Asuntomäärät rahoitusmuodoittain, {year}")
        return pie_chart_housing, pie_chart_funding

    def create_line_chart(df, column_year):
        yearly_data = df.groupby(column_year)['asuntolkm'].sum().reset_index()
        line_chart = px.line(yearly_data, x=column_year, y='asuntolkm', title='Kaikkien asuntojen määrän kehitys 2016-2019')
        line_chart.update_layout(xaxis=dict(tickmode='array', tickvals=yearly_data[column_year], ticktext=[int(x) for x in yearly_data[column_year]]))
        return line_chart

    def create_combined_line_chart(df_started, df_completed, municipality):
        filtered_started = df_started[df_started['kuntanimi'] == municipality]
        filtered_completed = df_completed[df_completed['kuntanimi'] == municipality]
        yearly_started = filtered_started.groupby('alkvuosi')['asuntolkm'].sum().reset_index()
        yearly_completed = filtered_completed.groupby('valmvuosi')['asuntolkm'].sum().reset_index()
        yearly_started.rename(columns={'alkvuosi': 'Vuosi', 'asuntolkm': 'Alkaneet'}, inplace=True)
        yearly_completed.rename(columns={'valmvuosi': 'Vuosi', 'asuntolkm': 'Valmistuneet'}, inplace=True)
        combined_data = pd.merge(yearly_started, yearly_completed, on='Vuosi', how='outer').fillna(0)
        fig = px.line(combined_data, x='Vuosi', y=['Alkaneet', 'Valmistuneet'], labels={'value': 'Asuntojen määrä', 'Vuosi': 'Vuosi'},
                    title=f'Alkaneiden ja valmistuneiden asuntojen määrän kehitys vuosina 2016–2019 kunnassa {municipality}')
        fig.update_layout(xaxis=dict(tickmode='array', tickvals=combined_data['Vuosi'], ticktext=[int(x) for x in combined_data['Vuosi']]))
        return fig

    def main():
        st.title("Asuntotuotannon Visualisointi")
        df_started, df_completed = load_data()
        years = sorted(set(df_started['alkvuosi'].dropna().unique()).union(df_completed['valmvuosi'].dropna().unique()))
        municipalities = sorted(set(df_started['kuntanimi'].unique()).union(df_completed['kuntanimi'].unique()))
        selected_year = st.selectbox("Valitse vuosi:", years)
        selected_municipality = st.selectbox("Valitse kunta:", municipalities)
        st.markdown("""

        ## Hyödyntäminen: Kuinka kauppias voi hyötyä asuntotuotannon datasta

        ### Yleiskatsaus
        Tämä visualisointi tarjoaa kauppiaille arvokasta tietoa asuntotuotannon trendeistä ja dynamiikasta Helsingin seudulla. Data kattaa uusien asuntojen alkamisen ja valmistumisen eri kunnissa, minkä avulla kauppiaat voivat ymmärtää paremmin alueellista kasvua ja väestönmuutoksia.

        ### Trendianalyysi
        Kauppiaat voivat seurata asuntotuotannon trendejä vuosien varrella, tunnistaa kasvavat alueet ja arvioida potentiaalista asiakaskuntaa. Tämä auttaa ennakoimaan markkinoiden kehitystä ja suunnittelemaan tulevia toimia.

        ### Hyödyntäminen
        1. **Varastonhallinta**: Ymmärtämällä missä ja milloin uusia asuntoja valmistuu, kauppiaat voivat optimoida varastonsa vastaamaan kysyntää. Esimerkiksi suuret kerrostalohankkeet voivat lisätä tarvetta kodinkoneille ja sisustustarvikkeille.
        
        2. **Markkinointitoimenpiteet**: Tiedot asuntotuotannon sijainnista ja tyypeistä auttavat kohdentamaan markkinointikampanjoita tehokkaammin. Kauppiaat voivat suunnata mainontaa erityisesti niille alueille, joilla uusia asuntoja rakennetaan.

        3. **Henkilöstöresurssit**: Alueen kasvu ja asuntotuotannon lisääntyminen voivat vaatia lisää henkilöstöä palvelemaan kasvavaa asiakaskuntaa. Kauppiaat voivat suunnitella henkilöstötarpeitaan ja koulutusta ennakkoon.

        4. **Asiakaskokemuksen parantaminen**: Tieto uusien asuntojen valmistumisesta auttaa kauppiaita ymmärtämään, millaisia tuotteita ja palveluita uudet asukkaat mahdollisesti tarvitsevat, mikä parantaa asiakaskokemusta.

        5. **Strategiset päätökset**: Pitkän aikavälin suunnittelussa ja uusien myymälöiden sijaintien valinnassa asuntotuotannon data tarjoaa perustan päätöksenteolle. Tieto siitä, mihin suuntaan kaupunki laajenee, voi ohjata uusien liiketilojen hankkimista.

        ### Yhteenveto
        Asuntotuotannon data ei ainoastaan valaise alueen väestökehitystä vaan myös tarjoaa kauppiaille mahdollisuuden ennakoivasti sopeuttaa liiketoimintastrategioitaan vastaamaan tulevaisuuden haasteita ja mahdollisuuksia.

        """
        )
        st.markdown(f"### Valitut vuosi: {selected_year}, kunta: {selected_municipality}")

        st.subheader("Alkaneet Asunnot")
        pie_chart_started_housing, pie_chart_started_funding = create_pie_charts(df_started, selected_year, selected_municipality, 'alkvuosi', 'talotyyppi', 'rahmuoto')
        st.plotly_chart(pie_chart_started_housing)
        st.plotly_chart(pie_chart_started_funding)
        line_chart_started = create_line_chart(df_started, 'alkvuosi')
        st.plotly_chart(line_chart_started)
        st.markdown(f"### Valitut vuosi: {selected_year}, kunta: {selected_municipality}")

        st.subheader("Valmistuneet Asunnot")
        pie_chart_completed_housing, pie_chart_completed_funding = create_pie_charts(df_completed, selected_year, selected_municipality, 'valmvuosi', 'talotyyppi', 'rahmuoto')
        st.plotly_chart(pie_chart_completed_housing)
        st.plotly_chart(pie_chart_completed_funding)
        line_chart_completed = create_line_chart(df_completed, 'valmvuosi')
        st.plotly_chart(line_chart_completed)

        st.subheader("Yhdistetty Viivadiagrammi Alkaneiden ja Valmistuneiden Asuntojen Määrästä")
        combined_line_chart = create_combined_line_chart(df_started, df_completed, selected_municipality)
        st.plotly_chart(combined_line_chart)


    main()

    st.markdown("""
    ## Asuntotuotannon Visualisointi: Metatiedot

    ### Datan kuvaus
    Tämä sovellus visualisoi Helsingin seudun asuntotuotannon dataa, joka kattaa vuodet 2016-2019. Datan on kerännyt Helsingin seudun ympäristöpalvelut (HSY) ja se sisältää tiedot alkaneista ja valmistuneista asunnoista 14 eri kunnassa.

    ### Kunnat
    Data kattaa seuraavat kunnat: Espoo, Helsinki, Kauniainen, Vantaa, Hyvinkää, Järvenpää, Kerava, Kirkkonummi, Mäntsälä, Nurmijärvi, Pornainen, Sipoo, Tuusula ja Vihti.

    ### Tiedonkeruu
    Tiedot on kerätty keväisin vuosina 2017, 2018, 2019 ja 2020 osana MAL-sopimuksen seurantatyötä.

    ### Datan sisältö

    - **talotyyppi**: Jaoteltu kerrostaloihin (AK) ja pientaloihin (AP).
    - **asuntolkm**: Asuntojen lukumäärä kohteessa.
    - **rahmuoto**: Rahoitusmuoto, joka sisältää seuraavat kategoriat:
    - ARA: Valtion tukema vuokra-asunnot
    - ASO: Asumisoikeusasunnot
    - LK: Lyhyellä korkotuella rahoitettu
    - VT: Valtiontakausalainalla rahoitettu
    - VO: Vapaarahoitteinen omistus
    - VV: Vapaarahoitteinen vuokra
    - **valmvuosi/alkvuosi**: Kohteen valmistumis- tai aloitusvuosi.
    """)
