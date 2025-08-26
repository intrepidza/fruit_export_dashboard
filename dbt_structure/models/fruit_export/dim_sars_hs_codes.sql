{{ config(
    materialized='table',
    unique_key='hs_id'
) }}

WITH stg_data AS (
    SELECT DISTINCT
    hs_code
    ,hs_code_description
    ,section_code
    ,section_description
    ,chapter_code
    ,chapter_description
    FROM {{ ref('stg_sars_export_data') }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['hs_code']) }} AS hs_id
    ,hs_code
    ,hs_code_description
    ,section_code
    ,section_description
    ,chapter_code
    ,chapter_description

FROM stg_data