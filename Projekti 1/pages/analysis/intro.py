import streamlit as st

def show():
    import altair as alt
    import duckdb

    con = duckdb.connect("data/ultimate.duckdb")

    st.markdown("## Johdanto & Aineiston Kuvaus")
    st.markdown("""
    # Alustus
    Projektissa annettiin raakadatana 31 ostoskärryn sisätilapaikannustiedot CSV-tiedostoissa, sekä mittauspaikan pohjapiirros. 
    Jokainen CSV-tiedosto sisältää sarakkeina yhden ostoskärryn (noden) idn, aikaleimat, x-, y- ja z-koordinaatit sekä q-arvon.
                
    Projekti olisi ollut mahdollista ajaa esimerkin mukaisesti Jupyerissa ja MariaDBssä, mutta tiimin yhteisen päätöksen mukaisesti
    otimme käyttöön Streamlitin alustaksi ja DuckDBn tietokannaksi.
                
    Tiimin kesken selvitimme mittauspaikan sijainnin tutkimalla mm. mittausdatan tehneen yrityksen
    (Iiwari Oy) sosiaalista mediaa, verraten tiedostojen aikaleimoihin. Selvisi, että kyseessä on Järvenpään Tokmanni.
                """)

    st.markdown("""
    # Datan luotettavuus 
    Ensimmäisenä asiana oli ajaa kaikki CSV-tiedostot yhteen tietokantaan. Tiedostoissa on kuitenkin myös tehtävänannon kannalta 
    tarpeetonta dataa, kuten z-arvo (korkeuden muutos, kaikissa nodeissa nolla) sekä q, joka on epävarma 
    mittari paikannuksen laadulle. 

    Luotu, kaikenkattava tietokanta (ns. masterdb) toimii pohjana kaikille muille operaatioille ja sieltä voidaan
    hajauttaa tarvittavat tiedot pienempiin tietokantatauluihin, jotta niitä on helpompi käsitellä myös 
    huonommilla tai hitaammilla tietokoneilla.
                """)

    st.divider()
    query = "SELECT node_id, COUNT(*) AS count FROM tokmanni2 GROUP BY node_id;"
    df = con.execute(query).fetch_df()
    amount = df['count'].sum()

    title_count = alt.TitleParams('Rivien määrä noden (kärryn) mukaan' , anchor='middle')

    chart = alt.Chart(df).mark_circle(size=90).encode(
        x=alt.X('node_id:N', title="Node ID"),
        y=alt.Y('count', title="Määrä"),
        color=alt.Color('node_id:N', scale=alt.Scale(scheme='turbo'), legend=None),
        tooltip='count:N'
    ).properties(
        title=title_count
    )

    st.altair_chart(chart)
    st.write(f"Suodatetun tietokannan rivien kokonaismäärä on {amount} riviä.")
    st.write(f"Koko datan alkuperäisen tietokannan (masterdb) pituus on 139 961 560 riviä.")