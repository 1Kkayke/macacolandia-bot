"""Poll/voting system"""

from typing import Dict, List
from datetime import datetime, timedelta


class Poll:
    """Poll/voting object"""
    
    def __init__(self, question: str, options: List[str], creator_id: str, duration_minutes: int = 5):
        self.question = question
        self.options = options
        self.creator_id = creator_id
        self.votes: Dict[str, int] = {}  # user_id -> option_index
        self.created_at = datetime.now()
        self.expires_at = self.created_at + timedelta(minutes=duration_minutes)
    
    def vote(self, user_id: str, option_index: int) -> bool:
        """Cast a vote"""
        if option_index < 0 or option_index >= len(self.options):
            return False
        self.votes[user_id] = option_index
        return True
    
    def get_results(self) -> Dict[str, int]:
        """Get vote counts for each option"""
        results = {i: 0 for i in range(len(self.options))}
        for vote in self.votes.values():
            results[vote] = results.get(vote, 0) + 1
        return results
    
    def is_expired(self) -> bool:
        """Check if poll has expired"""
        return datetime.now() > self.expires_at
    
    def get_total_votes(self) -> int:
        """Get total number of votes"""
        return len(self.votes)
    
    def has_user_voted(self, user_id: str) -> bool:
        """Check if user has already voted"""
        return user_id in self.votes


class PollManager:
    """Manages active polls"""
    
    def __init__(self):
        self.active_polls: Dict[int, Poll] = {}  # message_id -> Poll
        self._next_id = 1
    
    def create_poll(self, question: str, options: List[str], creator_id: str, 
                   duration_minutes: int = 5) -> int:
        """Create a new poll and return its ID"""
        poll_id = self._next_id
        self._next_id += 1
        
        poll = Poll(question, options, creator_id, duration_minutes)
        self.active_polls[poll_id] = poll
        return poll_id
    
    def get_poll(self, poll_id: int) -> Poll:
        """Get a poll by ID"""
        return self.active_polls.get(poll_id)
    
    def close_poll(self, poll_id: int) -> bool:
        """Close and remove a poll"""
        if poll_id in self.active_polls:
            del self.active_polls[poll_id]
            return True
        return False
    
    def cleanup_expired(self):
        """Remove expired polls"""
        expired = [pid for pid, poll in self.active_polls.items() if poll.is_expired()]
        for pid in expired:
            del self.active_polls[pid]
