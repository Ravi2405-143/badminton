import requests
import time

BASE_URL = "http://localhost:8000"

def test_custom_rules():
    # 1. Create tournament with custom points (3 for win, 0 for draw)
    t_data = {
        "name": "Custom Points Test",
        "sport": "badminton",
        "format": "league",
        "num_participants": 2,
        "points_per_win": 3,
        "points_per_draw": 0,
        "is_doubles": True
    }
    response = requests.post(f"{BASE_URL}/tournaments/", json=t_data)
    tournament = response.json()
    t_id = tournament['id']
    print(f"Created tournament {t_id} with points_per_win=3")

    # 2. Add two teams
    requests.post(f"{BASE_URL}/teams/", json={"name": "Team A", "tournament_id": t_id})
    requests.post(f"{BASE_URL}/teams/", json={"name": "Team B", "tournament_id": t_id})

    # 3. Generate fixtures
    fixtures = requests.post(f"{BASE_URL}/tournaments/{t_id}/fixtures").json()
    match_id = fixtures[0]['id']
    team1_id = fixtures[0]['team1_id']
    team2_id = fixtures[0]['team2_id']

    # 4. Score match (Team A wins)
    score_data = [
        {"team_id": team1_id, "sets_won": 2},
        {"team_id": team2_id, "sets_won": 0}
    ]
    requests.post(f"{BASE_URL}/matches/{match_id}/score", json=score_data)

    # 5. Verify standings
    standings = requests.get(f"{BASE_URL}/tournaments/{t_id}/standings").json()
    for team in standings:
        if team['id'] == team1_id:
            print(f"Team 1 points: {team['points']} (Expected: 3)")
            assert team['points'] == 3
        if team['id'] == team2_id:
            print(f"Team 2 points: {team['points']} (Expected: 0)")
            assert team['points'] == 0
    
    print("Verification successful!")

if __name__ == "__main__":
    try:
        test_custom_rules()
    except Exception as e:
        print(f"Test failed: {e}")
