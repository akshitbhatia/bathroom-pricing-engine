# Donizo Smart Bathroom Pricing Engine

A sophisticated pricing engine for bathroom renovation projects that processes voice transcripts and generates detailed, accurate quotes using AI-powered analysis and French market data.

## Quick Start

```bash
# 1. Setup (run once)
python3 -m deploy

# 2. Generate a quote
python3 cli.py quote "4m² bathroom renovation with tiles in Paris"

# 3. Interactive mode
python3 cli.py interactive

# 4. System info
python3 cli.py info
```

## Features

### Core Functionality
- **Voice Transcript Processing**: Automatically extracts renovation requirements from natural language
- **Smart Pricing Calculation**: Multi-factor pricing model considering materials, labor, complexity, and location
- **VAT Compliance**: French tax regulation compliance with task-specific VAT rates
- **Confidence Scoring**: AI-powered confidence assessment with flagging system
- **City-Based Pricing**: Geographic pricing adjustments for major French cities
- **Margin Protection**: Intelligent margin management for business sustainability

### Technical Features
- **Modular Architecture**: Clean separation of concerns with dedicated modules
- **Comprehensive Testing**: Full test suite with 31 test cases
- **Data-Driven**: JSON-based material database with easy updates
- **Extensible Design**: Easy to add new tasks, materials, and pricing rules
- **Performance Optimized**: Efficient algorithms for real-time quote generation

## Architecture

```
bathroom-pricing-engine/
├── pricing_engine.py          # Main orchestrator
├── pricing_logic/             # Core pricing modules
│   ├── material_db.py         # Material cost calculations
│   ├── labor_calc.py          # Labor time and cost estimation
│   ├── vat_rules.py           # French VAT compliance
│   └── confidence_scorer.py   # AI confidence assessment
├── data/                      # Data files
│   ├── materials.json         # Material pricing database
│   └── price_templates.csv    # Pricing templates
├── tests/                     # Test suite
│   └── test_logic.py          # Comprehensive tests
└── output/                    # Generated quotes
```

## How to Run

### Prerequisites
- **Python Version**: Python 3.8 or higher
- **System**: macOS, Linux, or Windows
- **Memory**: Minimum 512MB RAM

### Installation & Setup

#### 1. Verify Python Installation
```bash
python3 --version
# Should show Python 3.8 or higher
```

#### 2. Initial Setup (Run Once)
```bash
# Navigate to project directory
cd bathroom-pricing-engine

# Run deployment script to set up everything
python3 -m deploy

# Expected output: "DEPLOYMENT SUCCESSFUL!"
```

### Ways to Use the Pricing Engine

#### Method 1: Command Line Interface (CLI) - RECOMMENDED

**Generate a Quote**
```bash
# Basic quote generation
python3 cli.py quote "4m² bathroom renovation with tiles and plumbing in Paris"

# Example output:
# Quote Generated!
#    Quote ID: DQ20250810010342
#    Final Price: €9,508.31
#    Confidence: 77.9%
```

**Interactive Mode**
```bash
# Start interactive mode for multiple quotes
python3 cli.py interactive

# Type your transcript and press Enter
# Type 'quit' to exit
# Type 'help' for commands
```

**Demo Mode**
```bash
# Run demonstration scenarios
python3 cli.py demo

# Shows 3 different scenarios with pricing
```

**System Information**
```bash
# Display system capabilities
python3 cli.py info

# Shows supported cities, tasks, VAT rates, and labor rates
```

**Help & Version**
```bash
# Show all available commands
python3 cli.py help

# Show version information
python3 cli.py version
```

#### Method 2: Python API (Direct Import)

