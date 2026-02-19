import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def seed_data():
    # 1. Create a Cricket Tournament
    tournament_data = {
        "name": "Summer Cricket Blast",
        "sport": "cricket",
        "format": "league",
        "num_participants": 4,
        "rules": "20 overs per side"
    }
    response = requests.post(f"{BASE_URL}/tournaments/", json=tournament_data)
    tournament = response.json()
    print(f"Created Tournament: {tournament['name']} (ID: {tournament['id']})")

    # 2. Add Teams
    teams = ["Warriors", "Titans", "Kings", "Eagles"]
    team_ids = []
    for team_name in teams:
        team_resp = requests.post(f"{BASE_URL}/teams/", json={"name": team_name, "tournament_id": tournament['id']})
        team = team_resp.json()
        team_ids.append(team['id'])
        print(f"Added Team: {team['name']} (ID: {team['id']})")

    # 3. Generate Fixtures
    fixtures_resp = requests.post(f"{BASE_URL}/tournaments/{tournament['id']}/fixtures")
    fixtures = fixtures_resp.json()
    print(f"Generated {len(fixtures)} fixtures.")

if __name__ == "__main__":
    try:
        seed_data()
    except Exception as e:
        print(f"Error seeding data: {e}")
