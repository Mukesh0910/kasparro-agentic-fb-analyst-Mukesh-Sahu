"""
Data Loader Utility
Handles loading and basic preprocessing of CSV data
"""
import pandas as pd
from pathlib import Path
from typing import Optional


def load_facebook_ads_data(csv_path: str) -> pd.DataFrame:
    """
    Load Facebook ads CSV data
    
    Args:
        csv_path: Path to the CSV file
        
    Returns:
        DataFrame with parsed dates and cleaned data
    """
    df = pd.read_csv(csv_path)
    
    # Parse dates
    df['date'] = pd.to_datetime(df['date'])
    
    # Sort by date
    df = df.sort_values('date')
    
    return df


def get_data_summary(df: pd.DataFrame) -> dict:
    """
    Get summary statistics of the dataset
    
    Args:
        df: Facebook ads DataFrame
        
    Returns:
        Dictionary with summary statistics
    """
    return {
        'total_rows': len(df),
        'date_range': {
            'start': df['date'].min().strftime('%Y-%m-%d'),
            'end': df['date'].max().strftime('%Y-%m-%d'),
            'days': (df['date'].max() - df['date'].min()).days
        },
        'campaigns': df['campaign_name'].nunique(),
        'adsets': df['adset_name'].nunique(),
        'creative_types': df['creative_type'].unique().tolist(),
        'platforms': df['platform'].unique().tolist(),
        'countries': df['country'].unique().tolist(),
        'total_spend': float(df['spend'].sum()),
        'total_revenue': float(df['revenue'].sum()),
        'overall_roas': float(df['revenue'].sum() / df['spend'].sum()) if df['spend'].sum() > 0 else 0,
        'missing_values': df.isnull().sum().to_dict()
    }
