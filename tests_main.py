import pandas as pd
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app  

client = TestClient(app)
API_KEY = "mysecretapikey"

# Sample mock dataset as a pandas DataFrame
mock_df = pd.DataFrame({
        'Entity': ['Afghanistan', 'United States'],
    'Code': ['AFG', 'USA'],
    'Year': [1750, 1760],
    'Nitrogen oxide (NOx)': [555.4786, 578.50757],
    'Sulphur dioxide (SO₂) emissions': [174.87167, 181.99332],
    'Carbon monoxide (CO) emissions': [142073.31, 147859.23],
    'Organic carbon (OC) emissions': [5456.885, 5679.1167],
    'Non-methane volatile organic compounds (NMVOC) emissions': [13596.633, 14150.87],
    'Black carbon (BC) emissions': [1633.0308, 1699.5359],
    'Ammonia (NH₃) emissions': [7681.0464, 8000.8574]
})


@patch("main.df", mock_df) 
def test_get_countries_list():
    response = client.get("/getCountriesList",headers={"access_token": API_KEY})
    assert response.status_code == 200
    json_response = response.json()

    assert "countries" in json_response
    assert len(json_response["countries"]) == 2  

    assert json_response["countries"] == [
        { 'Country': 'Afghanistan','Code': 'AFG'},
        {'Country': 'United States','Code': 'USA' }
    ]

@patch("main.df", pd.DataFrame())  # Empty DataFrame
def test_get_countries_list_empty_dataset():
    response = client.get("/getCountriesList",headers={"access_token": API_KEY})
    assert response.status_code == 500
    json_response = response.json()

    assert json_response == {"detail": "Dataset is not loaded or empty."}

@patch("main.df", mock_df)
def test_get_country_info_valid():
    response = client.get("/getCountryInfo?code=AFG",headers={"access_token": API_KEY})
    assert response.status_code == 200
    json_response = response.json()

    expected_country_info = {
    "country_name": "Afghanistan",
    "years_interval": "1750 - 1750"
}

    assert json_response == expected_country_info

@patch("main.df", mock_df)
def test_get_country_info_invalid_code():
    response = client.get("/getCountryInfo?code=XYZ",headers={"access_token": API_KEY})
    assert response.status_code == 404
    json_response = response.json()

    assert "detail" in json_response
    assert "Country code not found" in json_response["detail"]