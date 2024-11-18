import streamlit as st

def show():
    st.markdown("## Analyysimenetelmät")
    st.markdown("""
    Tässä tutkimuksessa hyödynsimme monipuolisesti erilaisia analyysimenetelmiä saadaksemme kattavan kuvan kaupan asiakkaiden ostoskäyttäytymisestä ja siihen vaikuttavista tekijöistä. Keskeisimpinä menetelminä käytimme ostoskärryjen liikkeiden analysointia tilastollisten menetelmien, kuten kurtosiksen, kvartiilivälin (IQR) ja varianssin avulla. Nämä menetelmät auttoivat meitä tunnistamaan erilaisia käyttäytymismalleja ja poikkeamia kärryjen liikkeissä.

    Visualisoimme myös asiakkaiden liikkeitä kaupan sisällä heatmap-tekniikalla, mikä auttoi meitä hahmottamaan asiakasvirtojen keskittymistä ja suosittuja reittejä. Tämä oli erityisen hyödyllistä, kun yhdistimme tiedot tilastollisiin analyyseihin.

    ## Väestötilastojen analysointi

    Asiakaskäyttäytymiseen vaikuttavien ulkoisten tekijöiden ymmärtämiseksi analysoimme myös Järvenpään alueen väestötilastoja. Tarkastelimme erityisesti ikärakenteen muutoksia, kuolleisuutta ja työttömyyttä. Nämä tiedot auttoivat meitä muodostamaan kokonaiskuvan alueen demografisesta kehityksestä ja sen mahdollisista vaikutuksista kaupan toimintaan.

    ## Datan käsittely ja yhdistäminen

    Tutkimuksessamme hyödynsimme myös datan pisteitä, jotka vastaavat noin yhtä senttimetriä kartalla. Tämä mahdollisti suoraviivaisen liikkeiden analysoinnin ilman tarvetta erillisille koordinaattimuunnoksille. Lisäksi analysoimme kärryjen kokonaismatkaa tunnistaaksemme harvemmin käytetyt kärryt ja niihin mahdollisesti liittyviä ongelmia.

    Saadaksemme mahdollisimman monipuolisen kuvan asiakkaiden käyttäytymisestä, yhdistimme eri menetelmillä saatuja tuloksia toisiinsa. Esimerkiksi yhdistämällä IQR-arvot muihin tilastollisiin mittareihin, kuten keskiarvoon, mediaaniin, varianssiin ja keskihajontaan, pystyimme muodostamaan entistä tarkemman kuvan kärryjen liikkeistä ja niihin vaikuttavista tekijöistä.

    Kaiken kaikkiaan valitsemamme analyysimenetelmät tukivat toisiaan ja auttoivat meitä muodostamaan kattavan kuvan kaupan asiakkaiden ostoskäyttäytymisestä. Näiden menetelmien avulla saimme arvokasta tietoa, jota voimme hyödyntää kaupan toiminnan kehittämisessä ja asiakaskokemuksen parantamisessa.
    """)