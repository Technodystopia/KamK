{{ config(materialized='table') }}

SELECT
    yksikkokoodi,
    kvartaali_vuosi,
    kysymyskoodi,
    kyselyt,
    vastaukset,
    CASE
        WHEN keskiarvo IS NULL AND vastaukset > 0 THEN CAST(kyselyt AS FLOAT) / vastaukset
        ELSE keskiarvo
    END AS keskiarvo
INTO hopp_kooste_silver
FROM {{ ref('hopp_kooste_filtered_bronze') }}
