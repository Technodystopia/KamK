WITH source AS (
    SELECT
        CAST("Yksikkökoodi" AS VARCHAR) as yksikkokoodi,
        CAST("kvartaali ja vuosi" AS VARCHAR) as kvartaali_vuosi,
        CAST("Kysymys pitkä" AS VARCHAR) as kysymyskoodi,
        CAST("Kyselyitä" AS INTEGER) as kyselyt,
        CAST("Vastauksia" AS INTEGER) as vastaukset,
        CAST("Keskiarvo" AS FLOAT) as keskiarvo
    FROM read_csv_auto('../data/lake/staging/CSV/hopp/filtered/Hopp_kooste_filtered.csv')
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
    CAST(REGEXP_EXTRACT("kysymyskoodi", '[0-9]+') as INTEGER) as kysymyskoodi, 
    kyselyt, vastaukset, keskiarvo
from source