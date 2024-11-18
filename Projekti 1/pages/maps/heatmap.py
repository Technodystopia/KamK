def show():
    from io import BytesIO
    from PIL import Image
    from PIL import ImageOps

    import datetime
    import streamlit as st
    import numpy as np
    import pandas as pd
    import altair as alt
    import duckdb
    import matplotlib.pyplot as plt
    import calendar

    conn = duckdb.connect('data/ultimate.duckdb')
    background_image = Image.open('image/kauppa.jpg')
    image_width, image_height = background_image.size

    table_options = {"EET Aika": "tokmanni2", "UTC Aika": "tokmanni"}
    selected_table = st.selectbox('Aikavyöhyke:', options=list(table_options.keys()))
    invert_colors = st.selectbox('Kuvan värin vaihto:', options=['Ei', 'Kyllä'])

    # pitää noi funktion importit jossain kohtaa fiksata
    def plot_data(start_year, start_month, start_day, end_year, end_month, end_day, start_hour, 
                end_hour, invert_colors, scale_x=1.0, scale_y=1.0, offset_x=0, offset_y=0, 
                selected_nodes=None):
        background_image = Image.open('image/kauppa.jpg')
        heat_color = "Reds"
        if invert_colors == 'Kyllä':
            background_image = ImageOps.invert(background_image)
            heat_color = "gist_heat"
        image_width, image_height = background_image.size
        
        if start_date_selected > end_date_selected:
            # Special logic for not using BETWEEN
            query_part1 = f"SELECT * FROM {table_options[selected_table]} WHERE timestamp >= '{start_date_selected}' AND timestamp <= '{start_date_selected.replace(day=calendar.monthrange(start_date_selected.year, start_date_selected.month)[1])}'"
            query_part2 = f"SELECT * FROM {table_options[selected_table]} WHERE timestamp >= '{end_date_selected.replace(day=1)}' AND timestamp <= '{end_date_selected}'"
            query = f"({query_part1}) UNION ALL ({query_part2}) ORDER BY timestamp"
        else:
            # Safe to use BETWEEM
            query = f"SELECT * FROM {table_options[selected_table]} WHERE timestamp BETWEEN '{start_date_selected}' AND '{end_date_selected}' ORDER BY timestamp"

        result = conn.execute(query)
        df = result.fetchdf()

        df["x"] = df["x"] * scale_x + offset_x
        df["y"] = image_height - (df["y"] * scale_y + offset_y)

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.imshow(background_image, extent=[0, image_width, 0, image_height])

        # Note: the gridsize and opacity sliders are connected here.
        hb = ax.hexbin(df["x"], df["y"], gridsize=plot_size, cmap=heat_color, bins='log', alpha=opacity_level)

        cb = fig.colorbar(hb, ax=ax)
        cb.set_label('log10(N)')

        plt.axis('off')
        plt.tight_layout()
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img = Image.open(buf)
        plt.close()

        return img, df

    start_date = datetime.datetime(2019, 3, 1)
    end_date = datetime.datetime(2020, 1, 31)

    start_date_selected = st.date_input('Ensimmäinen päivämäärä:', start_date, min_value=start_date, max_value=end_date)
    end_date_selected = st.date_input('Viimeinen päivämäärä:', end_date, min_value=start_date, max_value=end_date)

    start_year = start_date_selected.year
    start_month = start_date_selected.month
    start_day = start_date_selected.day

    end_year = end_date_selected.year
    end_month = end_date_selected.month
    end_day = end_date_selected.day

    plot_size = st.slider('Alueiden koko:', 30, 300, 250)
    start_hour, end_hour = st.slider('Aikaväli:', 7, 23, (7, 23), 1)
    opacity_level = st.slider('Kuumien alueiden läpikuultavuus:', 0.0, 1.0, 1.0)

    img, df = plot_data(start_year, start_month, start_day, end_year, end_month, 
                        end_day, start_hour, end_hour, invert_colors, 
                        scale_x=0.1090, scale_y=0.1080, offset_x=116, offset_y=27)

    st.image(img)
