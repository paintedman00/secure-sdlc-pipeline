import subprocess

from flask import Blueprint, abort, jsonify, request

from .db import get_db

bp = Blueprint("api", __name__)

MAX_USERNAME_LEN = 32
MAX_EMAIL_LEN = 254


def _row_to_dict(row):
    return {"id": row["id"], "username": row["username"], "email": row["email"]}


@bp.get("/health")
def health():
    return jsonify(status="ok")


@bp.get("/users/<int:user_id>")
def get_user(user_id):
    row = get_db().execute(
        "SELECT id, username, email FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    if row is None:
        abort(404)
    return jsonify(_row_to_dict(row))


@bp.post("/users")
def create_user():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    email = data.get("email")
    if not isinstance(username, str) or not isinstance(email, str):
        return jsonify(error="username and email are required strings"), 400
    if not 0 < len(username) <= MAX_USERNAME_LEN:
        return jsonify(error=f"username must be 1-{MAX_USERNAME_LEN} characters"), 400
    if not 0 < len(email) <= MAX_EMAIL_LEN:
        return jsonify(error=f"email must be 1-{MAX_EMAIL_LEN} characters"), 400

    conn = get_db()
    try:
        cur = conn.execute(
            "INSERT INTO users (username, email) VALUES (?, ?)", (username, email)
        )
        conn.commit()
    except conn.IntegrityError:
        return jsonify(error="username already exists"), 409
    return jsonify(id=cur.lastrowid, username=username, email=email), 201


# INTENTIONALLY VULNERABLE: user input is concatenated into the SQL string,
# so /search?q=' OR '1'='1 returns every row. This exists so the SAST stage
# has a real finding to report. The safe pattern is the parameterized query
# used in get_user() above.
@bp.get("/search")
def search_users():
    q = request.args.get("q", "")
    query = f"SELECT id, username, email FROM users WHERE username = '{q}'"
    rows = get_db().execute(query).fetchall()
    return jsonify([_row_to_dict(r) for r in rows])


@bp.get("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    return subprocess.run(f"ping -c 1 {host}", shell=True, capture_output=True, text=True).stdout
