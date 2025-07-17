from app.utils import hash_password, verify_password, create_token, decode_token, login_required
from flask import Flask, jsonify

def test_hash_and_verify_password():
    pw = "password123"
    hashed = hash_password(pw)
    assert hashed != pw
    assert verify_password(pw, hashed)
    assert not verify_password("wrongpass", hashed)

def test_create_and_decode_jwt(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "my-secret1")
    token = create_token("identity1", "user")
    decoded = decode_token(token)
    assert decoded["identity"] == "identity1"
    assert decoded["user_type"] == "user"

def test_decode_token_expired(monkeypatch):
    import jwt
    import datetime
    monkeypatch.setenv("JWT_SECRET", "shortsecret")
    payload = {
        "identity": "identity-exp",
        "user_type": "user",
        "exp": datetime.datetime.utcnow() - datetime.timedelta(seconds=1)
    }
    token = jwt.encode(payload, "shortsecret", algorithm="HS256")
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    assert decode_token(token) is None

def test_login_required_decorator_accepts(monkeypatch):
    # Simulate token in request headers using Flask test_client and a view
    monkeypatch.setenv("JWT_SECRET", "unitsecret")
    app = Flask(__name__)
    @app.route("/protected")
    @login_required(user_type="user")
    def protected(identity):
        return jsonify({"identity": identity})

    client = app.test_client()
    token = create_token("xid", "user", expires_in=10)
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.get("/protected", headers=headers)
    assert resp.status_code == 200
    assert resp.json["identity"] == "xid"

def test_login_required_decorator_forbidden(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "unitsecret")
    app = Flask(__name__)
    @app.route("/protected")
    @login_required(user_type="provider")
    def protected(identity):
        return jsonify({"identity": identity})

    client = app.test_client()
    token = create_token("xid", "user", expires_in=10)
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.get("/protected", headers=headers)
    assert resp.status_code == 403
    assert "Forbidden" in resp.get_data(as_text=True)