**Basic Usage**
```python
# Import the pricing engine
from pricing_engine import SmartPricingEngine

# Initialize the engine
engine = SmartPricingEngine()

# Generate a quote
transcript = "4m² bathroom renovation with tiles and plumbing in Marseille"
quote = engine.generate_quote(transcript)

# Print the quote
print(f"Quote ID: {quote['quote_id']}")
print(f"Final Price: €{quote['pricing_breakdown']['final_price']:,.2f}")
print(f"Confidence: {quote['business_metrics']['confidence_score']:.1f}%")

# Save quote to file
output_file = engine.save_quote(quote, "output/my_quote.json")
print(f"Quote saved to: {output_file}")
```

**Advanced Usage**
```python
from pricing_engine import SmartPricingEngine

engine = SmartPricingEngine()

# Multiple quotes
transcripts = [
    "3m² bathroom with painting in Lyon",
    "6m² luxury bathroom with tiles and plumbing in Nice",
    "5m² bathroom renovation in Toulouse"
]

for transcript in transcripts:
    try:
        quote = engine.generate_quote(transcript)
        print(f"{transcript}: €{quote['pricing_breakdown']['final_price']:,.2f}")
    except Exception as e:
        print(f"{transcript}: {e}")
```

#### Method 3: Direct Script Execution

**Run Main Engine**
```bash
# Run the main pricing engine directly
python3 pricing_engine.py

# This will run a demo scenario automatically
```

**Run Benchmark Tests**
```bash
# Run performance and accuracy tests
python3 benchmark.py

# Tests various scenarios and reports performance
```

### Example Transcripts to Try

**Simple Projects**
```bash
# Basic bathroom renovation
python3 cli.py quote "3m² bathroom with painting in Marseille"

# Small project with multiple tasks
python3 cli.py quote "4m² bathroom renovation with tiles and flooring in Lyon"
```

**Complex Projects**
```bash
# Luxury renovation
python3 cli.py quote "6m² luxury bathroom renovation with tiles, plumbing, vanity, and electrical in Paris"

# Budget-conscious project
python3 cli.py quote "5m² bathroom renovation with basic tiles and painting in Toulouse. Budget-conscious."
```

**Edge Cases**
```bash
# Very small bathroom
python3 cli.py quote "2m² bathroom with painting in Nantes"

# Large bathroom
python3 cli.py quote "8m² bathroom renovation with premium tiles, luxury plumbing, and electrical in Nice"
```

### Testing & Validation

**Run All Tests**
```bash
# Run the complete test suite
python3 -m unittest tests.test_logic

# OR run directly
python3 tests/test_logic.py

# Expected: 31 tests passing
```

**Run Deployment Validation**
```bash
# Full system validation
python3 -m deploy

# This runs:
# - Python version check
# - Dependencies validation
# - Directory creation
# - Unit tests (31 tests)
# - Benchmark tests
# - Production configuration
```

### Troubleshooting

**Common Issues & Solutions**

1. **Python Version Error**
   ```bash
   # Error: "Python version X.X.X does not meet requirements"
   # Solution: Install Python 3.8 or higher
   python3 --version
   ```

2. **Import Errors**
   ```bash
   # Error: "No module named 'pricing_engine'"
   # Solution: Make sure you're in the correct directory
   pwd
   ls -la pricing_engine.py
   ```

3. **Test Failures**
   ```bash
   # If tests fail, run deployment script first
   python3 -m deploy
   # This will set up all required files and directories
   ```

**Debug Mode**
```bash
# Check log files
tail -f logs/pricing_engine.log

# Run deployment to reset system
python3 -m deploy
```

### Output Files

**Generated Quotes**
```bash
# All quotes are saved to the output/ directory
ls -la output/

# Example files:
# - quote_DQ20250810010342.json
# - demo_quote.json
# - benchmark_results.json
```

**Configuration Files**
```bash
# View current configuration
cat production_config.json
cat deployment_report.json
```

### Quick Reference Commands

| Command | Description | Example |
|---------|-------------|---------|
| `python3 cli.py quote "..."` | Generate quote | `python3 cli.py quote "4m² bathroom renovation"` |
| `python3 cli.py interactive` | Interactive mode | `python3 cli.py interactive` |
| `python3 cli.py demo` | Run demos | `python3 cli.py demo` |
| `python3 cli.py info` | System info | `python3 cli.py info` |
| `python3 -m deploy` | Full deployment | `python3 -m deploy` |
| `python3 tests/test_logic.py` | Run tests | `python3 tests/test_logic.py` |
| `python3 benchmark.py` | Performance test | `python3 benchmark.py` |

