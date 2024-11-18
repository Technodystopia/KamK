{{ config(materialized='table') }}

WITH unpivoted_data AS (
    {% for i in range(1, 10) %}
        SELECT
            yksikkokoodi,
            {{ i }} AS kysymyskoodi,
            value{{ i }} AS keskiarvo
        FROM {{ ref('nes_2023_national_avgs_filtered_bronze') }}
        {% if not loop.last %}UNION ALL{% endif %}
    {% endfor %}
)

SELECT
    yksikkokoodi,
    kysymyskoodi,
    keskiarvo
FROM unpivoted_data
