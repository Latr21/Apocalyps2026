"""
Export RGPD des données personnelles (article 15 — droit d'accès).

[Note pédagogique — perturbation J3-bis] Toute la logique de construction de
l'export vit ici (et non dans la vue), sur le même principe que `emails.py`
ou `tokens.py` dans cette app : un fichier par responsabilité. Le JSON produit
par `build_export_payload` est la SOURCE UNIQUE de vérité ; l'archive ZIP/CSV
(`build_zip_archive`) est dérivée de ce même payload pour ne jamais désynchroniser
les deux formats.
"""

import csv
import io
import zipfile

from django.http import HttpRequest

from .models import get_or_create_profile

# Catégories de données personnelles inexistantes dans ce MVP (aucun modèle de
# signalement ni de journal d'audit applicatif) : on renvoie une liste vide,
# comme l'exige le droit d'accès (déclarer explicitement l'absence de donnée).
EMPTY_CATEGORIES = ("reports", "audit_logs")


def client_ip(request: HttpRequest) -> str | None:
    """IP du client, en tenant compte d'un éventuel proxy (Caddy en prod)."""
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def build_export_payload(user) -> dict:
    """Construit le JSON complet des données personnelles de `user`.

    Ne touche à AUCUNE donnée d'un autre utilisateur : tout part de
    `user.quizzes` (related_name du FK Quiz.user), donc filtré nativement.
    """
    profile = get_or_create_profile(user)
    quizzes = list(user.quizzes.prefetch_related("questions").all())

    courses = [
        {
            "quiz_id": quiz.id,
            "title": quiz.title,
            "source_text": quiz.source_text,
            "created_at": quiz.created_at,
        }
        for quiz in quizzes
    ]

    quizzes_data = [
        {
            "id": quiz.id,
            "title": quiz.title,
            "score": quiz.score,
            "created_at": quiz.created_at,
            "updated_at": quiz.updated_at,
            "questions": [
                {
                    "index": question.index,
                    "prompt": question.prompt,
                    "options": question.options,
                    "correct_index": question.correct_index,
                    "selected_index": question.selected_index,
                }
                for question in quiz.questions.all()
            ],
        }
        for quiz in quizzes
    ]

    answers = [
        {
            "quiz_id": quiz.id,
            "quiz_title": quiz.title,
            "question_index": question.index,
            "selected_index": question.selected_index,
            "correct_index": question.correct_index,
            "is_correct": question.selected_index == question.correct_index,
        }
        for quiz in quizzes
        for question in quiz.questions.all()
        if question.selected_index is not None
    ]

    scores = [
        {
            "quiz_id": quiz.id,
            "quiz_title": quiz.title,
            "score": quiz.score,
            "total_questions": quiz.questions.count(),
            "updated_at": quiz.updated_at,
        }
        for quiz in quizzes
        if quiz.score is not None
    ]

    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "date_joined": user.date_joined,
            "email_verified": profile.email_verified,
        },
        "courses": courses,
        "quizzes": quizzes_data,
        "answers": answers,
        "scores": scores,
        "reports": [],
        "audit_logs": [],
    }


def build_zip_archive(payload: dict) -> bytes:
    """Dérive une archive ZIP (1 CSV par catégorie) du payload JSON.

    Les questions imbriquées dans `quizzes` sont extraites dans un fichier
    `questions.csv` séparé (une ligne CSV = une ligne, pas de structure
    imbriquée possible en CSV).
    """
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("user.csv", _to_csv([payload["user"]]))
        archive.writestr("courses.csv", _to_csv(payload["courses"]))

        quiz_rows = [
            {k: v for k, v in quiz.items() if k != "questions"} for quiz in payload["quizzes"]
        ]
        archive.writestr("quizzes.csv", _to_csv(quiz_rows))

        question_rows = [
            {"quiz_id": quiz["id"], **question, "options": " | ".join(question["options"])}
            for quiz in payload["quizzes"]
            for question in quiz["questions"]
        ]
        archive.writestr("questions.csv", _to_csv(question_rows))

        archive.writestr("answers.csv", _to_csv(payload["answers"]))
        archive.writestr("scores.csv", _to_csv(payload["scores"]))
        for category in EMPTY_CATEGORIES:
            archive.writestr(f"{category}.csv", _to_csv(payload[category]))

    return buffer.getvalue()


def _to_csv(rows: list[dict]) -> str:
    if not rows:
        return ""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()
