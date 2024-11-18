import streamlit as st

def show():
    st.markdown("## Tulokset & Tulkinnat")
    st.markdown("""
    Ostoskärryjen liikkeiden analyysi paljastaa mielenkiintoisia tuloksia kaupan asiakasvirroista ja käyttäytymismalleista. Yksi merkittävimmistä havainnoista on se, että kärryjen tasainen liikkuminen ympäri kauppaa ja erilaisten asiakkaiden käyttö johtavat huipukkuuden tasoittumiseen. Tämä tarkoittaa, että kärryjen liikkeiden jakauma on suhteellisen tasainen ilman selkeitä huippuarvoja tietyissä paikoissa.

    ### Asiakasvirtojen keskittyminen

    Tarkempi analyysi 28 ostoskärrystä osoittaa, että valtaosa (20 kärryä) sijoittuu IQR-X-välille 5150-6190 ja IQR-Y-välille 1830-2270. Nämä alueet sijaitsevat kaupan keskellä olevalla oikoreitillä, mikä voi selittää asiakasvirran keskittymistä juuri tälle alueelle. Tämä havainto viittaa siihen, että asiakkaat suosivat tätä reittiä liikkuessaan kaupassa, mahdollisesti säästääkseen aikaa tai välttääkseen ruuhkaisia käytäviä.

    ### Poikkeavat ostoskärryt

    Analyysi paljastaa myös, että kahdeksan ostoskärryä poikkeaa merkittävästi muista. Lisätutkimukset osoittavat, että näitä kärryjä käytetään harvemmin, mikä voi johtua niiden sijainnista kärryrivin lopussa tai mahdollisista teknisistä ongelmista. Tämä havainto korostaa tarvetta seurata yksittäisten kärryjen kuntoa ja sijaintia, jotta voidaan varmistaa tasainen käyttö ja asiakastyytyväisyys.

    ### Kärryjen liikkumiskäyttäytyminen

    Suurin osa ostoskärryistä (21) osoittaa merkittävän suurta varianssia, mikä viittaa "kaoottiseen" liikkumiskäyttäytymiseen kaupan sisällä. Tämä on odotettavissa tilastossa, jossa kärryjen liikkeitä ei ole erikseen jaoteltu erilaisten asiakaskuntien liikehdintään, vaan samoja kärryjä käyttää sekä miehet/naiset, nuoret ja vanhat, joka aiheuttaa suosittujen kärryjen varianssitilastojen suurta arvoa. Seitsemän kärryä osoittaa pienempää varianssia, mikä voi viitata vähäisempään suosioon tai tietynlaisiin ostoskäyttäytymisiin, kuten kohdennettuihin ostoksiin.

    ### Selkeä reitti kaupassa

    Heatmap ja scatterplot-visualisointi paljastaa, että kaupassa on yksi selkeä reitti, jota pitkin asiakkaat kulkevat. Tämä reitti alkaa kaupan alusta, jatkuu pääkäytävää pitkin kaupan takaosassa sijaitsevalle HeVi-, leipä- ja maito-osastolle ja päättyy takaisin kassalle. Tämä havainto auttaa ymmärtämään asiakkaiden tyypillistä kulkua kaupassa ja voi auttaa optimoimaan tuotesijoittelua ja hyllyjen järjestystä.

    ## Havaintoja lisätiedoissa
    ### Väestörakenteen muutokset

    Järvenpään väestötilastot osoittavat merkittäviä muutoksia ikärakenteessa. Eläkeläisten määrä on lähes kaksinkertaistunut vuosien varrella, kun taas lasten ja nuorten määrä on hieman laskenut. Vuonna 2010 eläkeläisten määrä ylitti lasten ja nuorten määrän. Nämä muutokset voivat vaikuttaa kaupan asiakaskunnan rakenteeseen ja ostokäyttäytymiseen, mikä on tärkeää huomioida tuotevalikoimaa ja palveluita suunniteltaessa.

    ### Työttömyyden vaikutukset

    Vuonna 2020 Järvenpään työttömyystilastoissa tapahtui merkittävä muutos, kun sekä miesten että naisten työttömyys nousi huomattavasti. Osa työttömistä näyttäisi siirtyneen opiskelijoiksi, sillä opiskelijoiden määrä on noussut samanaikaisesti. (Kuitenkin myös alueen astuntostatistiikkaa ja väestön liikehdintää tutkimalla käy ilmi, että alueelle on rakennettu opiskelija-asuntoja, sekä siellä on opiskelijoiden osalta sisäänmuuttoliikennettä.) Työttömyyden kasvu on keskittynyt erityisesti nuoriin ja yli 40-vuotiaisiin ihmisiin, kun taas 25-39-vuotiaiden työttömyys on lisääntynyt vain vähän ja 35-39-vuotiaiden työllisyys on jopa parantunut. Nämä muutokset voivat vaikuttaa asiakkaiden ostovoimaan ja kulutustottumuksiin, mikä on syytä ottaa huomioon kaupan strategiassa.

    Näiden tulosten ja tulkintojen pohjalta voidaan tehdä päätelmiä ja suosituksia kaupan toiminnan optimoimiseksi. On tärkeää huomioida asiakasvirtojen keskittyminen, poikkeavat ostoskärryt, kaoottinen liikkumiskäyttäytyminen, selkeä reitti kaupassa sekä väestörakenteen ja työttömyyden muutokset. Näiden tekijöiden ymmärtäminen auttaa kehittämään kaupan layoutia, tuotevalikoimaa ja palveluita vastaamaan paremmin asiakkaiden tarpeita ja mieltymyksiä.
    """)