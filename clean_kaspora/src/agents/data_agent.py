"""
Data Agent - Handles all data querying and filtering operations
"""
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional


class DataAgent:
    def __init__(self, csv_path: str):
        """Initialize the data agent with CSV data"""
        self.df = pd.read_csv(csv_path)
        self.df['date'] = pd.to_datetime(self.df['date'])
        
    def get_date_range_data(self, days: int = 7, end_date: Optional[str] = None) -> pd.DataFrame:
        """Get data for the last N days"""
        if end_date:
            end = pd.to_datetime(end_date)
        else:
            end = self.df['date'].max()
        
        start = end - timedelta(days=days)
        return self.df[(self.df['date'] >= start) & (self.df['date'] <= end)]
    
    def filter_by_dimensions(self, 
                            campaign: Optional[str] = None,
                            creative_type: Optional[str] = None,
                            platform: Optional[str] = None,
                            country: Optional[str] = None,
                            audience_type: Optional[str] = None) -> pd.DataFrame:
        """Filter data by various dimensions"""
        filtered = self.df.copy()
        
        if campaign:
            filtered = filtered[filtered['campaign_name'].str.contains(campaign, case=False, na=False)]
        if creative_type:
            filtered = filtered[filtered['creative_type'] == creative_type]
        if platform:
            filtered = filtered[filtered['platform'] == platform]
        if country:
            filtered = filtered[filtered['country'] == country]
        if audience_type:
            filtered = filtered[filtered['audience_type'] == audience_type]
            
        return filtered
    
    def get_aggregated_metrics(self, df: pd.DataFrame, group_by: List[str]) -> pd.DataFrame:
        """Aggregate metrics by specified dimensions"""
        agg_dict = {
            'spend': 'sum',
            'impressions': 'sum',
            'clicks': 'sum',
            'purchases': 'sum',
            'revenue': 'sum'
        }
        
        result = df.groupby(group_by, dropna=False).agg(agg_dict).reset_index()
        
        # Calculate derived metrics
        result['ctr'] = (result['clicks'] / result['impressions'] * 100).round(4)
        result['roas'] = (result['revenue'] / result['spend']).round(2)
        result['cpc'] = (result['spend'] / result['clicks']).round(2)
        result['cpa'] = (result['spend'] / result['purchases']).round(2)
        
        # Handle infinities and NaN
        result = result.replace([float('inf'), float('-inf')], 0)
        result = result.fillna(0)
        
        return result
    
    def get_campaign_level_analysis(self) -> Dict[str, Any]:
        """Campaign-level performance analysis"""
        campaign_agg = self.get_aggregated_metrics(self.df, ['campaign_name'])
        return {
            'campaign_performance': campaign_agg.to_dict('records'),
            'top_campaigns': campaign_agg.nlargest(5, 'roas').to_dict('records'),
            'bottom_campaigns': campaign_agg.nsmallest(5, 'roas').to_dict('records')
        }
    
    def get_adset_level_analysis(self) -> Dict[str, Any]:
        """Adset-level performance analysis"""
        adset_agg = self.get_aggregated_metrics(self.df, ['campaign_name', 'adset_name'])
        return {
            'adset_performance': adset_agg.to_dict('records'),
            'top_adsets': adset_agg.nlargest(10, 'roas').to_dict('records'),
            'bottom_adsets': adset_agg.nsmallest(10, 'roas').to_dict('records')
        }
    
    def get_audience_level_analysis(self) -> Dict[str, Any]:
        """Audience-level performance analysis"""
        audience_agg = self.get_aggregated_metrics(self.df, ['audience_type'])
        return {
            'audience_performance': audience_agg.to_dict('records'),
            'audience_comparison': audience_agg.to_dict('records')
        }
    
    def get_creative_level_analysis(self) -> Dict[str, Any]:
        """Creative-level detailed analysis"""
        # Creative type analysis
        creative_type_agg = self.get_aggregated_metrics(self.df, ['creative_type'])
        
        # Creative message analysis (top performing messages)
        message_agg = self.get_aggregated_metrics(self.df, ['creative_message'])
        top_messages = message_agg.nlargest(10, 'roas')
        
        return {
            'creative_type_performance': creative_type_agg.to_dict('records'),
            'top_creative_messages': top_messages.to_dict('records'),
            'creative_message_signals': message_agg.to_dict('records')
        }
    
    def get_geo_level_analysis(self) -> Dict[str, Any]:
        """Geographic-level performance analysis"""
        country_agg = self.get_aggregated_metrics(self.df, ['country'])
        return {
            'country_performance': country_agg.to_dict('records'),
            'geo_roas_patterns': country_agg.to_dict('records')
        }
    
    def get_rolling_trends(self, window: int = 7) -> Dict[str, Any]:
        """Get rolling trends analysis"""
        df_sorted = self.df.sort_values('date')
        
        # 7-day rolling ROAS
        daily_metrics = df_sorted.groupby('date').agg({
            'spend': 'sum',
            'revenue': 'sum',
            'clicks': 'sum',
            'impressions': 'sum',
            'purchases': 'sum'
        }).reset_index()
        
        # Handle division by zero
        daily_metrics['roas'] = daily_metrics.apply(lambda x: x['revenue'] / x['spend'] if x['spend'] > 0 else 0, axis=1)
        daily_metrics['ctr'] = daily_metrics.apply(lambda x: (x['clicks'] / x['impressions'] * 100) if x['impressions'] > 0 else 0, axis=1)
        
        # Rolling averages (only if we have enough data)
        if len(daily_metrics) >= window:
            daily_metrics['roas_7d_rolling'] = daily_metrics['roas'].rolling(window=window).mean()
            daily_metrics['ctr_7d_rolling'] = daily_metrics['ctr'].rolling(window=window).mean()
            
            # Trend direction (safe indexing)
            roas_trend = 'stable'
            ctr_trend = 'stable'
            
            if len(daily_metrics) > window and not daily_metrics['roas_7d_rolling'].isnull().all():
                recent_roas = daily_metrics['roas_7d_rolling'].iloc[-1]
                older_roas = daily_metrics['roas_7d_rolling'].iloc[-min(window, len(daily_metrics))]
                if pd.notna(recent_roas) and pd.notna(older_roas):
                    roas_trend = 'increasing' if recent_roas > older_roas else 'decreasing'
                    
            if len(daily_metrics) > window and not daily_metrics['ctr_7d_rolling'].isnull().all():
                recent_ctr = daily_metrics['ctr_7d_rolling'].iloc[-1]
                older_ctr = daily_metrics['ctr_7d_rolling'].iloc[-min(window, len(daily_metrics))]
                if pd.notna(recent_ctr) and pd.notna(older_ctr):
                    ctr_trend = 'increasing' if recent_ctr > older_ctr else 'decreasing'
        else:
            roas_trend = 'insufficient_data'
            ctr_trend = 'insufficient_data'
        
        return {
            'daily_trends': daily_metrics.to_dict('records'),
            'roas_trend_direction': roas_trend,
            'ctr_trend_direction': ctr_trend
        }
    
    def get_top_performers(self, metric: str = 'roas', n: int = 10, 
                          group_by: str = 'creative_type') -> pd.DataFrame:
        """Get top performing segments"""
        aggregated = self.get_aggregated_metrics(self.df, [group_by])
        return aggregated.nlargest(n, metric)
    
    def get_bottom_performers(self, metric: str = 'roas', n: int = 10,
                             group_by: str = 'creative_type') -> pd.DataFrame:
        """Get worst performing segments"""
        aggregated = self.get_aggregated_metrics(self.df, [group_by])
        # Filter out zero values for fair comparison
        aggregated = aggregated[aggregated[metric] > 0]
        return aggregated.nsmallest(n, metric)
    
    def compare_periods(self, current_days: int = 7, previous_days: int = 7) -> Dict[str, Any]:
        """Compare current period vs previous period"""
        end_date = self.df['date'].max()
        
        # Current period
        current_start = end_date - timedelta(days=current_days)
        current_df = self.df[self.df['date'] > current_start]
        
        # Previous period
        previous_end = current_start
        previous_start = previous_end - timedelta(days=previous_days)
        previous_df = self.df[(self.df['date'] > previous_start) & (self.df['date'] <= previous_end)]
        
        def get_metrics(df):
            return {
                'spend': df['spend'].sum(),
                'revenue': df['revenue'].sum(),
                'roas': df['revenue'].sum() / df['spend'].sum() if df['spend'].sum() > 0 else 0,
                'impressions': df['impressions'].sum(),
                'clicks': df['clicks'].sum(),
                'purchases': df['purchases'].sum(),
                'ctr': (df['clicks'].sum() / df['impressions'].sum() * 100) if df['impressions'].sum() > 0 else 0
            }
        
        current_metrics = get_metrics(current_df)
        previous_metrics = get_metrics(previous_df)
        
        # Calculate changes
        changes = {}
        for key in current_metrics:
            if previous_metrics[key] > 0:
                pct_change = ((current_metrics[key] - previous_metrics[key]) / previous_metrics[key] * 100)
                changes[f'{key}_change_pct'] = round(pct_change, 2)
            else:
                changes[f'{key}_change_pct'] = 0
        
        return {
            'current_period': current_metrics,
            'previous_period': previous_metrics,
            'changes': changes
        }
    
    def get_data_summary(self) -> Dict[str, Any]:
        """Get overall data summary"""
        return {
            'total_rows': len(self.df),
            'date_range': {
                'start': self.df['date'].min().strftime('%Y-%m-%d'),
                'end': self.df['date'].max().strftime('%Y-%m-%d')
            },
            'campaigns': self.df['campaign_name'].nunique(),
            'total_spend': round(self.df['spend'].sum(), 2),
            'total_revenue': round(self.df['revenue'].sum(), 2),
            'overall_roas': round(self.df['revenue'].sum() / self.df['spend'].sum(), 2),
            'missing_values': self.df.isnull().sum().to_dict()
        }


def execute_query(csv_path: str, instructions: str) -> Dict[str, Any]:
    """
    Execute a data query based on natural language instructions
    This is a simplified version - in production, you'd use LLM to parse instructions
    """
    agent = DataAgent(csv_path)
    
    # For now, return basic summary and recent data
    # This would be enhanced with LLM-based query parsing
    summary = agent.get_data_summary()
    recent_data = agent.get_date_range_data(days=7)
    top_creatives = agent.get_top_performers(metric='roas', group_by='creative_type')
    comparison = agent.compare_periods()
    
    return {
        'query_executed': instructions,
        'data_summary': summary,
        'recent_performance': recent_data.to_dict('records')[:20],  # Limit for readability
        'top_performers': top_creatives.to_dict('records'),
        'period_comparison': comparison
    }
