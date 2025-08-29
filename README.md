# Title:
SARS Trade Statistics for Fruit Exports mini-project

# Description:
A small end-to-end project that loads SARS Trade Statistics data specific to fruit exports (Section 2, Chapter 8), transforms it and makes it available in a Dashboard.

Source data files obtained from SARS website:
https://tools.sars.gov.za/tradestatsportal/data_download.aspx

These were cross-referenced with the Tariff Book document: 
https://www.sars.gov.za/wp-content/uploads/Legal/SCEA1964/Legal-LPrim-CE-Sch1P1Chpt1-to-99-Schedule-No-1-Part-1-Chapters-1-to-99.pdf

While not very granular (i.e. no data on varietals of fruit), the output is still useful to give an idea as to the overall trading volumes to various countries.
(i.e. for checking the FOB (Free on Board) value and weights. Data includes nuts.)

The tiering of the Tariff/HS Codes provided in the Tariff Book provided somewhat of a challenge in terms of how they are structured, in order to extract meaningful descriptions of the relevant items. I ended up creating my own reference Excel document with shortened descriptions (highlighted in yellow) as well as a 'friendly' summarized description (highlighted in green) which could then be used in the dashboard. 

This file exists under path: 
docs\hs_codes_details.xlsx

Interestingly I picked up two codes which I don't believe should be in the trade stats data as they're considered subheadings. I.E. '08045010','08045090'.
These have been excluded in the underlying data.


# Process:
1) Python scripts are used to:
- Upload any files from a local directory that are not already in specific Google Cloud Platform bucket.
- Create initial BigQuery Dataset and raw tables for inserting file data
- Convert file data into a Pandas Dataframe, normalize column names and adjust data types.
- Load the Dataframes into the raw tables.
- Result of script processes are logged to app_log.log file.

(Scripts were run manually but can easily be added to Google Scheduler or Google Composer.)


2) DBT Core (as seen in 'dbt_structure/' folder) was then used process the data further and to generate models based off of the initial raw table:
- stg_sars_export (staging) = Used for initial processing, renaming of fields, fixing case issues etc.
- lkp_hs_code_data - A lookup table I created to give more context to the HS Codes in the source files.
- dim_calendar (dimension) = Used to track the dates
- dim_region_codes (dimension) = For region related fields
- dim_sars_hs_codes (dimension) = For storing all relevant SARS tariff codes
- fct_sars_export_data (fact) = For storing of measures, de-normalized reporting fields
- vw_sars_export_data (view) = combines the dimensions and fact tables for easier reference, but not used in the Dashboard 

DBT helps to create consistent models, the surrogate keys for the dimensions, documentation, tracking of the data lineage of the data, versioning of the models, and running tests which can be derived from Business Rules.

Example DBT data lineage output:

![alt text](https://github.com/intrepidza/fruit_export_dashboard/blob/main/assets/dbt-dag.png?raw=true)


Example Entity Relationship Diagram: (created in dbdiagram.io)

![alt text](https://github.com/intrepidza/fruit_export_dashboard/blob/main/assets/ERD.png?raw=true)

To note:
- The surrogate keys are generated as guid's and stored as strings as per what was generated from DBT. Hence not integers.
- The 'dim_sars_hs_codes' Dimension table is rather cumbersome, but was mainly to allow for providing additional display options on the Dashboard.
- The 'fct_sars_export_data' Fact table could also be reduced further in terms of fields, but de-normalizing it further could come at the cost of performance when introducing additional joins etc.


3) Google Looker is then used to visualize the data in an interactive Dashboard which can be view using this address:

- https://lookerstudio.google.com/s/q6U8A0z0Lug


Snapshot sample:

![alt text](https://github.com/intrepidza/fruit_export_dashboard/blob/main/assets/Snapshot.png?raw=true)


This dashboard supports cross-filtering via the components, parameter selection (data and HS Code) and drill-down (of specific component)

Owing to the low volume of data and rather generous costing in GCP, all of this was done at $0.
A similar project should be easily achievable in Azure or AWS, but at a higher cost.
