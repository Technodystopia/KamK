{{ config(materialized='table') }}

WITH all_values AS (
    {% for i in range(1, 23) %}
        SELECT
            yksikkokoodi, kvartaali_vuosi,
            -- Count all rows, indicating how many times a question was asked
            COUNT(value{{ i }}) AS kyselyt,
            -- Count all answered questions, so everything besides 0
            COUNT(CASE WHEN value{{ i }} > 0 THEN 1 END) AS vastaukset,
            -- Calculate the average of values greater than 0
            AVG(CASE WHEN value{{ i }} > 0 THEN value{{ i }} END) AS keskiarvo,
            -- Change value1-22 columns to code-column with a corresponding number
            {{ i }} AS kysymyskoodi

        FROM {{ ref('hopp_combined_filtered_bronze') }}
        GROUP BY yksikkokoodi, kvartaali_vuosi, kysymyskoodi
        {% if not loop.last %}UNION ALL{% endif %}
    {% endfor %}
)

SELECT 
    yksikkokoodi, kvartaali_vuosi, kysymyskoodi,
    kyselyt, vastaukset, keskiarvo
FROM all_values