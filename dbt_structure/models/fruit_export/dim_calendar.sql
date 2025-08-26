{{ config(
    materialized='table',
    unique_key='calendar_id'
) }}

WITH stg_data AS (
    SELECT DISTINCT
        report_date
    FROM {{ ref('stg_sars_export_data') }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['report_date']) }} AS calendar_id
    ,report_date

FROM stg_data