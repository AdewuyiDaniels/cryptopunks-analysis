# scripts/clean_cryptopunks_data.py
import os
import json
import pandas as pd

# Constants
RAW_DATA_DIR = r"C:\Users\USER PC\Desktop\DATA PROJECTS\cryptopunks-analysis\data\raw"  # Path to raw data
PROCESSED_DATA_DIR = r"C:\Users\USER PC\Desktop\DATA PROJECTS\cryptopunks-analysis\data\processed"  # Path to processed data

def ensure_directory_exists(directory):
    """
    Ensures the specified directory exists. If not, creates it.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    else:
        print(f"Directory already exists: {directory}")

def load_json_data(filename):
    """
    Loads JSON data from a file in the raw data directory.
    """
    raw_data_path = os.path.join(RAW_DATA_DIR, filename)
    print(f"Loading raw data from: {raw_data_path}")  # Debugging statement

    try:
        with open(raw_data_path, "r") as f:
            data = json.load(f)
        print(f"Raw data loaded successfully from {filename}!")  # Debugging statement
        return data
    except FileNotFoundError:
        print(f"Error: The file {raw_data_path} does not exist.")
    except json.JSONDecodeError:
        print(f"Error: The file {raw_data_path} contains invalid JSON data.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def clean_etherscan_data(etherscan_data):
    """
    Cleans and preprocesses raw CryptoPunks transfer data from Etherscan.
    """
    print("Cleaning Etherscan data...")  # Debugging statement
    df = pd.DataFrame(etherscan_data)

    # Convert columns to appropriate data types
    df["value"] = df["value"].astype(float) / 1e18  # Convert value from wei to ETH
    df["timeStamp"] = pd.to_datetime(df["timeStamp"], unit="s")  # Convert timestamp to datetime

    # Rename columns for clarity
    df.rename(columns={"from": "sender", "to": "receiver"}, inplace=True)

    print("Etherscan data cleaned successfully!")  # Debugging statement
    return df

def clean_coingecko_data(coingecko_data):
    """
    Cleans and preprocesses ETH price data from CoinGecko.
    """
    print("Cleaning CoinGecko data...")  # Debugging statement
    df = pd.DataFrame([coingecko_data])
    df["last_updated"] = pd.to_datetime(df["last_updated_at"], unit="s")  # Convert timestamp to datetime

    print("CoinGecko data cleaned successfully!")  # Debugging statement
    return df

def merge_data(etherscan_df, coingecko_df):
    """
    Merges Etherscan and CoinGecko data.
    """
    print("Merging data...")  # Debugging statement
    etherscan_df["date"] = etherscan_df["timeStamp"].dt.date
    coingecko_df["date"] = coingecko_df["last_updated"].dt.date

    merged_df = pd.merge(etherscan_df, coingecko_df, on="date", how="left")
    merged_df["value_usd"] = merged_df["value"] * merged_df["usd"]

    print("Data merged successfully!")  # Debugging statement
    return merged_df

def save_cleaned_data(df, filename):
    """
    Saves cleaned data to a CSV file in the processed data directory.
    """
    try:
        # Ensure the processed data directory exists
        ensure_directory_exists(PROCESSED_DATA_DIR)

        # Construct the full file path
        processed_data_path = os.path.join(PROCESSED_DATA_DIR, filename)
        print(f"Saving processed data to: {processed_data_path}")  # Debugging statement

        # Save the data to a CSV file
        df.to_csv(processed_data_path, index=False)
        print(f"Cleaned data saved to {processed_data_path}")  # Debugging statement

    except Exception as e:
        print(f"Error saving data to {filename}: {e}")

def clean_cryptopunks_transfers():
    """
    Cleans and preprocesses raw CryptoPunks transfer data.
    """
    print("Starting clean_cryptopunks_transfers script...")  # Debugging statement

    # Load raw data
    etherscan_data = load_json_data("cryptopunks_transfers.json")
    coingecko_data = load_json_data("eth_price_data.json")

    if etherscan_data and coingecko_data:
        # Clean and preprocess data
        etherscan_df = clean_etherscan_data(etherscan_data)
        coingecko_df = clean_coingecko_data(coingecko_data)

        # Merge data
        merged_df = merge_data(etherscan_df, coingecko_df)

        # Save cleaned data
        save_cleaned_data(merged_df, "cryptopunks_transfers_cleaned.csv")
    else:
        print("Skipping data cleaning due to missing raw data.")

    print("Script execution completed.")  # Debugging statement

# Run the function
if __name__ == "__main__":
    clean_cryptopunks_transfers()