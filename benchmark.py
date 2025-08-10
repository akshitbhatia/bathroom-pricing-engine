#!/usr/bin/env python3
"""
Performance Benchmark for Donizo Smart Bathroom Pricing Engine
Tests various scenarios and measures performance metrics
"""

import time
import json
from pathlib import Path
from typing import Dict, List, Any
from pricing_engine import SmartPricingEngine


class PricingEngineBenchmark:
    def __init__(self):
        """Initialize benchmark suite"""
        self.engine = SmartPricingEngine()
        self.results = []
        
        # Test scenarios
        self.test_scenarios = [
            {
                'name': 'Small Budget Bathroom',
                'transcript': '2m² basic bathroom renovation with painting and vanity in Nantes',
                'expected_tasks': ['painting', 'vanity'],
                'expected_size': 2.0,
                'expected_location': 'nantes'
            },
            {
                'name': 'Standard Renovation',
                'transcript': '4m² bathroom renovation with tiles, plumbing, and painting in Marseille',
                'expected_tasks': ['tiles', 'plumbing', 'painting'],
                'expected_size': 4.0,
                'expected_location': 'marseille'
            },
            {
                'name': 'Luxury Bathroom',
                'transcript': '8m² luxury bathroom with premium tiles, smart plumbing, and electrical work in Paris',
                'expected_tasks': ['tiles', 'plumbing', 'electrical'],
                'expected_size': 8.0,
                'expected_location': 'paris'
            },
            {
                'name': 'Complex Project',
                'transcript': '6m² bathroom renovation with tiles, plumbing, painting, flooring, vanity, and electrical in Lyon',
                'expected_tasks': ['tiles', 'plumbing', 'painting', 'flooring', 'vanity', 'electrical'],
                'expected_size': 6.0,
                'expected_location': 'lyon'
            },
            {
                'name': 'Coastal Premium',
                'transcript': '5m² premium bathroom renovation with natural stone tiles and luxury fixtures in Nice',
                'expected_tasks': ['tiles', 'plumbing'],
                'expected_size': 5.0,
                'expected_location': 'nice'
            }
        ]
    
    def run_benchmark(self) -> Dict[str, Any]:
        """Run complete benchmark suite"""
        print("Starting Pricing Engine Benchmark")
        print("=" * 60)
        
        start_time = time.time()
        
        # Test each scenario
        for i, scenario in enumerate(self.test_scenarios, 1):
            print(f"\n📋 Test {i}: {scenario['name']}")
            print("-" * 40)
            
            result = self._test_scenario(scenario)
            self.results.append(result)
            
            # Display results
            self._display_scenario_result(result)
        
        # Calculate overall metrics
        total_time = time.time() - start_time
        benchmark_summary = self._calculate_benchmark_summary(total_time)
        
        # Display final results
        self._display_benchmark_summary(benchmark_summary)
        
        # Save results
        self._save_benchmark_results(benchmark_summary)
        
        return benchmark_summary
    
    def _test_scenario(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Test a single scenario"""
        start_time = time.time()
        
        try:
            # Generate quote
            quote = self.engine.generate_quote(scenario['transcript'])
            
            # Measure performance
            processing_time = time.time() - start_time
            
            # Validate results
            validation = self._validate_scenario_results(scenario, quote)
            
            return {
                'scenario_name': scenario['name'],
                'transcript': scenario['transcript'],
                'quote': quote,
                'processing_time': processing_time,
                'validation': validation,
                'success': True
            }
            
        except Exception as e:
            return {
                'scenario_name': scenario['name'],
                'transcript': scenario['transcript'],
                'error': str(e),
                'processing_time': time.time() - start_time,
                'success': False
            }
    
    def _validate_scenario_results(self, scenario: Dict[str, Any], quote: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that quote matches expected scenario"""
        requirements = quote['client_requirements']
        
        validation = {
            'size_match': abs(requirements['bathroom_size'] - scenario['expected_size']) < 0.1,
            'location_match': requirements['location'] == scenario['expected_location'],
            'tasks_match': all(task in requirements['tasks'] for task in scenario['expected_tasks']),
            'price_reasonable': 1000 < quote['pricing_breakdown']['final_price'] < 50000,
            'confidence_reasonable': 50 < quote['business_metrics']['confidence_score'] < 100
        }
        
        validation['overall_score'] = sum(validation.values()) / len(validation)
        
        return validation
    
    def _display_scenario_result(self, result: Dict[str, Any]):
        """Display results for a single scenario"""
        if result['success']:
            quote = result['quote']
            validation = result['validation']
            
            print(f"Success in {result['processing_time']:.3f}s")
            print(f"   Price: €{quote['pricing_breakdown']['final_price']:,.2f}")
            print(f"   Confidence: {quote['business_metrics']['confidence_score']:.1f}%")
            print(f"   Validation Score: {validation['overall_score']:.1%}")
            
            # Show validation details
            if not validation['size_match']:
                print(f"   Size mismatch: expected {quote['client_requirements']['bathroom_size']}m²")
            if not validation['location_match']:
                print(f"   Location mismatch: got {quote['client_requirements']['location']}")
            if not validation['tasks_match']:
                print(f"   Tasks mismatch: got {quote['client_requirements']['tasks']}")
        else:
            print(f"Failed in {result['processing_time']:.3f}s")
            print(f"   Error: {result['error']}")
    
    def _calculate_benchmark_summary(self, total_time: float) -> Dict[str, Any]:
        """Calculate overall benchmark metrics"""
        successful_tests = [r for r in self.results if r['success']]
        failed_tests = [r for r in self.results if not r['success']]
        
        if successful_tests:
            avg_processing_time = sum(r['processing_time'] for r in successful_tests) / len(successful_tests)
            avg_validation_score = sum(r['validation']['overall_score'] for r in successful_tests) / len(successful_tests)
            avg_confidence = sum(r['quote']['business_metrics']['confidence_score'] for r in successful_tests) / len(successful_tests)
            avg_price = sum(r['quote']['pricing_breakdown']['final_price'] for r in successful_tests) / len(successful_tests)
        else:
            avg_processing_time = avg_validation_score = avg_confidence = avg_price = 0
        
        return {
            'total_tests': len(self.results),
            'successful_tests': len(successful_tests),
            'failed_tests': len(failed_tests),
            'success_rate': len(successful_tests) / len(self.results) if self.results else 0,
            'total_time': total_time,
            'avg_processing_time': avg_processing_time,
            'avg_validation_score': avg_validation_score,
            'avg_confidence': avg_confidence,
            'avg_price': avg_price,
            'results': self.results
        }
    
    def _display_benchmark_summary(self, summary: Dict[str, Any]):
        """Display final benchmark summary"""
        print("\n" + "=" * 60)
        print("BENCHMARK SUMMARY")
        print("=" * 60)
        
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Successful: {summary['successful_tests']}")
        print(f"Failed: {summary['failed_tests']}")
        print(f"Success Rate: {summary['success_rate']:.1%}")
        print(f"Total Time: {summary['total_time']:.3f}s")
        print(f"Avg Processing Time: {summary['avg_processing_time']:.3f}s")
        print(f"Avg Validation Score: {summary['avg_validation_score']:.1%}")
        print(f"Avg Confidence: {summary['avg_confidence']:.1f}%")
        print(f"Avg Price: €{summary['avg_price']:,.2f}")
        
        # Performance analysis
        if summary['success_rate'] == 1.0:
            print("\nPERFECT SCORE! All tests passed successfully.")
        elif summary['success_rate'] >= 0.8:
            print("\nEXCELLENT! High success rate achieved.")
        elif summary['success_rate'] >= 0.6:
            print("\nGOOD! Most tests passed successfully.")
        else:
            print("\nNEEDS IMPROVEMENT! Several tests failed.")
        
        # Speed analysis
        if summary['avg_processing_time'] < 0.1:
            print("LIGHTNING FAST! Excellent performance.")
        elif summary['avg_processing_time'] < 0.5:
            print("FAST! Good performance.")
        elif summary['avg_processing_time'] < 1.0:
            print("MODERATE! Acceptable performance.")
        else:
            print("SLOW! Performance needs optimization.")
    
    def _save_benchmark_results(self, summary: Dict[str, Any]):
        """Save benchmark results to file"""
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        # Create clean results for saving (remove quote objects)
        clean_results = []
        for result in summary['results']:
            clean_result = result.copy()
            if 'quote' in clean_result:
                clean_result['quote_summary'] = {
                    'quote_id': clean_result['quote']['quote_id'],
                    'final_price': clean_result['quote']['pricing_breakdown']['final_price'],
                    'confidence': clean_result['quote']['business_metrics']['confidence_score']
                }
                del clean_result['quote']
            clean_results.append(clean_result)
        
        clean_summary = summary.copy()
        clean_summary['results'] = clean_results
        
        output_file = output_dir / "benchmark_results.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(clean_summary, f, indent=2, ensure_ascii=False)
        
        print(f"\nBenchmark results saved to: {output_file}")


def main():
    """Main benchmark execution"""
    print("🔬 Donizo Pricing Engine Benchmark Suite")
    print("Testing performance and accuracy across various scenarios")
    print()
    
    benchmark = PricingEngineBenchmark()
    results = benchmark.run_benchmark()
    
    return results


if __name__ == "__main__":
    main() 