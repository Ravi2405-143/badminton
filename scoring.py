from models import Match, Team, Score, SportType, MatchStatus
from sqlalchemy.orm import Session
import json

def update_match_score(db: Session, match_id: int, scores_data: list):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        return None
    
    if match.status == MatchStatus.COMPLETED:
        raise ValueError("Match is already completed and cannot be rescored.")
    
    # Update or Create Score objects
    for s_data in scores_data:
        db_score = db.query(Score).filter(Score.match_id == match_id, Score.team_id == s_data['team_id']).first()
        if not db_score:
            db_score = Score(match_id=match_id, team_id=s_data['team_id'])
            db.add(db_score)
        
        db_score.runs = s_data.get('runs', 0)
        db_score.wickets = s_data.get('wickets', 0)
        db_score.sets_won = s_data.get('sets_won', 0)

    db.commit()
    
    # Auto-calculate winner
    tournament = match.tournament
    sport = tournament.sport
    
    if sport == SportType.CRICKET:
        calculate_cricket_winner(db, match)
    elif sport == SportType.BADMINTON:
        calculate_badminton_winner(db, match)
        
    db.commit()
    return match

def calculate_cricket_winner(db: Session, match: Match):
    scores = match.scores
    if len(scores) < 2:
        return
    
    s1, s2 = scores[0], scores[1]
    if s1.runs > s2.runs:
        match.winner_id = s1.team_id
        match.status = MatchStatus.COMPLETED
    elif s2.runs > s1.runs:
        match.winner_id = s2.team_id
        match.status = MatchStatus.COMPLETED
    else:
        # Handle draw if needed
        match.winner_id = None
        match.status = MatchStatus.COMPLETED
    
    if match.status == MatchStatus.COMPLETED:
        update_points_table(db, match)

def calculate_badminton_winner(db: Session, match: Match):
    scores = match.scores
    if len(scores) < 2:
        return
        
    s1, s2 = scores[0], scores[1]
    if s1.sets_won > s2.sets_won:
        match.winner_id = s1.team_id
        match.status = MatchStatus.COMPLETED
    elif s2.sets_won > s1.sets_won:
        match.winner_id = s2.team_id
        match.status = MatchStatus.COMPLETED
    else:
        # Draw
        match.winner_id = None
        match.status = MatchStatus.COMPLETED

    if match.status == MatchStatus.COMPLETED:
        update_points_table(db, match)

def update_points_table(db: Session, match: Match):
    t1 = db.query(Team).filter(Team.id == match.team1_id).first()
    t2 = db.query(Team).filter(Team.id == match.team2_id).first()
    
    t1.matches_played += 1
    t2.matches_played += 1
    
    # Track points scored and conceded
    s1 = next((s for s in match.scores if s.team_id == t1.id), None)
    s2 = next((s for s in match.scores if s.team_id == t2.id), None)
    
    if s1 and s2:
        # For Badminton, we use sets won as points for differential? 
        # Or actual point totals if available. Let's use sets_won for badminton 
        # since it's the primary win condition.
        # But wait, cricket uses runs. Let's make it generic.
        p1 = s1.runs if match.tournament.sport == SportType.CRICKET else s1.sets_won
        p2 = s2.runs if match.tournament.sport == SportType.CRICKET else s2.sets_won
        
        t1.points_scored += p1
        t1.points_conceded += p2
        t2.points_scored += p2
        t2.points_conceded += p1

    if match.winner_id == t1.id:
        t1.wins += 1
        t1.points += match.tournament.points_per_win
        t2.losses += 1
    elif match.winner_id == t2.id:
        t2.wins += 1
        t2.points += match.tournament.points_per_win
        t1.losses += 1
    else:
        # No draw logic for now per request, but let's handle it just in case
        t1.points += match.tournament.points_per_draw
        t2.points += match.tournament.points_per_draw
    
    # NRR calculation: Point Differential
    t1.nrr = float(t1.points_scored - t1.points_conceded)
    t2.nrr = float(t2.points_scored - t2.points_conceded)
    pass
