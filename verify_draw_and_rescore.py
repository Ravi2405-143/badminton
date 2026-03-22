import requests
import sys

BASE_URL = "http://localhost:8000"

def test_draw_and_rescore():
    print("Testing Draw Logic & Rescore prevention...")
    
    # 1. Create a tournament
    t_data = {
        "name": "Draw Test Tournament",
        "sport": "badminton",
        "format": "league",
        "num_participants": 2,
        "is_doubles": False,
        "points_per_win": 3,
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

    # 4. Score match as a DRAW
    score_data = [
        {"team_id": t1_id, "sets_won": 2},
        {"team_id": t2_id, "sets_won": 2}
    ]
    res = requests.post(f"{BASE_URL}/matches/{match_id}/score", json=score_data)
    match = res.json()
    assert match['status'] == 'completed', "Match status should be completed for a draw"
    assert match['winner_id'] is None, "Winner should be None for a draw"

    # 5. Verify standings (Points should be 1 each)
    standings = requests.get(f"{BASE_URL}/tournaments/{t_id}/standings").json()
    for team in standings:
        assert team['points'] == 1, f"Team points should be 1, got {team['points']}"
        assert team['matches_played'] == 1, "Matches played should be 1"

    # 6. Attempt to rescore the same closed match
    score_data_2 = [
        {"team_id": t1_id, "sets_won": 4},
        {"team_id": t2_id, "sets_won": 0}
    ]
    res2 = requests.post(f"{BASE_URL}/matches/{match_id}/score", json=score_data_2)
    assert res2.status_code == 400, f"Expected 400 Bad Request, got {res2.status_code}"
    print("Successfully blocked rescoring of completed match!")

    # 7. Re-verify standings ensuring points were not duplicated
    standings2 = requests.get(f"{BASE_URL}/tournaments/{t_id}/standings").json()
    for team in standings2:
        assert team['points'] == 1, "Team points should STILL be 1!"
        assert team['matches_played'] == 1, "Matches played should STILL be 1!"

    print("Draw & Rescore verification successful!")

if __name__ == "__main__":
    try:
        test_draw_and_rescore()
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)
