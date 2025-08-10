#!/usr/bin/env python3
"""
VAT Rules Module
Handles task-specific VAT calculations based on French tax regulations
"""

from typing import Dict, List, Any


class VATRules:
    def __init__(self):
        """Initialize VAT rules with French tax rates"""
        # French VAT rates as of 2024
        self.vat_rates = {
            'standard': 0.20,      # 20% - Standard rate
            'reduced': 0.10,       # 10% - Reduced rate for renovation
            'super_reduced': 0.055  # 5.5% - Super reduced rate for essential work
        }
        
        # Task-specific VAT classifications
        self.task_vat_classification = {
            'tiles': 'reduced',           # Wall/floor tiles - renovation work
            'plumbing': 'reduced',        # Plumbing work - renovation
            'painting': 'reduced',        # Painting - renovation work
            'flooring': 'reduced',        # Flooring - renovation work
            'vanity': 'standard',         # Furniture/vanity - standard rate
            'electrical': 'reduced'      # Electrical work - renovation
        }
        
        # Special conditions for VAT reduction
        self.vat_conditions = {
            'reduced': {
                'min_work_value': 1000.0,  # €1000 minimum for reduced VAT
                'max_work_value': 50000.0, # €50k maximum for reduced VAT
                'property_age': 2,         # Property must be >2 years old
                'work_type': 'renovation'  # Must be renovation work
            }
        }
    
    def get_vat_rate(self, task: str, work_value: float = 0.0, property_age: int = 10) -> float:
        """
        Get VAT rate for a specific task
        
        Args:
            task: Type of renovation task
            work_value: Total value of work (for VAT reduction eligibility)
            property_age: Age of property in years
            
        Returns:
            VAT rate as decimal (e.g., 0.20 for 20%)
        """
        if task not in self.task_vat_classification:
            return self.vat_rates['standard']
        
        vat_type = self.task_vat_classification[task]
        
        # Check if reduced VAT conditions are met
        if vat_type == 'reduced':
            if self._is_eligible_for_reduced_vat(work_value, property_age):
                return self.vat_rates['reduced']
            else:
                return self.vat_rates['standard']
        
        return self.vat_rates[vat_type]
    
    def _is_eligible_for_reduced_vat(self, work_value: float, property_age: int) -> bool:
        """
        Check if work is eligible for reduced VAT rate
        
        Args:
            work_value: Total value of work
            property_age: Age of property in years
            
        Returns:
            True if eligible for reduced VAT
        """
        conditions = self.vat_conditions['reduced']
        
        # Check work value range
        if not (conditions['min_work_value'] <= work_value <= conditions['max_work_value']):
            return False
        
        # Check property age
        if property_age < conditions['property_age']:
            return False
        
        return True
    
    def calculate_task_vat(self, task: str, amount: float, work_value: float = 0.0, property_age: int = 10) -> Dict[str, float]:
        """
        Calculate VAT for a specific task
        
        Args:
            task: Type of renovation task
            amount: Amount to calculate VAT on
            work_value: Total work value for VAT eligibility
            property_age: Property age for VAT eligibility
            
        Returns:
            Dictionary with VAT rate and amount
        """
        vat_rate = self.get_vat_rate(task, work_value, property_age)
        vat_amount = amount * vat_rate
        
        return {
            'vat_rate': vat_rate,
            'vat_amount': round(vat_amount, 2),
            'vat_type': self.task_vat_classification.get(task, 'standard')
        }
    
    def calculate_total_vat(self, task_prices: List[Dict[str, Any]], work_value: float = 0.0, property_age: int = 10) -> float:
        """
        Calculate total VAT for all tasks
        
        Args:
            task_prices: List of task pricing dictionaries
            work_value: Total work value for VAT eligibility
            property_age: Property age for VAT eligibility
            
        Returns:
            Total VAT amount
        """
        total_vat = 0.0
        
        for task_price in task_prices:
            task_type = task_price.get('task_type', '')
            materials = task_price.get('materials', 0.0)
            labor = task_price.get('labor', 0.0)
            
            # Calculate VAT for materials and labor separately
            materials_vat = self.calculate_task_vat(task_type, materials, work_value, property_age)
            labor_vat = self.calculate_task_vat(task_type, labor, work_value, property_age)
            
            total_vat += materials_vat['vat_amount'] + labor_vat['vat_amount']
        
        return round(total_vat, 2)
    
    def get_vat_breakdown(self, task_prices: List[Dict[str, Any]], work_value: float = 0.0, property_age: int = 10) -> Dict[str, Any]:
        """
        Get detailed VAT breakdown for all tasks
        
        Args:
            task_prices: List of task pricing dictionaries
            work_value: Total work value for VAT eligibility
            property_age: Property age for VAT eligibility
            
        Returns:
            Detailed VAT breakdown
        """
        breakdown = {
            'total_vat': 0.0,
            'vat_by_task': [],
            'vat_by_rate': {
                'standard': 0.0,
                'reduced': 0.0,
                'super_reduced': 0.0
            }
        }
        
        for task_price in task_prices:
            task_type = task_price.get('task_type', '')
            materials = task_price.get('materials', 0.0)
            labor = task_price.get('labor', 0.0)
            
            # Calculate VAT for materials and labor
            materials_vat = self.calculate_task_vat(task_type, materials, work_value, property_age)
            labor_vat = self.calculate_task_vat(task_type, labor, work_value, property_age)
            
            task_vat_total = materials_vat['vat_amount'] + labor_vat['vat_amount']
            
            # Add to breakdown
            breakdown['total_vat'] += task_vat_total
            
            breakdown['vat_by_task'].append({
                'task_type': task_type,
                'materials_vat': materials_vat,
                'labor_vat': labor_vat,
                'total_task_vat': task_vat_total
            })
            
            # Aggregate by VAT rate
            vat_type = materials_vat['vat_type']
            breakdown['vat_by_rate'][vat_type] += task_vat_total
        
        # Round all amounts
        breakdown['total_vat'] = round(breakdown['total_vat'], 2)
        for rate in breakdown['vat_by_rate']:
            breakdown['vat_by_rate'][rate] = round(breakdown['vat_by_rate'][rate], 2)
        
        return breakdown
    
    def get_vat_summary(self) -> Dict[str, Any]:
        """Get summary of VAT rules and rates"""
        return {
            'vat_rates': self.vat_rates.copy(),
            'task_classifications': self.task_vat_classification.copy(),
            'reduced_vat_conditions': self.vat_conditions['reduced'].copy()
        }
    
    def update_vat_rates(self, new_rates: Dict[str, float]) -> None:
        """Update VAT rates (for regulatory changes)"""
        for rate_type, rate in new_rates.items():
            if rate_type in self.vat_rates:
                self.vat_rates[rate_type] = rate
    
    def update_task_classifications(self, new_classifications: Dict[str, str]) -> None:
        """Update task VAT classifications"""
        for task, vat_type in new_classifications.items():
            if vat_type in self.vat_rates:
                self.task_vat_classification[task] = vat_type
    
    def validate_vat_calculation(self, task_prices: List[Dict[str, Any]], total_vat: float) -> Dict[str, Any]:
        """
        Validate VAT calculation for quality assurance
        
        Args:
            task_prices: List of task pricing dictionaries
            total_vat: Total VAT amount to validate
            
        Returns:
            Validation results
        """
        calculated_vat = self.calculate_total_vat(task_prices)
        difference = abs(calculated_vat - total_vat)
        
        validation = {
            'is_valid': difference < 0.01,  # Allow for rounding differences
            'calculated_vat': calculated_vat,
            'provided_vat': total_vat,
            'difference': round(difference, 2),
            'tolerance': 0.01
        }
        
        return validation 