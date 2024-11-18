{{ config(materialized='table') }}

WITH source AS (
    SELECT
        CAST("Yksikkökoodi" AS VARCHAR) AS yksikkokoodi,
        "Laadukkaan ammatillisen toiminnan perusteet" AS value1,
        "Johtaminen" AS value2,
        "Autonomia" AS value3,
        "Moniammatillinen yhteistyö" AS value4,
        "Hoitajien välinen yhteistyö" AS value5,
        "Ammatillinen kasvu" AS value6,
        "Työnteossa tarvittavat resurssit" AS value7,
        "Muut sitoutumiseen vaikuttavat tekijät" AS value8,
        "Sitoutuneisuus" AS value9
    FROM read_csv_auto('../data/lake/staging/CSV/nes/filtered/nes_2023_national_avgs_filtered.csv')
    WHERE "Yksikkökoodi" IN ('AIKTEHOHO', 'EALAPSAIK', 'ENSIHOITO')
)

SELECT
    REGEXP_REPLACE(yksikkokoodi, 'ENSIHOITO|EALAPSAIK|AIKTEHOHO', 
        CASE 
            WHEN yksikkokoodi = 'ENSIHOITO' THEN 'A'
            WHEN yksikkokoodi = 'EALAPSAIK' THEN 'B'
            WHEN yksikkokoodi = 'AIKTEHOHO' THEN 'C'
        END
    ) AS yksikkokoodi,
    {% for i in range(1, 10) %}
        CAST(value{{ i }} AS FLOAT) AS value{{ i }}{% if not loop.last %},{% endif %}
    {% endfor %}
FROM source
