"""
Tests for Evaluator Agent
"""
import pytest
from src.agents.evaluator_agent import EvaluatorAgent


class TestEvaluatorAgent:
    """Test cases for the Evaluator Agent"""
    
    @pytest.fixture
    def config(self):
        """Test configuration"""
        return {
            'model': 'gemini-1.5-flash',
            'confidence_min': 0.6,
            'temperature': 0.3
        }
    
    @pytest.fixture
    def evaluator(self, config):
        """Create evaluator instance"""
        return EvaluatorAgent(config)
    
    def test_evaluator_rejects_low_confidence_insights(self, evaluator):
        """Test that evaluator rejects insights with weak evidence"""
        insight = {
            'title': 'ROAS increased',
            'description': 'ROAS went up',
            'severity': 'high',
            'confidence': 0.3,
            'evidence': {
                'metric': 'roas',
                'sample_size': 5  # Very small sample
            }
        }
        
        data = {'summary': {'total_rows': 100}}
        
        evaluation = evaluator.evaluate_insight(insight, data)
        
        assert evaluation['overall_score'] < 0.6, "Should reject low confidence insights"
        assert not evaluation['passed'], "Should not pass with weak evidence"
    
    def test_evaluator_accepts_strong_insights(self, evaluator):
        """Test that evaluator accepts insights with strong evidence"""
        insight = {
            'title': 'Video ads outperform Images by 200%',
            'description': 'Video ads achieved 8.5 ROAS vs Image ads 2.8 ROAS across 150 data points',
            'severity': 'high',
            'confidence': 0.9,
            'evidence': {
                'metric': 'roas',
                'comparison': 'Video: 8.5 vs Image: 2.8',
                'sample_size': 150,
                'statistical_significance': True
            },
            'recommendation': 'Shift 60% of budget to video format'
        }
        
        data = {
            'summary': {'total_rows': 500},
            'top_performers': [
                {'creative_type': 'Video', 'roas': 8.5},
                {'creative_type': 'Image', 'roas': 2.8}
            ]
        }
        
        evaluation = evaluator.evaluate_insight(insight, data)
        
        assert evaluation['overall_score'] >= 0.6, "Should accept strong insights"
        assert evaluation['passed'], "Should pass with strong evidence"
    
    def test_evaluator_checks_evidence_quality(self, evaluator):
        """Test that evaluator properly scores evidence quality"""
        insight = {
            'title': 'CTR improved',
            'description': 'Click-through rate increased',
            'severity': 'medium',
            'confidence': 0.7,
            'evidence': {}  # Empty evidence
        }
        
        data = {'summary': {}}
        
        evaluation = evaluator.evaluate_insight(insight, data)
        
        # Should have low evidence quality score
        assert 'scores' in evaluation
        assert 'evidence_quality' in evaluation['scores']
        # Empty evidence should result in low score
        assert evaluation['scores']['evidence_quality'] < 0.5


def test_evaluator_module_imports():
    """Test that evaluator module can be imported"""
    from src.agents import evaluator_agent
    assert hasattr(evaluator_agent, 'EvaluatorAgent')
    assert hasattr(evaluator_agent, 'evaluate_insights')
