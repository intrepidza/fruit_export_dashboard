{{ config(
    materialized='table'
) }}

WITH stg_data AS (
    SELECT * FROM {{ ref('stg_sars_export_data') }}
),
hs_dim AS (
    SELECT
        hs_id
        ,hs_code
    FROM {{ ref('dim_sars_hs_codes') }}
),
region_dim AS (
    SELECT
        region_id,
        country_of_destination_code
    FROM {{ ref('dim_region_codes') }}
),
calendar_dim AS (
    SELECT
        calendar_id,
        report_date
    FROM {{ ref('dim_calendar') }}
)

SELECT 
district_office_code
,district_office_name
,country_of_origin_code
,country_of_origin_name
,region_id
--,country_of_destination_code
--,country_of_destination_name
,hd.hs_id
--,tariff AS hs_code
,transport_code
,transport_code_description
,cd.calendar_id
--,2 AS section
--,'Vegetables' AS section_description
--,chapter
--,chapter_and_description
--,tariff_and_description
,statistical_quantity
,customs_value
--,world_region
FROM stg_data sd
LEFT OUTER JOIN hs_dim hd
    ON hd.hs_code = sd.hs_code
LEFT OUTER JOIN region_dim rd
    ON rd.country_of_destination_code = sd.country_of_destination_code
LEFT OUTER JOIN calendar_dim cd
    ON cd.report_date = sd.report_date