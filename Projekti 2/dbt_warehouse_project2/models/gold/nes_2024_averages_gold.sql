SELECT 
    * 
INTO nes_2024_averages_gold
FROM {{ ref('nes_2024_averages_silver') }}