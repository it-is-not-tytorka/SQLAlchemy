from app import app
from app.db import db
from app.models import User, Friend, Note
from flask import request, Response
from http import HTTPStatus
import json

@app.post("/user/<int:user_id>/note")
def note_create(user_id):
    if User.is_valid_id(user_id):
        data = request.get_json()
        friend_id = data["friend_id"]
        if Friend.is_valid_id(friend_id):
            score = data["score"]
            if Note.is_valid_score(score):
                note = Note(user_id=user_id, friend_id=friend_id, description=data["description"], score=score)
                friend = db.session.execute(
                    db.select(Friend).where(Friend.id == friend_id and Friend.user_id == user_id)
                ).scalars().all()[0]
                friend.count_notes += 1
                friend.sum_of_notes += data["score"]
                db.session.add(note)
                db.session.commit()
                response_data = note.to_dict()
                return Response(
                    response=json.dumps(response_data),
                    status=HTTPStatus.OK,
                    content_type="application/json",
                )
            else:
                response_data = {
                    "error": "Not valid score",
                }
                return Response(
                    response=json.dumps(response_data),
                    status=HTTPStatus.BAD_REQUEST,
                    content_type="application/json",
                )
        else:
            response_data = {
                "error": "No friend found with the provided ID",
            }
            return Response(
                response=json.dumps(response_data),
                status=HTTPStatus.NOT_FOUND,
                content_type="application/json",
            )
    else:
        response_data = {
            "error": "No user found with the provided ID",
        }
        return Response(
            response=json.dumps(response_data),
            status=HTTPStatus.NOT_FOUND,
            content_type="application/json",
        )