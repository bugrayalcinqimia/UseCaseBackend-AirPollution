import pandas as pd


def load_dataset():
    # Load the dataset
    df = pd.read_csv("data/air-pollution.csv")
    return df


def filter_countries_with_codes(df):
    # Filter out rows where the Code is missing (continents)
    country_df = df[df['Code'].notna()]

    # Create a unique list of country and code pairs, and rename 'Entity' to 'Country'
    country_list = country_df[['Entity', 'Code']].drop_duplicates()
    country_list.rename(columns={'Entity': 'Country'}, inplace=True)

    return country_list


def fetch_country_info(df, code):
    # Filter the DataFrame for the given country code
    country_data = df[df['Code'] == code.upper()]

    if country_data.empty:
        return None  # If no data is found, return None

    # Get the country name (assuming the name is the same for all years)
    country_name = country_data['Entity'].iloc[0]

    # Get the years interval (min and max year)
    min_year = country_data['Year'].min()
    max_year = country_data['Year'].max()

    return {
        "country_name": country_name,
        "years_interval": f"{min_year} - {max_year}"
    }


def filter_data_by_date(df, code, start_date, end_date):
    # Convert the input code and Code column to lowercase for case-insensitive comparison
    filtered_df = df[(df['Code'] == code.upper()) &
                     (df['Year'] >= start_date) & (df['Year'] <= end_date)]

    actual_start_date = filtered_df['Year'].min()
    actual_end_date = filtered_df['Year'].max()

    if filtered_df.empty:
        return None

    return filtered_df, actual_start_date, actual_end_date


def calculate_averages(filtered_df):
    # Fill NaN values with 0 or another appropriate value and return the averages
    return filtered_df.mean(numeric_only=True).fillna(0).to_dict()


def calculate_median(filtered_df):
    # Fill NaN values with 0 or another appropriate value and return the median
    return filtered_df.median(numeric_only=True).fillna(0).to_dict()


def calculate_std_dev(filtered_df):
    # Fill NaN values with 0 or another appropriate value and return the standard deviation
    return filtered_df.std(numeric_only=True).fillna(0).to_dict()

def filter_continent_data(df, start_date, end_date):
    # Filter for rows where Code is missing (continents) and within the date range
    continent_df = df[(df['Code'].isna()) & (df['Year'] >= start_date) & (df['Year'] <= end_date)]
    
    if continent_df.empty:
        return None

    # Group by continent (Entity)
    grouped_df = continent_df.groupby('Entity')

    return grouped_df
