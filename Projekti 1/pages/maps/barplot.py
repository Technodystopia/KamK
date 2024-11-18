def show():
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    import streamlit as st
    import duckdb
    import json
    from itertools import cycle
    from io import BytesIO
    from PIL import Image
    import matplotlib.pyplot as plt

    conn = duckdb.connect('data/ultimate.duckdb')
    conn2 = duckdb.connect('data/testdata.duckdb')
    background_image = Image.open('image/kauppa.jpg')
    image_width, image_height = background_image.size


    with open('data/json/zone.json', 'r') as f:
        ZONES = json.load(f)

    def count_rows_in_zones(df, zones):
        """Count the number of rows in each zone."""
        counts = []
        for zone in zones:
            count = df[(df['x'].between(zone['xmin'], zone['xmax'])) & (df['y'].between(zone['ymin'], zone['ymax']))].shape[0]
            counts.append(count)
        return counts

    query = "SELECT * FROM tokmanni"
    result = conn.execute(query)
    df = result.fetchdf()

    zone_counts = count_rows_in_zones(df, ZONES)
    df_counts = pd.DataFrame({'Zone': [zone['name'] for zone in ZONES], 'Count': zone_counts})

    color_discrete_sequence = cycle(px.colors.qualitative.Plotly)

    zone_to_color = {zone['name']: next(color_discrete_sequence) for zone in ZONES}


    fig = px.bar(df_counts, x='Zone', y='Count', title='Osastojakauma')
    fig.update_traces(marker_color=[zone_to_color[zone] for zone in df_counts['Zone']])
    fig.update_layout(xaxis_title=None, yaxis_title=None, showlegend=False)

    df_counts['Percentage'] = df_counts['Count'] / df_counts['Count'].sum() * 100

    fig2 = go.Figure(data=[go.Pie(labels=df_counts['Zone'], values=df_counts['Percentage'], hole=.3, marker=dict(colors=[zone_to_color[zone] for zone in df_counts['Zone']]))])
    fig2.update_layout(title_text='Prosenttijakauma')

    st.plotly_chart(fig)
    st.plotly_chart(fig2)

    def plot_data(scale_x=1.0, scale_y=1.0, offset_x=0, offset_y=0):
        query = "SELECT * FROM layer_table ORDER BY timestamp"

        result = conn2.execute(query)
        df = result.fetchdf()

        df["x"] = df["x"] * scale_x + offset_x
        df["y"] = image_height - (df["y"] * scale_y + offset_y)

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.imshow(background_image, extent=[0, image_width, 0, image_height])

        node_id_to_zone = {zone['node_id']: zone['name'] for zone in ZONES}
        node_id_to_color = {node_id: zone_to_color[zone_name] for node_id, zone_name in node_id_to_zone.items()}


        for node_id in df['node_id'].unique():
            df_node = df[df['node_id'] == node_id]
            color = node_id_to_color[node_id]
            ax.scatter(df_node["x"], df_node["y"], label=f"Node {node_id}", color=color, s=1)

        plt.axis('off')
        plt.tight_layout()
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img = Image.open(buf)
        plt.close()
        return img, df


    img, df = plot_data(scale_x=0.1090, scale_y=0.1085, offset_x=116, offset_y=27)
    st.image(img)