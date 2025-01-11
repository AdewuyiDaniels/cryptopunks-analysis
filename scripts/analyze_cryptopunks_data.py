import pandas as pd
import numpy as np
from scipy import stats

def analyze_cryptopunks_transfers(df):
    """
    Advanced analysis of CryptoPunks transfer data.
    Includes Holder Analysis, Liquidity Analysis, Market Impact Analysis, and Anomaly Detection.
    
    Args:
        df (pd.DataFrame): DataFrame containing CryptoPunks transfer data
        
    Returns:
        dict: Dictionary containing various analysis results
    """
    try:
        # Ensure timeStamp is datetime
        df['timeStamp'] = pd.to_datetime(df['timeStamp'])
        df['date'] = df['timeStamp'].dt.date
        
        # --- Holder Analysis ---
        holder_stats = df.groupby('to')['value'].sum().reset_index()
        holder_stats = holder_stats.dropna(subset=['value'])
        holder_stats = holder_stats[holder_stats['value'] > 0]
        
        # Categorize holders based on value
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
                # Fallback to regular cut if qcut fails
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
            # Simple binary categorization for few unique values
            median_value = holder_stats['value'].median()
            holder_stats['holder_type'] = np.where(
                holder_stats['value'] <= median_value,
                'Small',
                'Large'
            )
        
        # Track holdings over time
        holdings_over_time = df.groupby(['date', 'to']).size().unstack(fill_value=0)
        
        # --- Liquidity Analysis ---
        # Calculate daily trading metrics
        daily_volume = df.groupby('date')['value'].agg([
            ('value', 'sum'),
            ('transaction_count', 'count')
        ]).reset_index()
        
        # Calculate liquidity score
        liquidity = daily_volume.copy()
        liquidity['liquidity_score'] = (
            liquidity['value'] * 
            liquidity['transaction_count'] / 
            liquidity[['value', 'transaction_count']].mean().product()
        )
        
        # --- Market Impact Analysis ---
        # Identify whale transactions
        whale_threshold = df['value'].quantile(0.9)
        whale_trades = df[df['value'] >= whale_threshold].copy()
        
        # Calculate price impact
        daily_avg_price = df.groupby('date')['value'].mean()
        whale_daily_avg = whale_trades.groupby('date')['value'].mean()
        
        price_impact = pd.DataFrame({
            'timeStamp': daily_avg_price.index,
            'value': whale_daily_avg / daily_avg_price
        }).fillna(1.0)  # Fill days without whale trades with 1.0 (no impact)
        
        # --- Anomaly Detection ---
        # Calculate rolling statistics for more robust anomaly detection
        df_sorted = df.sort_values('timeStamp')
        rolling_mean = df_sorted['value'].rolling(window=50, min_periods=1).mean()
        rolling_std = df_sorted['value'].rolling(window=50, min_periods=1).std()
        
        # Z-score based anomaly detection
        z_scores = np.abs((df_sorted['value'] - rolling_mean) / rolling_std)
        anomalies = df_sorted[z_scores > 3].copy()  # Transactions more than 3 standard deviations from mean
        
        # --- Return Results ---
        results = {
            'holder_stats': holder_stats,
            'holdings_over_time': holdings_over_time,
            'daily_volume': daily_volume,
            'liquidity': liquidity,
            'whale_trades': whale_trades,
            'price_impact': price_impact,
            'anomalies': anomalies
        }
        
        return results
        
    except Exception as e:
        print(f"Error in analysis: {str(e)}")
        raise