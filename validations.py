import difflib
from fastapi import HTTPException

def validate_dataset(df):
    """Ensure the dataset is loaded and not empty."""
    if df is None or df.empty:
        raise HTTPException(
            status_code=500, detail="Dataset is not loaded or empty.")

def validate_country_list(country_list):
    """Validate that the filtered country list is not empty."""
    if country_list.empty:
        raise HTTPException(
            status_code=404, detail="No countries found in the dataset.")

def validate_country_code(code: str):
    """Validate that the country code is in the correct format."""
    if not code.isalpha() or len(code) != 3:
        raise HTTPException(
            status_code=400, detail="Invalid country code format. It should be a 3-letter alphabetic code.")
    return code.upper()

def validate_date_range(start_date: int, end_date: int, df):
    """Ensure the date range is valid and falls within the dataset's year range."""
    if start_date is not None and end_date is not None:
        if start_date > end_date:
            raise HTTPException(
                status_code=400, detail="Invalid date range: start_date cannot be greater than end_date.")
        
        # Get the minimum and maximum years from the dataset
        min_year = df['Year'].min()
        max_year = df['Year'].max()

        # Check if the provided dates are within the range of the dataset's years
        if end_date < min_year or start_date > max_year or start_date < min_year or end_date > max_year :
            raise HTTPException(
                status_code=400, 
                detail=f"Date range out of bounds. Please provide dates between {min_year} and {max_year}.")
    
    return start_date, end_date

def handle_not_found(df, code, start_date=None, end_date=None, entity="country"):
    """Handle cases where no data is found for the given country or continent."""
    valid_codes = df['Code'].dropna().unique()
    suggested_codes = difflib.get_close_matches(code, valid_codes, n=3, cutoff=0.6)

    if suggested_codes:
        raise HTTPException(
            status_code=404,
            detail=f"{entity.capitalize()} code not found. Did you mean: {', '.join(suggested_codes)}?"
        )
    else:
        raise HTTPException(
            status_code=404,
            detail=f"{entity.capitalize()} code not found and no similar codes were found."
        )
    
def validate_grouped_data(grouped_df, entity="continents"):
    """Validate that the grouped data is not None or empty, raise 404 if no data is found."""
    if grouped_df is None or len(grouped_df) == 0:
        raise HTTPException(
            status_code=404, detail=f"No data found for the given date range or {entity} not found.")
