"""Module for managing goldsmith candidates."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime
import json


@dataclass
class Candidate:
    """Represents a goldsmith candidate."""
    
    name: str
    email: str
    phone: str
    skills: List[str] = field(default_factory=list)
    years_experience: float = 0.0
    specializations: List[str] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    portfolio_url: Optional[str] = None
    availability: str = "available"  # available, placed, unavailable
    hourly_rate: Optional[float] = None
    preferred_locations: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    candidate_id: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert candidate to dictionary."""
        return {
            "candidate_id": self.candidate_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "skills": self.skills,
            "years_experience": self.years_experience,
            "specializations": self.specializations,
            "certifications": self.certifications,
            "portfolio_url": self.portfolio_url,
            "availability": self.availability,
            "hourly_rate": self.hourly_rate,
            "preferred_locations": self.preferred_locations,
            "created_at": self.created_at.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Candidate":
        """Create candidate from dictionary."""
        data = data.copy()
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        return cls(**data)
    
    def has_skill(self, skill: str) -> bool:
        """Check if candidate has a specific skill."""
        return skill.lower() in [s.lower() for s in self.skills]
    
    def matches_requirements(
        self, 
        required_skills: List[str] = None,
        min_experience: float = 0,
        required_specializations: List[str] = None
    ) -> bool:
        """Check if candidate meets job requirements."""
        if required_skills:
            for skill in required_skills:
                if not self.has_skill(skill):
                    return False
        
        if self.years_experience < min_experience:
            return False
        
        if required_specializations:
            candidate_specs = [s.lower() for s in self.specializations]
            for spec in required_specializations:
                if spec.lower() not in candidate_specs:
                    return False
        
        return True


class CandidateDatabase:
    """Manages a collection of goldsmith candidates."""
    
    def __init__(self):
        self.candidates: Dict[str, Candidate] = {}
        self._next_id = 1
    
    def add_candidate(self, candidate: Candidate) -> str:
        """Add a candidate to the database."""
        if candidate.candidate_id is None:
            candidate.candidate_id = f"CAND-{self._next_id:04d}"
            self._next_id += 1
        
        self.candidates[candidate.candidate_id] = candidate
        return candidate.candidate_id
    
    def get_candidate(self, candidate_id: str) -> Optional[Candidate]:
        """Retrieve a candidate by ID."""
        return self.candidates.get(candidate_id)
    
    def remove_candidate(self, candidate_id: str) -> bool:
        """Remove a candidate from the database."""
        if candidate_id in self.candidates:
            del self.candidates[candidate_id]
            return True
        return False
    
    def search_by_skill(self, skill: str) -> List[Candidate]:
        """Find all candidates with a specific skill."""
        return [c for c in self.candidates.values() if c.has_skill(skill)]
    
    def search_by_availability(self, availability: str = "available") -> List[Candidate]:
        """Find all candidates with a specific availability status."""
        return [c for c in self.candidates.values() if c.availability == availability]
    
    def search_by_experience(self, min_years: float) -> List[Candidate]:
        """Find all candidates with at least the specified years of experience."""
        return [c for c in self.candidates.values() if c.years_experience >= min_years]
    
    def find_matches(
        self,
        required_skills: List[str] = None,
        min_experience: float = 0,
        required_specializations: List[str] = None,
        availability: str = "available"
    ) -> List[Candidate]:
        """Find candidates matching specific criteria."""
        matches = []
        for candidate in self.candidates.values():
            if candidate.availability != availability:
                continue
            if candidate.matches_requirements(
                required_skills, min_experience, required_specializations
            ):
                matches.append(candidate)
        return matches
    
    def save_to_file(self, filepath: str):
        """Save database to JSON file."""
        data = {
            "candidates": {
                cid: candidate.to_dict() 
                for cid, candidate in self.candidates.items()
            },
            "next_id": self._next_id
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_from_file(self, filepath: str):
        """Load database from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.candidates = {
            cid: Candidate.from_dict(cdata)
            for cid, cdata in data["candidates"].items()
        }
        self._next_id = data.get("next_id", 1)
    
    def get_all_candidates(self) -> List[Candidate]:
        """Return all candidates."""
        return list(self.candidates.values())
    
    def count(self) -> int:
        """Return the total number of candidates."""
        return len(self.candidates)
