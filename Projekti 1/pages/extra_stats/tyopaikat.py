def show():
    import pandas as pd
    import streamlit as st
    import plotly.express as px

    st.title("Työpaikat Järvenpäässä")

    df = pd.read_csv("data/muut/tyopaikat.csv")

    selected_year = st.selectbox("Valikoi vuosi", df.columns[1:])

    color_sequence = px.colors.sequential.Turbo
    color_mapping = {toimiala: color_sequence[i % len(color_sequence)] for i, toimiala in enumerate(df["Toimiala"].unique())}

    fig_pie = px.pie(df, values=selected_year, names="Toimiala", title=f"Vuoden {selected_year} prosentuaalinen data", color="Toimiala", color_discrete_map=color_mapping)
    fig_bar = px.bar(df, x="Toimiala", y=selected_year, title=f"Vuoden {selected_year} työpaikkojen määrä", color="Toimiala", color_discrete_map=color_mapping)

    st.markdown("Tässä visualisoinnissa on esitetty työpaikkojen määrä Järvenpäässä toimialoittain valitsemallasi vuodella.")

    st.markdown("""
    ### Yleiskatsaus Järvenpään työmarkkinoihin

    - Tilastokeskuksen mukaan Järvenpäässä oli vuonna 2019 yhteensä 13699 työpaikkaa. 
    - Näistä suurin osa, 7 539, oli yksityisellä sektorilla. 
    - Merkittävimmät toimialat Järvenpäässä ovat.
        - Tukku- ja vähittäiskauppa; moottoriajoneuvojen ja moottoripyörien korjaus: 2112 työpaikkaa
        - Terveys- ja sosiaalipalvelut: 2287 työpaikkaa
        - Koulutus: 1412 työpaikkaa
        - Hallinto- ja tukipalvelutoiminta: 1385 työpaikkaa
        - Teollisuus: 1786 työpaikkaa
        - Järvenpään työllisyysaste on korkea, 78,1%. Työttömyysaste oli vuonna 2019 5,8%.

    ### Tokmannin näkökulma

    Tokmannin kaltaiselle vähittäiskaupalle Järvenpään työmarkkinat tarjoavat sekä mahdollisuuksia että haasteita.

    #### Mahdollisuudet:

    - Suuri väestö: Järvenpäässä on yli 46 000 asukasta, mikä tarjoaa Tokmannille laajan asiakaskunnan.
    - Korkea työllisyysaste: Korkea työllisyysaste tarkoittaa, että ihmisillä on rahaa käytettävissään ostoksille.
    - Monipuolinen työelämä: Monipuolinen työelämä tarkoittaa, että Järvenpäässä on ihmisiä eri tulotasoilla, mikä voi olla hyödyllistä Tokmannille, koska se tarjoaa edullisia tuotteita.

    #### Haasteet:

    - Kilpailu: Järvenpäässä on useita muita vähittäiskauppiaita, joten Tokmannin on oltava kilpailukykyinen hintojensa ja tuotevalikoimansa suhteen.
    - Verkkokauppa: Verkkokaupan kasvu on haaste kaikille vähittäiskaupialoille, mukaan lukien Tokmannille.
    - Pieni keskusta: Järvenpään keskusta on pieni, joten Tokmannilla voi olla vaikeuksia löytää sopivaa liiketilaa.

    #### Suosituksia Tokmannille

    Tokmannin tulisi harkita seuraavia asioita menestyäkseen Järvenpäässä:

    - Kilpailukykyisten hintojen ylläpitäminen: Tokmannin on varmistettava, että sen hinnat ovat kilpailukykyisiä muihin Järvenpään vähittäiskauppiaisiin nähden.
    - Laajan tuotevalikoiman tarjoaminen: Tokmannin tulisi tarjota laajan valikoiman tuotteita, jotta se voi houkutella mahdollisimman monia asiakkaita.
    - Verkkokaupan kehittäminen: Tokmannin tulisi kehittää verkkokauppaansa, jotta se voi kilpailla tehokkaammin verkkokauppiaiden kanssa.
    - Markkinoinnin tehostaminen: Tokmannin tulisi tehostaa markkinointiaan Järvenpäässä, jotta se voi tavoittaa potentiaalisia asiakkaita.
    - Asiakaspalvelun parantaminen: Tokmannin tulisi parantaa asiakaspalveluaan, jotta se voi erottua kilpailijoistaan.

    #### Yhteenveto

    Järvenpään työmarkkinat tarjoavat Tokmannille sekä mahdollisuuksia että haasteita. Tokmannin on oltava kilpailukykyinen hintojensa, tuotevalikoimansa ja markkinointinsa suhteen menestyäkseen Järvenpäässä.
    """)

    st.plotly_chart(fig_pie)

    st.markdown(""" 
    - A - Maatalous, metsätalous ja kalatalous
    - B - Kaivostoiminta ja louhinta
    - C - Teollisuus
    - D - Sähkö-, kaasu- ja lämpöhuolto, jäähdytysliiketoiminta
    - E - Vesihuolto, viemäri- ja jätevesihuolto, jätehuolto ja muu ympäristön puhtaanapito
    - F - Rakentaminen
    - G - Tukku- ja vähittäiskauppa; moottoriajoneuvojen ja moottoripyörien korjaus
    - H - Kuljetus ja varastointi
    - I - Majoitus- ja ravitsemistoiminta
    - J - Informaatio ja viestintä
    - K - Rahoitus- ja vakuutustoiminta
    - L - Kiinteistöalan toiminta
    - M - Ammatillinen, tieteellinen ja tekninen toiminta
    - N - Hallinto- ja tukipalvelutoiminta
    - O - Julkinen hallinto ja maanpuolustus; pakollinen sosiaalivakuutus
    - P - Koulutus
    - Q - Terveys- ja sosiaalipalvelut
    - R - Taiteet, viihde ja virkistys
    - S - Muu palvelutoiminta
    - T - Kotitalouksien toiminta työnantajina; kotitalouksien eriyttämätön toiminta tavaroiden ja palvelujen tuottamiseksi omaan käyttöön
    - U - Kansainvälisten organisaatioiden ja toimielinten toiminta
    - X - Toimiala tuntematon
    """)

    st.plotly_chart(fig_bar)

    st.markdown(""" 
    #### Uudenmaan työpaikkaprojektioissa käytetyt väestöprojektiot				
				
    |   | Vuosi | Väkiluku | Väestöosuudet, % | Väestöosuuden muutos, %-yks. ed. v:sta |
    |---|-------|----------|-----------------|-------------------------------------|
    | 2021 Ve0 Nopea PKS-painotteinen | 2019 | 43711 | 3 | 0 |
    |    | 2020 | 44411 | 3 | 0 |
    | 2021 Ve1 Nopea kaikkiin keskuksiin | 2019 | 43711 | 3 | 0 |
    |    | 2020 | 44291 | 3 | 0 |
    | 2021 Ve2 Hidastuva TK2019 | 2019 | 43711 | 3 | 0 |
    |    | 2020 | 44303 | 3 | 0 |
        """)

    st.markdown(""" 
    #### Tietosisältö ja tietolähde

    - Projektiot on laatinut Seppo Laakso Kaupunkitutkimus TA Oy:sta
    - Tietosisältö - Sisältää tietoja alueella työssäkäyvien määrästä henkilöluvun mukaan eli työpaikkojen määrän toimialan (TOL 2008) mukaan.
    - Tietolähde - Tilastokeskus
    - Kohdejoukko ja rajaus - Työpaikkamäärän mittarina käytetään kaikkien alueella työssäkäyvien henkilöiden määrää riippumatta heidän asuinpaikastaan. 
        - Alueella työssäkäyvät muodostavat ns. työllisen päiväväestön. 
        - Henkilön toimiala määräytyy hänen työpaikkansa toimialan mukaan.
        - Kaikki samassa toimipaikassa työskentelevät saavat saman toimialan ammatistaan riippumatta. 
        - Työpaikan toimiala määritetään kullekin toimipaikalle ja itsenäiselle ammatinharjoittajalle Tilastokeskuksen toimialaluokituksen mukaisesti. 
        - Toimialaluokitus on Tilastokeskuksen julkaisun Toimialaluokitus (TOL) 2008 mukainen.
    - Aikasarja - Tiedot ovat vuodesta 2007 lähtien.
    - Päivitystiheys - Vuosittain
    - Päivitetty viimeksi - 20240108 10:00
    - Lähde - Tilastokeskus
    """)
