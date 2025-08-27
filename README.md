SARS Trade Stats for Fruit Exports mini-project

# Description:
Uses source files obtained from SARS website: https://tools.sars.gov.za/tradestatsportal/data_download.aspx
Python scripts are used to:
- Upload any files not already in Google Cloud Platform bucket
- Create initial BigQuery Dataset and raw table for inserting file data
- Convert file data into a Pandas Dataframe, normalize column names and adjust data types.
- Read the Dataframe into the raw table

DBT (as seen in 'dbt_structure/' folder) was then used to generate models based off of the initial raw table:
- stg_sars_export (staging) = Used for initial processing, renaming of fields, fixing case issues etc.
- dim_calendar (dimension) = Used to track the dates
- dim_region_codes (dimension) = For region related fields
- dim_sars_hs_codes (dimension) = For storing all relevant SARS tariff codes
- fct_sars_export_data (fact) = For storing of measures, de-normalized reporting fields
- vw_sars_export_data (view) = combines the dimensions and fact tables for easier reference

DBT helps to create consistent models, track the data lineage of the data, version the models, and run tests which can be derived from Business Rules.

Looker is then used to visualize the data:
- https://lookerstudio.google.com/s/mIilDK4qltY
https://lookerstudio.google.com/s/u95ITVHcno0

<iframe width="600" height="450" src="https://lookerstudio.google.com/embed/reporting/59322c63-fcf6-419d-b835-5a372c7f7d27/page/tEnnC" frameborder="0" style="border:0" allowfullscreen sandbox="allow-storage-access-by-user-activation allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox"></iframe>

Owing to the low volume of data and generous costing in GCP, all of this was done at $0.


# TO DO
Finish MetaData logic
Copy scripts to CloudShell?
Use Cloud Scheduler or Airflow?