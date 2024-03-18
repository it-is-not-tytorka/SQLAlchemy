from app import app
from app.db import db
from app.models import User, Friend, Note
from flask import request, Response
from http import HTTPStatus
import json


@app.post("/user/<int:user_id>/note/create")
def note_create(user_id):
    if User.is_valid_id(user_id):
        data = request.get_json()
        friend_id = data["friend_id"]
        if Friend.is_valid_id(friend_id):
            score = data["score"]
            if Note.is_valid_score(score):
                note = Note(
                    user_id=user_id,
                    friend_id=friend_id,
                    description=data["description"],
                    score=score,
                )
                friend = (
                    db.session.execute(
                        db.select(Friend).where(Friend.id == friend_id)
                    )
                    .scalars()
                    .all()[0]
                )
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


@app.get("/note/<int:note_id>")
def note_get(note_id):
    if Note.is_valid_id(note_id):
        note = db.session.execute(
            db.select(Note).where(Note.id == note_id)
        ).scalars().all()
        response_data = note[0].to_dict()
        return Response(
            response=json.dumps(response_data),
            status=HTTPStatus.OK,
            content_type="application/json",
        )
    else:
        response_data = {
            "error": "No note found with the provided ID",
        }
        return Response(
            response=json.dumps(response_data),
            status=HTTPStatus.NOT_FOUND,
            content_type="application/json",
        )



@app.post("/note/<int:note_id>/edit")
def note_edit(note_id):
    if Note.is_valid_id(note_id):
        note = db.session.execute(
            db.select(Note).where(Note.id == note_id)
        ).scalars().all()
        note = note[0]
        data = request.get_json()
        # in a note we can change only description and score
        for key in data:
            if key == 'description':
                note.description = data['description']
            elif key == "score":
                # first of all we need to remove old friend's score and add new
                Friend.change_sum_of_notes(note.friend_id, data["score"] - note.score)
                # now we can change note's score
                note.score = data["score"]
        db.session.commit()
        response_data = note.to_dict()
        return Response(
            response=json.dumps(response_data),
            status=HTTPStatus.OK,
            content_type="application/json",
        )
    else:
        response_data = {
            "error": "No note found with the provided ID",
        }
        return Response(
            response=json.dumps(response_data),
            status=HTTPStatus.NOT_FOUND,
            content_type="application/json",
        )


@app.delete("/note/<int:note_id>/delete")
def note_delete(note_id):
    if Note.is_valid_id(note_id):
        note = db.session.execute(
            db.select(Note).where(Note.id == note_id)
        ).scalars().all()
        note = note[0]
        Friend.change_sum_of_notes(note.friend_id, -note.score)
        Friend.change_count_notes(note.friend_id, -1)
        note.remove()
        db.session.commit()
        response_data = {
            "message": "Note has been deleted successfully",
        }
        return Response(
            response=json.dumps(response_data),
            status=HTTPStatus.OK,
            content_type="application/json",
        )
    else:
        response_data = {
            "error": "No note found with the provided ID",
        }
        return Response(
            response=json.dumps(response_data),
            status=HTTPStatus.NOT_FOUND,
            content_type="application/json",
        )


@app.get("/note/<int:note_id>/restore")
def note_restore(note_id):
    if Note.is_valid_id(note_id):
        note = db.session.execute(
            db.select(Note).where(Note.id == note_id)
        ).scalars().all()[0]
        note.restore()
        Friend.change_count_notes(note.friend_id, 1)
        Friend.change_sum_of_notes(note.friend_id, note.score)
        db.session.commit()
        response_data = note.to_dict()
        return Response(
            response=json.dumps(response_data),
            status=HTTPStatus.OK,
            content_type="application/json",
        )
    else:
        response_data = {"error": "No note found with the provided ID"}
        return Response(
            response=json.dumps(response_data),
            status=HTTPStatus.NOT_FOUND,
            content_type="application/json",
        )