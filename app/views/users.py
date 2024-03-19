from app import app
from app.db import db
from app.models import User
from flask import request, Response
from http import HTTPStatus
import json


@app.post("/user/create")
def user_create():
    data = request.get_json()
    username = data["username"]
    email = data["email"]
    password = data["password"]
    if User.is_unique_email(email):
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        response_data = {
            "message": "User created successfully",
            "user_id": user.id,
        }
        return Response(
            response=json.dumps(response_data),
            status=HTTPStatus.CREATED,
            content_type="application/json",
        )
    else:
        response_data = {
            "error": "Email address is not unique",
        }
        return Response(
            response=json.dumps(response_data),
            status=HTTPStatus.CONFLICT,
            content_type="application/json",
        )


@app.get("/user/<int:user_id>")
def user_get(user_id):
    if User.is_valid_id(user_id):
        user = (
            db.session.execute(db.select(User).where(User.id == user_id))
            .scalars()
            .all()[0]
        )
        response_data = user.to_dict()
        return Response(
            response=json.dumps(response_data),
            status=HTTPStatus.OK,
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


@app.patch("/user/<int:user_id>/edit")
def user_edit(user_id: int):
    data = request.get_json()
    if User.is_valid_id(user_id):
        # if user want to change email we must check that it's unique.
        # if there's no new email in data, or there's a new email, and it's unique then everything is OK.
        # we just set new attrs.
        # if there's a not unique email in data we raise error CONFLICT and don't commit any changes
        if ("email" not in data) or (
            "email" in data and User.is_unique_email(data["email"])
        ):
            user = (
                db.session.execute(db.select(User).where(User.id == user_id))
                .scalars()
                .all()[0]
            )
            # here we edit user's info. but because we don't know what he wants to edit we use setattr and extra logic
            for key in data:
                # we can't change user's id, and it couldn't be in data
                if key != "id":
                    # check that user has this attr, so we can change it
                    if hasattr(user, key):
                        setattr(user, key, data[key])
            db.session.commit()
            response_data = user.to_dict()
            return Response(
                response=json.dumps(response_data),
                status=HTTPStatus.OK,
                content_type="application/json",
            )
        else:
            response_data = {"error": "Email address is not unique"}
            return Response(
                response=json.dumps(response_data),
                status=HTTPStatus.CONFLICT,
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
