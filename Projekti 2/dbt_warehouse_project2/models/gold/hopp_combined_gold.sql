{{ config(materialized='table') }}

SELECT 
    *
INTO hopp_combined_gold
FROM {{ ref('hopp_combined_silver') }}