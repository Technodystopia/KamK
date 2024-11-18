# Projektisuunnitelma

## Johdanto ja tausta

Projektin asiakkaana on Kainuun hyvinvointialue. Se on 1.1.2023 toimintansa aloittanut organisaatio, joka vastaa koko Kainuun maakunnan sosiaali- ja terveyspalveluista sekä pelastustoimesta. Tavoitteena on tarjota korkealaatuista ja saavutettavaa palvelua kaikille alueen asukkaille.

Kainuun hyvinvointialue on maakunnan suurin työnantaja, ja sen palveluksessa on yhteensä noin 4000 työntekijää.

Kainuun hyvinvointialueen strategia 2022-2025 on suunnitelmakokonaisuus, joka pyrkii ottamaan huomioon mm. asukkaiden hyvinvoinnin edistämisen sekä henkilöstöpolitiikan, joka on muuttotappiomaakunnassa erityisen tärkeää työvoiman saatavuuden ja työhyvinvoinnin näkökulmasta.

## Projektin lähtötiedot ja tehtävänanto

### HOPP = asiakastyytyväisyysmittari

#### Yksiköt

- AIKTEHOHO
- EALAPSAIK
- ENSIHOITO

#### Visualisointi - HOPP

- Visualisoidaan yksikköjen asiakaspalautteen kaikkien kysymysten keskiarvot, jotka kasataan erillisistä Excel-tiedostoista. Kaikilta kvartaaleilta ei ole dataa saatavilla. Kaikki mitä voidaan, visualisoidaan suhteessa kansallisiin keskiarvoihin eri vuosineljänneksillä 2021/Q3 - 2023/Q1.
- Visualisoidaan yksikköjen asiakaspalautteen kaikkien kysymysten vastausten jakauma saatavilla olleilta vuosineljänneksiltä.

#### Ennustus - HOPP

- Ennustetaan yksikköjen asiakaspalautteen keskiarvot seuraavalle (Q4/2023) kvartaalille.
- Tulos visualisoidaan niin, että siinä näkyvät myös kysymyksen kaikki edelliset arvot.

#### Työkalun muodostus - HOPP

- Muodostetaan työkalu, jolla käyttäjä voi valita yksikköjen asiakaspalautteesta halutun kysymyksen ja katsoa sen ennustetun arvon seuraavalle (Q4/2023) vuosineljännekselle.
- Kuten aiemmassakin, tulos näytetään niin, että siinä näkyvät myös kysymyksen kaikki edelliset arvot.

### NES = henkilöstön työtyytyväisyyskysely

#### Visualisoi - NES

- Visualisoidaan yksikköjen tulokset ja verrataan niitä kaikkien yksikköjen vastauksiin, sekä kansallisiin keskiarvoihin.
- Piirretään yksikköjen vastausten jakauma ja verrataan niitä vuoden 2023 vastausten jakaumiin.

#### Työkalun muodostus - NES

- Muodostetaan työkalu, jolla käyttäjä voi valita yksikköjen työtyytyväisyydestä halutun kysymyksen katsoa sille piirrettyä jakaumaa.
- Tulos näytetään niin, että siinä näkyy referenssinä myös kysymyksen edellisen vuoden (2023) jakauma.

### Data-aineisto

#### NES

- Henkilöstön työtyytyväisyyskysely, josta otetaan tutkittavaksi vain AIKTEHOHO, EALAPSAIK ja ENSIHOITO vastaukset.
- Sisältää yhteensä 9 eri osa-aluetta (tärkeimpänä johtaminen, muut sitoutuneisuuteen vaikuttavat tekijät ja sitoutuneisuus)

#### HOPP

- Asiakastyytyväisyysmittari, josta otetaan tutkittavaksi samat yksiköt kuin NES-aineistoistakin, eli AIKTEHOHO, EALAPSAIK ja ENSIHOITO.
- Sisältää yhteensä 22 kysymystä

Data on luottamuksellista ja poistetaan projektin loputtua.

## Henkilöt ja roolit

| Nimi | Rooli |
| --- | --- |
| Anssi | Scrum Master |
| Jari | Product Owner |
| Netta | Developer |
| Jyri | Developer |

Projektin ollessa näin pieni, roolit eivät ole kiinteitä ja niitä kierrätetään tarpeen mukaan. Kaikki pääsevät tekemään hieman kaikkea.

## Aikataulu ja välitavoitteet

| Pvm | Tehtävä |
| --- | --- |
| 21.10.2024 | Projektin aloitus |
| 6.11.2024 | Projektisuunnitelman esittely |
| 20.11.2024 | 2. Sprint esittely |
| 4.12.2024 | 3. Sprint esittely |
| 18.12.2024 | Loppudemo |
| 31.12.2024 | Deadline palautuksille |

## Käytettävät työkalut

- VSC
- GitLab
- Wakatime
- Clockify
- MongoDB
- Docker
- Evidence

## Dataputken kuvaus

Projektin lähtötiedot ovat asiakkaan toimittamissa Excel-tiedostoissa. Tiedostot esikäsitellään ohjelmallisesti siten, että tarpeettomat tiedot sekä tyhjät rivit poistetaan ja tiedostot muutetaan CSV-muotoon. Data myös pseudonymisoidaan siten, että yksilöiviä tietoja ei ole tunnistettavissa ilman erikseen annettua JSON-avainta.

CSV-tiedostoista data siirretään dbt-putkeen, jossa siitä lasketaan keskiarvot ja muut tarvittavat tunnusluvut. dbt-putken lopputuloksena syntyy tietovarasto, josta data siirretään visualisointityökalu Evidenceen.

``` mermaid
flowchart TD
    id1[(Data Lake)] --> A(HOPP raw) 
    id1 --> B(NES raw)
    B --> idf@{ shape: subproc, label: "Preprocess xlsx -> csv" }
    A --> idf
    idf --> id2[Bronze]
    id2 --> id3[Silver]
    id3 --> id4[Gold]
    id4 --> id5[Evidence]
    id6(Prediction Tool) --> id5
```

## Hyväksymiskriteerit

### Projektin tavoite

Tavoitteena on HOPP - asiakastyytyväisyysmittarin datasta visualisoida kolmen eri yksikön keskiarvoja suhteessa kansallisiin keskiarvoihin eri vuosineljänneksillä, sekä ennustaa keskiarvoja seuraavalle kvartaalille. Lisäksi luodaan interaktiivinen työkalu, jolla käyttäjä voi valikoida yksiköiden asiakaspalautteista halutun kysymyksen, sen tulokset ja ennusteet tulevalle vuosineljännekselle.

Henkilöstön työtyytyväisyyskyselystä (NES) visualisoidaan tuloksia vastaavalla tavalla kuin HOPP datasetistä. Toteutetaan työkalu, jolla voidaan tarkkailla jakaumia. Valinnan lisäksi näytetään referenssinä edellisen vuoden jakauma.

### Todentaminen

Projekti on valmis, kun molemmat työkalut ovat todistettavasti toimivia ja dokumentaatio on selkeä, hiottu ja asianmukaisesti viitattu.
