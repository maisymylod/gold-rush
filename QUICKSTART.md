# Goldsmith Connect - Quick Start Guide

## Repository Structure

```
goldsmith-connect/
├── goldsmith_connect/          # Main package
│   ├── __init__.py            # Package initialization
│   ├── candidate.py           # Candidate management
│   ├── client.py             # Client management
│   └── matcher.py            # Matching algorithm
├── tests/                     # Test suite
│   ├── test_candidate.py
│   ├── test_client.py
│   └── test_matcher.py
├── README.md                  # Full documentation
├── example_usage.py          # Example script
├── pyproject.toml           # Modern Python packaging
├── setup.py                 # Setup script
├── requirements.txt         # Dependencies
├── Makefile                # Common tasks
├── LICENSE                 # MIT License
├── MANIFEST.in            # Package manifest
└── .gitignore            # Git ignore rules

```

## Getting Started

### 1. Install the Package

For regular use:
```bash
cd goldsmith-connect
pip install -e .
```

For development (includes testing tools):
```bash
pip install -e ".[dev]"
```

### 2. Run the Example

```bash
python example_usage.py
```

This will demonstrate:
- Creating and managing candidates
- Creating and managing clients
- Finding matches between candidates and clients
- Generating match reports
- Searching capabilities
- Saving/loading databases

### 3. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
make coverage

# Or directly
pytest --cov=goldsmith_connect --cov-report=html
```

### 4. Basic Usage

```python
from goldsmith_connect import Candidate, CandidateDatabase, Client, ClientDatabase, SkillMatcher

# Create databases
candidate_db = CandidateDatabase()
client_db = ClientDatabase()

# Add a candidate
candidate = Candidate(
    name="John Smith",
    email="john@example.com",
    phone="555-0100",
    skills=["soldering", "stone setting"],
    years_experience=5.0
)
candidate_db.add_candidate(candidate)

# Add a client
client = Client(
    company_name="Elegant Jewelers",
    contact_name="Sarah Miller",
    email="sarah@example.com",
    phone="555-2000",
    required_skills=["soldering", "stone setting"]
)
client_db.add_client(client)

# Find matches
matcher = SkillMatcher(candidate_db, client_db)
matches = matcher.find_candidates_for_client(client)

for candidate, score in matches:
    print(f"{candidate.name}: {score}% match")
```

## Key Features

### Candidate Management
- Track skills, experience, certifications
- Manage availability status
- Set hourly rates and location preferences
- Search by skill, experience, or availability

### Client Management
- Track company information and requirements
- Specify required skills and specializations
- Set position types (full-time, contract, freelance)
- Mark urgent positions
- Search by type, location, or urgency

### Smart Matching
- 0-100 scoring system based on:
  - Required skills (40 points)
  - Experience level (30 points)
  - Specializations (20 points)
  - Location match (10 points)
- Generate detailed match reports
- Find top N candidates for any position

### Data Persistence
- Save/load databases as JSON
- Easy backup and restore
- Human-readable format

## Development Tasks

Use the Makefile for common tasks:

```bash
make install-dev    # Install with dev dependencies
make test          # Run tests
make coverage      # Run tests with coverage
make format        # Format code with black
make lint          # Check code with flake8
make type-check    # Type check with mypy
make clean         # Clean build artifacts
make example       # Run example script
```

## Next Steps

1. Review the full README.md for comprehensive documentation
2. Check out example_usage.py for more examples
3. Run the tests to see how everything works
4. Start building your own goldsmith recruitment system!

## Support

For questions or issues:
- Check the README.md for detailed documentation
- Review the example_usage.py script
- Look at the test files for usage patterns
- Open an issue on GitHub (if published)

---

Happy recruiting! 💍
