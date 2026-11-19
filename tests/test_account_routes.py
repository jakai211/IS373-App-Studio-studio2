"""Additional HTTP boundaries for the Student Assistant account implementation."""

from urllib.parse import urlencode

from app import database


def test_html_signup_rejects_extra_role_and_duplicate_fields(client, settings):
    """HTML submissions cannot bypass the same member-only input contract as JSON."""
    token = client.get("/api/csrf").json()["csrf_token"]
    fields = {
        "username": "student",
        "password": "disposable testing passphrase",
        "csrf_token": token,
    }
    assert client.post("/signup", data={**fields, "role": "admin"}).status_code == 422
    duplicate = urlencode(fields) + "&username=other"
    response = client.post(
        "/signup",
        content=duplicate,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 422
    with database.connect(settings) as connection:
        assert connection.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0


def test_expired_session_cannot_render_dashboard_or_private_api(client, settings):
    """A still-present signed cookie cannot override server-side session expiry."""
    credentials = {"username": "student", "password": "disposable testing passphrase"}
    headers = {"X-CSRF-Token": client.get("/api/csrf").json()["csrf_token"]}
    assert (
        client.post("/api/signup", json=credentials, headers=headers).status_code == 201
    )
    assert (
        client.post("/api/login", json=credentials, headers=headers).status_code == 200
    )
    page = client.get("/dashboard")
    assert page.status_code == 200 and "Welcome, student" in page.text
    with database.connect(settings) as connection:
        connection.execute("UPDATE sessions SET expires_at = 0")
    response = client.get("/dashboard", follow_redirects=False)
    assert response.status_code == 303 and response.headers["location"] == "/login"
    assert "Welcome, student" not in response.text
    assert client.get("/api/me").status_code == 401


def test_oversized_html_form_is_rejected_without_echoing_input(client):
    """Reject oversized text before credential parsing or password hashing."""
    response = client.post(
        "/login",
        content="password=" + "x" * 9000,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 413
    assert "x" * 100 not in response.text
