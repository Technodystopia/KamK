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
    from pages.stats.pie import show as show_pie
    from pages.stats.tilasto import show as show_tilasto
    from pages.stats.seasonality import show as show_seasonality
    from pages.stats.quantile import show as show_quantile
    from pages.stats.kurtosis import show as show_kurtosis
    from pages.stats.iqr import show as show_iqr
    from pages.stats.median import show as show_median
    from pages.stats.max import show as show_max
    from pages.stats.min import show as show_min
    from pages.stats.mean import show as show_mean
    from pages.stats.skew import show as show_skew
    from pages.stats.std_dev import show as show_std_dev
    from pages.stats.variance import show as show_variance

    # the unique key is for keeping the correct sub-page loaded
    # (so that it wont overflow from the previous main category)
    stats_current_subpage_key = 'stats_current_subpage'

    if stats_current_subpage_key not in st.session_state:
        st.session_state[stats_current_subpage_key] = show_default

    def display_page(subpage_key):
        # Sidebar setup stuff
        with st.sidebar:
            st.markdown("## Aihealueet")
            if st.button("Pie chart"):
                st.session_state[subpage_key] = show_pie
            if st.button("Datapisteiden määrä"):
                st.session_state[subpage_key] = show_tilasto
            if st.button("Seasonality"):
                st.session_state[subpage_key] = show_seasonality
            if st.button("Quantile"):
                st.session_state[subpage_key] = show_quantile
            if st.button("Kurtosis"):
                st.session_state[subpage_key] = show_kurtosis
            if st.button("IQR"):
                st.session_state[subpage_key] = show_iqr
            if st.button("Median"):
                st.session_state[subpage_key] = show_median
            if st.button("Mean"):
                st.session_state[subpage_key] = show_mean
            if st.button("Min"):
                st.session_state[subpage_key] = show_min
            if st.button("Max"):
                st.session_state[subpage_key] = show_max
            if st.button("Skew"):
                st.session_state[subpage_key] = show_skew
            if st.button("Standard deviation"):
                st.session_state[subpage_key] = show_std_dev
            if st.button("Variance"):
                st.session_state[subpage_key] = show_variance

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
            st.session_state[subpage_key] = show_default
            st.session_state[subpage_key]()

    display_page(stats_current_subpage_key)
else:
    st.error(AUTH_FAIL_LOGIN_MSG)
