#!/usr/bin/env python3
"""
Labor Calculator Module
Handles time estimates and labor costs for different renovation tasks
"""

from typing import Dict, List, Any
import math


class LaborCalculator:
    def __init__(self):
        """Initialize labor calculator with default rates and time estimates"""
        self.hourly_rates = {
            'tiles': 45.0,      # €/hour for tiling work
            'plumbing': 55.0,   # €/hour for plumbing work
            'painting': 35.0,   # €/hour for painting work
            'flooring': 40.0,   # €/hour for flooring work
            'vanity': 42.0,     # €/hour for cabinet installation
            'electrical': 48.0  # €/hour for electrical work
        }
        
        self.complexity_factors = {
            'tiles': 1.2,       # Tiling is complex
            'plumbing': 1.4,    # Plumbing is very complex
            'painting': 0.9,    # Painting is relatively simple
            'flooring': 1.1,    # Flooring has moderate complexity
            'vanity': 0.8,      # Vanity installation is simple
            'electrical': 1.3   # Electrical work is complex
        }
        
        self.base_time_estimates = {
            'tiles': {
                'per_m2': 2.5,      # hours per m²
                'setup_time': 2.0,   # hours for setup
                'cleanup_time': 1.5  # hours for cleanup
            },
            'plumbing': {
                'shower': 8.0,       # hours for shower
                'toilet': 4.0,       # hours for toilet
                'sink': 3.0,         # hours for sink
                'bath': 6.0,         # hours for bath
                'setup_time': 1.0,   # hours for setup
                'testing_time': 2.0  # hours for testing
            },
            'painting': {
                'per_m2': 0.3,       # hours per m²
                'prep_time': 1.5,    # hours for preparation
                'drying_time': 0.0,  # drying time (not billable)
                'cleanup_time': 1.0  # hours for cleanup
            },
            'flooring': {
                'per_m2': 1.8,       # hours per m²
                'prep_time': 2.0,    # hours for preparation
                'cleanup_time': 1.0  # hours for cleanup
            },
            'vanity': {
                'base_time': 3.0,    # hours for installation
                'plumbing_time': 1.5, # additional plumbing time
                'setup_time': 0.5    # hours for setup
            },
            'electrical': {
                'base_time': 2.0,    # hours for basic electrical
                'per_outlet': 0.5,   # hours per outlet
                'testing_time': 1.0  # hours for testing
            }
        }
    
    def calculate_labor_cost(self, task: str, bathroom_size: float, complexity: str = 'standard') -> float:
        """
        Calculate labor cost for a specific task
        
        Args:
            task: Type of renovation task
            bathroom_size: Bathroom size in m²
            complexity: Complexity level (simple, standard, complex)
            
        Returns:
            Total labor cost for the task
        """
        if task not in self.hourly_rates:
            return 0.0
        
        # Get time estimate
        total_hours = self.get_task_duration(task, bathroom_size, complexity)
        
        # Get hourly rate
        hourly_rate = self.hourly_rates[task]
        
        # Apply complexity factor
        complexity_multiplier = self._get_complexity_multiplier(complexity)
        
        # Calculate total cost
        total_cost = total_hours * hourly_rate * complexity_multiplier
        
        return round(total_cost, 2)
    
    def get_task_duration(self, task: str, bathroom_size: float, complexity: str = 'standard') -> float:
        """
        Calculate estimated duration for a specific task
        
        Args:
            task: Type of renovation task
            bathroom_size: Bathroom size in m²
            complexity: Complexity level
            
        Returns:
            Estimated duration in hours
        """
        if task not in self.base_time_estimates:
            return 0.0
        
        base_estimates = self.base_time_estimates[task]
        
        if task == 'tiles':
            return self._calculate_tiles_duration(base_estimates, bathroom_size, complexity)
        elif task == 'plumbing':
            return self._calculate_plumbing_duration(base_estimates, complexity)
        elif task == 'painting':
            return self._calculate_painting_duration(base_estimates, bathroom_size, complexity)
        elif task == 'flooring':
            return self._calculate_flooring_duration(base_estimates, bathroom_size, complexity)
        elif task == 'vanity':
            return self._calculate_vanity_duration(base_estimates, complexity)
        elif task == 'electrical':
            return self._calculate_electrical_duration(base_estimates, bathroom_size, complexity)
        else:
            return 0.0
    
    def _calculate_tiles_duration(self, estimates: Dict[str, float], bathroom_size: float, complexity: str) -> float:
        """Calculate tiling duration"""
        # Calculate wall area (assuming 2.4m height)
        wall_height = 2.4
        wall_area = (bathroom_size ** 0.5 * 4) * wall_height
        
        # Calculate time based on area
        area_time = wall_area * estimates['per_m2']
        
        # Add setup and cleanup time
        total_time = area_time + estimates['setup_time'] + estimates['cleanup_time']
        
        # Apply complexity multiplier
        complexity_mult = self._get_complexity_multiplier(complexity)
        
        return round(total_time * complexity_mult, 1)
    
    def _calculate_plumbing_duration(self, estimates: Dict[str, float], complexity: str) -> float:
        """Calculate plumbing duration"""
        # Sum up all fixture installation times
        fixture_time = sum([
            estimates['shower'],
            estimates['toilet'],
            estimates['sink']
            # Note: bath is optional, not included in default
        ])
        
        # Add setup and testing time
        total_time = fixture_time + estimates['setup_time'] + estimates['testing_time']
        
        # Apply complexity multiplier
        complexity_mult = self._get_complexity_multiplier(complexity)
        
        return round(total_time * complexity_mult, 1)
    
    def _calculate_painting_duration(self, estimates: Dict[str, float], bathroom_size: float, complexity: str) -> float:
        """Calculate painting duration"""
        # Calculate wall area (excluding floor)
        wall_height = 2.4
        wall_area = (bathroom_size ** 0.5 * 4) * wall_height
        
        # Calculate time based on area
        area_time = wall_area * estimates['per_m2']
        
        # Add prep and cleanup time
        total_time = area_time + estimates['prep_time'] + estimates['cleanup_time']
        
        # Apply complexity multiplier
        complexity_mult = self._get_complexity_multiplier(complexity)
        
        return round(total_time * complexity_mult, 1)
    
    def _calculate_flooring_duration(self, estimates: Dict[str, float], bathroom_size: float, complexity: str) -> float:
        """Calculate flooring duration"""
        # Calculate time based on floor area
        area_time = bathroom_size * estimates['per_m2']
        
        # Add prep and cleanup time
        total_time = area_time + estimates['prep_time'] + estimates['cleanup_time']
        
        # Apply complexity multiplier
        complexity_mult = self._get_complexity_multiplier(complexity)
        
        return round(total_time * complexity_mult, 1)
    
    def _calculate_vanity_duration(self, estimates: Dict[str, float], complexity: str) -> float:
        """Calculate vanity installation duration"""
        # Sum up all time components
        total_time = estimates['base_time'] + estimates['plumbing_time'] + estimates['setup_time']
        
        # Apply complexity multiplier
        complexity_mult = self._get_complexity_multiplier(complexity)
        
        return round(total_time * complexity_mult, 1)
    
    def _calculate_electrical_duration(self, estimates: Dict[str, float], bathroom_size: float, complexity: str) -> float:
        """Calculate electrical work duration"""
        # Estimate number of outlets based on bathroom size
        if bathroom_size <= 4:
            outlets = 2
        elif bathroom_size <= 6:
            outlets = 3
        else:
            outlets = 4
        
        # Calculate time based on outlets
        outlet_time = outlets * estimates['per_outlet']
        
        # Add base time and testing time
        total_time = estimates['base_time'] + outlet_time + estimates['testing_time']
        
        # Apply complexity multiplier
        complexity_mult = self._get_complexity_multiplier(complexity)
        
        return round(total_time * complexity_mult, 1)
    
    def _get_complexity_multiplier(self, complexity: str) -> float:
        """Get time multiplier based on complexity level"""
        complexity_multipliers = {
            'simple': 0.8,
            'standard': 1.0,
            'complex': 1.3
        }
        
        return complexity_multipliers.get(complexity, 1.0)
    
    def get_daily_rate(self, task: str) -> float:
        """Get daily rate for a specific task (8-hour day)"""
        if task not in self.hourly_rates:
            return 0.0
        
        return self.hourly_rates[task] * 8
    
    def update_hourly_rates(self, new_rates: Dict[str, float]) -> None:
        """Update hourly rates (for feedback loop integration)"""
        for task, rate in new_rates.items():
            if task in self.hourly_rates:
                self.hourly_rates[task] = rate
    
    def get_labor_summary(self) -> Dict[str, Any]:
        """Get summary of all labor rates and complexity factors"""
        return {
            'hourly_rates': self.hourly_rates.copy(),
            'complexity_factors': self.complexity_factors.copy(),
            'daily_rates': {task: self.get_daily_rate(task) for task in self.hourly_rates}
        }
    
    def estimate_project_duration(self, tasks: List[str], bathroom_size: float) -> Dict[str, Any]:
        """
        Estimate total project duration considering task dependencies
        
        Returns:
            Dictionary with total duration and breakdown
        """
        total_hours = 0
        task_durations = {}
        
        for task in tasks:
            duration = self.get_task_duration(task, bathroom_size)
            task_durations[task] = duration
            total_hours += duration
        
        # Convert to working days (8 hours per day)
        working_days = math.ceil(total_hours / 8)
        
        # Add buffer for coordination and unexpected issues
        buffer_days = max(1, working_days * 0.2)
        total_days = working_days + buffer_days
        
        return {
            'total_hours': total_hours,
            'working_days': working_days,
            'buffer_days': buffer_days,
            'total_days': total_days,
            'task_breakdown': task_durations
        } 