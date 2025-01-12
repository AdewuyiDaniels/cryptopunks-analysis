# CryptoPunks Analysis Platform

### Streamlit Dashboard Example  
*Replace with a direct link to an image of your dashboard*

This repository contains the code for a **CryptoPunks analytics platform** that fetches transaction data, cleans and analyzes it, and presents insights through an interactive Streamlit dashboard. The platform provides key metrics, visualizations, and filtering options to help users understand the CryptoPunks market.

---

## Project Overview
The project focuses on analyzing CryptoPunks transaction data to provide insights into market trends, holder behavior, and trading activity. Key features include:

- **Data Acquisition**: Fetching transaction data from Etherscan using their API.
- **Data Cleaning and Processing**: Preparing the data by cleaning and transforming it into a usable format.
- **Data Analysis**: Performing exploratory data analysis (EDA) and calculating key metrics.
- **Interactive Dashboard**: Displaying the analyzed data using a dynamic Streamlit web app.

---

## Project Structure
```plaintext
cryptopunks-analysis/
├── data/                  # Data storage
│   ├── processed/         # Cleaned and processed data
│   │   └── cryptopunks_transfers_cleaned.csv  # Processed transaction data
│   └── raw/               # Raw data fetched from Etherscan
│       └── cryptopunks_transfers.json         # Raw transaction data
│
├── scripts/               # Python scripts for data fetching and processing
│   ├── analyze_cryptopunks_data.py  # Script for data analysis
│   ├── clean_cryptopunks_data.py    # Script for cleaning and preprocessing data
│   └── fetch_cryptopunks_data.py    # Script to fetch raw data from Etherscan
│
├── app.py                 # Main Streamlit dashboard application
├── .env                   # Environment variables (API keys)
├── .gitignore             # Specifies files to ignore in Git
├── README.md              # Project documentation (this file)
└── requirements.txt       # Python dependencies for the project
```

---

## Setup and Installation

### Prerequisites
- Python 3.7 or higher.
- Pip package manager (should come with Python).
- A free **Etherscan API Key**. Obtain an API key by creating an account on [Etherscan](https://etherscan.io/).

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd cryptopunks-analysis
   ```
   Replace `https://github.com/your-username/your-repo-name.git` with the link to your repo.

2. **Create a `.env` file**:
   In the root directory, create a file named `.env` and add your Etherscan API Key in this format:
   ```plaintext
   ETHERSCAN_API_KEY=YOUR_ACTUAL_API_KEY
   ```
   Replace `YOUR_ACTUAL_API_KEY` with the API key you obtained from Etherscan.  
   **Important**: Do not commit the `.env` file to your repository, as it contains sensitive information.

3. **Install project dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Data Fetching
Run the `fetch_cryptopunks_data.py` script to fetch raw data from Etherscan. This will save the data as a JSON file inside `/data/raw/`:
```bash
python scripts/fetch_cryptopunks_data.py
```

### Data Cleaning
Run the `clean_cryptopunks_data.py` script to clean and process the raw data. This will save the cleaned data as a CSV file in `/data/processed/`:
```bash
python scripts/clean_cryptopunks_data.py
```

### Running the Dashboard
Start the Streamlit app to launch the interactive dashboard:
```bash
streamlit run app.py
```
This will open the dashboard in your default web browser.

---

## Dashboard Functionality

### Filters
- **Time Period**: Choose from preset time periods (e.g., Last 7 Days, Last 30 Days) or set a custom range *(default: January 1, 2017, to January 1, 2025)*.
- **Transaction Size**: Filter transactions by size (e.g., Small, Medium, Large, Whale).

### Key Metrics
- **Total Volume**: Total transaction volume in ETH.
- **Active Holders**: Number of unique addresses involved in transactions.
- **Avg Transaction**: Average transaction size in ETH.
- **Daily Transactions**: Average number of transactions per day.

### Visualizations
- **Holder Concentration**: A pie chart showing the distribution of holdings among the top addresses.
- **Transaction Size Distribution**: A bar chart showing the distribution of transaction sizes.
- **Price Analysis**: A line chart showing the price trend and 7-day moving average.
- **Trading Activity**: Bar charts showing daily trading volume and transaction count.




![image](https://github.com/user-attachments/assets/ea77e37a-bcb9-404f-9177-5f1a445f7694)
![image](https://github.com/user-attachments/assets/0cf3260b-497c-4029-abb0-dba4c7090af3)
![image](https://github.com/user-attachments/assets/eb647105-2868-4316-8d6f-ce9ad65ea36a)

---

## Testing
The project includes unit tests to verify the functionality of data fetching and cleaning. To run the tests, navigate to the `/tests` folder and execute:
```bash
python -m pytest
```

---

## Contributing
Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contact
For questions or feedback, feel free to reach out:

**Name**: Daniel  
**Email**: adewuyiaby@gmail.com
