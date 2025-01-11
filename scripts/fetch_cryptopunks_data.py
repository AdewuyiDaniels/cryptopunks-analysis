# scripts/fetch_cryptopunks_data.py
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def fetch_cryptopunks_transfers():
    """
    Fetches CryptoPunks transfer data from the Etherscan API and saves it to a JSON file.
    """
    # CryptoPunks contract address
    CONTRACT_ADDRESS = "0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB"

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
        if data["status"] == "1":
            print("Data fetched successfully!")  # Debugging statement

            # Save raw data to JSON file
            raw_data_path = os.path.join("..", "data", "raw", "cryptopunks_transfers.json")
            os.makedirs(os.path.dirname(raw_data_path), exist_ok=True)  # Create the directory if it doesn't exist

            with open(raw_data_path, "w") as f:
                json.dump(data, f, indent=4)  # Save data with pretty-printing

            print(f"Data saved to {raw_data_path}")  # Debugging statement
        else:
            print(f"Error fetching data: {data['message']}")  # Debugging statement

        return data

    except requests.exceptions.RequestException as e:
        print(f"HTTP request failed: {e}")  # Debugging statement
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response: {e}")  # Debugging statement
    except Exception as e:
        print(f"An unexpected error occurred: {e}")  # Debugging statement

# Run the function
if __name__ == "__main__":
    fetch_cryptopunks_transfers()