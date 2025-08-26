{{
  config(
    materialized='table'
  )
}}

SELECT 
trade_type
,district_office_code
,district_office_name
,country_of_origin AS country_of_origin_code
,country_of_origin_name
,country_of_destination AS country_of_destination_code
,country_of_destination_name
,tariff AS hs_code
,statistical_unit
,transport_code
,transport_code_description	
,LAST_DAY(CAST(CONCAT(SUBSTR(year_month,1,4),'-',SUBSTR(year_month,5),'-01') AS DATE)) AS report_date -- Derive proper date
,section AS section_code
,SUBSTRING(section_and_description, 5) AS section_description -- Extract description
,chapter AS chapter_code
,SUBSTRING(chapter_and_description, 6) AS chapter_description -- Extract description
,SUBSTRING(tariff_and_description, 12) AS hs_code_description -- Extract description
,statistical_quantity
,customs_value
,INITCAP(LOWER(world_region)) AS world_region -- Fixing case issues

--FROM trepz-gcp-data-eng.fruit_export.raw_sars_export_data
FROM {{ source('fruit_export', 'raw_sars_export_data') }}