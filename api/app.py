import os

import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)


def query(sql, params=None, fetch=False):
    conn = psycopg2.connect(
        host=os.environ["DB_HOST"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        connect_timeout=5,
    )
    try:
        with conn, conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall() if fetch else None
    finally:
        conn.close()


@app.after_request
def add_pod_header(resp):
    resp.headers["X-Served-By"] = os.environ.get("HOSTNAME", "unknown")
    return resp


@app.errorhandler(psycopg2.Error)
def db_error(_):
    return jsonify(error="database unavailable"), 503


@app.get("/health")
def health():
    query("SELECT 1")
    return jsonify(status="ok")


@app.post("/greet")
def greet():
    name = ((request.get_json(silent=True) or {}).get("name") or "").strip()
    if not name or len(name) > 100:
        return jsonify(error="name is required (max 100 chars)"), 400
    query("INSERT INTO names (name) VALUES (%s)", (name,))
    return jsonify(greeting=f"Hello, {name}!")


@app.get("/names")
def names():
    rows = query("SELECT id, name, created_at FROM names ORDER BY id DESC LIMIT 50", fetch=True)
    return jsonify([{"id": r[0], "name": r[1], "created_at": r[2].isoformat()} for r in rows])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
