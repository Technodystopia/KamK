def show():
   from io import BytesIO
   from PIL import Image

   import streamlit as st
   import numpy as np
   import duckdb
   import matplotlib.pyplot as plt

   conn = duckdb.connect('data/testdata.duckdb')
   background_image = Image.open('image/kauppa.jpg')
   image_width, image_height = background_image.size

   st.markdown("# ETL-prosessin kuvaus.")

   st.markdown("""
   1. **Käyttäjän syöttö ja siivous:**
      - Skripti pyytää ensin käyttäjää valitsemaan käyttöjärjestelmänsä (Windows tai MacOS/Linux), jotta voidaan määrittää sopiva Python-komento (`python` tai `python3`).
      - Sen jälkeen se poistaa joukon tiettyjä tiedostoja ja kaikki tiedostot "data"-hakemiston "results"-nimisessä hakemistossa.

   2. **Python-skriptien suorittaminen:**
      - Skripti määrittelee luettelon Python-tiedostoista nimillä `etl_step01.py` - `etl_step14.py`.
      - Se käy tämän luettelon läpi, etsii tiedostopolun "code"-hakemistosta ja yrittää ajaa jokaisen skriptin valitulla Python-komennolla (`subprocess.run`).

   3. **Tietojen tuottaminen:**
      - Tämä osio tuottaa joitakin esimerkkitietoja ja kirjoittaa ne CSV-tiedostoon nimeltä "test.csv" hakemistossa "data/results". 
      - Tiedot edustavat eri koordinaatteja (x, y) tietyllä ajanhetkellä.
               
   4. **Datan käsittely:**
      - Skripti käyttää tietojen käsittelyyn DuckDtä, joka on sulautettu relaatiotietokannan hallintajärjestelmä.
      - Se muodostaa yhteyden DuckDB-tietokantaan nimeltä "testdata.duckdb", joka sijaitsee "data"-hakemistossa.
      - Test.csv-tiedoston tiedot ladataan tietokannassa olevaan taulukkoon nimeltä "test_table".
      - Toinen skripti lukee kaikki tietokannan taulukot ja kirjoittaa niiden sisällön tiedostoon nimeltä "testresult.txt", joka sijaitsee hakemistossa "data/results".

   5. **Data Injection:**
      - Tässä osiossa määritellään luokka nimeltä `DataInjector` tietojen syöttämistä varten DuckDB-tietokantaan.
      - Se ottaa syötteenä tietokannan polun ja CSV-tiedostoja sisältävän hakemiston.
      - Luokka muodostaa yhteyden tietokantaan, luo taulukoita, jos niitä ei ole olemassa, käy läpi CSV-tiedostot ja lisää tiedot tietokannassa olevaan taulukkoon nimeltä "original".

   6. **Tietojen suodatus ehtojen perusteella:**
      - Skripti määrittelee sarjan SQL-lauseita, jotka suodattavat tiedot "alkuperäinen"-taulussa eri ehtojen perusteella. 
      - Nämä ehdot liittyvät x- ja y-koordinaatteihin tai aikaleimoihin.
      - Suodatetut tiedot tallennetaan erillisiin taulukoihin nimillä "step0" - "step6".
      - Lisäsuodatusvaiheessa poistetaan tietyn aika-alueen (6:00 AM - 23:00 PM) ulkopuolella olevat tiedot.
      - Lopulliset suodatetut tiedot tallennetaan taulukkoon nimeltä "time".

   7. **Tietojen käsittely - nopeus ja etäisyys:**
      - Skripti määrittelee luokan nimeltä `DataProcessor` tietojen jatkokäsittelyä varten.
      - Se laskee nopeuden kullekin datapisteelle vertaamalla sijainnin muutosta (x, y) aikaleimojen väliseen aikaeroon.
      - Luodaan väliaikainen taulukko, johon tallennetaan nopeustiedot alkuperäisten tietojen rinnalle.
      - Tämän jälkeen tiedot suodatetaan nopeuskynnyksen perusteella (poikkeavien arvojen tai kohinan poistamiseksi), ja suodatetut tiedot, joissa on nopeustiedot, lisätään taulukkoon nimeltä "speed".
      - Samanlaista lähestymistapaa käytetään peräkkäisten datapisteiden välisen etäisyyden laskemiseen, ja suodatus perustuu enimmäisetäisyyskynnykseen. Suodatetut tiedot, jotka sisältävät etäisyystiedot, lisätään taulukkoon nimeltä "distance".

   """)

   #TODO muokkaa tämä lässytys kuvaukseksi eri vaiheista

   st.image('image/etlstats.png')

   st.markdown("""
   ## 
   """)

   #TODO Tämä toimivaksi, animaatio kliksuttelua

   def plot_data(scale_x=1.0, scale_y=1.0, offset_x=0, offset_y=0):
      query = "SELECT * FROM test_table ORDER BY timestamp"

      result = conn.execute(query)
      df = result.fetchdf()

      df["x"] = df["x"] * scale_x + offset_x
      df["y"] = image_height - (df["y"] * scale_y + offset_y)

      fig, ax = plt.subplots(figsize=(12, 6))

      ax.imshow(background_image, extent=[0, image_width, 0, image_height])

      cmap = plt.get_cmap('turbo')
      unique_node_ids = df['node_id'].unique()
      colors = cmap(np.linspace(0, 1, len(unique_node_ids)*1))

      for node_id, color in zip(unique_node_ids, colors):
         df_node = df[df['node_id'] == node_id]
         ax.scatter(df_node["x"], df_node["y"], label=f"Node {node_id}", color=color, s=1)

   #    #! tähtäin
   #    ax.scatter(410 * scale_x + offset_x, image_height - (2150 * scale_y + offset_y), color='red', s=10)

      plt.axis('off')
      plt.tight_layout()
      buf = BytesIO()
      plt.savefig(buf, format='png')
      buf.seek(0)
      img = Image.open(buf)
      plt.close()
      return img, df

   img, df = plot_data(scale_x=0.1090, scale_y=0.1085, offset_x=116, offset_y=27)
   st.image(img)
