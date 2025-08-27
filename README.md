SARS Trade Stats for Fruit Exports mini-project

# Description:
Uses source files obtained from SARS website: https://tools.sars.gov.za/tradestatsportal/data_download.aspx
Python scripts are used to:
- Upload any files not already in Google Cloud Platform bucket
- Create initial BigQuery Dataset and raw table for inserting file data
- Convert file data into a Pandas Dataframe, normalize column names and adjust data types.
- Read the Dataframe into the raw table

DBT Core (as seen in 'dbt_structure/' folder) was then used to generate models based off of the initial raw table:
- stg_sars_export (staging) = Used for initial processing, renaming of fields, fixing case issues etc.
- dim_calendar (dimension) = Used to track the dates
- dim_region_codes (dimension) = For region related fields
- dim_sars_hs_codes (dimension) = For storing all relevant SARS tariff codes
- fct_sars_export_data (fact) = For storing of measures, de-normalized reporting fields
- vw_sars_export_data (view) = combines the dimensions and fact tables for easier reference

DBT helps to create consistent models, the surrogate keys for the dimensions, documentation, tracking of the data lineage of the data, versioning of the models, and running tests which can be derived from Business Rules.

Example DBT lineage output:
![alt text](https://github.com/intrepidza/fruit_export_dashboard/blob/main/assets/dbt-dag.png?raw=true)


Google Looker is then used to visualize the data in an interactive Dashboard:
- https://lookerstudio.google.com/s/onrhh4-3joU

This dashboard supports cross-filtering, parameter selection (data and HS Code) and drill-down (of specific component)

Owing to the low volume of data and rather generous costing in GCP, all of this was done at $0.
