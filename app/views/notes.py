from app import app
from app.db import db
from app.models import User
from flask import request, Response
from http import HTTPStatus
import json

@app.post("/user/<int:user_id>/note")
def note_create(user_id):
    if User.is_valid_id(user_id):
        data = request.get_json()

    else:
        response_data = {
            "error": "No user found with the provided ID",
        }
        return Response(
            response=json.dumps(response_data),
            status=HTTPStatus.NOT_FOUND,
            content_type="application/json",
        )