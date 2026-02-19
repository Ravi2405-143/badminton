import random
from typing import List
from models import Match, Team, Tournament, FormatType

def generate_fixtures(db, tournament: Tournament):
    teams = tournament.teams
    if len(teams) < 2:
        return []
    
    if tournament.format == FormatType.LEAGUE:
        return generate_round_robin(db, tournament, teams)
    elif tournament.format == FormatType.KNOCKOUT:
        return generate_knockout(db, tournament, teams)
    else:
        # League + Knockout (Hybrid) - initially generates league
        return generate_round_robin(db, tournament, teams)

def generate_round_robin(db, tournament: Tournament, teams: List[Team]):
    team_ids = [t.id for t in teams]
    if len(team_ids) % 2 != 0:
        team_ids.append(None) # Add a dummy team for bye handling
    
    num_teams = len(team_ids)
    fixtures = []
    
    # Standard circle method
    # For N teams, there are N-1 rounds (if N even) or N rounds (if N odd, but dummy makes it N even)
    for r in range(num_teams - 1):
        for i in range(num_teams // 2):
            t1 = team_ids[i]
            t2 = team_ids[num_teams - 1 - i]
            
            if t1 is not None and t2 is not None:
                match = Match(
                    tournament_id=tournament.id,
                    team1_id=t1,
                    team2_id=t2,
                    round_name=f"Round {r+1}"
                )
                db.add(match)
                fixtures.append(match)
        
        # Rotate all but the first element
        team_ids = [team_ids[0]] + [team_ids[-1]] + team_ids[1:-1]
        
    db.commit()
    return fixtures

def generate_knockout(db, tournament: Tournament, teams: List[Team]):
    # Simplified knockout: only Quarter (8), Semi (4), Final (2) supported for now
    # We should shuffle teams for randomness
    shuffled_teams = list(teams)
    random.shuffle(shuffled_teams)
    
    num_teams = len(shuffled_teams)
    # Power of 2 check and bye handling would be needed for a production system
    
    fixtures = []
    for i in range(0, num_teams, 2):
        if i + 1 < num_teams:
            match = Match(
                tournament_id=tournament.id,
                team1_id=shuffled_teams[i].id,
                team2_id=shuffled_teams[i+1].id,
                round_name="Opening Round"
            )
            db.add(match)
            fixtures.append(match)
            
    db.commit()
    return fixtures
