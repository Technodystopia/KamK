{{ config(materialized='table') }}

SELECT
    yksikkokoodi,
    kysymyskoodi,
    keskiarvo
FROM (
    {% set value_cols = range(1,59) %}  -- Generates numbers from 1 to 58
    {% for i in value_cols %}
    SELECT
        yksikkokoodi,
        {{ i }} AS kysymyskoodi,
        value{{ i }} AS keskiarvo
    FROM {{ ref('nes_2024_silver') }}
    {% if not loop.last %}
    UNION ALL
    {% endif %}
    {% endfor %}
) unpivoted
