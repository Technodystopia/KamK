import streamlit as st
from st_pages import Page, Section, add_page_title
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from code.constants import AUTH_FAIL_LOGIN_MSG

# sub pages
from pages.analysis import intro, methods, results, recommendations

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

# the unique key is for keeping the correct sub-page loaded
# (so that it wont overflow from the previous main category)
analysis_current_subpage_key = 'analysis_current_subpage'

def display_page(subpage_key):
    if st.session_state["authentication_status"]:
        # Sidebar stuff
        st.sidebar.markdown("## Aihealueet")
        create_sidebar_button("Johdanto & Aineiston Kuvaus", intro.show)
        create_sidebar_button("Analyysimenetelmät", methods.show)
        create_sidebar_button("Tulokset & Tulkinnat", results.show)
        create_sidebar_button("Päätelmät & Suositukset", recommendations.show)

        # Execute the current sub-page function based on the category-specific key
        if subpage_key in st.session_state:
            try:
                st.session_state[subpage_key]()
            except Exception as e:
                st.error(f"An error occurred while rendering the sub-page: {str(e)}")
                # Fallback to default sub-page in case of an error
                st.session_state[subpage_key] = intro.show
                st.session_state[subpage_key]()
        else:
            # Default to intro sub-page if no sub-page has been selected yet
            st.session_state[subpage_key] = intro.show
            st.session_state[subpage_key]()
    else:
        st.error(AUTH_FAIL_LOGIN_MSG)

def create_sidebar_button(page_name, page_content):
    if st.sidebar.button(page_name):
        st.session_state[analysis_current_subpage_key] = page_content

if analysis_current_subpage_key not in st.session_state:
    st.session_state[analysis_current_subpage_key] = intro.show

display_page(analysis_current_subpage_key)