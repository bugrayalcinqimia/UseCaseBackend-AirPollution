from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security.api_key import APIKeyHeader, APIKey
from utils import *
from fastapi.encoders import jsonable_encoder
from validations import *

API_KEY = "mysecretapikey"  # Change this to your actual API key
API_KEY_NAME = "access_token"  # This will be the key clients provide
app = FastAPI()

# Define the API key header
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Load the dataset at startup
df = load_dataset()

# Dependency to check API key
async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=403, detail="Could not validate API key"
        )
    return api_key

@app.get("/getCountriesList")
async def get_country_list(api_key: APIKey = Depends(get_api_key)):
    validate_dataset(df)

    # Get the filtered country list
    country_list = filter_countries_with_codes(df)

    # Validate the country list is not empty
    validate_country_list(country_list)

    # Convert the DataFrame to a list of dictionaries
    country_code_list = country_list.to_dict(orient="records")

    return {
        "countries": country_code_list
    }


@app.get("/getCountryInfo")
async def get_country_info(code: str,api_key: APIKey = Depends(get_api_key)):
    # Validate dataset
    validate_dataset(df)

    # Validate and convert country code to uppercase
    code = validate_country_code(code)

    # Fetch country info
    country_info = fetch_country_info(df, code)

    # Handle not found case
    if country_info is None:
        handle_not_found(df, code)

    return country_info


@app.get("/getCountryAverages")
async def get_country_averages(code: str, start_date: int = None, end_date: int = None,api_key: APIKey = Depends(get_api_key)):
    # Ensure the dataset is loaded
    validate_dataset(df)

    # Validate country code format (3-letter alphabetic code)
    code = validate_country_code(code)

    # Ensure valid date range if start_date and end_date are provided
    start_date, end_date = validate_date_range(start_date, end_date, df)

    # If no date range is provided, use the full date range
    if start_date is None or end_date is None:
        filtered_df, actual_start_date, actual_end_date = filter_data_by_date(
            df, code, df['Year'].min(), df['Year'].max())
    else:
        filtered_df, actual_start_date, actual_end_date = filter_data_by_date(
            df, code, start_date, end_date)

    # Check if the country code exists and data is found
    if filtered_df is None or filtered_df.empty:
        handle_not_found(df, code)

    # Calculate averages
    averages = calculate_averages(filtered_df)

    # Return the response with the country code, date range, and averages
    return jsonable_encoder({
        "country": code,
        "start_year": int(actual_start_date),
        "end_year": int(actual_end_date),
        "averages": averages
    })


@app.get("/getCountryMedians")
async def get_country_medians(code: str, start_date: int = None, end_date: int = None,api_key: APIKey = Depends(get_api_key)):
    # Ensure the dataset is loaded
    validate_dataset(df)

    # Validate country code format (3-letter alphabetic code)
    code = validate_country_code(code)

    # Ensure valid date range if start_date and end_date are provided
    start_date, end_date = validate_date_range(start_date, end_date, df)

    # If no date range is provided, use the full date range
    if start_date is None or end_date is None:
        filtered_df, actual_start_date, actual_end_date = filter_data_by_date(
            df, code, df['Year'].min(), df['Year'].max())
    else:
        filtered_df, actual_start_date, actual_end_date = filter_data_by_date(
            df, code, start_date, end_date)

    # Check if the country code exists and data is found
    if filtered_df is None or filtered_df.empty:
        handle_not_found(df, code)

    # Calculate medians
    median = calculate_median(filtered_df)

    return jsonable_encoder({
        "country": code,
        "start_year": int(actual_start_date),
        "end_year": int(actual_end_date),
        "median": median
    })


@app.get("/getCountryStandardDeviations")
async def get_country_std_dev(code: str, start_date: int = None, end_date: int = None,api_key: APIKey = Depends(get_api_key)):
    # Ensure the dataset is loaded
    validate_dataset(df)

    # Validate country code format (3-letter alphabetic code)
    code = validate_country_code(code)

    # Ensure valid date range if start_date and end_date are provided
    start_date, end_date = validate_date_range(start_date, end_date, df)

    # If no date range is provided, use the full date range
    if start_date is None or end_date is None:
        filtered_df, actual_start_date, actual_end_date = filter_data_by_date(
            df, code, df['Year'].min(), df['Year'].max())
    else:
        filtered_df, actual_start_date, actual_end_date = filter_data_by_date(
            df, code, start_date, end_date)

    # Check if the country code exists and data is found
    if filtered_df is None or filtered_df.empty:
        handle_not_found(df, code)

    # Calculate standard deviation
    std_dev = calculate_std_dev(filtered_df)

    return jsonable_encoder({
        "country": code,
        "start_year": int(actual_start_date),
        "end_year": int(actual_end_date),
        "standard_deviation": std_dev
    })


@app.get("/getCountryStatistics")
async def get_countries_all_statistics(code: str, start_date: int = None, end_date: int = None,api_key: APIKey = Depends(get_api_key)):
    # Ensure the dataset is loaded
    validate_dataset(df)

    # Validate country code format (3-letter alphabetic code)
    code = validate_country_code(code)

    # Ensure valid date range if start_date and end_date are provided
    start_date, end_date = validate_date_range(start_date, end_date, df)

    # If no date range is provided, use the full date range
    if start_date is None or end_date is None:
        filtered_df, actual_start_date, actual_end_date = filter_data_by_date(
            df, code, df['Year'].min(), df['Year'].max())
    else:
        filtered_df, actual_start_date, actual_end_date = filter_data_by_date(
            df, code, start_date, end_date)

    # Check if the country code exists and data is found
    if filtered_df is None or filtered_df.empty:
        handle_not_found(df, code)

    # Calculate all statistics
    averages = calculate_averages(filtered_df)
    median = calculate_median(filtered_df)
    std_dev = calculate_std_dev(filtered_df)

    # Return a combined response
    return jsonable_encoder({
        "country": code,
        "start_year": int(actual_start_date),  # Convert to Python int
        "end_year": int(actual_end_date),      # Convert to Python int
        "statistics": {
            "averages": averages,
            "median": median,
            "standard_deviation": std_dev
        }
    })


@app.get("/getAllContinenetStatistics")
async def get_all_continent_statistics(start_date: int = None, end_date: int = None,api_key: APIKey = Depends(get_api_key)):
    # Ensure the dataset is loaded
    validate_dataset(df)

    # Ensure valid date range if both start_date and end_date are provided
    start_date, end_date = validate_date_range(start_date, end_date, df)

    # Use the full date range if not provided
    if start_date is None or end_date is None:
        start_date = df['Year'].min()
        end_date = df['Year'].max()

    # Filter the data for continents within the provided date range
    grouped_df = filter_continent_data(df, start_date, end_date)

    validate_grouped_data(grouped_df, entity="continents")

    # Initialize an empty list to store statistics for each continent
    continent_statistics = []

    # Iterate over each continent group and calculate statistics
    for continent, data in grouped_df:
        averages = calculate_averages(data)
        median = calculate_median(data)
        std_dev = calculate_std_dev(data)

        # Add the continent's statistics to the list
        continent_statistics.append({
            "continent": continent,
            "start_year": int(data['Year'].min()),
            "end_year": int(data['Year'].max()),
            "statistics": {
                "averages": averages,
                "median": median,
                "standard_deviation": std_dev
            }
        })

    # Return the list of continent statistics
    return jsonable_encoder(continent_statistics)
