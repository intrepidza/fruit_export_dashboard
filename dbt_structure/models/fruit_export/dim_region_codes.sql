{{ config(
    materialized='table',
    unique_key='region_id'
) }}

WITH stg_data AS (
    SELECT DISTINCT
        country_of_destination_code,
        country_of_destination_name,
        world_region
    FROM {{ ref('stg_sars_export_data') }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['country_of_destination_code']) }} AS region_id,
    country_of_destination_code,
    country_of_destination_name,
    world_region

FROM stg_data