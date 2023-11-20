# SQLAlchemy Climate Analysis - Readme

## Overview

This project involves a climate analysis in Honolulu, Hawaii, using Python, SQLAlchemy, and various data analysis tools. The analysis is split into two main parts: Exploratory Data Analysis (EDA) and the development of a Flask API based on the EDA results.

## Part 1: Exploratory Data Analysis

### Setup

Ensure you have the necessary dependencies installed:

```bash
pip install matplotlib numpy pandas sqlalchemy
```

### Code References

Before starting the analysis, use the provided code to set up the environment, connect to the database, and reflect tables into SQLAlchemy ORM. The code for this can be found in the file `code_references.py`.

### Precipitation Analysis

1. Find the most recent date in the dataset.
2. Retrieve the last 12 months of precipitation data and plot the results.
3. Print summary statistics for the precipitation data.

### Station Analysis

1. Calculate the total number of stations in the dataset.
2. Find the most active stations, listing them with observation counts in descending order.
3. Calculate the lowest, highest, and average temperature for the most active station.
4. Query the last 12 months of temperature observation data for the most active station and plot the results as a histogram.

### Close Session

Ensure to close the session to maintain a clean environment.

## Part 2: Design Your Climate App

Design a Flask API based on the queries developed in the EDA.

### Routes

1. **Homepage** (`/`): Welcome page with links to available routes.
2. **Precipitation** (`/api/v1.0/precipitation`): Precipitation data for the last 12 months.
3. **Stations** (`/api/v1.0/stations`): List of stations from the dataset.
4. **Temperature Observations** (`/api/v1.0/tobs`): Temperature observations for the previous year.
5. **Temperature Stats for Start Date** (`/api/v1.0/<start_date>`): Temperature statistics for a specified start date.
6. **Temperature Stats for Start-End Date Range** (`/api/v1.0/<start_date>/<end_date>`): Temperature statistics for a specified start-end date range.

### Usage

1. Clone the repository.
2. Run the code in `code_references.py` to set up the environment and reflect tables.
3. Use the Jupyter notebook `climate_starter.ipynb` for the climate analysis.
4. Execute the Flask app by running `app.py`.
5. Access the API routes as needed.
