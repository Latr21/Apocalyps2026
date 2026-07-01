"""Tests pédagogiques pour l'app accounts.

Ces tests servent d'exemples : signup, login, logout, accès protégé.
Lancez : pytest accounts/
"""

import json
import zipfile
from io import BytesIO

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from quizzes.models import Question, Quiz

from .models import DataRequest

pytestmark = pytest.mark.django_db


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def user(db) -> User:
    return User.objects.create_user(
        username="alice", email="alice@test.com", password="motdepasse123"
    )


@pytest.fixture
def auth_client(user) -> APIClient:
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def other_user() -> User:
    return User.objects.create_user(username="bob", email="bob@test.com", password="motdepasse123")


def test_signup_creates_user(client):
    # Lot 3 : inscription par EMAIL (username = email en interne).
    response = client.post(
        "/api/accounts/signup/",
        {
            "email": "bob@test.com",
            "password": "motdepasse123",
        },
        format="json",
    )
    assert response.status_code == 201, response.data
    assert User.objects.filter(email="bob@test.com").exists()


def test_signup_requires_email(client):
    response = client.post(
        "/api/accounts/signup/",
        {"password": "motdepasse123"},
        format="json",
    )
    assert response.status_code == 400


def test_login_returns_token(client, user):
    response = client.post(
        "/api/accounts/login/",
        {"email": "alice@test.com", "password": "motdepasse123"},
        format="json",
    )
    assert response.status_code == 200, response.data
    assert "token" in response.data
    assert response.data["user"]["email"] == "alice@test.com"


def test_login_with_wrong_password(client, user):
    response = client.post(
        "/api/accounts/login/",
        {"email": "alice@test.com", "password": "wrong"},
        format="json",
    )
    assert response.status_code == 400


def test_me_requires_auth(client):
    response = client.get("/api/accounts/me/")
    assert response.status_code in (401, 403)


def test_me_with_token(client, user):
    from rest_framework.authtoken.models import Token

    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    response = client.get("/api/accounts/me/")
    assert response.status_code == 200
    assert response.data["username"] == "alice"


def test_logout_invalidates_token(client, user):
    from rest_framework.authtoken.models import Token

    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    response = client.post("/api/accounts/logout/")
    assert response.status_code == 204
    # Le token n'existe plus
    assert not Token.objects.filter(key=token.key).exists()


# ---------------------------------------------------------------------------
# Export RGPD (perturbation J3-bis, article 15) — GET /api/accounts/me/export/
# ---------------------------------------------------------------------------


@pytest.fixture
def quiz_with_answer(user) -> Quiz:
    quiz = Quiz.objects.create(
        user=user, title="RGPD 101", source_text="Le RGPD encadre...", score=8
    )
    Question.objects.create(
        quiz=quiz,
        index=1,
        prompt="Q1 ?",
        options=["A", "B", "C", "D"],
        correct_index=0,
        selected_index=0,
    )
    return quiz


def test_export_requires_auth(client):
    response = client.get("/api/accounts/me/export/")
    assert response.status_code in (401, 403)


def test_export_json_contains_own_data(auth_client, quiz_with_answer):
    response = auth_client.get("/api/accounts/me/export/")
    assert response.status_code == 200
    assert response["Content-Type"].startswith("application/json")

    payload = json.loads(response.content)
    assert payload["user"]["username"] == "alice"
    assert len(payload["courses"]) == 1
    assert payload["courses"][0]["title"] == "RGPD 101"
    assert len(payload["quizzes"]) == 1
    assert len(payload["quizzes"][0]["questions"]) == 1
    assert len(payload["answers"]) == 1
    assert payload["answers"][0]["is_correct"] is True
    assert len(payload["scores"]) == 1
    assert payload["scores"][0]["score"] == 8
    # Catégories sans modèle dans ce MVP : listes vides, jamais absentes.
    assert payload["reports"] == []
    assert payload["audit_logs"] == []


def test_export_never_leaks_other_users_data(auth_client, other_user):
    Quiz.objects.create(user=other_user, title="Quiz de Bob", source_text="Confidentiel")
    response = auth_client.get("/api/accounts/me/export/")
    payload = json.loads(response.content)
    assert payload["quizzes"] == []
    assert payload["courses"] == []


def test_export_creates_data_request(auth_client, user, quiz_with_answer):
    assert DataRequest.objects.filter(user=user).count() == 0
    auth_client.get("/api/accounts/me/export/")

    assert DataRequest.objects.filter(user=user).count() == 1
    data_request = DataRequest.objects.get(user=user)
    assert data_request.status == DataRequest.Status.COMPLETED
    assert data_request.format == DataRequest.Format.JSON
    assert data_request.response_at is not None


def test_export_records_hash(auth_client, user):
    auth_client.get("/api/accounts/me/export/")
    data_request = DataRequest.objects.get(user=user)
    assert len(data_request.export_hash) == 64  # SHA-256 en hexadécimal
    int(data_request.export_hash, 16)  # doit être un hex valide


def test_export_csv_returns_zip_archive(auth_client, user, quiz_with_answer):
    response = auth_client.get("/api/accounts/me/export/?export_format=csv")
    assert response.status_code == 200
    assert response["Content-Type"] == "application/zip"

    archive = zipfile.ZipFile(BytesIO(response.content))
    assert "quizzes.csv" in archive.namelist()
    assert "questions.csv" in archive.namelist()

    data_request = DataRequest.objects.get(user=user)
    assert data_request.format == DataRequest.Format.CSV


def test_export_rejects_invalid_format(auth_client):
    response = auth_client.get("/api/accounts/me/export/?export_format=xml")
    assert response.status_code == 400
