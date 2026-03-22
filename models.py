from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Float, Boolean, Table
from sqlalchemy.orm import relationship
import enum
from database import Base

class SportType(enum.Enum):
    CRICKET = "cricket"
    BADMINTON = "badminton"

class FormatType(enum.Enum):
    LEAGUE = "league"
    KNOCKOUT = "knockout"
    LEAGUE_KNOCKOUT = "league+knockout"

class MatchStatus(enum.Enum):
    UPCOMING = "upcoming"
    LIVE = "live"
    COMPLETED = "completed"

class Tournament(Base):
    __tablename__ = "tournaments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    sport = Column(Enum(SportType))
    format = Column(Enum(FormatType))
    rules = Column(String)  # JSON string for rules
    num_participants = Column(Integer)
    points_per_win = Column(Integer, default=2)
    points_per_draw = Column(Integer, default=1)
    is_doubles = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    teams = relationship("Team", back_populates="tournament", cascade="all, delete-orphan")
    matches = relationship("Match", back_populates="tournament", cascade="all, delete-orphan")

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"))
    
    tournament = relationship("Tournament", back_populates="teams")
    players = relationship("Player", back_populates="team", cascade="all, delete-orphan")
    
    # Points table stats (simplified)
    matches_played = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    points_scored = Column(Integer, default=0)
    points_conceded = Column(Integer, default=0)
    points = Column(Integer, default=0)
    nrr = Column(Float, default=0.0)

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    
    team = relationship("Team", back_populates="players")

class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"))
    round_name = Column(String, nullable=True) # e.g., "Round 1", "Quarter Final"
    team1_id = Column(Integer, ForeignKey("teams.id"))
    team2_id = Column(Integer, ForeignKey("teams.id"))
    status = Column(Enum(MatchStatus), default=MatchStatus.UPCOMING)
    winner_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    
    tournament = relationship("Tournament", back_populates="matches")
    team1 = relationship("Team", foreign_keys=[team1_id])
    team2 = relationship("Team", foreign_keys=[team2_id])
    winner = relationship("Team", foreign_keys=[winner_id])
    
    scores = relationship("Score", back_populates="match")

class Score(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"))
    team_id = Column(Integer, ForeignKey("teams.id"))
    
    # Generic score fields (can be interpreted based on sport)
    runs = Column(Integer, default=0)
    wickets = Column(Integer, default=0)
    sets_won = Column(Integer, default=0) # For Badminton

    match = relationship("Match", back_populates="scores")
