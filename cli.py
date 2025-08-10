#!/usr/bin/env python3
"""
Donizo Smart Bathroom Pricing Engine - Command Line Interface

Provides an interactive command-line interface for the pricing engine,
allowing users to generate quotes, run demos, and access system information.
"""

import argparse
import sys
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Configure logging for CLI
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    from pricing_engine import SmartPricingEngine
except ImportError as e:
    logger.error(f"Failed to import pricing engine: {e}")
    print("Error: Could not import pricing engine. Please check your installation.")
    sys.exit(1)


def print_banner():
    """Display the application banner"""
    print("🏠" + "=" * 60 + "🏠")
    print("    Donizo Smart Bathroom Pricing Engine v1.0.0")
    print("    Intelligent pricing for bathroom renovation projects")
    print("🏠" + "=" * 60 + "🏠")


def print_help():
    """Display help information"""
    print("\n📚 Available Commands:")
    print("  quote <transcript>  - Generate quote from transcript")
    print("  interactive         - Enter interactive mode")
    print("  demo               - Run demonstration scenarios")
    print("  info               - Show system information")
    print("  help               - Show this help message")
    print("  version            - Show version information")
    print("\nExamples:")
    print("  python3 cli.py quote '4m² bathroom renovation in Paris'")
    print("  python3 cli.py interactive")
    print("  python3 cli.py demo")


def print_version():
    """Display version information"""
    print("🏠 Donizo Smart Bathroom Pricing Engine")
    print("   Version: 1.0.0")
    print("   Python: 3.8+")
    print("   Status: Production Ready")
    print("   License: Proprietary")


def print_system_info():
    """Display comprehensive system information"""
    try:
        engine = SmartPricingEngine()
        
        print("\nSystem Information")
        print("=" * 50)
        
        # City information
        print(f"📍 Supported Cities: {len(engine.city_multipliers)}")
        for city, multiplier in engine.city_multipliers.items():
            print(f"   {city.title()}: {multiplier}x multiplier")
        
        # Task information
        print(f"\nSupported Tasks: {len(engine.material_db.supported_tasks)}")
        for task in engine.material_db.supported_tasks:
            base_cost = engine.material_db.get_base_cost(task)
            print(f"   {task.title()}: €{base_cost:.2f}/m²")
        
        # VAT information
        print(f"\nVAT Rates:")
        vat_rates = engine.vat_rules.vat_rates
        for rate_type, rate in vat_rates.items():
            print(f"   {rate_type}: {rate:.1f}%")
        
        # Labor rates
        print(f"\nLabor Rates (€/hour):")
        labor_rates = engine.labor_calc.hourly_rates
        for task, rate in labor_rates.items():
            print(f"   {task.title()}: €{rate:.2f}")
        
        print("\nSystem is fully operational and ready for use!")
        
    except Exception as e:
        logger.error(f"Failed to display system info: {e}")
        print(f"Error displaying system information: {e}")


