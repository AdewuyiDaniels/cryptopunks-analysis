# CryptoPunks Analytics Dashboard

![CryptoPunks Logo](https://www.larvalabs.com/cryptopunks/cryptopunk.png)

## Overview

This project provides an advanced analytics dashboard for **CryptoPunks**, one of the most iconic NFT collections on the Ethereum blockchain. The dashboard offers insights into **Holder Analysis**, **Liquidity Analysis**, **Market Impact Analysis**, and **Anomaly Detection** using interactive visualizations powered by **Streamlit** and **Plotly**.

---

## Features

### 1. **Holder Analysis**
- **Holder Distribution**: Categorizes holders into Small, Medium, Large, and Whales based on their holdings.
- **Holdings Over Time**: Tracks how holdings change over time for different holder categories.

### 2. **Liquidity Analysis**
- **Daily Trading Volume**: Visualizes the daily trading volume of CryptoPunks.
- **Liquidity Score**: Combines trading volume and frequency to measure market liquidity.

### 3. **Market Impact Analysis**
- **Whale Transactions**: Identifies and visualizes large transactions (top 10% by value).
- **Price Impact**: Tracks the impact of whale transactions on market prices.

### 4. **Anomaly Detection**
- **Unusual Transactions**: Detects and highlights unusual transactions using Z-scores.

---

## Technologies Used

- **Python**: Primary programming language.
- **Pandas**: Data manipulation and analysis.
- **Plotly**: Interactive visualizations.
- **Streamlit**: Web app framework for building the dashboard.
- **Scipy**: Statistical analysis (e.g., Z-scores for anomaly detection).
- **NetworkX**: Network analysis (optional for future features).

---

## Installation

### Prerequisites
- Python 3.8 or higher.
- Pip (Python package manager).

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/cryptopunks-analysis.git
   cd cryptopunks-analysis
Install the required dependencies:

      pip install -r requirements.txt
Place your dataset (cryptopunks_transfers_cleaned.csv) in the data/processed/ folder.

Run the Streamlit app:

         streamlit run app.py

Open your browser and navigate to the provided URL (e.g., http://localhost:8501).

Project Structure

               cryptopunks-analysis/
               ├── data/
               │   └── processed/
               │       └── cryptopunks_transfers_cleaned.csv  # Dataset
               ├── scripts/
               │   └── analyze_cryptopunks_data.py  # Analysis logic
               ├── app.py  # Streamlit dashboard
               ├── requirements.txt  # Dependencies
               └── README.md  # Project documentation



Dataset
The dataset (cryptopunks_transfers_cleaned.csv) should contain the following columns:

   blockNumber: Block number of the transaction.
   
   timeStamp: Timestamp of the transaction.
   
   from: Sender address.
   
   to: Receiver address.
   
   value: Transaction value in ETH.
   
   tokenName: Name of the token (e.g., "CRYPTOPUNKS").
   
   tokenSymbol: Symbol of the token (e.g., "Ͼ").
   
   tokenDecimal: Decimal precision of the token.

Usage
1. Holder Analysis:

   View the distribution of holders (Small, Medium, Large, Whales).
   
   Track how holdings change over time.

2. Liquidity Analysis:

   Analyze daily trading volume and liquidity scores.
   
   Market Impact Analysis:
   
   Identify whale transactions and their impact on prices.

3. Anomaly Detection:

   Detect unusual transactions using statistical methods.

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.

2. Create a new branch for your feature or bugfix.

3. Commit your changes.

4. Submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
Streamlit: For making it easy to build interactive dashboards.

Plotly: For creating beautiful and interactive visualizations.
