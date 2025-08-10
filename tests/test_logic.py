#!/usr/bin/env python3
"""
Test Suite for Donizo Smart Pricing Engine
Tests all modules and their interactions
"""

import unittest
import sys
import os
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from pricing_logic.material_db import MaterialDatabase
from pricing_logic.labor_calc import LaborCalculator
from pricing_logic.vat_rules import VATRules
from pricing_logic.confidence_scorer import ConfidenceScorer
from pricing_engine import SmartPricingEngine


class TestMaterialDatabase(unittest.TestCase):
    """Test MaterialDatabase module"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.material_db = MaterialDatabase()
    
    def test_material_loading(self):
        """Test that materials are loaded correctly"""
        self.assertIn('tiles', self.material_db.materials)
        self.assertIn('plumbing', self.material_db.materials)
        self.assertIn('painting', self.material_db.materials)
    
    def test_tiles_cost_calculation(self):
        """Test tiles cost calculation"""
        cost = self.material_db.get_task_materials_cost('tiles', 4.0, 'standard')
        self.assertGreater(cost, 0)
        self.assertIsInstance(cost, float)
    
    def test_plumbing_cost_calculation(self):
        """Test plumbing cost calculation"""
        cost = self.material_db.get_task_materials_cost('plumbing', 4.0)
        self.assertGreater(cost, 0)
        self.assertIsInstance(cost, float)
    
    def test_painting_cost_calculation(self):
        """Test painting cost calculation"""
        cost = self.material_db.get_task_materials_cost('painting', 4.0, 'premium')
        self.assertGreater(cost, 0)
        self.assertIsInstance(cost, float)
    
    def test_quality_multipliers(self):
        """Test quality multiplier effects"""
        basic_cost = self.material_db.get_task_materials_cost('tiles', 4.0, 'basic')
        premium_cost = self.material_db.get_task_materials_cost('tiles', 4.0, 'premium')
        self.assertGreater(premium_cost, basic_cost)
    
    def test_size_factor_effects(self):
        """Test bathroom size factor effects"""
        small_cost = self.material_db.get_task_materials_cost('tiles', 2.0, 'standard')
        large_cost = self.material_db.get_task_materials_cost('tiles', 8.0, 'standard')
        self.assertGreater(large_cost, small_cost)


class TestLaborCalculator(unittest.TestCase):
    """Test LaborCalculator module"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.labor_calc = LaborCalculator()
    
    def test_hourly_rates(self):
        """Test hourly rates are properly set"""
        self.assertIn('tiles', self.labor_calc.hourly_rates)
        self.assertIn('plumbing', self.labor_calc.hourly_rates)
        self.assertGreater(self.labor_calc.hourly_rates['plumbing'], self.labor_calc.hourly_rates['painting'])
    
    def test_labor_cost_calculation(self):
        """Test labor cost calculation"""
        cost = self.labor_calc.calculate_labor_cost('tiles', 4.0, 'standard')
        self.assertGreater(cost, 0)
        self.assertIsInstance(cost, float)
    
    def test_task_duration_calculation(self):
        """Test task duration calculation"""
        duration = self.labor_calc.get_task_duration('tiles', 4.0, 'standard')
        self.assertGreater(duration, 0)
        self.assertIsInstance(duration, float)
    
    def test_complexity_multipliers(self):
        """Test complexity multiplier effects"""
        simple_cost = self.labor_calc.calculate_labor_cost('painting', 4.0, 'simple')
        complex_cost = self.labor_calc.calculate_labor_cost('painting', 4.0, 'complex')
        self.assertGreater(complex_cost, simple_cost)
    
    def test_project_duration_estimation(self):
        """Test project duration estimation"""
        tasks = ['tiles', 'plumbing', 'painting']
        duration_info = self.labor_calc.estimate_project_duration(tasks, 4.0)
        self.assertIn('total_days', duration_info)
        self.assertIn('working_days', duration_info)
        self.assertGreater(duration_info['total_days'], 0)


