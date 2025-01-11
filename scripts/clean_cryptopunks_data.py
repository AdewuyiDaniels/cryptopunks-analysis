# scripts/clean_cryptopunks_data.py
import os
import json
import pandas as pd

def clean_cryptopunks_transfers():
    """
    Cleans and preprocesses raw CryptoPunks transfer data from a JSON file and saves it to a CSV file.
    """
    # Path to the raw data file
    raw_data_path = os.path.join("..", "data", "raw", "cryptopunks_transfers.json")
    print(f"Loading raw data from: {raw_data_path}")  # Debugging statement

    try:
        # Load raw data from JSON file
        print("Attempting to load JSON data...")  # Debugging statement
        with open(raw_data_path, "r") as f:
            data = json.load(f)

        print("Raw data loaded successfully!")  # Debugging statement

        # Convert raw data to a DataFrame
        print("Converting JSON data to DataFrame...")  # Debugging statement
        df = pd.DataFrame(data["result"])
        print(f"DataFrame created with {len(df)} rows")  # Debugging statement

        # Convert columns to appropriate data types
        print("Converting data types...")  # Debugging statement
        df["value"] = df["value"].astype(float) / 1e18  # Convert value from wei to ETH
        df["timeStamp"] = pd.to_datetime(df["timeStamp"], unit="s")  # Convert timestamp to datetime

        # Save processed data to CSV
        processed_data_path = os.path.join("..", "data", "processed", "cryptopunks_transfers_cleaned.csv")
        print(f"Saving processed data to: {processed_data_path}")  # Debugging statement
        os.makedirs(os.path.dirname(processed_data_path), exist_ok=True)  # Create the directory if it doesn't exist

        df.to_csv(processed_data_path, index=False)
        print(f"Data saved to {processed_data_path}")  # Debugging statement

        return df

    except FileNotFoundError:
        print(f"Error: The file {raw_data_path} does not exist. Please run the fetch_cryptopunks_data.py script first.")
    except json.JSONDecodeError:
        print(f"Error: The file {raw_data_path} contains invalid JSON data.")
    except KeyError as e:
        print(f"Error: The key '{e}' is missing in the JSON data.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run the function
if __name__ == "__main__":
    print("Starting clean_cryptopunks_transfers script...")  # Debugging statement
    clean_cryptopunks_transfers()
    print("Script execution completed.")  # Debugging statement