WITH averages_by_yksikkokoodi AS (
    SELECT
        Yksikkokoodi,
            value1,
            value2,
            value3,
            value4,
            value5,
            AVG(value6) AS value6,
            AVG(value7) AS value7,
            AVG(value8) AS value8,
            AVG(value9) AS value9,
            AVG(value10) AS value10,
            AVG(value11) AS value11,
            AVG(value12) AS value12,
            AVG(value13) AS value13,
            AVG(value14) AS value14,
            AVG(value15) AS value15,
            AVG(value16) AS value16,
            AVG(value17) AS value17,
            AVG(value18) AS value18,
            AVG(value19) AS value19,
            AVG(value20) AS value20,
            AVG(value21) AS value21,
            AVG(value22) AS value22,
            AVG(value23) AS value23,
            AVG(value24) AS value24,
            AVG(value25) AS value25,
            AVG(value26) AS value26,
            AVG(value27) AS value27,
            AVG(value28) AS value28,
            AVG(value29) AS value29,
            AVG(value30) AS value30,
            AVG(value31) AS value31,
            AVG(value32) AS value32,
            AVG(value33) AS value33,
            AVG(value34) AS value34,
            AVG(value35) AS value35,
            AVG(value36) AS value36,
            AVG(value37) AS value37,
            AVG(value38) AS value38,
            AVG(value39) AS value39,
            AVG(value40) AS value40,
            AVG(value41) AS value41,
            AVG(value42) AS value42,
            AVG(value43) AS value43,
            AVG(value44) AS value44,
            AVG(value45) AS value45,
            AVG(value46) AS value46,
            AVG(value47) AS value47,
            AVG(value48) AS value48,
            AVG(value49) AS value49,
            AVG(value50) AS value50,
            AVG(value51) AS value51,
            AVG(value52) AS value52,
            AVG(value53) AS value53,
            AVG(value54) AS value54,
            AVG(value55) AS value55,
            AVG(value56) AS value56,
            AVG(value57) AS value57,
            AVG(value58) AS value58
        
    FROM
        {{ ref('nes_2023_filtered_bronze') }}
    GROUP BY
        Yksikkokoodi,
        value1,
        value2,
        value3,
        value4,
        value5
)

SELECT * FROM averages_by_yksikkokoodi