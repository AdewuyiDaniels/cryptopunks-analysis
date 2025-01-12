# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import sys
from datetime import datetime, timedelta
import numpy as np

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
from scripts.analyze_cryptopunks_data import analyze_cryptopunks_transfers

# Streamlit Config
st.set_page_config(
    layout="wide",
    page_title="CryptoPunks Analytics",
    page_icon="🎨"
)

# Modern Light Theme CSS
st.markdown("""
<style>
    .main {
        background-color: #FFFFFF;
    }
    .stApp {
        background-color: #FFFFFF;
    }
    .css-1d391kg {
        background-color: #FFFFFF;
    }
    .metric-card {
        background-color: #FFFFFF;
        border: 1px solid #EAEAEA;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .filter-container {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .section-header {
        color: #333333;
        font-size: 24px;
        font-weight: 600;
        margin: 20px 0;
    }
    .sidebar .sidebar-content {
        background-color: #F8F9FA;
    }
    @media (max-width: 768px) {
        .metric-card {
            padding: 10px;
        }
        .section-header {
            font-size: 20px;
        }
    }
</style>
""", unsafe_allow_html=True)

def load_data():
    """
    Loads processed CryptoPunks transfer data.
    """
    try:
        df = pd.read_csv(os.path.join(project_root, "data", "processed", "cryptopunks_transfers_cleaned.csv"))
        df['timeStamp'] = pd.to_datetime(df['timeStamp'])
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def filter_data(df, date_filter, size_filter, start_date=None, end_date=None):
    """Filter data based on user selections"""
    filtered_df = df.copy()
    
    # Date filtering
    if date_filter == "Last 7 Days":
        filtered_df = filtered_df[filtered_df['timeStamp'] >= (df['timeStamp'].max() - pd.Timedelta(days=7))]
    elif date_filter == "Last 30 Days":
        filtered_df = filtered_df[filtered_df['timeStamp'] >= (df['timeStamp'].max() - pd.Timedelta(days=30))]
    elif date_filter == "Last 90 Days":
        filtered_df = filtered_df[filtered_df['timeStamp'] >= (df['timeStamp'].max() - pd.Timedelta(days=90))]
    elif date_filter == "Year to Date":
        filtered_df = filtered_df[filtered_df['timeStamp'].dt.year == datetime.now().year]
    elif date_filter == "Custom Range" and start_date and end_date:
        filtered_df = filtered_df[(filtered_df['timeStamp'].dt.date >= start_date) & 
                                (filtered_df['timeStamp'].dt.date <= end_date)]
    
    # Size filtering
    size_conditions = {
        "Small (<10 ETH)": filtered_df['value'] < 10,
        "Medium (10-50 ETH)": (filtered_df['value'] >= 10) & (filtered_df['value'] < 50),
        "Large (50-100 ETH)": (filtered_df['value'] >= 50) & (filtered_df['value'] < 100),
        "Whale (>100 ETH)": filtered_df['value'] >= 100
    }
    
    if size_filter:
        mask = pd.Series(False, index=filtered_df.index)
        for size in size_filter:
            mask = mask | size_conditions[size]
        filtered_df = filtered_df[mask]
    
    return filtered_df

