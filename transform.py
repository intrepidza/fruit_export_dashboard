import pandas as pd

from utils import print_and_log, deco_print_and_log

@deco_print_and_log("Read and convert to DataFrame")
def read_file(file_name):
    return pd.read_excel(file_name, na_filter=False) # na_filter is important to not drop Namibia Country Code


def clean_data(df):
    # Drop column: 'TradeType'
    df = df.drop(columns=['TradeType'])

    # Drop column: 'Section'
    df = df.drop(columns=['Section'])

    # Drop column: 'SectionAndDescription'
    df = df.drop(columns=['SectionAndDescription'])

    # Drop column: 'Chapter'
    df = df.drop(columns=['Chapter'])

    # Drop column: 'TransportCode'
    df = df.drop(columns=['TransportCode'])
    

    # Change column type to string for column: 'YearMonth'
    df = df.astype({'YearMonth': 'string'})
       
    # Transform based on the following examples:
    df.insert(10, "Date", df["YearMonth"].str[:4] + "-" + df["YearMonth"].str[4:] + "-01")

    # Derive column 'hs_description' from column: 'TariffAndDescription'
    df.insert(11, "hs_description", df["TariffAndDescription"].str[10:])

    # Drop column: 'TariffAndDescription'
    df = df.drop(columns=['TariffAndDescription'])
    
    # Drop column: 'YearMonth'
    df = df.drop(columns=['YearMonth'])
    
    # Drop column: 'CalendarYear'
    df = df.drop(columns=['CalendarYear'])
    
    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Change 'Date' column to end of month
    df['Date'] = df['Date'].dt.to_period('M').dt.to_timestamp('M')
    
    # Fix empty values:


    # Rename columns
    df = df.rename(columns={
        'Tariff': 'hs_code',
        'DistrictOfficeCode': 'district_office_code',
        'DistrictOfficeName': 'district_office_name',
        'CountryOfOrigin': 'country_of_origin_code',
        'CountryOfOriginName': 'country_of_origin_name',
        'CountryOfDestination': 'destination_country_code',
        'CountryOfDestinationName': 'destination_country_name',
        'ChapterAndDescription': 'chapter_and_description',
        'WorldRegion': 'world_region',
        'StatisticalUnit': 'unit',
        'StatisticalQuantity': 'quantity', 
        'CustomsValue': 'value',
        'TransportCodeDescription': 'transport_code_description',
        })

    # Reorder columns:


    return df
