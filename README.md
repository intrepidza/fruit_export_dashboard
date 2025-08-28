# Title:
SARS Trade Statistics for Fruit Exports mini-project

# Description:
A small end-to-end project that uses SARS Trade Statistics data specific to fruit exports (Section 2, Chapter 8).
Source data files obtained from SARS website: https://tools.sars.gov.za/tradestatsportal/data_download.aspx

These were cross-referenced with the Tariff Book document: https://www.sars.gov.za/wp-content/uploads/Legal/SCEA1964/Legal-LPrim-CE-Sch1P1Chpt1-to-99-Schedule-No-1-Part-1-Chapters-1-to-99.pdf

While not very granular, the output is still useful to give an idea as to the trading volumes to various countries.
Appears to be good for checking the FOB (Free on Board) value. Data includes nuts.

The tiering of the Tariff/HS Codes provided in the Tariff Book
Interestingly I picked up two codes which I don't believe should be in the trade stats data as they're considered subheadings. I.E. '08045010','08045090'

# Process:
1) Python scripts are used to:
- Upload any files not already in Google Cloud Platform bucket
- Create initial BigQuery Dataset and raw table for inserting file data
- Convert file data into a Pandas Dataframe, normalize column names and adjust data types.
- Read the Dataframe into the raw table
- (Scripts kicked off manually but can easily be added to Google Scheduler or Google Composer.)
- Generates and populates Lookup table in Bigquery
- Result of script processes are logged to app_log.log file.

2) DBT Core (as seen in 'dbt_structure/' folder) was then used process the data further and to generate models based off of the initial raw table:
- stg_sars_export (staging) = Used for initial processing, renaming of fields, fixing case issues etc.
- lkp_hs_code_data - A lookup table I created to give more context to the HS Codes in the source files.
- dim_calendar (dimension) = Used to track the dates
- dim_region_codes (dimension) = For region related fields
- dim_sars_hs_codes (dimension) = For storing all relevant SARS tariff codes
- fct_sars_export_data (fact) = For storing of measures, de-normalized reporting fields
- vw_sars_export_data (view) = combines the dimensions and fact tables for easier reference

DBT helps to create consistent models, the surrogate keys for the dimensions, documentation, tracking of the data lineage of the data, versioning of the models, and running tests which can be derived from Business Rules.

Example DBT lineage output:
![alt text](https://github.com/intrepidza/fruit_export_dashboard/blob/main/assets/dbt-dag.png?raw=true)


3) Google Looker is then used to visualize the data in an interactive Dashboard:
- https://lookerstudio.google.com/s/q6U8A0z0Lug

Snapshot sample:
![alt text](https://github.com/intrepidza/fruit_export_dashboard/blob/main/assets/snapshot.jpg?raw=true)


This dashboard supports cross-filtering via the components, parameter selection (data and HS Code) and drill-down (of specific component)

Owing to the low volume of data and rather generous costing in GCP, all of this was done at $0.
