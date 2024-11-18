import streamlit as st
from st_pages import Page, Section, add_page_title
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from code.constants import AUTH_FAIL_LOGIN_MSG

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

add_page_title()

if st.session_state["authentication_status"]:
    # the unique key is for keeping the correct sub-page loaded
    # (so that it wont overflow from the previous main category)
    from pages.default import show as show_default
    from pages.extra_stats.jarvenpaa import show as show_jarvenpaa_events
    from pages.extra_stats.activity_deaths import show as show_deaths
    from pages.extra_stats.rak_data import show as show_rak_data
    from pages.extra_stats.tyopaikat import show as show_tyopaikat
    from pages.extra_stats.muuttoliike import show as show_muuttoliike
    from pages.extra_stats.asunto import show as show_asunto
    from pages.extra_stats.tyovoima import show as show_tyovoima
    from pages.extra_stats.tayttaneet import show as show_tayttaneet
    from pages.extra_stats.alk_valm_as import show as show_alk_valm_as
    from pages.extra_stats.saa import show as show_weather
    extra_stats_current_subpage_key = 'extra_stats_current_subpage'

    if extra_stats_current_subpage_key not in st.session_state:
        st.session_state[extra_stats_current_subpage_key] = show_default

    def display_page(subpage_key):
        with st.sidebar:
            st.markdown("## Aihealueet")
            if st.button("Järvenpään tapahtumat"):
                st.session_state[subpage_key] = show_jarvenpaa_events
            if st.button("Järvenpään väestön pääasiallinen toiminta ja muutokset"):
                st.session_state[subpage_key] = show_deaths
            if st.button("Rakennusdata"):
                st.session_state[subpage_key] = show_rak_data
            if st.button("Asuntotuotanto"):
                st.session_state[subpage_key] = show_alk_valm_as       
            if st.button("Työpaikat"):
                st.session_state[subpage_key] = show_tyopaikat
            if st.button("Työvoima"):
                st.session_state[subpage_key] = show_tyovoima
            if st.button("Muuttoliike"):
                st.session_state[subpage_key] = show_muuttoliike
            if st.button("Asuntokunnat"):
                st.session_state[subpage_key] = show_asunto  
            if st.button("15 vuotta täyttäneet pääas.toiminnan, koulutusasteen ja äidinkielen mukaan"):
                st.session_state[subpage_key] = show_tayttaneet
            if st.button("Sää"):
                st.session_state[subpage_key] = show_weather

        if subpage_key in st.session_state:
            try:
                st.session_state[subpage_key]()
            except Exception as e:
                st.error(f"An error occurred while rendering the sub-page: {str(e)}")
                st.session_state[subpage_key] = show_default
                st.session_state[subpage_key]()
        else:
            st.session_state[subpage_key] = show_default
            st.session_state[subpage_key]()

    display_page(extra_stats_current_subpage_key)
else:
    st.error(AUTH_FAIL_LOGIN_MSG)
