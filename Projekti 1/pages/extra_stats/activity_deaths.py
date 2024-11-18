def show():
    import plotly.graph_objects as go
    import streamlit as st
    import duckdb

    # deaths
    CATEGORIES_D = ["molemmat", "miehet", "naiset"]
    AGE_GROUPS_D = ["yhteensä", "0", "1-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49",
                  "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80-84", "85-89", "90-94", "95-"]
    
    # main activity
    CATEGORIES_A = ["molemmat sukupuolet", "miehet", "naiset"]
    AGE_GROUPS_A = ["väestö yhteensä", "0-14-vuotiaat", "15-19-vuotiaat", "20-24-vuotiaat", "25-29-vuotiaat",
                "30-34-vuotiaat", "35-39-vuotiaat", "40-44-vuotiaat", "45-49-vuotiaat", "50-54-vuotiaat",
                "55-59-vuotiaat", "60-64-vuotiaat", "65-69-vuotiaat", "70-74-vuotiaat", "Yli 75-vuotiaat",
                "15-64-vuotiaat yhteensä", "20-64-vuotiaat yhteensä", "15-74-vuotiaat yhteensä"]
    MAIN_ACTIVITIES_A = ["0-14-vuotiaat", "opiskelijat, koululaiset", "työlliset", "työttömät", "eläkeläiset",
                        "varus- ja siviilipalvelu", "muut"]

    conn = duckdb.connect('data/stats.duckdb')

    

    # main activity function thing
    def plot_activity_data(start_year, end_year, selected_categories, selected_age_groups, selected_main_activities):
        query = "SELECT * FROM activity_data WHERE 1=1"
        query += f" AND Year BETWEEN {start_year} AND {end_year}"

        if selected_categories:
            categories = ', '.join(f"'{cat}'" for cat in selected_categories)
            query += f" AND Category IN ({categories})"
        if selected_age_groups:
            age_groups = ', '.join(f"'{group}'" for group in selected_age_groups)
            query += f" AND Age_Group IN ({age_groups})"
        if selected_main_activities:
            main_activities = ', '.join(f"'{activity}'" for activity in selected_main_activities)
            query += f" AND Main_Activity IN ({main_activities})"

        query += " ORDER BY Year"

        result = conn.execute(query)
        df = result.fetchdf()

        fig = go.Figure()
        for category in df['Category'].unique():
            df_category = df[df['Category'] == category]
            for age_group in df_category['Age_Group'].unique():
                df_age_group = df_category[df_category['Age_Group'] == age_group]
                for main_activity in df_age_group['Main_Activity'].unique():
                    df_main_activity = df_age_group[df_age_group['Main_Activity'] == main_activity]
                    fig.add_trace(go.Scatter(x=df_main_activity['Year'], y=df_main_activity['Value'],
                                            mode='lines', name=f"{category} - {age_group} - {main_activity}"))

        fig.update_layout(
            legend=dict(
                y=-0.1,
                traceorder='reversed',
                font=dict(
                    size=10,
                )
            ),
            legend_orientation="h"
        )

        st.plotly_chart(fig, use_container_width=True)

    # deaths function
    def plot_data(start_year, end_year, selected_categories, selected_age_groups):
        query = "SELECT * FROM deaths_age_sex WHERE 1=1"
        query += f" AND Year BETWEEN {start_year} AND {end_year}"

        if selected_categories:
            categories = ', '.join(f"'{cat}'" for cat in selected_categories)
            query += f" AND Category IN ({categories})"
        if selected_age_groups:
            age_groups = ', '.join(f"'{group}'" for group in selected_age_groups)
            query += f" AND Age_group IN ({age_groups})"

        query += " ORDER BY Year"

        result = conn.execute(query)
        df = result.fetchdf()

        fig = go.Figure()
        for category in df['Category'].unique():
            df_category = df[df['Category'] == category]
            for age_group in df_category['Age_group'].unique():
                df_age_group = df_category[df_category['Age_group'] == age_group]
                fig.add_trace(go.Scatter(x=df_age_group['Year'], y=df_age_group['Value'], mode='lines', name=f"{category} - {age_group}"))

        fig.update_layout(
            legend=dict(
                y=-0.1,
                traceorder='reversed',
                font=dict(
                    size=10,
                )
            ),
            legend_orientation="h"
        )

        st.plotly_chart(fig, use_container_width=True)

    # page stuff starts here
    st.title("Tutkimusta lähiasukkaiden väestön pääasiallisesta toiminnasta ja muutoksista")

    # activity buttons = a
    with st.expander("Tilastot: Väestön pääasiallinen toiminta", expanded=True):
        st.markdown("## Väestö pääasiallisen toiminnan mukaan")
        selected_categories_a = st.multiselect('Kategoriat:', options=CATEGORIES_A, default=["molemmat sukupuolet"])
        selected_age_groups_a = st.multiselect('Ikäryhmät:', options=AGE_GROUPS_A, default=["väestö yhteensä"])
        selected_main_activities_a = st.multiselect('Pääasiallinen toiminta:', options=MAIN_ACTIVITIES_A, default=["työlliset"])
        start_year_a, end_year_a = st.slider('Vuosiväli:', 2001, 2020, (2001, 2020), 1)
        plot_activity_data(start_year_a, end_year_a, selected_categories_a, selected_age_groups_a, selected_main_activities_a)

    # death buttons = d
    with st.expander("Tilastot: Kuolemat iän ja sukupuolen mukaan", expanded=False):
        st.markdown("## Kuolemat iän ja sukupuolen mukaan")
        selected_categories_d = st.multiselect('Kategoriat:', options=CATEGORIES_D, default=["molemmat"])
        selected_age_groups_d = st.multiselect('Ikäryhmät:', options=AGE_GROUPS_D, default=["yhteensä"])
        start_year_d, end_year_d = st.slider('Vuosiväli:', 1994, 2020, (1994, 2020), 1)
        plot_data(start_year_d, end_year_d, selected_categories_d, selected_age_groups_d)

    st.markdown("""
        # Järvenpään väestötilastojen analyysi ja vaikutukset kaupan strategiaan

        Olemme analysoineet Järvenpään väestötilastoja vuosituhannen alusta lähtien. 
        Tarkastelumme keskittyy erityisesti ikärakenteen muutoksiin, kuolleisuuteen ja työttömyyteen. 
        Näiden pohjalta olemme tehneet päätelmiä siitä, miten havainnot tulisi huomioida kaupan strategiassa.

        ## Ikärakenteen muutokset

        Vuosituhannen alusta lähtien olemme havainneet merkittäviä muutoksia Järvenpään väestön ikärakenteessa:

        - Eläkeläisten määrä on lähes kaksinkertaistunut 5038 --> 9754.
        - Samaan aikaan 0-14-vuotiaiden määrä on hieman laskenut 7767 --> 7463.
        - Merkittävä käännekohta tapahtui vuonna 2010, jolloin eläkeläisten määrä ylitti lasten ja nuorten määrän.

        ## Kuolleisuustilastot

        Kuolleisuustilastoissa olemme havainneet seuraavia trendejä:

        - Yli 65-vuotiaiden kuolleisuus on ollut tasaisessa nousussa, mikä on odotettavaa Suomen yleisen väestöpyramidin huomioiden.
        - Koronapandemialla ei näytä olleen suurta vaikutusta Järvenpään alueen kuolleisuuteen.
        - Alle 59-vuotiaiden kuolleisuus on pysynyt ennallaan, ja alle 54-vuotiaiden kuolleisuus on jopa laskenut.

        Kuolleisuustilastojen tarkempi tutkiminen ei vaikuta olevan tarpeen kaupan myynnin ja strategian näkökulmasta.

        ## Työttömyystilastot

        Vuonna 2020 Järvenpään työttömyystilastoissa tapahtui merkittävä muutos:

        - Miesten työttömyys nousi 1010 --> 1474.
        - Naisten työttömyys kasvoi 769 --> 1169.

        Osa työttömistä näyttäisi siirtyneen opiskelijoiksi, sillä opiskelijoiden määrä on noussut samanaikaisesti. 
        (alueella on myös rakennettu uusia opiskelijoille tarkoitettuja asuntoja, joka voi selittää osan kasvusta)
        Työttömien siirtymisestä opiskelijoiksi ei kuitenkaan ole täyttä varmuutta, sillä meiltä puuttuu toistaiseksi tarkempi tieto eri ikäryhmien suhteellisista osuuksista väestössä.

        On huomionarvoista, että työssäkäyviä on edelleen yli kymmenkertainen määrä työttömiin nähden, 
        joten muutos on suhteellisesti pieni. Sillä voi kuitenkin olla merkittävä vaikutus yleiseen ilmapiiriin ja asiakkaiden kuluttajakäyttäytymiseen.

        ## Yllättävä havainto työttömyydestä

        Mielenkiintoinen yksityiskohta työttömyystilastoissa on se, että työttömyyden kasvu on keskittynyt 
        nuoriin-, yli 40-vuotiaisiin työssä-käyviin ihmisiin. Sen sijaan 25-39-vuotiaiden työttömyys on lisääntynyt vain vähän, 
        ja 35-39-vuotiaiden työllisyys on jopa parantunut. Tämän taustalla olevat syyt vaatisivat lisätutkimusta, 
        mahdollisesti toimialakohtaista tarkastelua.

        ## Suositukset kaupan strategiaan

        Epävarman ilmapiirin vallitessa on odotettavissa, että ihmiset vähentävät kulutustaan ja välttävät suuria hankintoja.
        Tämän vuoksi suosittelemme seuraavia toimenpiteitä kaupan strategiaan:

        - Vähennetään yleisesti brändituotteiden hankintaa.
        - Panostetaan **oma merkki** ja **edullinen oma merkki** -tuotekategorioihin.
        - Pidetään omavaraisuuteen liittyvät tuotteet hyvin edustettuina valikoimissa.

        ## Yhteenveto

        Järvenpään väestötilastojen analyysi tarjoaa arvokasta tietoa kaupan strategian suunnitteluun.
        Keskeisiä havaintoja ovat ikärakenteen vanheneminen, työttömyyden kasvu tietyissä ikäryhmissä sekä
        yleisen epävarmuuden mahdolliset vaikutukset kuluttajakäyttäytymiseen.
        Näihin havaintoihin pohjautuvilla toimenpiteillä voimme sopeuttaa kaupan strategiaa
        vastaamaan paremmin muuttuvan toimintaympäristön haasteisiin.
        
        """)

    st.markdown("""
                
    ### Tilastojen tiedot
                
    - Tietosisältö - Sisältää tietoa Järvenpään väestön päätoimisesta aktiviteeteista ikä- ja sukupuoliryhmittäin, sekä tilastoja kuolleista iän ja sukupuolen mukaan.
    - Tietolähde - Tilastokeskus.
    - Kohdejoukko ja rajaus
        - Väestörekisterikeskus (VRK) kerää keskitetysti kaikki väestönmuutoksia - syntymää, kuolemaa, avioliiton solmimista ja avioeroa sekä muuttoliikettä - koskevat ilmoitukset.
        - Väestörekisterikeskus saa muutosilmoitukset väestörekisterin pitäjiltä, maistraateilta, tuomioistuimilta ym. Väestörekisterikeskus käsittelee ja tarkistaa aineiston sekä päivittää väestötietojärjestelmänsä (jota 1.11.1993 asti kutsuttiin väestön keskusrekisteriksi). Väestörekisterikeskus lähettää viikoittain, järjestelmän päivityksen jälkeen, väestönmuutostiedot konekielisessä muodossa Tilastokeskukselle, missä tiedot muokataan tilastollista käyttöä varten ja tulostetaan tilastotaulukoiksi.
    - Tietojen luotettavuus - Tiedot henkilöiden asuinpaikasta saadaan väestötietojärjestelmään muuttoilmoituksen kautta.
    - Päivitystiheys- Vuosittain
    - Päivitetty viimeksi - 20230426 10:00
    """)