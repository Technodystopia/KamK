{{ config(materialized='table') }}

WITH source AS (
    SELECT
        yksikkokoodi,
        value1, value2, value3, value4, value5, value6, value7, value8, value9, value10,
        value11, value12, value13, value14, value15, value16, value17, value18, value19, value20,
        value21, value22, value23, value24, value25, value26, value27, value28, value29, value30,
        value31, value32, value33, value34, value35, value36, value37, value38, value39, value40,
        value41, value42, value43, value44, value45, value46, value47, value48, value49, value50,
        value51, value52, value53, value54, value55, value56, value57, value58
    FROM {{ ref('nes_2024_filtered_bronze') }}
)

SELECT
    CASE
        WHEN yksikkokoodi = 'ENSIHOITO' THEN 'A'
        WHEN yksikkokoodi = 'EALAPSAIK' THEN 'B'
        WHEN yksikkokoodi = 'AIKTEHOHO' THEN 'C'
    END AS yksikkokoodi,
    value1, value2, value3, value4, value5, value6, value7, value8, value9, value10,
    value11, value12, value13, value14, value15, value16, value17, value18, value19, value20,
    value21, value22, value23, value24, value25, value26, value27, value28, value29, value30,
    value31, value32, value33, value34, value35, value36, value37, value38, value39, value40,
    value41, value42, value43, value44, value45, value46, value47, value48, value49, value50,
    value51, value52, value53, value54, value55, value56, value57, value58
FROM source
