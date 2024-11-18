def show():
    import streamlit as st
    from datetime import datetime, timedelta
    from data.codimd import markdown_data

    min_date_allowed = min(markdown_data.keys())
    max_date_allowed = max(markdown_data.keys()) + timedelta(days=1)

    def display_markdown_for_date(selected_date):
        markdown_text = markdown_data.get(selected_date)
        if markdown_text:
            st.markdown(markdown_text)
        else:
            st.markdown("### Eipä löytynyt mittään =( Dev tiimi vaan laiskotellut")

    st.title("Daily-SCRUM palaverien koosteet")
    default_date = min_date_allowed
    selected_date = st.date_input("valikoi päivä", min_value=min_date_allowed, max_value=max_date_allowed, value=default_date)
    display_markdown_for_date(selected_date)

