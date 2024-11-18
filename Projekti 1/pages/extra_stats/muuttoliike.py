def show():
    import streamlit as st
    import pandas as pd
    import plotly.express as px

    df0 = pd.read_csv('data/muut/muutot/nettomuutto.csv', delimiter=';')
    df1 = pd.read_csv('data/muut/muutot/tulomuutto.csv', delimiter=';')
    df2 = pd.read_csv('data/muut/muutot/menomuutto.csv', delimiter=';')

    st.title("Muuttoliike Järvenpäässä")

    st.markdown("Tässä visualisoinnissa on esitetty muuttoliike Järvenpäässä valitsemallasi vuodella ja äidinkielellä.")

    available_years = df0.columns[2:]
    available_languages = df0['Äidinkieli'].unique()

    available_years = df1.columns[2:]
    available_languages = df1['Äidinkieli'].unique()

    available_years = df2.columns[2:]
    available_languages = df2['Äidinkieli'].unique()

    selected_year = st.selectbox("Vuosi", available_years)
    selected_language = st.selectbox("Äidinkieli", available_languages)

    filtered_df0 = df0[df0['Äidinkieli'] == selected_language]
    total_migrations0 = filtered_df0.groupby('Alue')[selected_year].sum().reset_index()

    filtered_df1 = df1[df1['Äidinkieli'] == selected_language]
    total_migrations1 = filtered_df1.groupby('Alue')[selected_year].sum().reset_index()

    filtered_df2 = df2[df2['Äidinkieli'] == selected_language]
    total_migrations2 = filtered_df2.groupby('Alue')[selected_year].sum().reset_index()

    fig0 = px.bar(total_migrations0, x='Alue', y=selected_year,
                labels={'x': 'Alue', 'y': 'Total Migrations'},
                title=f'Nettomuutto kohdealueen mukaan vuonna {selected_year} ({selected_language})',
                color='Alue',
                color_discrete_sequence=px.colors.sequential.Turbo)

    fig1 = px.bar(total_migrations1, x='Alue', y=selected_year,
                labels={'x': 'Alue', 'y': 'Total Migrations'},
                title=f'Tulomuutto kohdealueen mukaan vuonna {selected_year} ({selected_language})',
                color='Alue',
                color_discrete_sequence=px.colors.sequential.Turbo)

    fig2 = px.bar(total_migrations2, x='Alue', y=selected_year,
                labels={'x': 'Alue', 'y': 'Total Migrations'},
                title=f'Lähtömuutto kohdealueen mukaan vuonna {selected_year} ({selected_language})',
                color='Alue',
                color_discrete_sequence=px.colors.sequential.Turbo)


    st.markdown("Järvenpään alueen nettomuutto tilasto tarjoaa arvokasta tietoa alueen väestönkehityksestä ja muuttoliikkeestä. Analysoimalla näitä tietoja voidaan tehdä päätelmiä alueen elinvoimaisuudesta, asumisen houkuttelevuudesta ja mahdollisista markkinamahdollisuuksista.")

    fig0.update_layout(showlegend=False)
    fig1.update_layout(showlegend=False)
    fig2.update_layout(showlegend=False)

    st.plotly_chart(fig0)

    st.markdown("Tilasto antaa kuvan siitä, kuinka paljon ihmisiä on muuttanut Järvenpään alueelle ja poismuuttaneet sieltä kunkin vuoden aikana. Positiivinen nettomuutto osoittaa alueen houkuttelevuutta, kun taas negatiivinen nettomuutto voi viitata ongelmiin, kuten työpaikkojen puutteeseen tai asumiskustannusten korkeuteen.")

    st.plotly_chart(fig1)

    st.markdown("Järvenpään alueen muutto tilastot tarjoavat arvokasta tietoa alueen kehityksestä ja potentiaalisista markkinamahdollisuuksista. Tokmanni-kaupan kannalta tämä tieto voi auttaa sijoittamaan kaupan strategisesti ja tarjoamaan oikeanlaisia tuotteita ja palveluita alueen asukkaille.")

    st.plotly_chart(fig2)

    st.markdown(""" 
    ### Yleiskatsaus Järvenpään muuttoliikkeeseen

    - Tietosisältö - Sisältää tietoa muuttaneista lähtö- tai kohdealueen ja äidinkielen mukaan.
    - Aluerajat - Helsingin seudun muodostavat neljä pääkaupunkiseudun kuntaa Helsinki, Espoo, Vantaa ja Kauniainen ja kymmenen kehyskuntaa: Hyvinkää, Järvenpää, Kerava, Kirkkonummi, Mäntsälä, Nurmijärvi, Pornainen, Sipoo Tuusula ja Vihti.
        - Helsingin seutu on asunto- ja työmarkkina-alue.	
        - Uudenmaan maakunta muodostuu Helsingin, Raaseporin, Loviisan ja Porvoon seutukunnissa. Uusimaa kuuluu EU-alueluokituksessa NUTS-3-luokkaan.	
        - Helsingin seutukuntaan kuuluvat Espoo, Helsinki, Hyvinkää, Järvenpää, Kauniainen, Karkkila, Kerava, Kirkkonummi, Lohja, Mäntsälä, Nurmijärvi, Pornainen, Sipoo, Siuntio, Tuusula, Vantaa ja Vihti.
        - Raaseporin seutukuntaan kuuluvat Hanko, Inkoo ja Raasepori.
        - Loviisan seutukuntaan kuuluvat Lapinjärvi ja Loviisa.
        - Porvoon seutukuntaan kuuluvat Askola, Myrskylä, Pukkila ja Porvoo."	
        - Seutukunnat kuuluvat EU-alueluokituksessa NUTS-4-luokkaan.	
    - Tässä tilastossa epäloogiset alueparit (esim. Helsingin tulomuutto Helsingistä tai Helsingin seudun tulomuutto Helsingistä tai Pääkaupunkiseudun tulomuutto Helsingistä) saavat arvon 0 (nolla).	
    - Lähtö- tai kohdealue *Muu Suomi tarkoittaa tarkoittaa Uudenmaan, Varsinais-Suomen, Kanta-Hämeen, Pirkanmaan ja Päijät-Hämeen maakuntien ulkopuolista Suomea.	
    - Tietolähde - Tilastokeskus
    - Kohdejoukko ja rajaus - Väestörekisterikeskus (VRK) kerää keskitetysti kaikki väestönmuutoksia 
        - syntymää, kuolemaa, avioliiton solmimista ja avioeroa sekä muuttoliikettä - koskevat ilmoitukset. 
        - Väestörekisterikeskus saa muutosilmoitukset väestörekisterin pitäjiltä, maistraateilta, tuomioistuimilta ym. 
        - Väestörekisterikeskus käsittelee ja tarkistaa aineiston sekä päivittää väestötietojärjestelmänsä (jota 1.11.1993 asti kutsuttiin väestön keskusrekisteriksi). 
        - Väestörekisterikeskus lähettää viikoittain, järjestelmän päivityksen jälkeen, väestönmuutostiedot konekielisessä muodossa Tilastokeskukselle, missä tiedot muokataan tilastollista käyttöä varten ja tulostetaan tilastotaulukoiksi.
    - Tilastoyksikkönä on muutto (ei muuttaja).	
    - Väestönmuutostilastoista laskettu väestönmuutostieto poikkeaa väestörakennetilaston vastaavasta tiedosta, koska kaikkia muuttoja ei ole voitu tilastoida ja väkilukua korjataan muiden tietojen perusteella.	
    - Viiteajankohta - Tiedot ovat vuodesta 1999 lähtien.
    - Tietojen luotettavuus - Tiedot henkilöiden asuinpaikasta saadaan väestötietojärjestelmään muuttoilmoituksen kautta."	
    - Päivitystiheys - Vuosittain
    - Päivitetty viimeksi - 20230601 15:00	
    - Lähde - Tilastokeskus	
    """)