#!/usr/bin/env python3
"""
Material Database Module
Handles material costs for different renovation tasks and bathroom sizes
"""

import json
from typing import Dict, List, Any
from pathlib import Path


class MaterialDatabase:
    def __init__(self):
        """Initialize material database with default pricing"""
        self.materials = self._load_default_materials()
        self.supported_tasks = ['tiles', 'plumbing', 'painting', 'flooring', 'vanity', 'electrical']
        
    def _load_default_materials(self) -> Dict[str, Any]:
        """Load default material pricing data"""
        return {
            'tiles': {
                'base_cost_per_m2': 45.0,  # €/m² for ceramic tiles
                'size_factor': 0.95,       # Slightly cheaper for smaller bathrooms
                'quality_multipliers': {
                    'basic': 0.8,
                    'standard': 1.0,
                    'premium': 1.4,
                    'luxury': 2.0
                }
            },
            'plumbing': {
                'shower': {
                    'base_cost': 180.0,
                    'size_factor': 0.9
                },
                'toilet': {
                    'base_cost': 120.0,
                    'size_factor': 1.0
                },
                'sink': {
                    'base_cost': 85.0,
                    'size_factor': 0.95
                },
                'bath': {
                    'base_cost': 350.0,
                    'size_factor': 1.1
                }
            },
            'painting': {
                'base_cost_per_m2': 8.5,   # €/m² for wall paint
                'size_factor': 1.05,       # Slightly more expensive for smaller areas
                'coats': 2,                # Number of coats
                'quality_multipliers': {
                    'basic': 0.7,
                    'standard': 1.0,
                    'premium': 1.3
                }
            },
            'flooring': {
                'base_cost_per_m2': 32.0,  # €/m² for floor tiles
                'size_factor': 0.98,
                'quality_multipliers': {
                    'basic': 0.8,
                    'standard': 1.0,
                    'premium': 1.5
                }
            },
            'vanity': {
                'base_cost': 220.0,
                'size_factor': 1.0,
                'quality_multipliers': {
                    'basic': 0.7,
                    'standard': 1.0,
                    'premium': 1.6
                }
            },
            'electrical': {
                'base_cost': 45.0,
                'size_factor': 1.0,
                'per_outlet': 15.0
            }
        }
    
    def get_task_materials_cost(self, task: str, bathroom_size: float, quality: str = 'standard') -> float:
        """
        Calculate material costs for a specific task
        
        Args:
            task: Type of renovation task
            bathroom_size: Bathroom size in m²
            quality: Material quality level
            
        Returns:
            Total material cost for the task
        """
        if task not in self.materials:
            return 0.0
        
        task_materials = self.materials[task]
        
        if task == 'tiles':
            return self._calculate_tiles_cost(task_materials, bathroom_size, quality)
        elif task == 'plumbing':
            return self._calculate_plumbing_cost(task_materials, bathroom_size)
        elif task == 'painting':
            return self._calculate_painting_cost(task_materials, bathroom_size, quality)
        elif task == 'flooring':
            return self._calculate_flooring_cost(task_materials, bathroom_size, quality)
        elif task == 'vanity':
            return self._calculate_vanity_cost(task_materials, quality)
        elif task == 'electrical':
            return self._calculate_electrical_cost(task_materials, bathroom_size)
        else:
            return 0.0
    
    def _calculate_tiles_cost(self, materials: Dict[str, Any], bathroom_size: float, quality: str) -> float:
        """Calculate tiles cost based on bathroom size and quality"""
        base_cost = materials['base_cost_per_m2']
        size_factor = materials['size_factor']
        quality_mult = materials['quality_multipliers'].get(quality, 1.0)
        
        # Calculate wall area (assuming 2.4m height)
        wall_height = 2.4
        wall_area = (bathroom_size ** 0.5 * 4) * wall_height
        
        # Apply size and quality factors
        total_cost = wall_area * base_cost * size_factor * quality_mult
        
        return round(total_cost, 2)
    
    def _calculate_plumbing_cost(self, materials: Dict[str, Any], bathroom_size: float) -> float:
        """Calculate plumbing cost for all fixtures"""
        total_cost = 0.0
        
        for fixture, data in materials.items():
            base_cost = data['base_cost']
            size_factor = data['size_factor']
            fixture_cost = base_cost * size_factor
            total_cost += fixture_cost
        
        return round(total_cost, 2)
    
    def _calculate_painting_cost(self, materials: Dict[str, Any], bathroom_size: float, quality: str) -> float:
        """Calculate painting cost for walls"""
        base_cost = materials['base_cost_per_m2']
        size_factor = materials['size_factor']
        quality_mult = materials['quality_multipliers'].get(quality, 1.0)
        coats = materials['coats']
        
        # Calculate wall area (excluding floor)
        wall_height = 2.4
        wall_area = (bathroom_size ** 0.5 * 4) * wall_height
        
        # Apply factors
        total_cost = wall_area * base_cost * size_factor * quality_mult * coats
        
        return round(total_cost, 2)
    
    def _calculate_flooring_cost(self, materials: Dict[str, Any], bathroom_size: float, quality: str) -> float:
        """Calculate flooring cost"""
        base_cost = materials['base_cost_per_m2']
        size_factor = materials['size_factor']
        quality_mult = materials['quality_multipliers'].get(quality, 1.0)
        
        # Floor area is the bathroom size
        total_cost = bathroom_size * base_cost * size_factor * quality_mult
        
        return round(total_cost, 2)
    
    def _calculate_vanity_cost(self, materials: Dict[str, Any], quality: str) -> float:
        """Calculate vanity/cabinet cost"""
        base_cost = materials['base_cost']
        quality_mult = materials['quality_multipliers'].get(quality, 1.0)
        
        total_cost = base_cost * quality_mult
        
        return round(total_cost, 2)
    
    def _calculate_electrical_cost(self, materials: Dict[str, Any], bathroom_size: float) -> float:
        """Calculate electrical work cost"""
        base_cost = materials['base_cost']
        size_factor = materials['size_factor']
        
        # Estimate number of outlets based on bathroom size
        if bathroom_size <= 4:
            outlets = 2
        elif bathroom_size <= 6:
            outlets = 3
        else:
            outlets = 4
        
        outlet_cost = outlets * materials['per_outlet']
        total_cost = base_cost * size_factor + outlet_cost
        
        return round(total_cost, 2)
    
    def update_material_prices(self, new_prices: Dict[str, Any]) -> None:
        """Update material prices (for feedback loop integration)"""
        for task, prices in new_prices.items():
            if task in self.materials:
                self.materials[task].update(prices)
    
    def get_base_cost(self, task: str) -> float:
        """Get base cost for a specific task"""
        if task not in self.materials:
            return 0.0
        
        task_materials = self.materials[task]
        
        if task == 'tiles':
            return task_materials['base_cost_per_m2']
        elif task == 'painting':
            return task_materials['base_cost_per_m2']
        elif task == 'flooring':
            return task_materials['base_cost_per_m2']
        elif task == 'plumbing':
            # Return average plumbing cost
            plumbing_items = [item['base_cost'] for item in task_materials.values() if isinstance(item, dict) and 'base_cost' in item]
            return sum(plumbing_items) / len(plumbing_items) if plumbing_items else 0.0
        elif task == 'vanity':
            return task_materials['base_cost']
        elif task == 'electrical':
            return task_materials['base_cost']
        else:
            return 0.0
    
    def get_material_summary(self) -> Dict[str, Any]:
        """Get summary of all material costs for reporting"""
        summary = {}
        for task, data in self.materials.items():
            if isinstance(data, dict) and 'base_cost' in data:
                summary[task] = {
                    'base_cost': data['base_cost'],
                    'size_factor': data.get('size_factor', 1.0)
                }
            elif isinstance(data, dict) and 'base_cost_per_m2' in data:
                summary[task] = {
                    'base_cost_per_m2': data['base_cost_per_m2'],
                    'size_factor': data.get('size_factor', 1.0)
                }
        
        return summary
    
    def save_materials_to_file(self, filename: str = "data/materials.json") -> str:
        """Save current material database to JSON file"""
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.materials, f, indent=2, ensure_ascii=False)
        
        return filename 