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
    from pages.default import show as show_default
    from pages.etl.expl import show as show_etl
    from pages.etl.ani import show as show_ani

    etl_current_subpage_key = 'maps_current_subpage'

    if etl_current_subpage_key not in st.session_state:
        st.session_state[etl_current_subpage_key] = show_default

    def display_page(subpage_key):
        with st.sidebar:
            st.markdown("## Aihealueet")
            if st.button("Prosessin kuvaus"):
                st.session_state[subpage_key] = show_etl
            if st.button("Filtterit"):
                st.session_state[subpage_key] = show_ani

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

    display_page(etl_current_subpage_key)
else:
    st.error(AUTH_FAIL_LOGIN_MSG)
