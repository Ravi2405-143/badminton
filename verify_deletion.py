import requests

BASE_URL = "http://localhost:8000"

def test_deletion():
    print("Testing tournament deletion...")
    # 1. Create a tournament
    t_data = {
        "name": "Delete Me",
        "sport": "badminton",
        "format": "league",
        "num_participants": 2,
        "is_doubles": False
    }
    response = requests.post(f"{BASE_URL}/tournaments/", json=t_data)
    tournament = response.json()
    t_id = tournament['id']
    print(f"Created tournament with id: {t_id}")

    # 2. Verify it exists
    tournaments = requests.get(f"{BASE_URL}/tournaments/").json()
    if any(t['id'] == t_id for t in tournaments):
        print("Tournament successfully verified in list.")
    else:
        print("Error: Tournament not found after creation.")
        return

    # 3. Delete it
    del_res = requests.delete(f"{BASE_URL}/tournaments/{t_id}")
    print(f"Delete response: {del_res.status_code} - {del_res.json()}")

    # 4. Verify it's gone
    tournaments = requests.get(f"{BASE_URL}/tournaments/").json()
    if not any(t['id'] == t_id for t in tournaments):
        print("Tournament successfully deleted and removed from list.")
    else:
        print("Error: Tournament still exists after deletion.")

if __name__ == "__main__":
    try:
        test_deletion()
    except Exception as e:
        print(f"Test failed: {e}")
