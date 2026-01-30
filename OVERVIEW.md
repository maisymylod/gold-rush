# Goldsmith Connect

**Internal Candidate & Client Management System**  
*Built for Goldsmith & Co - Executive Search in Asset Management*

---

## What is this?

Goldsmith Connect is a Python library designed to streamline Goldsmith & Co's executive search operations. It provides smart tools for tracking candidates, managing client relationships, and intelligently matching talent with opportunities in the asset management industry.

## Key Capabilities

**🎯 Smart Matching**  
Automatically score candidate-client fit on a 0-100 scale based on skills, experience, specializations, and location preferences.

**👥 Candidate Tracking**  
Maintain detailed profiles including skills, certifications, experience, compensation expectations, and availability status.

**🏢 Client Management**  
Track asset managers, hedge funds, private equity firms, and family offices with their specific hiring needs and requirements.

**🔍 Powerful Search**  
Find candidates by skills, experience level, or availability. Filter clients by urgency, location, or firm type.

**📊 Match Reports**  
Generate detailed reports showing exactly how well a candidate aligns with a client's requirements.

**💾 Data Persistence**  
Save and load your entire database as JSON files for easy backup and sharing.

---

## Quick Example

```python
from goldsmith_connect import Candidate, Client, SkillMatcher

# Add a candidate
candidate = Candidate(
    name="Sarah Chen",
    skills=["Portfolio Management", "Risk Analysis"],
    years_experience=15.0,
    specializations=["Fixed Income"]
)

# Add a client
client = Client(
    company_name="Atlas Capital",
    required_skills=["Portfolio Management", "Risk Analysis"],
    min_experience_years=10.0
)

# Find the match score
matcher = SkillMatcher(candidate_db, client_db)
score = matcher.calculate_match_score(candidate, client)
# Returns: 100.0 (perfect match!)
```

---

## When to Use This

- **Building your talent pipeline**: Add promising candidates as you meet them
- **New client engagement**: Record client requirements and immediately see matching candidates
- **Candidate presentation**: Generate match reports to show clients exactly why you're recommending someone
- **Search prioritization**: Quickly identify which candidates to call for urgent roles
- **Team collaboration**: Share databases across the team for coordinated search efforts

---

## Installation

```bash
cd goldsmith-connect
pip install -e .
```

Then run the example to see it in action:
```bash
python example_usage.py
```

---

**For detailed documentation, see [README.md](README.md)**  
**For a quick tutorial, see [QUICKSTART.md](QUICKSTART.md)**

---

*Proprietary software - Copyright © 2026 Goldsmith & Co*
