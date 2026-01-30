"""
Example usage of the goldsmith-connect library.

This script demonstrates the basic functionality of the library including
adding executive candidates and clients, searching, and matching for
Goldsmith & Co's asset management executive search practice.
"""

from goldsmith_connect import (
    Candidate, CandidateDatabase,
    Client, ClientDatabase,
    SkillMatcher
)


def main():
    print("=== Goldsmith Connect - Executive Search System ===\n")
    
    # Create databases
    candidate_db = CandidateDatabase()
    client_db = ClientDatabase()
    
    # Add some candidates
    print("Adding executive candidates...")
    
    candidates_data = [
        {
            "name": "Sarah Chen",
            "email": "sarah.chen@example.com",
            "phone": "555-0101",
            "skills": ["Portfolio Management", "Risk Analysis", "Client Relations", "Team Leadership"],
            "years_experience": 15.0,
            "specializations": ["Fixed Income", "Multi-Asset Strategies"],
            "certifications": ["CFA Charter", "MBA - Wharton"],
            "hourly_rate": 500.0,
            "preferred_locations": ["New York, NY", "Greenwich, CT"]
        },
        {
            "name": "Michael Rodriguez",
            "email": "michael.r@example.com",
            "phone": "555-0102",
            "skills": ["Quantitative Analysis", "Algorithmic Trading", "Python", "R"],
            "years_experience": 8.0,
            "specializations": ["Systematic Strategies", "Factor Investing"],
            "certifications": ["PhD - MIT", "CFA Level III"],
            "hourly_rate": 450.0,
            "preferred_locations": ["Boston, MA", "Chicago, IL"]
        },
        {
            "name": "Jennifer Park",
            "email": "jennifer.p@example.com",
            "phone": "555-0103",
            "skills": ["Private Equity", "Due Diligence", "Deal Structuring", "Portfolio Monitoring"],
            "years_experience": 12.0,
            "specializations": ["Middle Market Buyouts", "Growth Equity"],
            "certifications": ["MBA - Harvard", "CPA"],
            "hourly_rate": 550.0,
            "preferred_locations": ["San Francisco, CA", "Menlo Park, CA"]
        },
        {
            "name": "David Thompson",
            "email": "david.t@example.com",
            "phone": "555-0104",
            "skills": ["Credit Analysis", "High Yield", "Distressed Debt", "Restructuring"],
            "years_experience": 10.0,
            "specializations": ["Corporate Credit", "Special Situations"],
            "certifications": ["CFA Charter", "MBA - Columbia"],
            "hourly_rate": 475.0,
            "preferred_locations": ["New York, NY", "London, UK"]
        }
    ]
    
    for data in candidates_data:
        candidate = Candidate(**data)
        cid = candidate_db.add_candidate(candidate)
        print(f"  Added: {candidate.name} (ID: {cid})")
    
    print(f"\nTotal candidates: {candidate_db.count()}\n")
    
    # Add some clients
    print("Adding clients...")
    
    clients_data = [
        {
            "company_name": "Atlas Capital Management",
            "contact_name": "Robert Morrison",
            "email": "rmorrison@atlascapital.com",
            "phone": "555-2001",
            "client_type": "asset_manager",
            "required_skills": ["Portfolio Management", "Risk Analysis", "Client Relations"],
            "preferred_specializations": ["Fixed Income", "Multi-Asset Strategies"],
            "location": "New York, NY",
            "position_type": "full_time",
            "min_experience_years": 10.0,
            "urgent": False
        },
        {
            "company_name": "Vertex Quantitative Partners",
            "contact_name": "Lisa Zhang",
            "email": "lzhang@vertexquant.com",
            "phone": "555-2002",
            "client_type": "hedge_fund",
            "required_skills": ["Quantitative Analysis", "Algorithmic Trading", "Python"],
            "preferred_specializations": ["Systematic Strategies", "Factor Investing"],
            "location": "Boston, MA",
            "position_type": "full_time",
            "min_experience_years": 5.0,
            "urgent": True
        },
        {
            "company_name": "Summit Growth Equity",
            "contact_name": "James Mitchell",
            "email": "jmitchell@summitgrowth.com",
            "phone": "555-2003",
            "client_type": "private_equity",
            "required_skills": ["Private Equity", "Due Diligence", "Deal Structuring"],
            "preferred_specializations": ["Growth Equity", "Technology"],
            "location": "San Francisco, CA",
            "position_type": "full_time",
            "min_experience_years": 8.0,
            "urgent": False
        }
    ]
    
    for data in clients_data:
        client = Client(**data)
        cid = client_db.add_client(client)
        print(f"  Added: {client.company_name} (ID: {cid})")
    
    print(f"\nTotal clients: {client_db.count()}\n")
    
    # Create matcher
    matcher = SkillMatcher(candidate_db, client_db)
    
    # Example 1: Find candidates for Vertex Quantitative Partners
    print("=" * 60)
    print("Example 1: Finding candidates for Vertex Quantitative Partners")
    print("=" * 60)
    
    vertex = client_db.get_client("CLI-0002")
    print(f"\nClient: {vertex.company_name}")
    print(f"Required Skills: {', '.join(vertex.required_skills)}")
    print(f"Min Experience: {vertex.min_experience_years} years")
    print(f"Urgent: {vertex.urgent}\n")
    
    matches = matcher.find_candidates_for_client(vertex, min_score=50.0)
    
    print(f"Found {len(matches)} matching candidates:\n")
    for candidate, score in matches:
        print(f"  {candidate.name}")
        print(f"    Match Score: {score:.1f}%")
        print(f"    Experience: {candidate.years_experience} years")
        print(f"    Skills: {', '.join(candidate.skills[:3])}...")
        print(f"    Location: {', '.join(candidate.preferred_locations)}")
        print()
    
    # Example 2: Detailed match report
    if matches:
        print("=" * 60)
        print("Example 2: Detailed Match Report")
        print("=" * 60)
        
        best_candidate = matches[0][0]
        report = matcher.get_match_report(best_candidate, vertex)
        
        print(f"\nCandidate: {report['candidate_name']}")
        print(f"Client: {report['client_name']}")
        print(f"\nOverall Score: {report['overall_score']}%")
        print(f"Recommendation: {report['recommendation']}")
        print(f"\nSkills Met: {', '.join(report['skills_met'])}")
        if report['skills_missing']:
            print(f"Skills Missing: {', '.join(report['skills_missing'])}")
        print(f"\nExperience Required: {report['experience_requirement']} years")
        print(f"Candidate Experience: {report['candidate_experience']} years")
        print(f"Experience Requirement Met: {report['experience_met']}")
        
        if report['specializations_matched']:
            print(f"\nMatching Specializations: {', '.join(report['specializations_matched'])}")
    
    # Example 3: Search capabilities
    print("\n" + "=" * 60)
    print("Example 3: Search Capabilities")
    print("=" * 60)
    
    print("\nCandidates with 'Portfolio Management' skill:")
    pm_candidates = candidate_db.search_by_skill("Portfolio Management")
    for c in pm_candidates:
        print(f"  - {c.name}")
    
    print("\nCandidates with 10+ years experience:")
    experienced = candidate_db.search_by_experience(10.0)
    for c in experienced:
        print(f"  - {c.name} ({c.years_experience} years)")
    
    print("\nUrgent client searches:")
    urgent = client_db.search_urgent()
    for c in urgent:
        print(f"  - {c.company_name}")
    
    # Example 4: Find opportunities for a candidate
    print("\n" + "=" * 60)
    print("Example 4: Finding Opportunities for a Candidate")
    print("=" * 60)
    
    sarah = candidate_db.get_candidate("CAND-0001")
    print(f"\nCandidate: {sarah.name}")
    print(f"Skills: {', '.join(sarah.skills)}")
    print(f"Experience: {sarah.years_experience} years\n")
    
    opportunities = matcher.find_clients_for_candidate(sarah, min_score=50.0)
    
    print(f"Found {len(opportunities)} matching opportunities:\n")
    for client, score in opportunities:
        print(f"  {client.company_name}")
        print(f"    Match Score: {score:.1f}%")
        print(f"    Position Type: {client.position_type}")
        print(f"    Location: {client.location}")
        if client.urgent:
            print(f"    ⚠️  URGENT")
        print()
    
    # Save databases
    print("=" * 60)
    print("Saving databases to files...")
    candidate_db.save_to_file("candidates_example.json")
    client_db.save_to_file("clients_example.json")
    print("Databases saved successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
