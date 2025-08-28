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
),

hs_codes_lookup AS (
    SELECT
        hs_code
        ,hs_code_heading
        ,hs_code_heading_shortened
        ,hs_code_subheading_1
        ,hs_code_subheading_1_shortened
        ,hs_code_subheading_2
        ,hs_code_subheading_2_shortened
        ,detail
        ,detail_shortened
        ,friendly_summary_description
    FROM {{ source('fruit_export', 'lkp_hs_code_data') }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['stg.hs_code']) }} AS hs_id
    ,stg.hs_code
    ,stg.hs_code_description
    ,stg.section_code
    ,stg.section_description
    ,stg.chapter_code
    ,stg.chapter_description
    ,lkp.hs_code_heading
    ,lkp.hs_code_heading_shortened
    ,lkp.hs_code_subheading_1
    ,lkp.hs_code_subheading_1_shortened
    ,lkp.hs_code_subheading_2
    ,lkp.hs_code_subheading_2_shortened
    ,lkp.detail
    ,lkp.detail_shortened
    ,lkp.friendly_summary_description

FROM stg_data stg
LEFT OUTER JOIN hs_codes_lookup lkp
    ON lkp.hs_code = stg.hs_code
WHERE stg.hs_code NOT IN (
    '08045010',
    '08045090'
)