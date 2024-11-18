{{ config(materialized='table') }}

WITH source AS (
    SELECT
        CAST("Yksikkökoodi" AS VARCHAR) as yksikkokoodi,
        CAST("kvartaali ja vuosi" AS VARCHAR) as kvartaali_vuosi,
        "1" as value1, "2" as value2, "3" as value3,
        "4" as value4, "5" as value5, "6" as value6,
        "7" as value7, "8" as value8, "9" as value9,
        "10" as value10, "11" as value11, "12" as value12,
        "13" as value13, "14" as value14, "15" as value15,
        "16" as value16, "17" as value17, "18" as value18,
        "19" as value19, "20" as value20, "21" as value21,
        "22" as value22
    FROM read_csv_auto('../data/lake/staging/CSV/hopp/filtered/Hopp_combined_filtered.csv')
)

SELECT
    REGEXP_REPLACE("yksikkokoodi", 'ENSIHOITO|EALAPSAIK|AIKTEHOHO', 
        CASE 
            WHEN "yksikkokoodi" = 'ENSIHOITO' then 'A'
            WHEN "yksikkokoodi" = 'EALAPSAIK' then 'B'
            WHEN "yksikkokoodi" = 'AIKTEHOHO' then 'C'
        END
    ) AS "yksikkokoodi",
    kvartaali_vuosi,
    {% for i in range(1, 23) %}
        CAST(
            CASE 
                WHEN value{{ i }} = 'E' or value{{ i }} = '' or value{{ i }} is NULL then 0
                ELSE CAST(value{{ i }} as integer)
            END 
        AS integer) AS value{{ i }}{% if not loop.last %},{% endif %}
    {% endfor %}
FROM source
