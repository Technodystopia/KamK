"""
This module is used to create a web application using Streamlit. 
It includes functionalities such as authentication, page navigation, 
and user registration. The application is designed for data analysis 
and visualization.

The module uses the `streamlit_authenticator` for user authentication 
and `st_pages` for page navigation..
"""
# original imports
import streamlit as st
from st_pages import Page, Section, show_pages, add_page_title, hide_pages
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from code.constants import AUTH_FAIL_LOGIN_MSG # <-- store the error message globally

# from welcome
import duckdb
import os
import sys
import altair as alt



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

hide_pages([
    "pages/start.py",
])

authenticator.login()

def render_registration_form():
    """
    This function is used to render a registration form for new users. 
    It uses the `register_user` method from the `streamlit_authenticator` 
    module to register a new user. If the registration is successful, 
    it displays a success message. If there's an exception, 
    it displays an error message.
    """
    try:
        email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user()
        if email_of_registered_user:
            st.success('User registered successfully')
    except Exception as e:
        st.error(e)

if st.session_state["authentication_status"]:
    authenticator.logout()

    username = st.session_state.get("username")
    pages = [
        Page("start.py", "Käyttäjähallinta", icon=":closed_lock_with_key:"),
        Page("pages/etl.py", "ETL-putken kuvaus", icon=":desktop_computer:"),
        Page("pages/analysis.py", "Data-analyysi", icon=":page_facing_up:"),
        Page("pages/maps.py", "Kartat ja visualisointi", icon=":world_map:"),
        Page("pages/stats.py", "Tilastotietoja", icon=":bar_chart:"),
        Page("pages/extra_stats.py", "Lisädata", icon=":bar_chart:"),

        ]

    if username == "sadmin":
        pages.append(Page("pages/course_stats.py", "Kurssin tilastot (admin)", icon=":goat:"))

    show_pages(pages)

    st.write(f'Welcome *{st.session_state["name"]}*')

    sys.path.insert(0, os.path.join(os.getcwd(), 'pages'))
    sys.path.insert(0, os.path.join(os.getcwd(), 'data'))
    con = duckdb.connect("data/ultimate.duckdb")

else:
    if st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
        render_registration_form()



