from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List
import os
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

import models, schemas, database, fixtures, scoring, auth
from database import engine, get_db

try:
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Warning: Database initialization failed: {e}")

app = FastAPI(title="Sports Tournament Management API")

# Mount static files
# Use absolute path for robustness on Vercel
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")

try:
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
except OSError:
    print(f"Warning: Could not create static directory {static_dir} due to read-only filesystem.")

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def read_root():
    from fastapi.responses import FileResponse
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Sportify API is running, but index.html was not found."}

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.USERS.get(form_data.username)
    if not user or not auth.verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Tournament Endpoints
@app.post("/tournaments/", response_model=schemas.Tournament)
def create_tournament(tournament: schemas.TournamentCreate, db: Session = Depends(get_db)):
    db_tournament = models.Tournament(
        name=tournament.name,
        sport=tournament.sport,
        format=tournament.format,
        num_participants=tournament.num_participants,
        points_per_win=tournament.points_per_win,
        points_per_draw=tournament.points_per_draw,
        is_doubles=tournament.is_doubles,
        rules=tournament.rules
    )
    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)
    return db_tournament

@app.get("/tournaments/", response_model=List[schemas.Tournament])
def get_tournaments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tournaments = db.query(models.Tournament).offset(skip).limit(limit).all()
    return tournaments

@app.get("/tournaments/{tournament_id}", response_model=schemas.Tournament)
def get_tournament(tournament_id: int, db: Session = Depends(get_db)):
    db_tournament = db.query(models.Tournament).filter(models.Tournament.id == tournament_id).first()
    if not db_tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return db_tournament

@app.post("/tournaments/{tournament_id}/fixtures", response_model=List[schemas.Match])
def generate_tournament_fixtures(tournament_id: int, db: Session = Depends(get_db)):
    db_tournament = db.query(models.Tournament).filter(models.Tournament.id == tournament_id).first()
    if not db_tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return fixtures.generate_fixtures(db, db_tournament)

@app.get("/matches/recent", response_model=List[schemas.Match])
def get_recent_matches(limit: int = 10, db: Session = Depends(get_db)):
    """Get the most recent completed matches across all tournaments."""
    return db.query(models.Match).filter(models.Match.status == "completed").order_by(models.Match.id.desc()).limit(limit).all()

@app.get("/rankings/players")
def get_player_rankings(limit: int = 20, db: Session = Depends(get_db)):
    """Get global player rankings based on wins (calculated from team wins)."""
    # This is a simplified ranking: top teams across all tournaments
    teams = db.query(models.Team).order_by(models.Team.points.desc(), models.Team.nrr.desc()).limit(limit).all()
    rankings = []
    for team in teams:
        rankings.append({
            "team_name": team.name,
            "tournament_name": team.tournament.name,
            "wins": team.wins,
            "points": team.points,
            "nrr": team.nrr
        })
    return rankings

# Match & Scoring Endpoints
@app.post("/matches/{match_id}/score", response_model=schemas.Match)
def update_match_score(match_id: int, scores: List[schemas.ScoreBase], db: Session = Depends(get_db)):
    match = scoring.update_match_score(db, match_id, [s.dict() for s in scores])
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match

@app.get("/tournaments/{tournament_id}/standings", response_model=List[schemas.Team])
def get_standings(tournament_id: int, db: Session = Depends(get_db)):
    teams = db.query(models.Team).filter(models.Team.tournament_id == tournament_id).order_by(models.Team.points.desc(), models.Team.nrr.desc()).all()
    return teams

# Team Endpoints
@app.delete("/tournaments/{tournament_id}")
def delete_tournament(tournament_id: int, db: Session = Depends(get_db)):
    tournament = db.query(models.Tournament).filter(models.Tournament.id == tournament_id).first()
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    db.delete(tournament)
    db.commit()
    return {"message": "Tournament deleted successfully"}

@app.post("/teams/", response_model=schemas.Team)
def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db)):
    db_team = models.Team(name=team.name, tournament_id=team.tournament_id)
    db.add(db_team)
    db.commit()
    
    # Initialize players if provided
    if team.players:
        for p_name in team.players:
            if p_name.strip():
                db_player = models.Player(name=p_name.strip(), team_id=db_team.id)
                db.add(db_player)
        db.commit()
        db.refresh(db_team)
        
    return db_team

# Player Endpoints
@app.post("/players/", response_model=schemas.Player)
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    db_player = models.Player(name=player.name, team_id=player.team_id)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