def run_demo():
    """Run demonstration scenarios"""
    try:
        print("\nRunning Demo Scenarios")
        print("=" * 50)
        
        engine = SmartPricingEngine()
        
        # Demo scenarios
        scenarios = [
            {
                'name': 'Small Budget Bathroom',
                'transcript': '3m² bathroom renovation with painting and flooring in Marseille. Budget-conscious.',
                'description': 'Small bathroom with basic renovations'
            },
            {
                'name': 'Luxury Paris Bathroom',
                'transcript': '6m² luxury bathroom renovation with tiles, plumbing, and electrical in Paris. Premium quality.',
                'description': 'Luxury renovation in high-cost area'
            },
            {
                'name': 'Coastal Premium',
                'transcript': '5m² bathroom renovation with tiles, vanity, and painting in Nice. Standard quality.',
                'description': 'Premium coastal location renovation'
            }
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\nDemo {i}: {scenario['name']}")
            print(f"   Description: {scenario['description']}")
            print(f"   Transcript: {scenario['transcript']}")
            
            try:
                quote = engine.generate_quote(scenario['transcript'])
                
                print(f"Quote Generated:")
                print(f"   Quote ID: {quote['quote_id']}")
                print(f"   Final Price: €{quote['pricing_breakdown']['final_price']:,.2f}")
                print(f"   Confidence: {quote['business_metrics']['confidence_score']:.1f}%")
                print(f"   Location: {quote['client_requirements']['location'].title()}")
                print(f"   Tasks: {', '.join(quote['client_requirements']['tasks']).title()}")
                
                # Save demo quote
                output_file = engine.save_quote(quote, f"output/demo_quote_{i}.json")
                print(f"   Saved to: {output_file}")
                
            except Exception as e:
                logger.error(f"Demo {i} failed: {e}")
                print(f"Demo {i} failed: {e}")
        
        print("\nDemo completed successfully!")
        
    except Exception as e:
        logger.error(f"Demo execution failed: {e}")
        print(f"Demo execution failed: {e}")


def interactive_mode():
    """Run interactive mode for quote generation"""
    print("\nInteractive Mode")
    print("=" * 50)
    print("Type 'quit' to exit, 'help' for commands")
    print()
    
    try:
        engine = SmartPricingEngine()
        
        while True:
            try:
                user_input = input("Enter transcript (or command): ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                elif user_input.lower() in ['help', 'h']:
                    print("Commands: quit, help, info, demo, version")
                    print("Or enter a transcript to generate a quote")
                    continue
                elif user_input.lower() in ['info', 'i']:
                    print_system_info()
                    continue
                elif user_input.lower() in ['demo', 'd']:
                    run_demo()
                    continue
                elif user_input.lower() in ['version', 'v']:
                    print_version()
                    continue
                elif not user_input:
                    continue
                
                # Validate input length
                if len(user_input) < 10:
                    print("Please provide more details in your transcript (at least 10 characters)")
                    continue
                
                # Generate quote
                print(f"\nProcessing transcript...")
                quote = engine.generate_quote(user_input)
                
                # Display summary
                print(f"\nQuote Generated!")
                print(f"   Quote ID: {quote['quote_id']}")
                print(f"   Final Price: €{quote['pricing_breakdown']['final_price']:,.2f}")
                print(f"   Confidence: {quote['business_metrics']['confidence_score']:.1f}%")
                print(f"   Location: {quote['client_requirements']['location'].title()}")
                print(f"   Tasks: {', '.join(quote['client_requirements']['tasks']).title()}")
                
                # Ask if user wants to save
                while True:
                    save_choice = input("\nSave quote? (y/n): ").strip().lower()
                    if save_choice in ['y', 'yes', 'n', 'no']:
                        break
                    print("Please enter 'y' or 'n'")
                
                if save_choice in ['y', 'yes']:
                    filename = input("Enter filename (or press Enter for default): ").strip()
                    if not filename:
                        filename = f"output/quote_{quote['quote_id']}.json"
                    else:
                        if not filename.endswith('.json'):
                            filename += '.json'
                        if not filename.startswith('output/'):
                            filename = f"output/{filename}"
                    
                    try:
                        output_file = engine.save_quote(quote, filename)
                        print(f"Quote saved to: {output_file}")
                    except Exception as e:
                        logger.error(f"Failed to save quote: {e}")
                        print(f"Failed to save quote: {e}")
                
                print("\n" + "-"*50 + "\n")
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except ValueError as e:
                print(f"Input Error: {e}")
                print("Please try again with a more detailed transcript\n")
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                print(f"Unexpected Error: {e}")
                print("Please try again or type 'help' for assistance\n")
                
    except Exception as e:
        logger.error(f"Interactive mode initialization failed: {e}")
        print(f"Failed to start interactive mode: {e}")


def generate_quote(transcript: str, save: bool = True) -> Dict[str, Any]:
    """Generate a quote from transcript"""
    try:
        if not transcript or len(transcript.strip()) < 10:
            raise ValueError("Transcript must be at least 10 characters long")
        
        engine = SmartPricingEngine()
        quote = engine.generate_quote(transcript)
        
        if save:
            try:
                output_file = engine.save_quote(quote)
                print(f"Quote saved to: {output_file}")
            except Exception as e:
                logger.error(f"Failed to save quote: {e}")
                print(f"Quote generated but could not be saved: {e}")
        
        return quote
        
    except Exception as e:
        logger.error(f"Quote generation failed: {e}")
        raise


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="Donizo Smart Bathroom Pricing Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s quote '4m² bathroom renovation in Paris'
  %(prog)s interactive
  %(prog)s demo
  %(prog)s info
  %(prog)s version
        """
    )
    
    parser.add_argument(
        'command',
        nargs='?',
        default='help',
        help='Command to execute'
    )
    
    parser.add_argument(
        'transcript',
        nargs='?',
        help='Transcript for quote generation'
    )
    
    parser.add_argument(
        '--no-save',
        action='store_true',
        help='Do not save generated quote to file'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        if args.command == 'quote':
            if not args.transcript:
                print("Error: Transcript required for quote command")
                print("Usage: python3 cli.py quote 'your transcript here'")
                sys.exit(1)
            
            print_banner()
            print(f"Generating quote for transcript...")
            
            quote = generate_quote(args.transcript, save=not args.no_save)
            
            print(f"\nQuote Generated!")
            print(f"   Quote ID: {quote['quote_id']}")
            print(f"   Final Price: €{quote['pricing_breakdown']['final_price']:,.2f}")
            print(f"   Confidence: {quote['business_metrics']['confidence_score']:.1f}%")
            
        elif args.command == 'interactive':
            print_banner()
            interactive_mode()
            
        elif args.command == 'demo':
            print_banner()
            run_demo()
            
        elif args.command == 'info':
            print_banner()
            print_system_info()
            
        elif args.command == 'version':
            print_version()
            
        elif args.command == 'help':
            print_banner()
            print_help()
            
        else:
            print(f"Unknown command: {args.command}")
            print_help()
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        logger.error(f"CLI execution failed: {e}")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 