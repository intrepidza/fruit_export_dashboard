{{ config(
    materialized='view'
) }}

WITH fct_data AS (
    SELECT * FROM {{ ref('fct_sars_export_data') }}
),
hs_dim AS (
    SELECT
        *
    FROM {{ ref('dim_sars_hs_codes') }}
),
region_dim AS (
    SELECT
        *
    FROM {{ ref('dim_region_codes') }}
),
calendar_dim AS (
    SELECT
        *
    FROM {{ ref('dim_calendar') }}
)

SELECT 
    fct.district_office_code
    ,fct.district_office_name
    ,fct.country_of_origin_code
    ,fct.country_of_origin_name
    ,r_dim.country_of_destination_code
    ,r_dim.country_of_destination_name
    ,dim.hs_code
    ,dim.hs_code_description
    ,fct.transport_code
    ,fct.transport_code_description	
    ,cd.report_date
    ,dim.section_code
    ,dim.section_description
    ,dim.chapter_code
    ,dim.chapter_description
    ,fct.statistical_quantity
    ,fct.customs_value
    ,r_dim.world_region
FROM fct_data fct
INNER JOIN hs_dim dim
    ON dim.hs_id = fct.hs_id
INNER JOIN region_dim r_dim
    ON r_dim.region_id = fct.region_id
LEFT OUTER JOIN calendar_dim cd
    ON cd.calendar_id = fct.calendar_id 