"""
Configuration file for Donizo Smart Bathroom Pricing Engine

Centralizes all system settings, constants, and configuration values
to make the system easily configurable and maintainable.
"""

import os
from typing import Dict, Any

# System Configuration
SYSTEM_CONFIG = {
    'name': 'Donizo Smart Bathroom Pricing Engine',
    'version': '1.0.0',
    'description': 'Intelligent pricing for bathroom renovation projects',
    'author': 'Donizo Development Team',
    'license': 'Proprietary',
    'python_version': '3.8+',
    'status': 'Production Ready'
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': os.getenv('LOG_LEVEL', 'INFO'),
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': os.getenv('LOG_FILE', None),
    'max_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5
}

# City-based Pricing Multipliers
CITY_MULTIPLIERS = {
    'marseille': 1.0,    # Base pricing
    'paris': 1.3,        # High-cost metropolitan
    'nice': 1.25,        # Premium coastal
    'lyon': 1.15,        # Major urban center
    'toulouse': 1.1,     # Growing tech hub
    'nantes': 1.05,      # Moderate cost
    'strasbourg': 1.1,   # Eastern France
    'montpellier': 1.05  # Southern France
}

# Business Margins
BUSINESS_MARGINS = {
    'default': 0.25,     # 25% default margin
    'budget': 0.15,      # 15% margin for budget projects
    'premium': 0.35,     # 35% margin for premium projects
    'minimum': 0.10      # 10% minimum margin
}

# Validation Rules
VALIDATION_RULES = {
    'min_transcript_length': 10,
    'max_transcript_length': 1000,
    'min_bathroom_size': 1.0,      # m²
    'max_bathroom_size': 50.0,     # m²
    'min_confidence_score': 50.0,  # percentage
    'max_confidence_score': 100.0, # percentage
    'min_price': 100.0,            # euros
    'max_price': 100000.0          # euros
}

# File Paths
FILE_PATHS = {
    'output_dir': 'output',
    'data_dir': 'data',
    'materials_file': 'data/materials.json',
    'price_templates_file': 'data/price_templates.csv',
    'quote_prefix': 'quote_',
    'benchmark_results_file': 'output/benchmark_results.json'
}

# Supported Tasks Configuration
SUPPORTED_TASKS = {
    'tiles': {
        'keywords': ['tiles', 'tile', 'ceramic', 'porcelain'],
        'complexity': 'high',
        'base_cost_range': (35, 65),
        'unit': 'm²'
    },
    'plumbing': {
        'keywords': ['plumbing', 'shower', 'bath', 'sink', 'toilet'],
        'complexity': 'very_high',
        'base_cost_range': (120, 200),
        'unit': 'project'
    },
    'painting': {
        'keywords': ['paint', 'repaint', 'wall'],
        'complexity': 'low',
        'base_cost_range': (6, 12),
        'unit': 'm²'
    },
    'flooring': {
        'keywords': ['floor', 'flooring', 'laying'],
        'complexity': 'medium',
        'base_cost_range': (25, 45),
        'unit': 'm²'
    },
    'vanity': {
        'keywords': ['vanity', 'cabinet', 'storage'],
        'complexity': 'low',
        'base_cost_range': (180, 300),
        'unit': 'unit'
    },
    'electrical': {
        'keywords': ['electrical', 'lighting', 'outlet', 'switch'],
        'complexity': 'high',
        'base_cost_range': (35, 60),
        'unit': 'outlet'
    }
}

# Quality Options
QUALITY_OPTIONS = {
    'basic': {
        'multiplier': 0.7,
        'description': 'Budget-friendly materials',
        'features': ['Standard quality', 'Cost-effective']
    },
    'standard': {
        'multiplier': 1.0,
        'description': 'Default quality materials',
        'features': ['Good quality', 'Balanced cost']
    },
    'premium': {
        'multiplier': 1.4,
        'description': 'Enhanced quality materials',
        'features': ['High quality', 'Premium features']
    },
    'luxury': {
        'multiplier': 2.0,
        'description': 'High-end luxury materials',
        'features': ['Luxury quality', 'Premium finish']
    }
}

# VAT Configuration
VAT_CONFIG = {
    'standard_rate': 0.20,      # 20%
    'reduced_rate': 0.10,       # 10%
    'super_reduced_rate': 0.055, # 5.5%
    'eligible_tasks': ['tiles', 'flooring', 'painting'],
    'property_age_threshold': 2, # years
    'work_value_threshold': 3000 # euros
}

# Performance Configuration
PERFORMANCE_CONFIG = {
    'max_processing_time': 5.0,  # seconds
    'benchmark_timeout': 30.0,   # seconds
    'max_concurrent_quotes': 10,
    'cache_size': 100,
    'cache_ttl': 3600            # seconds
}

# Error Messages
ERROR_MESSAGES = {
    'invalid_transcript': 'Transcript must be a non-empty string with at least {min_length} characters',
    'invalid_size': 'Bathroom size must be between {min_size} and {max_size} m²',
    'no_tasks_detected': 'No renovation tasks detected in transcript',
    'unsupported_location': 'Location "{location}" is not supported',
    'unsupported_task': 'Task "{task}" is not supported',
    'calculation_failed': 'Failed to calculate pricing for task: {task}',
    'save_failed': 'Failed to save quote to file',
    'initialization_failed': 'Failed to initialize pricing engine'
}

# Success Messages
SUCCESS_MESSAGES = {
    'quote_generated': 'Quote generated successfully: {quote_id}',
    'quote_saved': 'Quote saved to: {filename}',
    'engine_initialized': 'Pricing engine initialized successfully',
    'benchmark_completed': 'Benchmark completed successfully'
}

# CLI Configuration
CLI_CONFIG = {
    'banner_width': 60,
    'max_display_width': 80,
            'interactive_prompt': 'Enter transcript (or command): ',
    'help_commands': ['help', 'h', '?'],
    'quit_commands': ['quit', 'exit', 'q'],
    'info_commands': ['info', 'i'],
    'demo_commands': ['demo', 'd'],
    'version_commands': ['version', 'v']
}

# Export all configurations
__all__ = [
    'SYSTEM_CONFIG',
    'LOGGING_CONFIG', 
    'CITY_MULTIPLIERS',
    'BUSINESS_MARGINS',
    'VALIDATION_RULES',
    'FILE_PATHS',
    'SUPPORTED_TASKS',
    'QUALITY_OPTIONS',
    'VAT_CONFIG',
    'PERFORMANCE_CONFIG',
    'ERROR_MESSAGES',
    'SUCCESS_MESSAGES',
    'CLI_CONFIG'
] 