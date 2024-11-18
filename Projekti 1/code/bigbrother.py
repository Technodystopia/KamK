import requests
import json
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
    print(f"Total Time: {total_hours:.2f} hours")

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
                print(f"{group['name']}: {hours:.2f} hours, Remaining Hours to minimum : {remaining_hours:.2f} hours")

    return team_hours

with open('../data/json/data.json') as f:
    data = json.load(f)

workspace_id = data['workspace_id']
api_key = data['api_key']
start_date = data['start_date']
end_date = data['end_date']
project_name = data['project_name']

team_hours = get_team_hours(workspace_id, api_key, start_date, end_date, project_name)
