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

st.markdown("""
            ## Projekti 1 / Team GOAT
            Valitse aihealue sivupaneelista.
            """)

if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'], st.session_state['username'] = authenticator.login("Login", "main", fields=['username', 'password'])

if st.session_state["authentication_status"]:
    from pages.default import show as show_default
    from pages.course_stats.clockify import show as show_clockify
    from pages.course_stats.cource import show as show_cource
    from pages.course_stats.scrum import show as show_scrum

    # the unique key is for keeping the correct sub-page loaded
    # (so that it wont overflow from the previous main category)
    course_stats_current_subpage_key = 'course_stats_current_subpage'

    def display_page(subpage_key):
        # Sidebar setup stuff
        with st.sidebar:
            st.markdown("## Aihealueet")
            if st.button("Tiimin kuvaus"):
                st.session_state[subpage_key] = show_cource
            if st.button("SCRUM koosteet"):
                st.session_state[subpage_key] = show_scrum
            if st.button("Clockify tilasto"):
                st.session_state[subpage_key] = show_clockify

        # Execute the current sub-page function based on the category-specific key
        if subpage_key in st.session_state:
            try:
                st.session_state[subpage_key]()
            except Exception as e:
                st.error(f"An error occurred while rendering the sub-page: {str(e)}")
                # Fallback to default sub-page in case of an error
                st.session_state[subpage_key] = show_default
                st.session_state[subpage_key]()
        else:
            # Default to scrum sub-page if no sub-page has been selected yet
            st.session_state[subpage_key] = show_default
            st.session_state[subpage_key]()

    display_page(course_stats_current_subpage_key)
else:
    st.error(AUTH_FAIL_LOGIN_MSG)

# a neat expander element for showing/hiding stuff if needed. example here
#with st.expander("Näytä tulokset"):
    #st.markdown("...")