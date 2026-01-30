"""Module for matching candidates with client requirements."""

from typing import List, Tuple
from .candidate import Candidate, CandidateDatabase
from .client import Client, ClientDatabase


class SkillMatcher:
    """Matches candidates with clients based on requirements."""
    
    def __init__(
        self, 
        candidate_db: CandidateDatabase, 
        client_db: ClientDatabase
    ):
        self.candidate_db = candidate_db
        self.client_db = client_db
    
    def calculate_match_score(
        self, 
        candidate: Candidate, 
        client: Client
    ) -> float:
        """
        Calculate a match score between a candidate and client.
        
        Returns a score from 0.0 to 100.0, where higher is better.
        """
        score = 0.0
        max_score = 100.0
        
        # Check required skills (40 points max)
        if client.required_skills:
            skills_matched = sum(
                1 for skill in client.required_skills 
                if candidate.has_skill(skill)
            )
            skill_score = (skills_matched / len(client.required_skills)) * 40
            score += skill_score
        else:
            score += 40  # No required skills means full points
        
        # Check experience requirement (30 points max)
        if candidate.years_experience >= client.min_experience_years:
            experience_ratio = min(
                candidate.years_experience / max(client.min_experience_years, 1), 
                2.0
            )
            score += min(experience_ratio * 15, 30)
        else:
            # Partial credit if close
            if client.min_experience_years > 0:
                ratio = candidate.years_experience / client.min_experience_years
                score += ratio * 15
        
        # Check specializations (20 points max)
        if client.preferred_specializations:
            specs_matched = sum(
                1 for spec in client.preferred_specializations
                if spec.lower() in [s.lower() for s in candidate.specializations]
            )
            spec_score = (specs_matched / len(client.preferred_specializations)) * 20
            score += spec_score
        else:
            score += 20  # No preferred specializations means full points
        
        # Location match (10 points max)
        if client.location and candidate.preferred_locations:
            location_match = any(
                client.location.lower() in loc.lower() 
                for loc in candidate.preferred_locations
            )
            if location_match:
                score += 10
        else:
            score += 10  # No location preference means full points
        
        return min(score, max_score)
    
    def find_candidates_for_client(
        self, 
        client: Client, 
        min_score: float = 50.0,
        limit: int = None
    ) -> List[Tuple[Candidate, float]]:
        """
        Find the best matching candidates for a client.
        
        Returns a list of (Candidate, score) tuples, sorted by score (highest first).
        """
        available_candidates = self.candidate_db.search_by_availability("available")
        
        matches = []
        for candidate in available_candidates:
            score = self.calculate_match_score(candidate, client)
            if score >= min_score:
                matches.append((candidate, score))
        
        # Sort by score descending
        matches.sort(key=lambda x: x[1], reverse=True)
        
        if limit:
            matches = matches[:limit]
        
        return matches
    
    def find_clients_for_candidate(
        self, 
        candidate: Candidate, 
        min_score: float = 50.0,
        limit: int = None
    ) -> List[Tuple[Client, float]]:
        """
        Find the best matching clients for a candidate.
        
        Returns a list of (Client, score) tuples, sorted by score (highest first).
        """
        all_clients = self.client_db.get_all_clients()
        
        matches = []
        for client in all_clients:
            score = self.calculate_match_score(candidate, client)
            if score >= min_score:
                matches.append((client, score))
        
        # Sort by score descending, with urgent clients prioritized
        matches.sort(key=lambda x: (x[0].urgent, x[1]), reverse=True)
        
        if limit:
            matches = matches[:limit]
        
        return matches
    
    def get_match_report(
        self, 
        candidate: Candidate, 
        client: Client
    ) -> dict:
        """
        Generate a detailed match report between a candidate and client.
        """
        score = self.calculate_match_score(candidate, client)
        
        # Skills analysis
        required_skills_met = []
        required_skills_missing = []
        
        for skill in client.required_skills:
            if candidate.has_skill(skill):
                required_skills_met.append(skill)
            else:
                required_skills_missing.append(skill)
        
        # Specializations analysis
        specs_matched = [
            spec for spec in client.preferred_specializations
            if spec.lower() in [s.lower() for s in candidate.specializations]
        ]
        
        return {
            "candidate_id": candidate.candidate_id,
            "candidate_name": candidate.name,
            "client_id": client.client_id,
            "client_name": client.company_name,
            "overall_score": round(score, 2),
            "skills_met": required_skills_met,
            "skills_missing": required_skills_missing,
            "specializations_matched": specs_matched,
            "experience_requirement": client.min_experience_years,
            "candidate_experience": candidate.years_experience,
            "experience_met": candidate.years_experience >= client.min_experience_years,
            "recommendation": "Strong match" if score >= 80 else 
                           "Good match" if score >= 60 else 
                           "Possible match" if score >= 40 else 
                           "Weak match"
        }
