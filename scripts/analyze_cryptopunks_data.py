# scripts/analyze_cryptopunks_data.py
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def analyze_holders(df):
    """
    Analyzes holder statistics and categorizes holders.
    """
    holder_stats = df.groupby('receiver')['value'].sum().reset_index()
    holder_stats = holder_stats.dropna(subset=['value'])
    holder_stats = holder_stats[holder_stats['value'] > 0]

    # Categorize holders
    unique_values = holder_stats['value'].nunique()
    if unique_values >= 4:
        try:
            holder_stats['holder_type'] = pd.qcut(
                holder_stats['value'],
                q=4,
                labels=['Small', 'Medium', 'Large', 'Whale'],
                duplicates='drop'
            )
        except ValueError:
            value_range = holder_stats['value'].max() - holder_stats['value'].min()
            bins = [
                holder_stats['value'].min() - 1,
                holder_stats['value'].min() + value_range * 0.25,
                holder_stats['value'].min() + value_range * 0.5,
                holder_stats['value'].min() + value_range * 0.75,
                holder_stats['value'].max() + 1
            ]
            holder_stats['holder_type'] = pd.cut(
                holder_stats['value'],
                bins=bins,
                labels=['Small', 'Medium', 'Large', 'Whale'],
                include_lowest=True
            )
    else:
        median_value = holder_stats['value'].median()
        holder_stats['holder_type'] = np.where(
            holder_stats['value'] <= median_value,
            'Small',
            'Large'
        )

    return holder_stats

def analyze_liquidity(df):
    """
    Analyzes daily trading metrics and calculates liquidity score.
    """
    daily_volume = df.groupby('date')['value'].agg([
        ('value', 'sum'),
        ('transaction_count', 'count')
    ]).reset_index()

    liquidity = daily_volume.copy()
    liquidity['liquidity_score'] = (
        liquidity['value'] * 
        liquidity['transaction_count'] / 
        liquidity[['value', 'transaction_count']].mean().product()
    )

    return liquidity

def analyze_market_impact(df):
    """
    Analyzes whale transactions and calculates price impact.
    """
    whale_threshold = df['value'].quantile(0.9)
    whale_trades = df[df['value'] >= whale_threshold].copy()

    daily_avg_price = df.groupby('date')['value'].mean()
    whale_daily_avg = whale_trades.groupby('date')['value'].mean()

    price_impact = pd.DataFrame({
        'timeStamp': daily_avg_price.index,
        'value': whale_daily_avg / daily_avg_price
    }).fillna(1.0)  # Fill days without whale trades with 1.0 (no impact)

    return whale_trades, price_impact

def detect_anomalies(df):
    """
    Detects anomalies in transaction values using rolling statistics.
    """
    df_sorted = df.sort_values('timeStamp')
    rolling_mean = df_sorted['value'].rolling(window=50, min_periods=1).mean()
    rolling_std = df_sorted['value'].rolling(window=50, min_periods=1).std()

    z_scores = np.abs((df_sorted['value'] - rolling_mean) / rolling_std)
    anomalies = df_sorted[z_scores > 3].copy()

    return anomalies

def analyze_cryptopunks_transfers(df):
    """
    Performs advanced analysis of CryptoPunks transfer data.
    """
    try:
        # Ensure timeStamp is datetime
        df['timeStamp'] = pd.to_datetime(df['timeStamp'])
        df['date'] = df['timeStamp'].dt.date

        # Perform analyses
        holder_stats = analyze_holders(df)
        liquidity = analyze_liquidity(df)
        whale_trades, price_impact = analyze_market_impact(df)
        anomalies = detect_anomalies(df)

        # Return results
        results = {
            'holder_stats': holder_stats,
            'liquidity': liquidity,
            'whale_trades': whale_trades,
            'price_impact': price_impact,
            'anomalies': anomalies
        }

        return results

    except Exception as e:
        print(f"Error in analysis: {str(e)}")
        raise