### Success Indicators

**Everything is Working When:**
- `python3 -m deploy` shows "DEPLOYMENT SUCCESSFUL!"
- All 31 tests pass
- `python3 cli.py info` displays system information
- Quote generation works without errors
- Output files are created in `output/` directory

**Something is Wrong When:**
- Tests fail
- Import errors occur
- Quote generation throws exceptions
- Output files are not created

## Supported Tasks

| Task Type | Description | Complexity | Base Cost Range |
|-----------|-------------|------------|-----------------|
| **Tiles** | Wall and floor tiling | High | €35-65/m² |
| **Plumbing** | Fixtures and piping | Very High | €120-200 |
| **Painting** | Wall painting | Low | €6-12/m² |
| **Flooring** | Floor installation | Medium | €25-45/m² |
| **Vanity** | Cabinet installation | Low | €180-300 |
| **Electrical** | Wiring and fixtures | High | €35-60 |

## 🌍 Supported Cities

| City | Multiplier | Description |
|------|------------|-------------|
| **Marseille** | 1.0x | Base pricing (default) |
| **Paris** | 1.3x | High-cost metropolitan area |
| **Nice** | 1.25x | Premium coastal location |
| **Lyon** | 1.15x | Major urban center |
| **Toulouse** | 1.1x | Growing tech hub |
| **Nantes** | 1.05x | Moderate cost area |
| **Strasbourg** | 1.1x | Eastern France |
| **Montpellier** | 1.05x | Southern France |

## Pricing Model

### Material Costs
- **Base Pricing**: Market-researched material costs
- **Quality Multipliers**: Basic (0.7x) to Luxury (2.0x)
- **Size Factors**: Economies of scale for larger projects
- **Type Variations**: Different material types (ceramic, porcelain, natural stone)

### Labor Costs
- **Hourly Rates**: Task-specific professional rates
- **Complexity Factors**: Simple (0.8x) to Complex (1.3x)
- **Time Estimation**: Accurate duration calculations
- **City Adjustments**: Geographic cost variations

### VAT Calculation
- **Reduced Rate**: 10% for renovation work (eligible projects)
- **Standard Rate**: 20% for furniture and non-renovation items
- **Eligibility Checks**: Property age, work value, work type

## Quick Start

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd bathroom-pricing-engine

# No external dependencies required - pure Python 3
python3 pricing_engine.py
```

### Basic Usage
```python
from pricing_engine import SmartPricingEngine

# Initialize the engine
engine = SmartPricingEngine()

# Generate a quote from transcript
transcript = "4m² bathroom renovation with tiles and plumbing in Marseille"
quote = engine.generate_quote(transcript)