def create_holder_concentration_chart(df):
    """Create holder concentration donut chart"""
    holder_stats = df.groupby('receiver')['value'].sum().sort_values(ascending=False)
    
    top_10_holders = holder_stats.head(10)
    others = pd.Series({'Others': holder_stats[10:].sum()})
    final_data = pd.concat([top_10_holders, others])
    
    fig = go.Figure(data=[go.Pie(
        labels=final_data.index,
        values=final_data.values,
        hole=.6,
        textinfo='label+percent',
        marker=dict(colors=px.colors.qualitative.Set3)
    )])
    
    fig.update_layout(
        title="Holder Concentration",
        annotations=[dict(text='Top<br>Holders', x=0.5, y=0.5, font_size=20, showarrow=False)],
        showlegend=False,
        height=400,
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    
    return fig

def create_transaction_distribution(df):
    """Create transaction size distribution chart"""
    df['size_category'] = pd.cut(
        df['value'],
        bins=[0, 10, 50, 100, float('inf')],
        labels=['Small (<10 ETH)', 'Medium (10-50 ETH)', 'Large (50-100 ETH)', 'Whale (>100 ETH)']
    )
    
    size_dist = df['size_category'].value_counts()
    
    fig = go.Figure(data=[go.Bar(
        x=size_dist.index,
        y=size_dist.values,
        marker_color=px.colors.qualitative.Set3,
        text=size_dist.values,
        textposition='auto',
    )])
    
    fig.update_layout(
        title="Transaction Size Distribution",
        xaxis_title="Transaction Size Category",
        yaxis_title="Number of Transactions",
        height=400,
        paper_bgcolor='white',
        plot_bgcolor='white',
        showlegend=False
    )
    
    return fig

def create_price_analysis_chart(df):
    """Create price analysis chart"""
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(
            x=df['timeStamp'],
            y=df['value'],
            name='Price',
            line=dict(color='#1E88E5', width=1),
            fill='tonexty',
            fillcolor='rgba(30,136,229,0.1)'
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=df['timeStamp'],
            y=df['value'].rolling(7).mean(),
            name='7-day MA',
            line=dict(color='#FFA000', width=2)
        )
    )
    
    fig.update_layout(
        template='plotly',
        height=500,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='white',
        plot_bgcolor='white',
        yaxis_title='Price (ETH)',
        xaxis_title='Date',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_volume_analysis_chart(df):
    """Create volume analysis chart"""
    daily_volume = df.resample('D', on='timeStamp')['value'].agg(['sum', 'count']).reset_index()
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Daily Trading Volume', 'Transaction Count'),
        specs=[[{"type": "bar"}, {"type": "bar"}]]
    )
    
    fig.add_trace(
        go.Bar(
            x=daily_volume['timeStamp'],
            y=daily_volume['sum'],
            name='Volume',
            marker_color='#1E88E5'
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(
            x=daily_volume['timeStamp'],
            y=daily_volume['count'],
            name='Transactions',
            marker_color='#FFA000'
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        template='plotly',
        height=400,
        showlegend=True,
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def main():
    st.title("CryptoPunks Analytics Platform")
    st.markdown("""
        Welcome to the **CryptoPunks Analytics Platform**! This dashboard provides insights into CryptoPunks transactions, 
        including holder concentration, transaction size distribution, price analysis, and trading activity.
    """)

    # Load data
    df = load_data()
    if df is None:
        return

    # Sidebar for filters
    with st.sidebar:
        st.header("Filters")
        date_filter = st.selectbox(
            "Time Period",
            ["Last 7 Days", "Last 30 Days", "Last 90 Days", "Year to Date", "Custom Range"]
        )
        
        size_filter = st.multiselect(
            "Transaction Size",
            ["Small (<10 ETH)", "Medium (10-50 ETH)", "Large (50-100 ETH)", "Whale (>100 ETH)"],
            default=["Small (<10 ETH)", "Medium (10-50 ETH)"]
        )
        
        if date_filter == "Custom Range":
            # Set default date range from 01/01/2017 to 01/01/2025
            start_date = st.date_input("Start Date", value=datetime(2017, 1, 1))
            end_date = st.date_input("End Date", value=datetime(2025, 1, 1))
        else:
            start_date = None
            end_date = None

    # Filter the data
    filtered_df = filter_data(df, date_filter, size_filter, start_date, end_date)

    # Key Metrics Dashboard
    st.markdown('<div class="section-header">Key Metrics</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            "Total Volume",
            f"Ξ {filtered_df['value'].sum():,.2f}",
            f"+{(filtered_df['value'].tail(7).sum() / filtered_df['value'].head(7).sum() - 1):.1%}"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            "Active Holders",
            f"{filtered_df['receiver'].nunique():,}",
            f"+{(filtered_df['receiver'].tail(7).nunique() / filtered_df['receiver'].head(7).nunique() - 1):.1%}"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            "Avg Transaction",
            f"Ξ {filtered_df['value'].mean():,.2f}",
            f"{(filtered_df['value'].tail(7).mean() / filtered_df['value'].head(7).mean() - 1):.1%}"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            "Daily Transactions",
            f"{filtered_df.groupby(filtered_df['timeStamp'].dt.date)['value'].count().mean():.0f}",
            f"{(filtered_df.tail(7)['value'].count() / filtered_df.head(7)['value'].count() - 1):.1%}"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # Holder and Transaction Distribution Charts
    st.markdown('<div class="section-header">Holder and Transaction Distribution</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_holder_concentration_chart(filtered_df), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_transaction_distribution(filtered_df), use_container_width=True)

    # Price Analysis
    st.markdown('<div class="section-header">Price Analysis</div>', unsafe_allow_html=True)
    st.plotly_chart(create_price_analysis_chart(filtered_df), use_container_width=True)

    # Volume Analysis
    st.markdown('<div class="section-header">Trading Activity</div>', unsafe_allow_html=True)
    st.plotly_chart(create_volume_analysis_chart(filtered_df), use_container_width=True)

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #666;">
            <p>Developed by Daniel</p>
            <p>Contact: <a href="mailto:adewuyiaby@gmail.com">adewuyiaby@gmail.com</a></p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()