#!/usr/bin/env python3
"""
Donizo Smart Pricing Engine for Bathroom Renovations
Main orchestrator that processes voice transcripts and generates structured quotes
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from pricing_logic.material_db import MaterialDatabase
from pricing_logic.labor_calc import LaborCalculator
from pricing_logic.vat_rules import VATRules
from pricing_logic.confidence_scorer import ConfidenceScorer


class SmartPricingEngine:
    """
    Intelligent pricing engine for bathroom renovation projects.
    
    Processes voice transcripts and generates accurate, detailed quotes
    using AI-powered analysis and French market data.
    """
    
    def __init__(self):
        """Initialize the pricing engine with all required modules"""
        try:
            self.material_db = MaterialDatabase()
            self.labor_calc = LaborCalculator()
            self.vat_rules = VATRules()
            self.confidence_scorer = ConfidenceScorer()
            
            # City-based pricing multipliers
            self.city_multipliers = {
                'marseille': 1.0,    # Base pricing
                'paris': 1.3,        # High-cost metropolitan
                'nice': 1.25,        # Premium coastal
                'lyon': 1.15,        # Major urban center
                'toulouse': 1.1,     # Growing tech hub
                'nantes': 1.05,      # Moderate cost
                'strasbourg': 1.1,   # Eastern France
                'montpellier': 1.05  # Southern France
            }
            
            logger.info("Pricing engine initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize pricing engine: {e}")
            raise RuntimeError(f"Pricing engine initialization failed: {e}")
    
    def parse_transcript(self, transcript: str) -> Dict[str, Any]:
        """
        Parse voice transcript to extract renovation requirements.
        
        Args:
            transcript: Voice transcript text describing renovation needs
            
        Returns:
            Dictionary containing structured renovation requirements
            
        Raises:
            ValueError: If transcript is invalid or empty
        """
        if not transcript or not isinstance(transcript, str):
            raise ValueError("Transcript must be a non-empty string")
        
        if len(transcript.strip()) < 10:
            raise ValueError("Transcript too short - please provide more details")
        
        transcript_lower = transcript.lower().strip()
        logger.info(f"Parsing transcript: {transcript[:100]}...")
        
        try:
            # Extract bathroom size
            size_match = re.search(r'(\d+(?:\.\d+)?)\s*m²', transcript_lower)
            bathroom_size = float(size_match.group(1)) if size_match else 4.0
            
            # Validate size range
            if bathroom_size < 1.0 or bathroom_size > 50.0:
                logger.warning(f"Bathroom size {bathroom_size}m² is outside normal range (1-50m²)")
            
            # Extract location
            location = self._extract_location(transcript_lower)
            
            # Extract tasks
            tasks = self._extract_tasks(transcript_lower)
            
            # Validate that at least one task was found
            if not tasks:
                logger.warning("No renovation tasks detected in transcript")
                tasks = ['painting']  # Default fallback
            
            # Extract budget constraint
            budget_conscious = any(word in transcript_lower for word in ['budget', 'cheap', 'affordable', 'economy'])
            
            requirements = {
                'bathroom_size': bathroom_size,
                'location': location,
                'tasks': tasks,
                'budget_conscious': budget_conscious,
                'original_transcript': transcript
            }
            
            logger.info(f"Extracted requirements: {requirements}")
            return requirements
            
        except Exception as e:
            logger.error(f"Failed to parse transcript: {e}")
            raise ValueError(f"Failed to parse transcript: {e}")
    
    def _extract_location(self, transcript: str) -> str:
        """Extract city/location from transcript"""
        # Common French cities
        cities = list(self.city_multipliers.keys())
        for city in cities:
            if city in transcript:
                return city
        return 'marseille'  # Default
    
    def _extract_tasks(self, transcript: str) -> List[str]:
        """Extract renovation tasks from transcript"""
        task_keywords = {
            'tiles': ['tiles', 'tile', 'ceramic', 'porcelain'],
            'plumbing': ['plumbing', 'shower', 'bath', 'sink', 'toilet'],
            'painting': ['paint', 'repaint', 'wall'],
            'flooring': ['floor', 'flooring', 'laying'],
            'vanity': ['vanity', 'cabinet', 'storage'],
            'electrical': ['electrical', 'lighting', 'outlet', 'switch']
        }
        
        detected_tasks = []
        for task_type, keywords in task_keywords.items():
            if any(keyword in transcript for keyword in keywords):
                detected_tasks.append(task_type)
        
        return detected_tasks
    
    def generate_quote(self, transcript: str) -> Dict[str, Any]:
        """
        Main method to generate a complete renovation quote.
        
        Args:
            transcript: Voice transcript describing renovation needs
            
        Returns:
            Complete quote with pricing breakdown and business metrics
            
        Raises:
            ValueError: If transcript is invalid
            RuntimeError: If quote generation fails
        """
        try:
            logger.info("Starting quote generation")
            
            # Parse transcript
            requirements = self.parse_transcript(transcript)
            
            # Calculate pricing for each task
            task_prices = []
            total_labor = 0
            total_materials = 0
            
            for task in requirements['tasks']:
                task_price = self._calculate_task_price(task, requirements)
                task_prices.append(task_price)
                total_labor += task_price['labor']
                total_materials += task_price['materials']
            
            # Calculate VAT
            vat_amount = self.vat_rules.calculate_total_vat(task_prices)
            
            # Calculate subtotal and total
            subtotal = total_labor + total_materials
            total_with_vat = subtotal + vat_amount
            
            # Apply margin protection
            final_price = self._apply_margin_protection(total_with_vat, requirements['budget_conscious'])
            
            # Calculate confidence score
            confidence_score = self.confidence_scorer.calculate_confidence(
                requirements, task_prices, final_price
            )
            
            # Generate quote
            quote = {
                'quote_id': f"DQ{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'generated_at': datetime.now().isoformat(),
                'client_requirements': requirements,
                'pricing_breakdown': {
                    'tasks': task_prices,
                    'labor_total': total_labor,
                    'materials_total': total_materials,
                    'vat_amount': vat_amount,
                    'subtotal': subtotal,
                    'final_price': final_price
                },
                'business_metrics': {
                    'confidence_score': confidence_score,
                    'margin_percentage': self._calculate_margin_percentage(subtotal, final_price),
                    'city_multiplier': self.city_multipliers[requirements['location']],
                    'total_duration': self._calculate_total_duration(task_prices, requirements),
                    'estimated_duration': self._calculate_total_duration(task_prices, requirements)
                },
                'metadata': {
                    'version': '1.0.0',
                    'generated_by': 'Donizo Smart Pricing Engine',
                    'algorithm_version': '2.1.0',
                    'last_updated': datetime.now().isoformat()
                }
            }
            
            logger.info(f"Quote generated successfully: {quote['quote_id']}")
            return quote
            
        except Exception as e:
            logger.error(f"Quote generation failed: {e}")
            raise RuntimeError(f"Failed to generate quote: {e}")
    
    def _calculate_task_price(self, task: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate pricing for a specific renovation task"""
        try:
            # Get material costs
            material_cost = self.material_db.get_task_materials_cost(
                task, requirements['bathroom_size']
            )
            
            # Get labor costs
            labor_cost = self.labor_calc.calculate_labor_cost(
                task, requirements['bathroom_size']
            )
            
            # Apply city multiplier
            city_multiplier = self.city_multipliers[requirements['location']]
            adjusted_material_cost = material_cost * city_multiplier
            adjusted_labor_cost = labor_cost * city_multiplier
            
            return {
                'task': task,
                'materials': adjusted_material_cost,
                'labor': adjusted_labor_cost,
                'total': adjusted_material_cost + adjusted_labor_cost,
                'city_multiplier': city_multiplier
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate price for task {task}: {e}")
            # Return safe fallback values
            return {
                'task': task,
                'materials': 100.0,
                'labor': 200.0,
                'total': 300.0,
                'city_multiplier': 1.0,
                'error': str(e)
            }
    
    def _apply_margin_protection(self, base_price: float, budget_conscious: bool) -> float:
        """Apply business margin protection"""
        if budget_conscious:
            margin = 0.15  # 15% margin for budget projects
        else:
            margin = 0.25  # 25% margin for standard projects
        
        return base_price * (1 + margin)
    
    def _calculate_margin_percentage(self, subtotal: float, final_price: float) -> float:
        """Calculate the applied margin percentage"""
        if subtotal > 0:
            return ((final_price - subtotal) / subtotal) * 100
        return 0.0
    
    def _calculate_total_duration(self, task_prices: List[Dict[str, Any]], requirements: Dict[str, Any]) -> float:
        """Calculate total project duration"""
        return sum(self.labor_calc.get_task_duration(task['task'], requirements['bathroom_size']) for task in task_prices)
    
    def save_quote(self, quote: Dict[str, Any], filename: str = None) -> str:
        """
        Save quote to JSON file.
        
        Args:
            quote: Quote dictionary to save
            filename: Optional custom filename
            
        Returns:
            Path to saved file
        """
        try:
            if filename is None:
                # Create output directory if it doesn't exist
                output_dir = Path("output")
                output_dir.mkdir(exist_ok=True)
                
                filename = output_dir / f"quote_{quote['quote_id']}.json"
            
            # Ensure filename has .json extension
            if not str(filename).endswith('.json'):
                filename = str(filename) + '.json'
            
            # Ensure output directory exists
            output_path = Path(filename)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(quote, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Quote saved to: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Failed to save quote: {e}")
            raise RuntimeError(f"Failed to save quote: {e}")


def main():
    """Main function for direct script execution"""
    try:
        engine = SmartPricingEngine()
        
        # Example usage
        transcript = "4m² bathroom renovation with tiles and painting in Paris"
        quote = engine.generate_quote(transcript)
        
        print(f"Generated quote: {quote['quote_id']}")
        print(f"Final price: €{quote['pricing_breakdown']['final_price']:,.2f}")
        
        # Save quote
        output_file = engine.save_quote(quote)
        print(f"Quote saved to: {output_file}")
        
    except Exception as e:
        logger.error(f"Main execution failed: {e}")
        print(f"Error: {e}")


if __name__ == "__main__":
    main() 