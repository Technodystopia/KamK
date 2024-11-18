def show():
    import streamlit as st
    import requests
    import json
    import pandas as pd
    import altair as alt
    from datetime import datetime, timedelta

    def get_team_hours(workspace_id, api_key, start_date, end_date, project_name):
        url = f"https://reports.api.clockify.me/v1/workspaces/{workspace_id}/reports/summary"
        headers = {'X-Api-Key': api_key}
        data = {
            "dateRangeStart": start_date,
            "dateRangeEnd": end_date,
            "summaryFilter": {
                "groups": ["USER", "PROJECT"],
                "sortColumn": "GROUP"
            },
            "exportType": "JSON"
        }
        response = requests.post(url, headers=headers, json=data)
        data = response.json()
        total_hours = round(data['totals'][0]['totalTime'] / 3600, 2)
        
        team_hours = []
        week = (datetime.now() - datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")).days // 7 + 1
        min_hours_per_week = 16.625 * week
        for group in data['groupOne']:
            for subgroup in group['children']:
                if subgroup['name'] == project_name:
                    hours = round(subgroup['duration'] / 3600, 2)
                    remaining_hours = max(0, min_hours_per_week - hours)
                    team_hours.append({
                        'user': group['name'],
                        'hours': hours,
                        'remaining_hours': remaining_hours
                    })
        df_team_hours = pd.DataFrame(team_hours)
        return df_team_hours

    @st.cache_data
    def load_config():
        with open('data/json/data.json') as f:
            return json.load(f)

    data = load_config()
    workspace_id = data['workspace_id']
    api_key = data['api_key']
    start_date = data['start_date']
    end_date = data['end_date']
    project_name = data['project_name']

    week = (datetime.now() - datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")).days // 7 + 1
    min_hours_per_week = 16.625 * week

    st.title(f'Clockify Team {project_name} tunnit')
    if st.button('Hae tiimin tunnit'):
        df_team_hours = get_team_hours(workspace_id, api_key, start_date, end_date, project_name)
        df_team_hours = df_team_hours[df_team_hours['user'] != "Markus Maltela"]
        if not df_team_hours.empty:
            st.write(f"Kokonaistyötunnit: {df_team_hours['hours'].sum():.2f} tuntia")
            for row in df_team_hours.itertuples():
                st.write(f"{row.user}: {row.hours:.2f} tuntia, jäljellä olevat tunnit minimiin: {row.remaining_hours:.2f} tuntia")

            chart = alt.Chart(df_team_hours).mark_bar().encode(
                x='user:N',
                y='hours:Q',
                color='user:N',
                tooltip=['user', 'hours', 'remaining_hours']
            ).properties(width=600, height=300, title=f"Viikottaiset tunnit projektissa {project_name}")

            target_line = alt.Chart(pd.DataFrame({'hours': [min_hours_per_week]})).mark_rule(color='red').encode(
                y='hours:Q'
            )

            st.altair_chart(chart + target_line, use_container_width=True)
        else:
            st.write("Ei tunteja näytettäväksi.")
