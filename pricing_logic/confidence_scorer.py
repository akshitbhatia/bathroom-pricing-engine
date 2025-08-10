#!/usr/bin/env python3
"""
Confidence Scorer Module
Evaluates the reliability of pricing estimates and flags suspicious inputs
"""

from typing import Dict, List, Any
import math


class ConfidenceScorer:
    def __init__(self):
        """Initialize confidence scorer with scoring rules"""
        self.confidence_factors = {
            'bathroom_size': {
                'very_small': {'range': (0, 2), 'score': 0.7, 'flag': 'unusually_small'},
                'small': {'range': (2, 4), 'score': 0.9, 'flag': None},
                'medium': {'range': (4, 8), 'score': 1.0, 'flag': None},
                'large': {'range': (8, 12), 'score': 0.95, 'flag': None},
                'very_large': {'range': (12, float('inf')), 'score': 0.8, 'flag': 'unusually_large'}
            },
            'task_complexity': {
                'simple': ['painting', 'vanity'],
                'moderate': ['flooring', 'electrical'],
                'complex': ['tiles', 'plumbing']
            },
            'location_confidence': {
                'paris': 0.95,
                'marseille': 1.0,      # Default location
                'lyon': 0.9,
                'toulouse': 0.9,
                'nice': 0.9,
                'nantes': 0.9,
                'strasbourg': 0.9,
                'montpellier': 0.9
            },
            'price_thresholds': {
                'very_low': {'multiplier': 0.5, 'score': 0.6, 'flag': 'suspiciously_low'},
                'low': {'multiplier': 0.8, 'score': 0.8, 'flag': 'below_average'},
                'normal': {'multiplier': 1.0, 'score': 1.0, 'flag': None},
                'high': {'multiplier': 1.3, 'score': 0.9, 'flag': 'above_average'},
                'very_high': {'multiplier': 1.8, 'score': 0.7, 'flag': 'suspiciously_high'}
            }
        }
        
        # Historical pricing data for comparison (€/m²)
        self.historical_pricing = {
            'tiles': {'min': 35, 'max': 65, 'avg': 50},
            'plumbing': {'min': 120, 'max': 200, 'avg': 160},
            'painting': {'min': 6, 'max': 12, 'avg': 9},
            'flooring': {'min': 25, 'max': 45, 'avg': 35},
            'vanity': {'min': 180, 'max': 300, 'avg': 240},
            'electrical': {'min': 35, 'max': 60, 'avg': 48}
        }
        
        # Confidence flags
        self.flags = []
    
    def calculate_confidence(self, requirements: Dict[str, Any], task_prices: List[Dict[str, Any]], final_price: float) -> float:
        """
        Calculate overall confidence score for the pricing estimate
        
        Args:
            requirements: Client requirements dictionary
            task_prices: List of task pricing dictionaries
            final_price: Final calculated price
            
        Returns:
            Confidence score as percentage (0-100)
        """
        self.flags = []  # Reset flags
        
        # Calculate individual confidence factors
        size_confidence = self._calculate_size_confidence(requirements.get('bathroom_size', 4.0))
        location_confidence = self._calculate_location_confidence(requirements.get('location', 'marseille'))
        task_confidence = self._calculate_task_confidence(requirements.get('tasks', []))
        price_confidence = self._calculate_price_confidence(task_prices, final_price)
        complexity_confidence = self._calculate_complexity_confidence(requirements.get('tasks', []))
        
        # Weighted average of confidence factors
        weights = {
            'size': 0.15,
            'location': 0.10,
            'tasks': 0.20,
            'price': 0.35,
            'complexity': 0.20
        }
        
        weighted_confidence = (
            size_confidence * weights['size'] +
            location_confidence * weights['location'] +
            task_confidence * weights['tasks'] +
            price_confidence * weights['price'] +
            complexity_confidence * weights['complexity']
        )
        
        # Convert to percentage and apply final adjustments
        confidence_percentage = weighted_confidence * 100
        
        # Apply penalty for multiple flags
        flag_penalty = min(len(self.flags) * 0.05, 0.20)  # Max 20% penalty
        confidence_percentage = max(confidence_percentage * (1 - flag_penalty), 0)
        
        return round(confidence_percentage, 1)
    
    def _calculate_size_confidence(self, bathroom_size: float) -> float:
        """Calculate confidence based on bathroom size"""
        for size_category, data in self.confidence_factors['bathroom_size'].items():
            min_size, max_size = data['range']
            if min_size <= bathroom_size < max_size:
                if data['flag']:
                    self.flags.append(data['flag'])
                return data['score']
        
        # Default for very large bathrooms
        self.flags.append('unusually_large')
        return 0.7
    
    def _calculate_location_confidence(self, location: str) -> float:
        """Calculate confidence based on location"""
        return self.confidence_factors['location_confidence'].get(location, 0.8)
    
    def _calculate_task_confidence(self, tasks: List[str]) -> float:
        """Calculate confidence based on task types"""
        if not tasks:
            self.flags.append('no_tasks_detected')
            return 0.5
        
        # Check for unusual task combinations
        if len(tasks) == 1:
            self.flags.append('single_task_project')
        
        if len(tasks) > 5:
            self.flags.append('many_tasks')
        
        # Check for missing essential tasks
        essential_tasks = ['plumbing', 'tiles']
        missing_essential = [task for task in essential_tasks if task not in tasks]
        if missing_essential:
            self.flags.append(f'missing_essential_tasks: {", ".join(missing_essential)}')
        
        # Base confidence on number of tasks
        if len(tasks) <= 2:
            return 0.8
        elif len(tasks) <= 4:
            return 0.9
        else:
            return 0.85
    
    def _calculate_price_confidence(self, task_prices: List[Dict[str, Any]], final_price: float) -> float:
        """Calculate confidence based on price reasonableness"""
        if not task_prices:
            return 0.5
        
        # Calculate total materials and labor
        total_materials = sum(task.get('materials', 0) for task in task_prices)
        total_labor = sum(task.get('labor', 0) for task in task_prices)
        
        # Calculate price per m²
        bathroom_size = 4.0  # Default, could be extracted from requirements
        price_per_m2 = final_price / bathroom_size if bathroom_size > 0 else 0
        
        # Compare with historical ranges
        historical_avg = sum(data['avg'] for data in self.historical_pricing.values())
        price_ratio = price_per_m2 / historical_avg if historical_avg > 0 else 1.0
        
        # Determine price category
        for category, data in self.confidence_factors['price_thresholds'].items():
            if price_ratio <= data['multiplier']:
                if data['flag']:
                    self.flags.append(data['flag'])
                return data['score']
        
        # Very high price
        self.flags.append('suspiciously_high')
        return 0.7
    
    def _calculate_complexity_confidence(self, tasks: List[str]) -> float:
        """Calculate confidence based on task complexity"""
        if not tasks:
            return 0.5
        
        complexity_scores = []
        for task in tasks:
            if task in self.confidence_factors['task_complexity']['simple']:
                complexity_scores.append(0.9)
            elif task in self.confidence_factors['task_complexity']['moderate']:
                complexity_scores.append(0.95)
            elif task in self.confidence_factors['task_complexity']['complex']:
                complexity_scores.append(0.85)
            else:
                complexity_scores.append(0.8)
        
        # Average complexity confidence
        return sum(complexity_scores) / len(complexity_scores)
    
    def get_flags(self) -> List[str]:
        """Get list of confidence flags"""
        return self.flags.copy()
    
    def get_flag_summary(self) -> Dict[str, Any]:
        """Get detailed summary of confidence flags"""
        flag_categories = {
            'size_issues': [],
            'task_issues': [],
            'price_issues': [],
            'location_issues': []
        }
        
        for flag in self.flags:
            if 'size' in flag or 'small' in flag or 'large' in flag:
                flag_categories['size_issues'].append(flag)
            elif 'task' in flag:
                flag_categories['task_issues'].append(flag)
            elif 'price' in flag or 'low' in flag or 'high' in flag:
                flag_categories['price_issues'].append(flag)
            elif 'location' in flag:
                flag_categories['location_issues'].append(flag)
        
        return {
            'total_flags': len(self.flags),
            'flag_categories': flag_categories,
            'all_flags': self.flags.copy(),
            'severity': self._calculate_flag_severity()
        }
    
    def _calculate_flag_severity(self) -> str:
        """Calculate overall severity of flags"""
        if not self.flags:
            return 'none'
        
        high_severity_flags = ['suspiciously_low', 'suspiciously_high', 'no_tasks_detected']
        medium_severity_flags = ['unusually_small', 'unusually_large', 'missing_essential_tasks']
        
        high_count = sum(1 for flag in self.flags if flag in high_severity_flags)
        medium_count = sum(1 for flag in self.flags if flag in medium_severity_flags)
        
        if high_count > 0:
            return 'high'
        elif medium_count > 0:
            return 'medium'
        else:
            return 'low'
    
    def suggest_improvements(self) -> List[str]:
        """Suggest improvements based on confidence flags"""
        suggestions = []
        
        for flag in self.flags:
            if flag == 'suspiciously_low':
                suggestions.append("Review material and labor costs - prices seem unusually low")
            elif flag == 'suspiciously_high':
                suggestions.append("Review pricing calculations - prices seem unusually high")
            elif flag == 'unusually_small':
                suggestions.append("Verify bathroom size - very small bathrooms may need special considerations")
            elif flag == 'unusually_large':
                suggestions.append("Verify bathroom size - very large bathrooms may need different pricing model")
            elif flag == 'missing_essential_tasks':
                suggestions.append("Consider adding essential renovation tasks for complete bathroom renovation")
            elif flag == 'single_task_project':
                suggestions.append("Single task projects may need different pricing approach")
            elif flag == 'many_tasks':
                suggestions.append("Many tasks detected - verify all are necessary for this project")
        
        return suggestions
    
    def update_historical_pricing(self, new_data: Dict[str, Dict[str, float]]) -> None:
        """Update historical pricing data (for feedback loop integration)"""
        for task, data in new_data.items():
            if task in self.historical_pricing:
                self.historical_pricing[task].update(data)
    
    def get_confidence_report(self) -> Dict[str, Any]:
        """Get comprehensive confidence report"""
        return {
            'confidence_score': self.calculate_confidence({}, [], 0),
            'flags': self.get_flag_summary(),
            'suggestions': self.suggest_improvements(),
            'historical_data': self.historical_pricing.copy(),
            'confidence_factors': {
                'size_ranges': self.confidence_factors['bathroom_size'],
                'task_complexity': self.confidence_factors['task_complexity'],
                'location_confidence': self.confidence_factors['location_confidence'],
                'price_thresholds': self.confidence_factors['price_thresholds']
            }
        } 