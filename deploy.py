#!/usr/bin/env python3
"""
Deployment script for Donizo Smart Bathroom Pricing Engine

This script helps with production deployment by:
- Validating system requirements
- Setting up directories and permissions
- Running system tests
- Creating production configuration
- Generating deployment report
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Tuple

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from config import SYSTEM_CONFIG, VALIDATION_RULES, FILE_PATHS
except ImportError:
    print("Error: Could not import configuration. Please check your installation.")
    sys.exit(1)


class DeploymentManager:
    """Manages the deployment process for the pricing engine"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.deployment_log = []
        self.errors = []
        self.warnings = []
        
    def log(self, message: str, level: str = "INFO"):
        """Log a deployment message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        self.deployment_log.append(log_entry)
        print(log_entry)
    
    def log_error(self, message: str):
        """Log an error message"""
        self.log(message, "ERROR")
        self.errors.append(message)
    
    def log_warning(self, message: str):
        """Log a warning message"""
        self.log(message, "WARNING")
        self.warnings.append(message)
    
    def check_python_version(self) -> bool:
        """Check if Python version meets requirements"""
        try:
            version = sys.version_info
            required_version = (3, 8)
            
            if version >= required_version:
                self.log(f"Python version {version.major}.{version.minor}.{version.micro} meets requirements")
                return True
            else:
                self.log_error(f"Python version {version.major}.{version.minor}.{version.micro} does not meet requirements (3.8+)")
                return False
                
        except Exception as e:
            self.log_error(f"Failed to check Python version: {e}")
            return False
    
    def check_dependencies(self) -> bool:
        """Check if all required dependencies are available"""
        try:
            # Check if we can import the main modules
            import pricing_engine
            import pricing_logic.material_db
            import pricing_logic.labor_calc
            import pricing_logic.vat_rules
            import pricing_logic.confidence_scorer
            
            self.log("All required modules imported successfully")
            return True
            
        except ImportError as e:
            self.log_error(f"Failed to import required modules: {e}")
            return False
    
    def create_directories(self) -> bool:
        """Create necessary directories"""
        try:
            directories = [
                FILE_PATHS['output_dir'],
                FILE_PATHS['data_dir'],
                'logs',
                'temp'
            ]
            
            for directory in directories:
                dir_path = self.project_root / directory
                dir_path.mkdir(exist_ok=True)
            self.log(f"Created directory: {directory}")
            
            return True
            
        except Exception as e:
            self.log_error(f"Failed to create directories: {e}")
            return False
    
    def check_data_files(self) -> bool:
        """Check if required data files exist"""
        try:
            required_files = [
                FILE_PATHS['materials_file'],
                FILE_PATHS['price_templates_file']
            ]
            
            missing_files = []
            for file_path in required_files:
                if not (self.project_root / file_path).exists():
                    missing_files.append(file_path)
            
            if missing_files:
                self.log_error(f"Missing required data files: {', '.join(missing_files)}")
                return False
            else:
                self.log("All required data files found")
                return True
                
        except Exception as e:
            self.log_error(f"Failed to check data files: {e}")
            return False
    
    def run_tests(self) -> bool:
        """Run the test suite"""
        try:
            self.log("Running test suite...")
            
            # Run tests using unittest
            result = subprocess.run(
                [sys.executable, '-m', 'unittest', 'tests.test_logic', '-v'],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=60
            )
            
            if result.returncode == 0:
                self.log("All tests passed successfully")
                return True
            else:
                self.log_error(f"Tests failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.log_error("Tests timed out after 60 seconds")
            return False
        except Exception as e:
            self.log_error(f"Failed to run tests: {e}")
            return False
    
    def run_benchmark(self) -> bool:
        """Run the benchmark suite"""
        try:
            self.log("Running benchmark suite...")
            
            result = subprocess.run(
                [sys.executable, 'benchmark.py'],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=30
            )
            
            if result.returncode == 0:
                self.log("Benchmark completed successfully")
                return True
            else:
                self.log_error(f"Benchmark failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.log_error("Benchmark timed out after 30 seconds")
            return False
        except Exception as e:
            self.log_error(f"Failed to run benchmark: {e}")
            return False
    
    def create_production_config(self) -> bool:
        """Create production configuration file"""
        try:
            config = {
                'deployment_info': {
                    'deployed_at': datetime.now().isoformat(),
                    'deployed_by': os.getenv('USER', 'unknown'),
                    'version': SYSTEM_CONFIG['version'],
                    'environment': 'production'
                },
                'system_settings': {
                    'log_level': 'INFO',
                    'max_log_size': '10MB',
                    'backup_count': 5,
                    'timeout': 30
                },
                'performance_settings': {
                    'max_concurrent_quotes': 10,
                    'cache_enabled': True,
                    'cache_size': 100,
                    'cache_ttl': 3600
                }
            }
            
            config_file = self.project_root / 'production_config.json'
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            self.log("Production configuration created")
            return True
            
        except Exception as e:
            self.log_error(f"Failed to create production config: {e}")
            return False
    
    def generate_deployment_report(self) -> Dict[str, Any]:
        """Generate a comprehensive deployment report"""
        try:
            report = {
                'deployment_info': {
                    'timestamp': datetime.now().isoformat(),
                    'version': SYSTEM_CONFIG['version'],
                    'status': 'SUCCESS' if not self.errors else 'FAILED'
                },
                'system_checks': {
                    'python_version': self.check_python_version(),
                    'dependencies': self.check_dependencies(),
                    'directories': self.create_directories(),
                    'data_files': self.check_data_files()
                },
                'testing': {
                    'unit_tests': self.run_tests(),
                    'benchmark': self.run_benchmark()
                },
                'configuration': {
                    'production_config': self.create_production_config()
                },
                'summary': {
                    'total_checks': len(self.deployment_log),
                    'errors': len(self.errors),
                    'warnings': len(self.warnings),
                    'success_rate': ((len(self.deployment_log) - len(self.errors)) / len(self.deployment_log) * 100) if self.deployment_log else 0
                }
            }
            
            # Save report
            report_file = self.project_root / 'deployment_report.json'
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            self.log(f"Deployment report saved to: {report_file}")
            return report
            
        except Exception as e:
            self.log_error(f"Failed to generate deployment report: {e}")
            return {}
    
    def deploy(self) -> bool:
        """Run the complete deployment process"""
        self.log("Starting deployment process...")
        self.log(f"Project root: {self.project_root}")
        self.log(f"Python executable: {sys.executable}")
        
        # Run all deployment steps
        steps = [
            ("Python Version Check", self.check_python_version),
            ("Dependencies Check", self.check_dependencies),
            ("Directory Creation", self.create_directories),
            ("Data Files Check", self.check_data_files),
            ("Unit Tests", self.run_tests),
            ("Benchmark Tests", self.run_benchmark),
            ("Production Config", self.create_production_config)
        ]
        
        for step_name, step_func in steps:
            self.log(f"Running: {step_name}")
            if not step_func():
                self.log_error(f"Deployment failed at: {step_name}")
                return False
        
        # Generate final report
        report = self.generate_deployment_report()
        
        if report.get('deployment_info', {}).get('status') == 'SUCCESS':
            self.log("Deployment completed successfully!")
            return True
        else:
            self.log_error("Deployment completed with errors")
            return False


def main():
    """Main deployment function"""
    print("Donizo Smart Bathroom Pricing Engine - Deployment Script")
    print("=" * 70)
    
    try:
        deployer = DeploymentManager()
        success = deployer.deploy()
        
        print("\n" + "=" * 70)
        if success:
            print("DEPLOYMENT SUCCESSFUL!")
            print("The pricing engine is now ready for production use.")
        else:
            print("DEPLOYMENT FAILED!")
            print("Please check the error messages above and fix any issues.")
        
        print(f"\nSummary:")
        print(f"   Total checks: {len(deployer.deployment_log)}")
        print(f"   Errors: {len(deployer.errors)}")
        print(f"   Warnings: {len(deployer.warnings)}")
        
        if deployer.errors:
            print(f"\nErrors encountered:")
            for error in deployer.errors:
                print(f"   - {error}")
        
        if deployer.warnings:
            print(f"\nWarnings:")
            for warning in deployer.warnings:
                print(f"   - {warning}")
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n\nDeployment interrupted by user")
        return 1
    except Exception as e:
        print(f"\nUnexpected error during deployment: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 