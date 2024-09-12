# Air Pollution Statistics API

## Overview

This FastAPI-based API provides various endpoints to retrieve air pollution-related statistics for countries and continents. The statistics include averages, medians, and standard deviations over specified time ranges.

To access the endpoints, an API key (`access_token`) is required for authentication.
## Getting Started

### Prerequisites
- Python 3.8 or later
- FastAPI
- Uvicorn
- Required libraries (see `requirements.txt` for full list)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/bugrayalcinqimia/air-pollution-api.git

2. Navigate to the project directory:
   ```bash
   cd air-pollution-api
   
3. Navigate to the project directory:
   ```bash
   pip install -r requirements.txt

4. Run the FastAPI application with Uvicorn:
   ```bash
   uvicorn main:app --reload
  
5. The API will be available at http://127.0.0.1:8000

## API Key Authentication

To access any endpoint, you must provide the API key via the `access_token` header.

- **API Key**: `mysecretapikey`
- **Header Format**:
access_token: mysecretapikey

# API Documentation

## Example Usage with `curl`

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/getCountriesList' \
  -H 'access_token: mysecretapikey'
```

## Swagger Documentation

You can access the interactive API documentation (provided by **Swagger UI**) by navigating to:

- **[Swagger UI](http://127.0.0.1:8000/docs)**

This interface allows you to explore and interact with the API endpoints directly from the browser.

## Available Endpoints

The API includes the following endpoints, which provide statistical data on air pollution for different countries and continents:

1. **GET** `/getCountriesList`
2. **GET** `/getCountryInfo`
3. **GET** `/getCountryAverages`
4. **GET** `/getCountryMedians`
5. **GET** `/getCountryStandardDeviations`
6. **GET** `/getCountryStatistics`
7. **GET** `/getAllContinentStatistics`

For full details of each endpoint, including parameters, request/response formats, and example outputs, refer to the **Swagger UI** link provided above.
- **CI/CD Pipeline**: The pipeline is set up to trigger on pull requests or pushes to the `dev` branch. It runs tests and builds a Docker image only if tests pass.
- **Automated Tests**: `pytest` is used for automated tests in the CI pipeline.
- **Docker Containerization**: Docker is used to containerize the application, and the image is pushed to Docker Hub if all tests pass.

  **Do not forget to add you own Docker name and pasword token to github in order to run the CI/CD pipeline successfully.**
