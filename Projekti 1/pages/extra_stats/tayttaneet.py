def show():
    import streamlit as st
    import pandas as pd
    import plotly.express as px

    y15 = pd.read_csv("data/muut/15v/yhteensa_kaikki_15v.csv", sep=";", index_col=0)
    ytyolliset = pd.read_csv("data/muut/15v/yhteensa_kaikki_tyolliset.csv", sep=";", index_col=0)
    ytyottomat = pd.read_csv("data/muut/15v/yhteensa_kaikki_tyottomat.csv", sep=";", index_col=0)
    ytyovoima = pd.read_csv("data/muut/15v/yhteensa_kaikki_tyovoima.csv", sep=";", index_col=0)
    yulkopuolella = pd.read_csv("data/muut/15v/yhteensa_kaikki_ulkopuolella.csv", sep=";", index_col=0)

    s15 = pd.read_csv("data/muut/15v/yhteensa_suomi_15v.csv", sep=";", index_col=0)
    styolliset = pd.read_csv("data/muut/15v/yhteensa_suomi_tyolliset.csv", sep=";", index_col=0)
    styottomat = pd.read_csv("data/muut/15v/yhteensa_suomi_tyottomat.csv", sep=";", index_col=0)
    styovoima = pd.read_csv("data/muut/15v/yhteensa_suomi_tyovoima.csv", sep=";", index_col=0)
    sulkopuolella = pd.read_csv("data/muut/15v/yhteensa_suomi_ulkopuolella.csv", sep=";", index_col=0)

    r15 = pd.read_csv("data/muut/15v/yhteensa_ruotsi_15v.csv", sep=";", index_col=0)
    rtyolliset = pd.read_csv("data/muut/15v/yhteensa_ruotsi_tyolliset.csv", sep=";", index_col=0)
    rtyottomat = pd.read_csv("data/muut/15v/yhteensa_ruotsi_tyottomat.csv", sep=";", index_col=0)
    rtyovoima = pd.read_csv("data/muut/15v/yhteensa_ruotsi_tyovoima.csv", sep=";", index_col=0)
    rulkopuolella = pd.read_csv("data/muut/15v/yhteensa_ruotsi_ulkopuolella.csv", sep=";", index_col=0)

    m15 = pd.read_csv("data/muut/15v/yhteensa_muut_15v.csv", sep=";", index_col=0)
    mtyolliset = pd.read_csv("data/muut/15v/yhteensa_muut_tyolliset.csv", sep=";", index_col=0)
    mtyottomat = pd.read_csv("data/muut/15v/yhteensa_muut_tyottomat.csv", sep=";", index_col=0)
    mtyovoima = pd.read_csv("data/muut/15v/yhteensa_muut_tyovoima.csv", sep=";", index_col=0)
    mulkopuolella = pd.read_csv("data/muut/15v/yhteensa_muut_ulkopuolella.csv", sep=";", index_col=0)

    st.title("15 vuotta täyttäneet pääas.toiminnan, koulutusasteen, sukupuolen ja äidinkielen mukaan")

    st.markdown(""" 
    Kauppiaan näkökulmasta tarkasteltuna alueen demografinen ja koulutustason kehitys tarjoaa arvokasta tietoa asiakaskunnasta ja mahdollisuuksista liiketoiminnan kehittämiselle. Vuosina 2001–2020 alueen väestö on kasvanut jatkuvasti, mikä viittaa potentiaaliseen asiakaskunnan kasvuun. Samalla koulutustason nousu, erityisesti toisen asteen ja korkea-asteen koulutuksen suorittaneiden osalta, antaa viitteitä siitä, että asiakaskunta saattaa olla keskimäärin paremmin koulutettua, mikä voi heijastua ostovoiman ja monipuolisemman kulutuskäyttäytymisen kasvuun.

    Työllisyystilanne on vaihdellut vuosittain, mutta pitkällä aikavälillä työllisten määrä on kasvanut, mikä puoltaa positiivista näkemystä alueen taloudellisesta kehityksestä. Työttömyyden väheneminen on myös myönteinen merkki, vaikka työttömyysaste on vaihdellutkin. Tämä saattaa heijastaa alueen talouden vahvistumista ja ostovoiman lisääntymistä.

    Lisäksi on huomionarvoista, että alueella on monikielinen väestö, mikä voi avata uusia mahdollisuuksia kohdennetulle markkinoinnille ja palveluiden tarjoamiselle eri kieliryhmille.

    Kauppiaan on tärkeää hyödyntää näitä tietoja liiketoimintastrategioiden suunnittelussa. Esimerkiksi markkinoinnin kohdentaminen eri kohderyhmille, valikoiman optimointi asiakkaiden tarpeiden mukaisesti sekä monikielisten palveluiden tarjoaminen voivat olla tehokkaita keinoja parantaa asiakastyytyväisyyttä ja siten vahvistaa liiketoimintaa alueella. Lisäksi on tärkeää seurata jatkuvasti väestönmuutoksia ja taloudellisia indikaattoreita pysyäkseen ajan tasalla alueen kehityksestä ja mahdollisista muutoksista asiakaskunnassa.""")

    option = st.selectbox(
        'Valitse näytettävä kuvaaja:',
        ('Yhteensä kaikki', 'Kaikki työlliset', 'Kaikki työttömät', 'Kaikki työvoima', 'Kaikki työvoiman ulkopuolella')
    )

    if option == 'Yhteensä kaikki':
        df0 = y15
    elif option == 'Kaikki työlliset':
        df0 = ytyolliset
    elif option == 'Kaikki työttömät':
        df0 = ytyottomat
    elif option == 'Kaikki työvoima':
        df0 = ytyovoima
    elif option == 'Kaikki työvoiman ulkopuolella':
        df0 = yulkopuolella

    df0 = df0.T
    title = option
    fig0 = px.line(df0, x=df0.index, y=df0.columns, title=title)
    fig0.update_xaxes(title="Vuosi")
    fig0.update_yaxes(title="Henkilömäärä")
    st.plotly_chart(fig0)

    option = st.selectbox(
        'Valitse näytettävä kuvaaja:',
        ('Suomenkieliset kaikki', 'Suomenkieliset työlliset', 'Suomenkieliset työttömät', 'Suomenkieliset työvoima', 'Suomenkieliset työvoiman ulkopuolella')
    )

    if option == 'Suomenkieliset kaikki':
        df1 = s15
    elif option == 'Suomenkieliset työlliset':
        df1 = styolliset
    elif option == 'Suomenkieliset työttömät':
        df1 = styottomat
    elif option == 'Suomenkieliset työvoima':
        df1 = styovoima
    elif option == 'Suomenkieliset työvoiman ulkopuolella':
        df1 = sulkopuolella

    df1 = df1.T
    title = option
    fig1 = px.line(df1, x=df1.index, y=df1.columns, title=title)
    fig1.update_xaxes(title="Vuosi")
    fig1.update_yaxes(title="Henkilömäärä")
    st.plotly_chart(fig1)

    option = st.selectbox(
        'Valitse näytettävä kuvaaja:',
        ('Ruotsinkieliset kaikki', 'Ruotsinkieliset työlliset', 'Ruotsinkieliset työttömät', 'Ruotsinkieliset työvoima', 'Ruotsinkieliset työvoiman ulkopuolella')
    )

    if option == 'Ruotsinkieliset kaikki':
        df2 = r15
    elif option == 'Ruotsinkieliset työlliset':
        df2 = rtyolliset
    elif option == 'Ruotsinkieliset työttömät':
        df2 = rtyottomat
    elif option == 'Ruotsinkieliset työvoima':
        df2 = rtyovoima
    elif option == 'Ruotsinkieliset työvoiman ulkopuolella':
        df2 = rulkopuolella

    df2 = df2.T
    title = option
    fig2 = px.line(df2, x=df2.index, y=df2.columns, title=title)
    fig2.update_xaxes(title="Vuosi")
    fig2.update_yaxes(title="Henkilömäärä")
    st.plotly_chart(fig2)

    option = st.selectbox(
        'Valitse näytettävä kuvaaja:',
        ('Muun kieliset kaikki', 'Muun kieliset työlliset', 'Muun kieliset työttömät', 'Muun kieliset työvoima', 'Muun kieliset työvoiman ulkopuolella')
    )

    if option == 'Muun kieliset kaikki':
        df3 = m15
    elif option == 'Muun kieliset työlliset':
        df3 = mtyolliset
    elif option == 'Muun kieliset työttömät':
        df3 = mtyottomat
    elif option == 'Muun kieliset työvoima':
        df3 = mtyovoima
    elif option == 'Muun kieliset työvoiman ulkopuolella':
        df3 = mulkopuolella

    df3 = df3.T
    title = option
    fig3 = px.line(df3, x=df3.index, y=df3.columns, title=title)
    fig3.update_xaxes(title="Vuosi")
    fig3.update_yaxes(title="Henkilömäärä")
    st.plotly_chart(fig3)

    st.markdown(""" 
    - Tietosisältö - Sisältää tietoja väestöstä koulutuksen, pääasiallisen toiminnan ja äidinkielen mukaan
    - Kohdejoukko ja rajaus
        - Pääasiallisen toiminnan käsite kuvaa henkilön taloudellisen toiminnan laatua. 
        - Väestö jaetaan pääasiallisen toiminnan perusteella työvoimaan kuuluviin ja työvoiman ulkopuolella oleviin. 
        - Nämä ryhmät voidaan edelleen jakaa alaryhmiin. 
        - Luokitus perustuu tietoihin henkilön toiminnasta vuoden viimeisellä viikolla.
    - Koulutukseksi katsotaan kaikki sellainen perusasteen jälkeinen loppuun suoritettu koulutus, jonka kesto on vähintään 400 tuntia. 
        - Aikuiskoulutusta, kuten työnantajan järjestämää koulutusta, järjestöjen ja yhdistysten antamaa koulutusta, kielikursseja, kirjeopetusta tms., ei lueta koulutukseksi. 
        - Koulutusastejaottelu noudattaa koulujärjestelmän rakennetta, jossa koulutus etenee vuosijaksottain alemmilta koulutuksen asteilta ylemmille. 
        - Mitä pidemmästä koulutuksesta on kysymys, sitä korkeampi on koulutusaste. 
        - Kultakin henkilöltä on otettu huomioon vain yksi koulutus, joka on korkein suoritettu tutkinto tai samanasteisista tutkinnoista viimeksi suoritettu tutkinto. 
        - Jos henkilö on suorittanut ylioppilastutkinnon toisen asteen tutkinto) ja toisen asteen ammatillisen tutkinnon, koulutus määräytyy ammatillisen tutkinnon mukaan.
    - Koulutustieto on puutteellinen ulkomaan kansalaisten osalta.
    - Aikasarja - Tiedot ovat vuodesta 2001 lähtien.
    - Tietolähde - Tilastokeskus - Statistikcentralen
    - Päivitystiheys - Vuosittain
    - Päivitetty viimeksi - 20240109 09:00
""")