"""
Tests for All Agents
"""
import pytest
from src.agents.planner_agent import PlannerAgent
from src.agents.data_agent import DataAgent
from src.utils.data_loader import load_facebook_ads_data


class TestDataAgent:
    """Test cases for Data Agent"""
    
    @pytest.fixture
    def data_agent(self):
        """Create data agent instance"""
        return DataAgent('data/synthetic_fb_ads_undergarments.csv')
    
    def test_data_agent_loads_data(self, data_agent):
        """Test that data agent loads CSV successfully"""
        summary = data_agent.get_data_summary()
        
        assert summary['total_rows'] > 0
        assert 'date_range' in summary
        assert summary['overall_roas'] > 0
    
    def test_data_agent_filters_by_date(self, data_agent):
        """Test date range filtering"""
        recent_data = data_agent.get_date_range_data(days=7)
        
        assert len(recent_data) > 0
        assert len(recent_data) < data_agent.df.shape[0]
    
    def test_data_agent_compares_periods(self, data_agent):
        """Test period comparison"""
        comparison = data_agent.compare_periods(current_days=7, previous_days=7)
        
        assert 'current_period' in comparison
        assert 'previous_period' in comparison
        assert 'changes' in comparison
        assert 'roas' in comparison['current_period']


class TestPlannerAgent:
    """Test cases for Planner Agent"""
    
    @pytest.fixture
    def config(self):
        """Test configuration"""
        return {
            'model': 'gemini-1.5-flash',
            'temperature': 0.7
        }
    
    def test_planner_creates_plan(self, config):
        """Test that planner creates a structured plan"""
        planner = PlannerAgent(config)
        plan = planner.create_plan("Analyze ROAS trends")
        
        assert 'objective' in plan
        assert 'steps' in plan
        assert len(plan['steps']) > 0
        assert 'user_query' in plan


def test_data_loader():
    """Test data loader utility"""
    df = load_facebook_ads_data('data/synthetic_fb_ads_undergarments.csv')
    
    assert len(df) > 0
    assert 'date' in df.columns
    assert 'roas' in df.columns
    assert df['date'].dtype == 'datetime64[ns]'
