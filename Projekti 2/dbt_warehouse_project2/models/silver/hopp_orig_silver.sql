SELECT 
    * 
INTO hopp_orig_silver
FROM {{ ref('hopp_combined_filtered_bronze') }}