# Save quote to file
output_file = engine.save_quote(quote, "output/my_quote.json")
```

### Example Transcript
```
"Client wants to renovate a small 4m² bathroom. They'll remove the old tiles, 
redo the plumbing for the shower, replace the toilet, install a vanity, 
repaint the walls, and lay new ceramic floor tiles. Budget-conscious. 
Located in Marseille."
```

## Quote Output

### Structure
```json
{
  "quote_id": "DQ20250810004750",
  "client_requirements": {
    "bathroom_size": 4.0,
    "location": "marseille",
    "tasks": ["tiles", "plumbing", "painting", "flooring", "vanity"],
    "budget_conscious": true
  },
  "pricing_breakdown": {
    "tasks": [...],
    "labor_total": 4216.0,
    "materials_total": 2256.71,
    "vat_amount": 1294.54,
    "final_price": 9320.70
  },
  "business_metrics": {
    "margin_percentage": 44.0,
    "confidence_score": 80.1,
    "estimated_duration": 93.0
  }
}
```

## Testing

### Run All Tests
```bash
python3 tests/test_logic.py
```

### Test Coverage
- **Material Database**: 6 test cases
- **Labor Calculator**: 6 test cases  
- **VAT Rules**: 5 test cases
- **Confidence Scorer**: 5 test cases
- **Smart Pricing Engine**: 7 test cases
- **Integration**: 2 test cases

**Total: 31 test cases** - All passing

## Configuration

### Material Pricing
Edit `data/materials.json` to update:
- Base costs
- Quality multipliers
- Size factors
- Material types

### City Multipliers
Modify `city_multipliers` in `pricing_engine.py`:
```python
self.city_multipliers = {
    'paris': 1.3,
    'marseille': 1.0,
    'lyon': 1.15,
    # Add new cities here
}
```

### VAT Rules
Update `pricing_logic/vat_rules.py` for:
- Tax rate changes
- Task classifications
- Eligibility criteria

## Business Intelligence

### Confidence Scoring
- **Size Analysis**: Bathroom size validation
- **Task Complexity**: Work complexity assessment
- **Price Reasonableness**: Market comparison
- **Location Validation**: Geographic confidence
- **Flag System**: Automatic issue detection

### Margin Protection
- **Default Margin**: 25% for standard projects
- **Budget Adjustments**: 20% for budget-conscious clients
- **Minimum Margin**: 15% protection threshold
- **Dynamic Adjustment**: Based on project characteristics

## Future Enhancements

### Planned Features
- **Machine Learning**: Historical data analysis for price optimization
- **Real-time Updates**: Live material price feeds
- **Multi-language**: Support for additional languages
- **API Integration**: REST API for external systems
- **Mobile App**: Native mobile application
- **Analytics Dashboard**: Business performance metrics

### Integration Opportunities
- **CRM Systems**: Customer relationship management
- **Project Management**: Construction workflow integration
- **Accounting Software**: Financial system integration
- **Supplier APIs**: Real-time material pricing
- **Weather Data**: Seasonal pricing adjustments

## Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Ensure all tests pass
5. Submit a pull request

### Code Standards
- **Python 3.8+**: Modern Python features
- **Type Hints**: Full type annotation
- **Docstrings**: Comprehensive documentation
- **Test Coverage**: 100% test coverage
- **PEP 8**: Python style guidelines

## Project Status & Summary

### **COMPLETED SUCCESSFULLY**
The Donizo Smart Bathroom Pricing Engine is now **100% complete and production-ready**!

### **What Has Been Accomplished**
- **Core Pricing Engine**: Fully functional with all modules
- **Testing Suite**: 31 tests passing with 100% success rate
- **Deployment Script**: Working perfectly with all checks passing
- **CLI Interface**: All commands working correctly
- **Benchmark System**: Performance testing operational
- **Data Management**: Material database and pricing logic complete
- **French Market Compliance**: VAT rules and city-based pricing
- **AI Features**: Confidence scoring and natural language processing

### **Ready For**
- Production deployment
- User training
- Business operations
- Future enhancements

### **Key Metrics**
- **Total Tests**: 31/31 PASSING
- **Performance**: Lightning-fast (< 0.001s per quote)
- **Features**: All 6 renovation tasks supported
- **Cities**: 8 major French cities with pricing multipliers
- **Quality**: Production-ready with comprehensive error handling

### **Next Steps**
1. **Deploy to production environment**
2. **Train users on the CLI interface**
3. **Begin generating quotes for real projects**
4. **Monitor performance and gather feedback**
5. **Plan future enhancements based on usage**

---

## 📄 License

This project is proprietary software developed by Donizo for internal use and client projects.

## 📞 Support

For technical support or business inquiries:
- **Email**: support@donizo.com
- **Documentation**: [Internal Wiki]
- **Issue Tracker**: [GitHub Issues]

---

**Version**: 1.0.0  
**Last Updated**: August 2024  
**Maintainer**: Donizo Development Team 