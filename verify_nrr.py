import requests
import time

BASE_URL = "http://localhost:8000"

def test_nrr_logic():
    print("Testing Point Differential NRR logic...")
    # 1. Create a tournament
    t_data = {
        "name": "NRR Test",
        "sport": "badminton",
        "format": "league",
        "num_participants": 2,
        "is_doubles": False,
        "points_per_win": 2,
        "points_per_draw": 1
    }
    response = requests.post(f"{BASE_URL}/tournaments/", json=t_data)
    t_id = response.json()['id']

    # 2. Add 2 teams
    requests.post(f"{BASE_URL}/teams/", json={"name": "Team A", "tournament_id": t_id, "players": ["P1"]})
    requests.post(f"{BASE_URL}/teams/", json={"name": "Team B", "tournament_id": t_id, "players": ["P2"]})

    # 3. Generate fixtures
    fixtures = requests.post(f"{BASE_URL}/tournaments/{t_id}/fixtures").json()
    match_id = fixtures[0]['id']
    t1_id = fixtures[0]['team1_id']
    t2_id = fixtures[0]['team2_id']

    # 4. Score match (Team A wins 2-1)
    # This means Team A: PG=2, PL=1. Team B: PG=1, PL=2.
    score_data = [
        {"team_id": t1_id, "sets_won": 2},
        {"team_id": t2_id, "sets_won": 1}
    ]
    requests.post(f"{BASE_URL}/matches/{match_id}/score", json=score_data)

    # 5. Verify standings
    standings = requests.get(f"{BASE_URL}/tournaments/{t_id}/standings").json()
    for team in standings:
        if team['id'] == t1_id:
            print(f"Team A: PG={team['points_scored']}, PL={team['points_conceded']}, NRR={team['nrr']}")
            assert team['points_scored'] == 2
            assert team['points_conceded'] == 1
            assert team['nrr'] == 1.0 # 2 - 1
        if team['id'] == t2_id:
            print(f"Team B: PG={team['points_scored']}, PL={team['points_conceded']}, NRR={team['nrr']}")
            assert team['points_scored'] == 1
            assert team['points_conceded'] == 2
            assert team['nrr'] == -1.0 # 1 - 2
    
    print("Point Differential NRR verification successful!")

if __name__ == "__main__":
    try:
        test_nrr_logic()
    except Exception as e:
        print(f"Test failed: {e}")
