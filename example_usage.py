"""
Example usage of the goldsmith-connect library.

This script demonstrates the basic functionality of the library including
adding candidates and clients, searching, and matching.
"""

from goldsmith_connect import (
    Candidate, CandidateDatabase,
    Client, ClientDatabase,
    SkillMatcher
)


def main():
    print("=== Goldsmith Connect Example ===\n")
    
    # Create databases
    candidate_db = CandidateDatabase()
    client_db = ClientDatabase()
    
    # Add some candidates
    print("Adding candidates...")
    
    candidates_data = [
        {
            "name": "Emily Chen",
            "email": "emily.chen@example.com",
            "phone": "555-0101",
            "skills": ["soldering", "stone setting", "engraving", "CAD design"],
            "years_experience": 8.0,
            "specializations": ["engagement rings", "custom design"],
            "certifications": ["GIA Graduate Gemologist"],
            "hourly_rate": 50.0,
            "preferred_locations": ["New York, NY", "Brooklyn, NY"]
        },
        {
            "name": "Marcus Johnson",
            "email": "marcus.j@example.com",
            "phone": "555-0102",
            "skills": ["casting", "finishing", "polishing", "wax carving"],
            "years_experience": 5.0,
            "specializations": ["manufacturing", "production"],
            "certifications": [],
            "hourly_rate": 40.0,
            "preferred_locations": ["Los Angeles, CA"]
        },
        {
            "name": "Sofia Rodriguez",
            "email": "sofia.r@example.com",
            "phone": "555-0103",
            "skills": ["antique restoration", "repair", "stone setting", "engraving"],
            "years_experience": 12.0,
            "specializations": ["antique restoration", "vintage pieces"],
            "certifications": ["Certified Master Jeweler"],
            "hourly_rate": 65.0,
            "preferred_locations": ["Boston, MA", "Providence, RI"]
        },
        {
            "name": "David Kim",
            "email": "david.kim@example.com",
            "phone": "555-0104",
            "skills": ["3D printing", "CAD design", "prototyping", "soldering"],
            "years_experience": 3.0,
            "specializations": ["modern design", "rapid prototyping"],
            "certifications": [],
            "hourly_rate": 35.0,
            "preferred_locations": ["San Francisco, CA", "San Jose, CA"]
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
            "company_name": "Elegant Jewelers",
            "contact_name": "Sarah Miller",
            "email": "sarah@elegantjewelers.com",
            "phone": "555-2001",
            "client_type": "jewelry_store",
            "required_skills": ["stone setting", "engraving", "repair"],
            "preferred_specializations": ["custom design"],
            "location": "New York, NY",
            "position_type": "full_time",
            "min_experience_years": 5.0,
            "urgent": False
        },
        {
            "company_name": "Heritage Restorations",
            "contact_name": "Robert Thompson",
            "email": "robert@heritagerest.com",
            "phone": "555-2002",
            "client_type": "repair_shop",
            "required_skills": ["antique restoration", "repair", "stone setting"],
            "preferred_specializations": ["antique restoration", "vintage pieces"],
            "location": "Boston, MA",
            "position_type": "contract",
            "min_experience_years": 8.0,
            "urgent": True
        },
        {
            "company_name": "ModernLux Designs",
            "contact_name": "Jennifer Lee",
            "email": "jennifer@modernlux.com",
            "phone": "555-2003",
            "client_type": "independent_designer",
            "required_skills": ["CAD design", "3D printing", "prototyping"],
            "preferred_specializations": ["modern design"],
            "location": "San Francisco, CA",
            "position_type": "freelance",
            "min_experience_years": 2.0,
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
    
    # Example 1: Find candidates for Heritage Restorations
    print("=" * 60)
    print("Example 1: Finding candidates for Heritage Restorations")
    print("=" * 60)
    
    heritage = client_db.get_client("CLI-0002")
    print(f"\nClient: {heritage.company_name}")
    print(f"Required Skills: {', '.join(heritage.required_skills)}")
    print(f"Min Experience: {heritage.min_experience_years} years")
    print(f"Urgent: {heritage.urgent}\n")
    
    matches = matcher.find_candidates_for_client(heritage, min_score=50.0)
    
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
        report = matcher.get_match_report(best_candidate, heritage)
        
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
    
    print("\nCandidates with 'CAD design' skill:")
    cad_candidates = candidate_db.search_by_skill("CAD design")
    for c in cad_candidates:
        print(f"  - {c.name}")
    
    print("\nCandidates with 7+ years experience:")
    experienced = candidate_db.search_by_experience(7.0)
    for c in experienced:
        print(f"  - {c.name} ({c.years_experience} years)")
    
    print("\nUrgent clients:")
    urgent = client_db.search_urgent()
    for c in urgent:
        print(f"  - {c.company_name}")
    
    # Example 4: Find opportunities for a candidate
    print("\n" + "=" * 60)
    print("Example 4: Finding Opportunities for a Candidate")
    print("=" * 60)
    
    emily = candidate_db.get_candidate("CAND-0001")
    print(f"\nCandidate: {emily.name}")
    print(f"Skills: {', '.join(emily.skills)}")
    print(f"Experience: {emily.years_experience} years\n")
    
    opportunities = matcher.find_clients_for_candidate(emily, min_score=50.0)
    
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
