def show():
    import streamlit as st
    import pandas as pd
    import plotly.graph_objects as go

    st.title('Työllinen työvoima')

    st.markdown("""
    On huomioitava, että 20-39-vuotiaat muodostavat suurimman osan työvoimasta monilla toimialoilla. Heidän osuutensa on merkittävä, ja he todennäköisesti muodostavat suuren osan paikallisen Tokmanni-kaupan henkilöstöstä. Tässä ikäryhmässä olevilla työntekijöillä on yleensä hyvä energiataso ja kyky suoriutua fyysisestä työstä, joka voi olla tarpeen kaupan toiminnassa.

    Toisaalta, nuoremmat työntekijät, erityisesti 18-24-vuotiaat, voivat tarjota arvokasta apua esimerkiksi asiakaspalvelussa ja varastotyössä. Heillä voi olla myös erityistä osaamista esimerkiksi tietotekniikassa ja markkinoinnissa, mikä voi hyödyttää kaupan toimintaa.

    On myös tärkeää huomata, että ikääntyneemmät työntekijät, erityisesti yli 50-vuotiaat, voivat tuoda mukanaan laajaa kokemusta ja ammattitaitoa. He voivat olla arvokkaita resursseja esimerkiksi esimies- ja koulutustehtävissä sekä tarjota vakautta ja luotettavuutta työyhteisöön.

    Kun tarkastellaan toimialoittain, kaupan ala (tukku- ja vähittäiskauppa) sekä majoitus- ja ravitsemistoiminta ovat merkittäviä. Tämä osoittaa, että paikallisen Tokmanni-kaupan kannalta on tärkeää ymmärtää asiakkaiden ostokäyttäytymistä ja tarjota heille sopivia tuotteita ja palveluita.

    Lisäksi informaatio ja viestintä -ala voi olla merkityksellinen, kun mietitään markkinointia ja asiakasviestintää. Näillä aloilla työskentelevät voivat tuoda osaamista esimerkiksi digitaalisen markkinoinnin ja verkkokaupan kehittämiseen.

    Yhteenvetona voidaan todeta, että paikallisen kaupan menestyksen kannalta on tärkeää hyödyntää monipuolisesti eri ikäryhmiin kuuluvien työntekijöiden osaamista ja kokemusta. On myös olennaista seurata markkinatrendejä ja asiakkaiden tarpeita sekä tarjota heille houkuttelevia tuotteita ja palveluita.            
    """)

    df = pd.read_csv("data/muut/tyovoima/tyovoima0.csv", delimiter=";")
    df = df.set_index(df.columns[0])
    df.index.name = 'Category'
    df = df.transpose()

    fig = go.Figure()
    for column in df.columns:
        fig.add_trace(go.Bar(name=column, x=df.index, y=df[column]))
    fig.update_layout(barmode='stack', xaxis_title='Ikä ryhmä', yaxis_title='Työvoiman määrä',
                    title='Työllinen työvoima toimialan ja iän mukaan')
    fig.update_traces(showlegend=False)
    st.plotly_chart(fig)

    st.markdown(""" 
    - A Maatalous, metsätalous ja kalatalous
    - B Kaivostoiminta ja louhinta
    - C Teollisuus
    - D Sähkö-, kaasu- ja lämpöhuolto, jäähdytysliiketoiminta
    - E Vesihuolto, viemäri- ja jätevesihuolto, jätehuolto ja muu ympäristön puhtaanapito
    - F Rakentaminen;
    - G Tukku- ja vähittäiskauppa: moottoriajoneuvojen ja moottoripyörien korjaus
    - H Kuljetus ja varastointi
    - I Majoitus- ja ravitsemistoiminta
    - J Informaatio ja viestintä
    - K Rahoitus- ja vakuutustoiminta
    - L Kiinteistöalan toiminta
    - M Ammatillinen, tieteellinen ja tekninen toiminta;1199
    - N Hallinto- ja tukipalvelutoiminta
    - O Julkinen hallinto ja maanpuolustus: pakollinen sosiaalivakuutus
    - P Koulutus
    - Q Terveys- ja sosiaalipalvelut
    - R Taiteet, viihde ja virkistys
    - S Muu palvelutoiminta
    - T Kotitalouksien toiminta työnantajina: kotitalouksien eriyttämätön toiminta tavaroiden ja palvelut
    - U Kansainvälisten organisaatioiden ja toimielinten toiminta
    - X Toimiala tuntematon""")

    df1 = pd.read_csv("data/muut/tyovoima/tyovoima1.csv", delimiter=";")
    df1 = df1.set_index(df1.columns[0])
    df1.index.name = 'Category'
    df1 = df1.transpose()

    fig1 = go.Figure()
    for column in df1.columns:
        fig1.add_trace(go.Bar(name=column, x=df1.index, y=df1[column]))
    fig1.update_layout(barmode='stack', xaxis_title='Ikä ryhmä', yaxis_title='Työvoiman määrä',
                    title='Työllinen työvoima toimialan ja iän mukaan - Miehet')
    fig1.update_traces(showlegend=False)
    st.plotly_chart(fig1)
    
    #Kaikki toimialat yhteensä;20916;454;1532;2299;2422;2643;2571;2162;2508;2459;1592;274

    fig2 = go.Figure()
    df2 = pd.read_csv("data/muut/tyovoima/tyovoima2.csv", delimiter=";")
    df2 = df2.set_index(df2.columns[0])
    df2.index.name = 'Category'
    df2 = df2.transpose()

    for column in df2.columns:
        fig2.add_trace(go.Bar(name=column, x=df2.index, y=df2[column]))
    fig2.update_layout(barmode='stack', xaxis_title='Ikä ryhmä', yaxis_title='Työvoiman määrä',
                    title='Työllinen työvoima toimialan ja iän mukaan - Naiset')
    fig2.update_traces(showlegend=False)
    st.plotly_chart(fig2)

    st.markdown("""	
- Tietosisältö - Sisältää tietoja työllisestä työvoimasta toimialan mukaan.
    - (Luokka T: Kotitalouksien toiminta työnantajina; kotitalouksien eriyttämätön toiminta tavaroiden ja palvelujen tuottamiseksi omaan käyttöön)	
- Tietolähde - Tilastokeskus työssäkäyntitilasto. 
    - Tiedot on päätelty hallinnollisista ja tilastollisista rekistereistä ja muista aineistoista.
- Kohdejoukko ja rajaus - Työlliseen työvoimaan luetaan kaikki 18-74-vuotiaat henkilöt, jotka vuoden viimeisellä viikolla olivat ansiotyössä eivätkä olleet työttömänä työnhakijana työvoimatoimistossa tai suorittamassa varusmies- tai siviilipalvelua. 
    - Tieto työllisyydestä perustuu työeläke- ja veroviranomaisten tietoihin."	
- Henkilön toimiala määräytyy hänen työpaikkansa toimialan mukaan. 
    - Kaikki samassa toimipaikassa työskentelevät saavat saman toimialan ammatistaan riippumatta.
    - Toimialaluokitus on Tilastokeskuksen julkaisun Toimialaluokitus (TOL) 2008 mukainen.
- Päivitystiheys - Vuosittain.
	
- Päivitetty viimeksi - 20240108 16:00
    """)
