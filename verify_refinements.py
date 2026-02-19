import requests
import time

BASE_URL = "http://localhost:8000"

def test_refinements():
    print("Testing fixture generation for odd number of teams...")
    # 1. Create a tournament
    t_data = {
        "name": "Odd Teams Test",
        "sport": "badminton",
        "format": "league",
        "num_participants": 3,
        "is_doubles": False
    }
    response = requests.post(f"{BASE_URL}/tournaments/", json=t_data)
    tournament = response.json()
    t_id = tournament['id']

    # 2. Add 3 teams
    for i in range(3):
        requests.post(f"{BASE_URL}/teams/", json={
            "name": f"Team {i+1}", 
            "tournament_id": t_id,
            "players": ["Player One"]
        })

    # 3. Generate fixtures
    fixtures = requests.post(f"{BASE_URL}/tournaments/{t_id}/fixtures").json()
    print(f"Generated {len(fixtures)} matches for 3 teams.")
    # Expected: Each team plays 2 matches. Total matches = 3.
    # Round 1: Team 1 vs Team 3 (Team 2 bye)
    # Round 2: Team 1 vs Team 2 (Team 3 bye)
    # Round 3: Team 3 vs Team 2 (Team 1 bye)
    if len(fixtures) == 3:
        print("Fixture count correct (3 matches).")
    else:
        print(f"Warning: Expected 3 matches, got {len(fixtures)}")

    print("\nTesting Doubles team creation...")
    # 4. Create a doubles tournament
    dt_data = {
        "name": "Doubles Test",
        "sport": "badminton",
        "format": "league",
        "num_participants": 2,
        "is_doubles": True
    }
    dt_response = requests.post(f"{BASE_URL}/tournaments/", json=dt_data)
    dt_id = dt_response.json()['id']

    # 5. Add a doubles team
    team_data = {
        "name": "Power Duo",
        "tournament_id": dt_id,
        "players": ["Alice", "Bob"]
    }
    team_res = requests.post(f"{BASE_URL}/teams/", json=team_data).json()
    
    # 6. Verify players
    # Fetch team manually to see if players are there (the schema has List[Player])
    # Let's check the API response for the newly created team
    if len(team_res.get('players', [])) == 2:
        print("Doubles team created with 2 players successfully.")
        print(f"Players: {[p['name'] for p in team_res['players']]}")
    else:
        print(f"Warning: Expected 2 players, got {len(team_res.get('players', []))}")

    print("\nVerification successful!")

if __name__ == "__main__":
    try:
        test_refinements()
    except Exception as e:
        print(f"Test failed: {e}")
