# CryptoPunks Analysis Platform

![Streamlit Dashboard Example](link_to_your_dashboard_screenshot)  
*Replace with a direct link to an image of your dashboard*

This repository contains the code for a comprehensive CryptoPunks analytics platform. The project fetches transaction data, performs cleaning and analysis, and presents insights using an interactive Streamlit dashboard. This documentation provides a detailed overview of the project's architecture, setup instructions, and usage guidelines.

## Project Overview

This project aims to provide detailed insights into the CryptoPunks NFT collection using on-chain transaction data. By collecting, cleaning, and analyzing this data, we provide users with tools to monitor key metrics, identify trends, and understand the dynamics of the CryptoPunks market. The main features of this project include:

*   **Data Acquisition**: Fetching transaction data from Etherscan using their API.
*   **Data Cleaning and Processing**: Preparing the data by cleaning and transforming it into a usable format.
*   **Data Analysis**: Performing exploratory data analysis (EDA) and calculating key metrics.
*   **Interactive Dashboard**: Displaying the analyzed data using a dynamic Streamlit web app.

## Project Structure

The project is organized into the following directories:

cryptopunks-analysis/
├── dashboard/ # Streamlit dashboard application
│ ├── assets/ # Static assets (e.g., logos, images)
│ ├── app.py # Main Streamlit application logic
│ └── requirements.txt # Python dependencies for the dashboard
│
├── data/ # Data storage
│ ├── processed/ # Cleaned and processed data
│ │ └── cryptopunks_transfers_cleaned.csv # Processed transaction data
│ └── raw/ # Raw data fetched from Etherscan
│ └── cryptopunks_transfers.json # Raw transaction data from Etherscan
│
├── docs/ # Documentation files
│
├── notebooks/ # Jupyter notebooks for analysis and exploration
│
├── scripts/ # Python scripts for data fetching and processing
│ ├── analyze_cryptopunks_data.py # Script for data analysis
│ ├── clean_cryptopunks_data.py # Script for cleaning and preprocessing data
│ ├── fetch_cryptopunks_data.py # Script to fetch raw data from Etherscan
│ └── utils.py # Utility functions shared across scripts
│
├── tests/ # Unit tests
│ └── test_fetch_cryptopunks_data.py # Unit tests for data fetching scripts
│
├── .env # Environment variables (API keys)
├── README.md # Project documentation (this file)
└── requirements.txt # Python dependencies for the scripts



## Setup and Installation

### Prerequisites

*   Python 3.7 or higher.
*   Pip package manager (should come with Python)
*   A free Etherscan API Key. Obtain an API key by creating an account on [Etherscan](https://etherscan.io/)

### Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd cryptopunks-analysis
    ```
   Replace `https://github.com/your-username/your-repo-name.git` with the link to your repo.
2.  **Create a `.env` file:** In the root directory, create a file named `.env`. Add your Etherscan API Key in this format:
    ```
    ETHERSCAN_API_KEY=YOUR_ACTUAL_API_KEY
    ```
    Replace `YOUR_ACTUAL_API_KEY` with the API key you obtained from Etherscan.  **Important:** Do not commit the `.env` file to your repository, as it contains sensitive information.
3.  **Install project dependencies (for scripts and analysis):**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Install dashboard dependencies:**
    ```bash
    cd dashboard
    pip install -r requirements.txt
    cd .. # go back to the root project folder
    ```

## Usage

### Data Fetching

1.  Run the `fetch_cryptopunks_data.py` script to get raw data from Etherscan. This will save the data as a JSON file inside `/data/raw/`
    ```bash
    python scripts/fetch_cryptopunks_data.py
    ```

### Data Cleaning

1.  Execute the `clean_cryptopunks_data.py` script. This will clean and process the raw data and save as a csv file in `/data/processed/`
    ```bash
    python scripts/clean_cryptopunks_data.py
    ```

### Running the Analysis and Dashboard

1.  **Start the Streamlit app:**
    ```bash
    cd dashboard
    streamlit run app.py
    ```
    This will launch the Streamlit app in your default web browser.
2.  **Interact with the dashboard:** The dashboard allows users to dynamically filter data by different time periods, transaction size, and metrics.

## Dashboard Functionality

The Streamlit dashboard provides an interactive way to explore CryptoPunks transaction data. Here's how it works:

*   **Time Period Selector:**
    *   Users can choose from various preset time periods to view metrics for specific timeframes.
*   **Transaction Size Filter:**
    *   Filters the data based on transaction size to focus on particular categories (e.g. small, medium, large transactions).
*   **Metric Selector:**
    *   Users can choose which metrics to show in the summary boxes (e.g., Price, Volume, etc.)
*   **Summary Boxes**: These display aggregated metrics such as:
    *   **Total Volume**: Total volume of transactions over the selected time period
    *   **Active Holders**: Number of unique addresses that have participated in a trade during the period.
    *   **Avg Transaction**: Average transaction amount during the selected period.
    *   **Daily Transactions**: Total number of transactions per day during the selected period.
*   **Charts:** The dashboard also features charts, including:
    *   **Holder Concentration**: A pie chart showing the distribution of CryptoPunk holdings among the top addresses.
    *   **Transaction Size Distribution**: A bar chart of the transaction sizes to give a high level overview
    *   **Trading Activity:** A line and bar chart for transaction activity, displaying daily trading volume and transaction count over time.

## Testing
The project contains a suite of unit tests to verify the functionality of data fetching. To run these tests navigate to the `/tests` folder and run