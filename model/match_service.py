from __future__ import annotations

from .enums import MatchState, PromotingType
from .figure import Figure
from .match import Match

class MatchService:
    def __init__(self):
        self._matches: list[Match] = []
        self._next_id: int = 0

    def create_match(self, player1_name: str, player2_name: str) -> int:
        match: Match = Match(self._next_id, player1_name, player2_name)
        self._matches.append(match)
        self._next_id += 1
        return match.get_id()

    def get_match(self, match_id: int) -> Match | None:
        if match_id < 0:
            return None
        for m in self._matches:
            if m.get_id() == match_id:
                return m
        return None 

    def get_all_matches(self) -> list[int]:
        matches: list[int] = []
        for m in self._matches:
            id = m.get_id()
            matches.append(id)
        return matches
    
    def start(self, match_id: int) -> bool:
        match = self.get_match(match_id)
        if match is not None:
            if match.get_match_state() == MatchState.WAITING:
                match.start()
                return True
        return False

    def move(self, match_id: int, fig: Figure, x: int, y: int) -> bool:
        match = self.get_match(match_id)
        if match is not None:
                return match.move(fig, x, y)
        return False
    
    def promote(self, match_id, desired_type: PromotingType):
        match = self.get_match(match_id)
        if match is not None and match.get_match_state() == MatchState.WAITING_PROMOTION:
            match.promote (desired_type)
        return


    def delete_match(self, match_id: int) -> bool:
        match = self.get_match(match_id)
        if match is not None:
            self._matches.remove(match)
            return True
        return False