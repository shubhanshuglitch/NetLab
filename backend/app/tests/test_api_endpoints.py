from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_healthcheck():
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"

def test_list_scenarios():
    resp = client.get("/api/scenarios")
    assert resp.status_code == 200
    scenarios = resp.json()
    assert len(scenarios) >= 5
    assert scenarios[0]["id"] == "scenario-youtube-tabs"

def test_get_scenario_detail():
    resp = client.get("/api/scenarios/scenario-youtube-tabs")
    assert resp.status_code == 200
    data = resp.json()
    assert "topology" in data
    assert len(data["topology"]["devices"]) >= 3

def test_list_concepts():
    resp = client.get("/api/concepts")
    assert resp.status_code == 200
    concepts = resp.json()
    assert len(concepts) >= 5

def test_interactive_crc_endpoint():
    resp = client.post("/api/concepts/crc/calculate", json={
        "data_bits": "1101011011",
        "generator_bits": "10011"
    })
    assert resp.status_code == 200
    res = resp.json()
    assert "remainder_crc_bits" in res

def test_interactive_arq_endpoint():
    resp = client.post("/api/concepts/arq/simulate", json={
        "protocol": "Go-Back-N",
        "total_frames": 6,
        "window_size": 3,
        "drop_frame_index": 1
    })
    assert resp.status_code == 200
    res = resp.json()
    assert "events" in res

def test_interview_questions():
    resp = client.get("/api/interview/questions")
    assert resp.status_code == 200
    questions = resp.json()
    assert len(questions) >= 50

def test_interview_verify():
    resp = client.post("/api/interview/verify", json={
        "question_id": "q1",
        "selected_option_index": 1
    })
    assert resp.status_code == 200
    res = resp.json()
    assert res["is_correct"] is True
    assert "explanation" in res

def test_search():
    resp = client.get("/api/search?q=youtube")
    assert resp.status_code == 200
    res = resp.json()
    assert len(res["scenarios"]) >= 1

def test_run_simulation_endpoint():
    resp = client.post("/api/simulations", json={
        "topology_id": "scenario-youtube-tabs",
        "sender_id": "laptop",
        "receiver_id": "youtube_server",
        "payload": "GET /video HTTP/1.1"
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "COMPLETED"
    assert len(data["events"]) > 0
    assert "simulation_id" in data