class TestVATRules(unittest.TestCase):
    """Test VATRules module"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.vat_rules = VATRules()
    
    def test_vat_rates(self):
        """Test VAT rates are properly set"""
        self.assertEqual(self.vat_rules.vat_rates['standard'], 0.20)
        self.assertEqual(self.vat_rules.vat_rates['reduced'], 0.10)
    
    def test_task_vat_classification(self):
        """Test task VAT classification"""
        self.assertEqual(self.vat_rules.task_vat_classification['tiles'], 'reduced')
        self.assertEqual(self.vat_rules.task_vat_classification['vanity'], 'standard')
    
    def test_vat_rate_retrieval(self):
        """Test VAT rate retrieval for tasks"""
        vat_rate = self.vat_rules.get_vat_rate('tiles')
        self.assertIn(vat_rate, [0.10, 0.20])  # Could be reduced or standard
    
    def test_vat_calculation(self):
        """Test VAT calculation"""
        vat_info = self.vat_rules.calculate_task_vat('tiles', 1000.0)
        self.assertIn('vat_rate', vat_info)
        self.assertIn('vat_amount', vat_info)
        self.assertGreater(vat_info['vat_amount'], 0)
    
    def test_total_vat_calculation(self):
        """Test total VAT calculation"""
        task_prices = [
            {'task_type': 'tiles', 'materials': 500, 'labor': 300},
            {'task_type': 'vanity', 'materials': 200, 'labor': 150}
        ]
        total_vat = self.vat_rules.calculate_total_vat(task_prices)
        self.assertGreater(total_vat, 0)
        self.assertIsInstance(total_vat, float)


class TestConfidenceScorer(unittest.TestCase):
    """Test ConfidenceScorer module"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.confidence_scorer = ConfidenceScorer()
    
    def test_confidence_factors(self):
        """Test confidence factors are properly set"""
        self.assertIn('bathroom_size', self.confidence_scorer.confidence_factors)
        self.assertIn('task_complexity', self.confidence_scorer.confidence_factors)
    
    def test_size_confidence_calculation(self):
        """Test bathroom size confidence calculation"""
        # Test normal size
        confidence = self.confidence_scorer._calculate_size_confidence(4.0)
        self.assertGreater(confidence, 0.8)
        
        # Test very small size
        confidence = self.confidence_scorer._calculate_size_confidence(1.0)
        self.assertLess(confidence, 0.8)
    
    def test_task_confidence_calculation(self):
        """Test task confidence calculation"""
        tasks = ['tiles', 'plumbing', 'painting']
        confidence = self.confidence_scorer._calculate_task_confidence(tasks)
        self.assertGreater(confidence, 0.8)
    
    def test_price_confidence_calculation(self):
        """Test price confidence calculation"""
        task_prices = [
            {'materials': 500, 'labor': 300},
            {'materials': 200, 'labor': 150}
        ]
        confidence = self.confidence_scorer._calculate_price_confidence(task_prices, 2000)
        self.assertGreater(confidence, 0.5)
    
    def test_flag_generation(self):
        """Test confidence flag generation"""
        requirements = {'bathroom_size': 1.0, 'tasks': ['painting']}
        task_prices = [{'materials': 100, 'labor': 50}]
        
        # This should generate flags
        self.confidence_scorer.calculate_confidence(requirements, task_prices, 300)
        flags = self.confidence_scorer.get_flags()
        self.assertGreater(len(flags), 0)


