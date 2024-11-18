# Tokmanni - Sijaintidatan visualisointi

Tämä projekti on sijaintidatan visualisointityökalu Tokmanni-datasetille. Ohjelma käyttää muunmuassa Streamlit, DuckDB, ja Matplotlib kirjastoja luodakseen interaktiivisen web-sovelluksen, joka mahdollistaa datan analysoinnin sekä seikkaperäisen tutkimisen.

Projektiin on sisällytetty sijaintidata-analyysin lisäksi erilaisia visualisoituja tilastoja tuomaan lisäarvoa. Visualisointeja on saatavilla esimerkiksi Järvenpään tapahtumista, väestökehityksestä ja säästä valitulla ajanjaksolla.

Toimiakseen oikein ohjelmaan tulee erikseen ladata ja lisätä "data"-kansio kaikkine tiedostoineen. Kansio on saatavilla pyynnöstä.

# Asennus

Kloonaa tämä repositorio.

Ilman Docker-konttia sovellus tulee alustaa terminaalissa asentamalla tarvittavat kirjastot. 
```python
# Asenna tarvittavat kirjastot
pip install -r requirements.txt

# Rakenna tietokannat käynnistämällä
build.py 

# Käynnistä sovellus
streamlit run start.py
```

### Docker-kontin käyttö
```bash
# Rakenna kontti
docker build -t tokmanni .

# Käynnistä kontti
# Windows 11
docker run -it -v "/$(pwd):/app" -p 8501:8501 tokmanni bash
# Linux, MacOS
docker run -it -v `pwd`:/app -p 8501:8501 tokmanni bash

# Käynnistä sovellus
streamlit run start.py
```

# Käyttö
Ohjelma aukeaa verkkosivumaiseen näkymään, josta sivupalkin navigaatiosta pääsee siirtymään sivulta toiselle. Sovellus on rakennettu Streamlitillä ja data on tallennettu DuckDB-tietokantaan. Visualisointi käyttää muunmuassa Matplotlibia, Plotlya ja PIL:iä luodakseen ja näyttääkseen kuvaajat.

Siirtymällä "Kartat ja visualisointi" sivulle pääset tutkimaan sijaintidataa interaktiivisesti. 
Valitsemalla "Scatterplot" sivuvalikosta voit tehdä pudotusvalikoista valintoja aikavyöhykkeen, ostoskärryn (ostoskärryjen), päivämäärien sekä aikavälin perusteella. Ohjelma piirtää datapisteet pohjapiirroksen päälle valintojen perusteella. Saatavilla on myös heatmap, lineplot, cart time and distance ja barplot.

"Tilastotiedoja" piirtää erilaisia diagrammeja ja taulukon tietokannasta haetun sijaintidatan perustella. Sivupalkin valikosta voi valikoida tutkittavan datasetin ja tutustua niistä tehtyihin päätelmiin.

"Lisädata" sisältää nimensä mukaisesti sijaintidatan lisäksi visualisoituja datasettejä. Saatavilla on useita alasivuja kevyine analyyseineen.

Kirjautumalla admin-tunnuksilla pääset käsiksi "Kurssin tilastot"-sivulle. Tämän alta löytyy tiimin kuvaus, yhteenvedot Scrum-palavereista sekä Clockify-tilasto projektiin käytetystä ajasta.

# Osallistuminen
TBA

# Lisenssi
TBA