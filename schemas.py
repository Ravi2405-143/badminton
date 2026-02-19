from pydantic import BaseModel
from typing import List, Optional
from models import SportType, FormatType, MatchStatus

class PlayerBase(BaseModel):
    name: str

class PlayerCreate(PlayerBase):
    team_id: Optional[int] = None

class Player(PlayerBase):
    id: int
    team_id: Optional[int]

    class Config:
        from_attributes = True

class TeamBase(BaseModel):
    name: str

class TeamCreate(TeamBase):
    tournament_id: int
    players: Optional[List[str]] = []
    points_scored: Optional[int] = 0
    points_conceded: Optional[int] = 0

class Team(TeamBase):
    id: int
    tournament_id: int
    matches_played: int
    wins: int
    losses: int
    points_scored: int
    points_conceded: int
    points: int
    nrr: float
    players: List[Player] = []

    class Config:
        from_attributes = True

class TournamentBase(BaseModel):
    name: str
    sport: SportType
    format: FormatType
    num_participants: int
    points_per_win: Optional[int] = 2
    points_per_draw: Optional[int] = 1
    is_doubles: Optional[bool] = False
    rules: Optional[str] = None

class TournamentCreate(TournamentBase):
    pass

class TeamSimple(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class Tournament(TournamentBase):
    id: int
    is_active: bool
    teams: List[Team] = []
    matches: List['Match'] = []

    class Config:
        from_attributes = True

class ScoreBase(BaseModel):
    team_id: int
    runs: Optional[int] = 0
    wickets: Optional[int] = 0
    sets_won: Optional[int] = 0

class Score(ScoreBase):
    id: int
    match_id: int

    class Config:
        from_attributes = True

class MatchBase(BaseModel):
    tournament_id: int
    team1_id: int
    team2_id: int
    round_name: Optional[str] = None

class Match(MatchBase):
    id: int
    status: MatchStatus
    winner_id: Optional[int] = None
    scores: List[Score] = []
    team1: Optional[TeamSimple] = None
    team2: Optional[TeamSimple] = None
    winner: Optional[TeamSimple] = None

    class Config:
        from_attributes = True
