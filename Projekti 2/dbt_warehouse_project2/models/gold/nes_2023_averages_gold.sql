SELECT 
    * 
INTO nes_2023_averages_gold
FROM {{ ref('nes_2023_averages_silver') }}