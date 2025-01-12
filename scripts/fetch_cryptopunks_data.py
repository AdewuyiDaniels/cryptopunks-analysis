# scripts/fetch_cryptopunks_data.py
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Constants
CONTRACT_ADDRESS = "0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB"  # CryptoPunks contract address
RAW_DATA_DIR = r"C:\Users\USER PC\Desktop\DATA PROJECTS\cryptopunks-analysis\data\raw"  # Absolute path to the raw data directory

def ensure_directory_exists(directory):
    """
    Ensures the specified directory exists. If not, creates it.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    else:
        print(f"Directory already exists: {directory}")

def fetch_etherscan_data():
    """
    Fetches CryptoPunks transfer data from the Etherscan API.
    """
    # Get the API key from the environment variable
    API_KEY = os.getenv("ETHERSCAN_API_KEY")
    if not API_KEY:
        raise ValueError("Etherscan API key not found in .env file. Please add ETHERSCAN_API_KEY=YourApiKeyToken to .env.")

    # Etherscan API endpoint for token transfers
    url = f"https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={CONTRACT_ADDRESS}&startblock=0&endblock=99999999&sort=asc&apikey={API_KEY}"

    print("Fetching data from Etherscan API...")  # Debugging statement

    try:
        # Make the API request
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        # Check if the API request was successful
        if data.get("status") == "1" and data.get("result"):
            print(f"Etherscan data fetched successfully! Number of transactions: {len(data['result'])}")
            return data["result"]
        else:
            error_message = data.get("message", "Unknown error")
            print(f"Error fetching Etherscan data: {error_message}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"HTTP request failed: {e}")
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def fetch_coingecko_data():
    """
    Fetches ETH price data from the CoinGecko API.
    """
    # Get the API key from the environment variable
    API_KEY = os.getenv("COINGECKO_API_KEY")
    if not API_KEY:
        raise ValueError("CoinGecko API key not found in .env file. Please add COINGECKO_API_KEY=YourApiKeyToken to .env.")

    # CoinGecko API endpoint for ETH price
    url = f"https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true&apikey={API_KEY}"

    print("Fetching data from CoinGecko API...")  # Debugging statement

    try:
        # Make the API request
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        if data.get("ethereum"):
            print("CoinGecko data fetched successfully!")
            return data["ethereum"]
        else:
            print(f"Error fetching CoinGecko data: {data.get('error', 'Unknown error')}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"HTTP request failed: {e}")
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def save_data(data, filename):
    """
    Saves data to a JSON file in the raw data directory.
    Overwrites the file if it already exists.
    """
    try:
        # Ensure the raw data directory exists
        ensure_directory_exists(RAW_DATA_DIR)

        # Construct the full file path
        file_path = os.path.join(RAW_DATA_DIR, filename)
        print(f"Saving data to: {file_path}")  # Debugging statement

        # Save the data to a JSON file (overwrite if exists)
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)  # Save data with pretty-printing

        print(f"Data saved successfully to {file_path}")  # Debugging statement

    except Exception as e:
        print(f"Error saving data to {filename}: {e}")

def fetch_cryptopunks_transfers():
    """
    Fetches CryptoPunks transfer data from Etherscan and ETH price data from CoinGecko.
    Overwrites existing data in the raw data directory.
    """
    print("Starting data fetch process...")  # Debugging statement

    # Fetch data from Etherscan
    etherscan_data = fetch_etherscan_data()
    if etherscan_data:
        save_data(etherscan_data, "cryptopunks_transfers.json")
    else:
        print("No Etherscan data fetched. Skipping save.")

    # Fetch data from CoinGecko
    coingecko_data = fetch_coingecko_data()
    if coingecko_data:
        save_data(coingecko_data, "eth_price_data.json")
    else:
        print("No CoinGecko data fetched. Skipping save.")

    print("Data fetch process completed.")  # Debugging statement

# Run the function
if __name__ == "__main__":
    fetch_cryptopunks_transfers()