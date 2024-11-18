SELECT 
    * 
INTO nes_2023_national_avgs_gold
FROM {{ ref('nes_2023_national_avgs_silver') }}