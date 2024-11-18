SELECT 
    * 
INTO hopp_orig_gold
FROM {{ ref('hopp_orig_silver') }}