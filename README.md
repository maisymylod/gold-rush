# Goldsmith Connect

Internal candidate and client management system for Goldsmith & Co - executive search specialists in asset management.

## Overview

Goldsmith Connect is a Python library built to streamline executive search operations. It provides sophisticated candidate tracking, client relationship management, and intelligent matching capabilities tailored for the asset management industry.

## Features

- **Executive Candidate Management**: Track candidates with skills, experience, specializations, and availability
- **Client Relationship Management**: Manage asset management firms and their hiring needs
- **Intelligent Matching**: Automatically match candidates with client requirements using a sophisticated scoring algorithm
- **Persistent Storage**: Save and load databases to/from JSON files
- **Comprehensive Search**: Find candidates and clients based on various criteria
- **Detailed Match Reports**: Generate in-depth analysis of candidate-client fit

## Installation

```bash
pip install goldsmith-connect
```

For development:

```bash
git clone https://github.com/yourusername/goldsmith-connect.git
cd goldsmith-connect
pip install -e ".[dev]"
```

## Quick Start

### Managing Candidates

```python
from goldsmith_connect import Candidate, CandidateDatabase

# Create a database
candidate_db = CandidateDatabase()

# Add a candidate
candidate = Candidate(
    name="Sarah Chen",
    email="sarah.chen@example.com",
    phone="555-0100",
    skills=["Portfolio Management", "Risk Analysis", "Client Relations", "Team Leadership"],
    years_experience=12.0,
    specializations=["Fixed Income", "Multi-Asset Strategies"],
    certifications=["CFA Charter", "MBA - Wharton"],
    hourly_rate=500.0,
    preferred_locations=["New York, NY", "Boston, MA"]
)

candidate_id = candidate_db.add_candidate(candidate)

# Search for candidates
experienced_candidates = candidate_db.search_by_experience(min_years=10.0)
available_candidates = candidate_db.search_by_availability("available")

# Save to file
candidate_db.save_to_file("candidates.json")
```

### Managing Clients

```python
from goldsmith_connect import Client, ClientDatabase

# Create a database
client_db = ClientDatabase()

# Add a client
client = Client(
    company_name="Atlas Capital Management",
    contact_name="Michael Roberts",
    email="mroberts@atlascapital.com",
    phone="555-2000",
    client_type="asset_manager",
    required_skills=["Portfolio Management", "Risk Analysis", "Quantitative Analysis"],
    preferred_specializations=["Fixed Income", "Credit Strategies"],
    location="New York, NY",
    position_type="full_time",
    min_experience_years=10.0,
    urgent=True
)

client_id = client_db.add_client(client)

# Search for clients
urgent_clients = client_db.search_urgent()
ny_clients = client_db.search_by_location("New York")
```

### Matching Candidates with Clients

```python
from goldsmith_connect import SkillMatcher

# Create a matcher
matcher = SkillMatcher(candidate_db, client_db)

# Find candidates for a client
matches = matcher.find_candidates_for_client(
    client, 
    min_score=60.0,  # Minimum match score (0-100)
    limit=5          # Top 5 matches
)

for candidate, score in matches:
    print(f"{candidate.name}: {score:.1f}% match")

# Get a detailed match report
report = matcher.get_match_report(candidate, client)
print(f"Overall Score: {report['overall_score']}")
print(f"Skills Met: {report['skills_met']}")
print(f"Skills Missing: {report['skills_missing']}")
print(f"Recommendation: {report['recommendation']}")
```

## Match Scoring Algorithm

The matching algorithm calculates a score from 0-100 based on:

- **Required Skills (40 points)**: Percentage of required skills the candidate possesses
- **Experience (30 points)**: How well the candidate's experience matches the requirement
- **Specializations (20 points)**: Match between candidate specializations and client preferences
- **Location (10 points)**: Whether candidate's preferred locations match client location

Scores are interpreted as:
- 80-100: Strong match
- 60-79: Good match
- 40-59: Possible match
- 0-39: Weak match

## API Reference

### Candidate

```python
Candidate(
    name: str,
    email: str,
    phone: str,
    skills: List[str] = [],
    years_experience: float = 0.0,
    specializations: List[str] = [],
    certifications: List[str] = [],
    portfolio_url: Optional[str] = None,
    availability: str = "available",
    hourly_rate: Optional[float] = None,
    preferred_locations: List[str] = []
)
```

**Methods:**
- `has_skill(skill: str) -> bool`: Check if candidate has a specific skill
- `matches_requirements(...)`: Check if candidate meets job requirements
- `to_dict()`: Convert to dictionary
- `from_dict(data)`: Create from dictionary

### CandidateDatabase

**Methods:**
- `add_candidate(candidate)`: Add a candidate
- `get_candidate(id)`: Retrieve a candidate
- `remove_candidate(id)`: Remove a candidate
- `search_by_skill(skill)`: Find candidates with a skill
- `search_by_availability(status)`: Find by availability
- `search_by_experience(min_years)`: Find by experience
- `find_matches(...)`: Find matching candidates
- `save_to_file(filepath)`: Save database
- `load_from_file(filepath)`: Load database

### Client

```python
Client(
    company_name: str,
    contact_name: str,
    email: str,
    phone: str,
    client_type: str = "asset_manager",  # asset_manager, hedge_fund, private_equity, family_office
    required_skills: List[str] = [],
    preferred_specializations: List[str] = [],
    location: str = "",
    position_type: str = "full_time",
    min_experience_years: float = 0.0,
    budget_range: Optional[str] = None,
    urgent: bool = False
)
```

### ClientDatabase

**Methods:**
- `add_client(client)`: Add a client
- `get_client(id)`: Retrieve a client
- `remove_client(id)`: Remove a client
- `search_by_type(type)`: Find by client type
- `search_urgent()`: Find urgent clients
- `search_by_location(location)`: Find by location
- `save_to_file(filepath)`: Save database
- `load_from_file(filepath)`: Load database

### SkillMatcher

```python
SkillMatcher(candidate_db, client_db)
```

**Methods:**
- `calculate_match_score(candidate, client)`: Calculate match score (0-100)
- `find_candidates_for_client(client, min_score, limit)`: Find matching candidates
- `find_clients_for_candidate(candidate, min_score, limit)`: Find matching clients
- `get_match_report(candidate, client)`: Generate detailed match report

## Development

### Running Tests

```bash
pytest
```

With coverage:

```bash
pytest --cov=goldsmith_connect --cov-report=html
```

### Code Formatting

```bash
black goldsmith_connect/ tests/
```

### Type Checking

```bash
mypy goldsmith_connect/
```

## License

Proprietary - Copyright © 2026 Goldsmith & Co. For internal use only.

## Support

For issues or questions, contact the development team internally or reach out to info@goldsmithandco.com.
