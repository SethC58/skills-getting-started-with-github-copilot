import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

# Initial activities data for resetting
INITIAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball team for tournament play",
        "schedule": "Tuesdays, Thursdays, Saturdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["james@mergington.edu", "ryan@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Develop tennis skills and friendly matches",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["alex@mergington.edu"]
    },
    "Art Studio": {
        "description": "Painting, drawing, and mixed media techniques",
        "schedule": "Wednesdays and Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["isabella@mergington.edu", "avery@mergington.edu"]
    },
    "Music Band": {
        "description": "Perform in school concerts and events",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 30,
        "participants": ["lucas@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop argumentation and public speaking skills",
        "schedule": "Tuesdays and Fridays, 3:45 PM - 5:15 PM",
        "max_participants": 18,
        "participants": ["grace@mergington.edu", "marcus@mergington.edu"]
    },
    "Science Club": {
        "description": "Explore experiments and STEM-related projects",
        "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["noah@mergington.edu", "nina@mergington.edu"]
    }
}

@pytest.fixture
def client():
    # Reset activities to initial state before each test
    activities.clear()
    activities.update(INITIAL_ACTIVITIES)
    return TestClient(app)

def test_get_activities(client):
    # Arrange: Client is set up with initial data

    # Act: Make GET request to /activities
    response = client.get("/activities")

    # Assert: Status code is 200, returns activities dict
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"

def test_signup_success(client):
    # Arrange: Client is set up, choose an activity and new email
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Status code 200, message returned, participant added
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert email in activities[activity_name]["participants"]

def test_signup_duplicate(client):
    # Arrange: Client is set up, choose an activity and existing email
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Status code 400, error message
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]

def test_signup_activity_not_found(client):
    # Arrange: Client is set up, choose non-existent activity
    activity_name = "NonExistent Activity"
    email = "student@mergington.edu"

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Status code 404, error message
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]

def test_unregister_success(client):
    # Arrange: Client is set up, choose an activity and existing participant
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up

    # Act: Make DELETE request to unregister
    response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert: Status code 200, message returned, participant removed
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert email not in activities[activity_name]["participants"]

def test_unregister_not_signed_up(client):
    # Arrange: Client is set up, choose an activity and non-participant email
    activity_name = "Chess Club"
    email = "notsignedup@mergington.edu"

    # Act: Make DELETE request to unregister
    response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert: Status code 400, error message
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"]

def test_unregister_activity_not_found(client):
    # Arrange: Client is set up, choose non-existent activity
    activity_name = "NonExistent Activity"
    email = "student@mergington.edu"

    # Act: Make DELETE request to unregister
    response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert: Status code 404, error message
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]

def test_root_redirect(client):
    # Arrange: Client is set up

    # Act: Make GET request to / without following redirects
    response = client.get("/", follow_redirects=False)

    # Assert: Status code 307 (redirect), redirects to /static/index.html
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"