{{ config(materialized='table') }}

SELECT
    *
INTO hopp_kooste_gold
FROM {{ ref('hopp_kooste_silver') }}