def show():
    from io import BytesIO
    from PIL import Image
    from PIL import ImageOps

    import datetime
    import streamlit as st
    import numpy as np
    import duckdb
    import matplotlib.pyplot as plt

    conn = duckdb.connect('data/ultimate.duckdb')
    background_image = Image.open('image/kauppa.jpg')
    image_width, image_height = background_image.size

    table_options = {"EET Aika": "tokmanni2", "UTC Aika": "tokmanni"}
    selected_table = st.selectbox('Aikavyöhyke:', options=list(table_options.keys()))
    invert_colors = st.selectbox('Kuvan värin vaihto:', options=['Ei', 'Kyllä'])

    unique_node_ids = [3200, 3224, 3240, 42787, 45300, 51719, 51720, 51735, 51751, 51850, 51866, 51889, 
                    51968, 51976, 51992, 52003, 52008, 52023, 52099, 52535, 53000, 53011, 53027, 53130,
                    53768, 53795, 53888, 53924, 53936, 54016, 64458]

    selected_nodes = st.multiselect('Ostoskärry(t):', options=list(unique_node_ids))

    def plot_data(start_year, start_month, start_day, end_year, end_month, end_day, start_hour, 
                end_hour, invert_colors, scale_x=1.0, scale_y=1.0, offset_x=0, offset_y=0, 
                selected_nodes=None):
        background_image = Image.open('image/kauppa.jpg')
        if invert_colors == 'Kyllä':
            background_image = ImageOps.invert(background_image)
        image_width, image_height = background_image.size
        if start_hour == "All" and start_day == "All" and end_day == "All":
            query = f"SELECT * FROM {table_options[selected_table]} WHERE EXTRACT(YEAR FROM timestamp) BETWEEN {start_year} AND {end_year} AND EXTRACT(MONTH FROM timestamp) BETWEEN {start_month} AND {end_month} ORDER BY timestamp"
        elif start_hour == "All" and end_day == "All":
            query = f"SELECT * FROM {table_options[selected_table]} WHERE EXTRACT(YEAR FROM timestamp) = {start_year} AND EXTRACT(MONTH FROM timestamp) = {start_month} AND EXTRACT(DAY FROM timestamp) BETWEEN {start_day} AND {end_day} ORDER BY timestamp"
        elif start_day == "All" and end_day == "All":
            query = f"SELECT * FROM {table_options[selected_table]} WHERE EXTRACT(YEAR FROM timestamp) = {start_year} AND EXTRACT(MONTH FROM timestamp) = {start_month} AND EXTRACT(HOUR FROM timestamp) BETWEEN {start_hour} AND {end_hour} ORDER BY timestamp"
        else:
            query = f"SELECT * FROM {table_options[selected_table]} WHERE EXTRACT(YEAR FROM timestamp) = {start_year} AND EXTRACT(MONTH FROM timestamp) = {start_month} AND EXTRACT(DAY FROM timestamp) BETWEEN {start_day} AND {end_day} AND EXTRACT(HOUR FROM timestamp) BETWEEN {start_hour} AND {end_hour} ORDER BY timestamp"

        result = conn.execute(query)
        df = result.fetchdf()

        df["x"] = df["x"] * scale_x + offset_x
        df["y"] = image_height - (df["y"] * scale_y + offset_y)

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.imshow(background_image, extent=[0, image_width, 0, image_height])

        cmap = plt.get_cmap('turbo')
        unique_node_ids = df['node_id'].unique()
        colors = cmap(np.linspace(0, 1, len(unique_node_ids)*1))

        for node_id, color in zip(unique_node_ids, colors):
            if selected_nodes is None or node_id in selected_nodes:
                df_node = df[df['node_id'] == node_id]
                ax.scatter(df_node["x"], df_node["y"], label=f"Node {node_id}", color=color, s=1)

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

    start_hour, end_hour = st.slider('Aikaväli:', 7, 23, (7, 23), 1)

    img, df = plot_data(start_year, start_month, start_day, end_year, end_month, 
                        end_day, start_hour, end_hour, invert_colors, 
                        scale_x=0.1090, scale_y=0.1080, offset_x=116, offset_y=27, selected_nodes=selected_nodes)

    st.image(img)
