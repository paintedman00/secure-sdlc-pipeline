def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_get_user(client):
    resp = client.get("/users/1")
    assert resp.status_code == 200
    assert resp.get_json()["username"] == "alice"


def test_get_user_not_found(client):
    assert client.get("/users/999").status_code == 404


def test_create_user(client):
    resp = client.post("/users", json={"username": "dave", "email": "dave@example.com"})
    assert resp.status_code == 201
    assert client.get(f"/users/{resp.get_json()['id']}").status_code == 200


def test_create_user_rejects_missing_fields(client):
    assert client.post("/users", json={"username": "dave"}).status_code == 400


def test_create_user_rejects_duplicate(client):
    resp = client.post("/users", json={"username": "alice", "email": "x@example.com"})
    assert resp.status_code == 409


def test_search_normal_input(client):
    resp = client.get("/search", query_string={"q": "bob"})
    assert [u["username"] for u in resp.get_json()] == ["bob"]


def test_search_is_injectable(client):
    # Documents the intentional flaw: a tautology payload dumps the whole table.
    resp = client.get("/search", query_string={"q": "' OR '1'='1"})
    assert len(resp.get_json()) == 3