class TestSmartPricingEngine(unittest.TestCase):
    """Test SmartPricingEngine integration"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.engine = SmartPricingEngine()
    
    def test_engine_initialization(self):
        """Test engine initialization"""
        self.assertIsNotNone(self.engine.material_db)
        self.assertIsNotNone(self.engine.labor_calc)
        self.assertIsNotNone(self.engine.vat_rules)
        self.assertIsNotNone(self.engine.confidence_scorer)
    
    def test_transcript_parsing(self):
        """Test transcript parsing"""
        transcript = "4m² bathroom renovation with tiles and plumbing in Marseille"
        requirements = self.engine.parse_transcript(transcript)
        
        self.assertEqual(requirements['bathroom_size'], 4.0)
        self.assertEqual(requirements['location'], 'marseille')
        self.assertIn('tiles', requirements['tasks'])
        self.assertIn('plumbing', requirements['tasks'])
    
    def test_location_extraction(self):
        """Test location extraction from transcript"""
        transcript = "Renovate bathroom in Paris"
        requirements = self.engine.parse_transcript(transcript)
        self.assertEqual(requirements['location'], 'paris')
    
    def test_task_extraction(self):
        """Test task extraction from transcript"""
        transcript = "Install vanity and paint walls"
        requirements = self.engine.parse_transcript(transcript)
        self.assertIn('vanity', requirements['tasks'])
        self.assertIn('painting', requirements['tasks'])
    
    def test_budget_conscious_detection(self):
        """Test budget-conscious detection"""
        transcript = "Budget-friendly bathroom renovation"
        requirements = self.engine.parse_transcript(transcript)
        self.assertTrue(requirements['budget_conscious'])
    
    def test_quote_generation(self):
        """Test complete quote generation"""
        transcript = "4m² bathroom renovation with tiles and plumbing in Marseille"
        quote = self.engine.generate_quote(transcript)
        
        self.assertIn('quote_id', quote)
        self.assertIn('pricing_breakdown', quote)
        self.assertIn('business_metrics', quote)
        self.assertGreater(quote['business_metrics']['confidence_score'], 0)
    
    def test_city_multiplier_application(self):
        """Test city-based pricing adjustments"""
        marseille_transcript = "4m² bathroom renovation in Marseille"
        paris_transcript = "4m² bathroom renovation in Paris"
        
        marseille_quote = self.engine.generate_quote(marseille_transcript)
        paris_quote = self.engine.generate_quote(paris_transcript)
        
        # Paris should be more expensive
        self.assertGreater(
            paris_quote['pricing_breakdown']['final_price'],
            marseille_quote['pricing_breakdown']['final_price']
        )
    
    def test_margin_protection(self):
        """Test margin protection logic"""
        budget_transcript = "Budget 4m² bathroom renovation in Marseille"
        luxury_transcript = "Luxury 4m² bathroom renovation in Marseille"
        
        budget_quote = self.engine.generate_quote(budget_transcript)
        luxury_quote = self.engine.generate_quote(luxury_transcript)
        
        # Budget-conscious should have lower margin
        budget_margin = budget_quote['business_metrics']['margin_percentage']
        luxury_margin = luxury_quote['business_metrics']['margin_percentage']
        self.assertLess(budget_margin, luxury_margin)


class TestIntegration(unittest.TestCase):
    """Test full system integration"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.engine = SmartPricingEngine()
    
    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow"""
        # Sample transcript from requirements
        transcript = (
            "Client wants to renovate a small 4m² bathroom. They'll remove the old tiles, "
            "redo the plumbing for the shower, replace the toilet, install a vanity, "
            "repaint the walls, and lay new ceramic floor tiles. Budget-conscious. Located in Marseille."
        )
        
        # Generate quote
        quote = self.engine.generate_quote(transcript)
        
        # Verify quote structure
        self.assertIn('quote_id', quote)
        self.assertIn('client_requirements', quote)
        self.assertIn('pricing_breakdown', quote)
        self.assertIn('business_metrics', quote)
        self.assertIn('metadata', quote)
        
        # Verify pricing breakdown
        pricing = quote['pricing_breakdown']
        self.assertIn('tasks', pricing)
        self.assertIn('labor_total', pricing)
        self.assertIn('materials_total', pricing)
        self.assertIn('vat_amount', pricing)
        self.assertIn('final_price', pricing)
        
        # Verify business metrics
        metrics = quote['business_metrics']
        self.assertIn('margin_percentage', metrics)
        self.assertIn('city_multiplier', metrics)
        self.assertIn('confidence_score', metrics)
        self.assertIn('estimated_duration', metrics)
        
        # Verify confidence score is reasonable
        self.assertGreater(metrics['confidence_score'], 70)
        self.assertLess(metrics['confidence_score'], 100)
        
        # Verify final price is reasonable
        self.assertGreater(pricing['final_price'], 3000)
        self.assertLess(pricing['final_price'], 15000)
    
    def test_quote_saving(self):
        """Test quote saving functionality"""
        transcript = "4m² bathroom renovation in Marseille"
        quote = self.engine.generate_quote(transcript)
        
        # Save quote
        output_file = self.engine.save_quote(quote, "output/test_quote.json")
        
        # Verify file exists
        self.assertTrue(os.path.exists(output_file))
        
        # Verify file content
        with open(output_file, 'r') as f:
            saved_quote = json.load(f)
        
        self.assertEqual(quote['quote_id'], saved_quote['quote_id'])
        self.assertEqual(quote['pricing_breakdown']['final_price'], 
                       saved_quote['pricing_breakdown']['final_price'])
        
        # Clean up
        os.remove(output_file)


def run_tests():
    """Run all tests"""
    # Create output directory if it doesn't exist
    Path("output").mkdir(exist_ok=True)
    
    # Run tests
    unittest.main(verbosity=2)


if __name__ == "__main__":
    run_tests() 