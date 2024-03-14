from sqlalchemy import desc

from app import app
from app.db import db
from app.models import User, Friend
from flask import request, Response
from http import HTTPStatus
import json


@app.post("/user/<int:user_id>/friend/create")
def friend_create(user_id):
    data = request.get_json()
    name = data["name"]
    description = data["description"]
    if User.is_valid_id(user_id):
        friend = Friend(user_id=user_id, name=name, description=description)
        db.session.add(friend)
        db.session.commit()
        response_data = friend.to_dict()
        return Response(
            response=json.dumps(response_data),
            status=HTTPStatus.CREATED,
            content_type="application/json",
        )
    else:
        response_data = {"error": "No friend found with the provided ID"}
        return Response(
            response=json.dumps(response_data),
            status=HTTPStatus.NOT_FOUND,
            content_type="application/json",
        )


@app.get("/user/<int:user_id>/friend/<int:friend_id>")
def friend_get(user_id, friend_id):
    if User.is_valid_id(user_id):
        if Friend.is_valid_id(friend_id):
            friend = (
                db.session.execute(
                    db.select(Friend).where(
                        Friend.id == friend_id and Friend.user_id == user_id
                    )
                )
                .scalars()
                .all()
            )
            if friend:
                response_data = friend[0].to_dict()
                return Response(
                    response=json.dumps(response_data),
                    status=HTTPStatus.OK,
                    content_type="application/json",
                )
            else:
                response_data = {
                    "error": "User with the provided ID doesn't have friend with the provided friendID"
                }
                return Response(
                    response=json.dumps(response_data),
                    status=HTTPStatus.NOT_FOUND,
                    content_type="application/json",
                )
        else:
            response_data = {"error": "No friend found with the provided ID"}
            return Response(
                response=json.dumps(response_data),
                status=HTTPStatus.NOT_FOUND,
                content_type="application/json",
            )
    else:
        response_data = {"error": "No user found with the provided ID"}
        return Response(
            response=json.dumps(response_data),
            status=HTTPStatus.NOT_FOUND,
            content_type="application/json",
        )


@app.get("/user/<int:user_id>/friend/all")
def friend_get_all(user_id):
    if User.is_valid_id(user_id):
        friends = (
            db.session.execute(
                db.select(Friend)
                .where(Friend.user_id == user_id)
                .order_by(desc(Friend.count_notes))
            )
            .scalars()
            .all()
        )
        response_data = [friend.to_dict() for friend in friends]
        return Response(
            response=json.dumps(response_data),
            status=HTTPStatus.OK,
            content_type="application/json",
        )
    else:
        response_data = {"error": "No user found with the provided ID"}
        return Response(
            response=json.dumps(response_data),
            status=HTTPStatus.NOT_FOUND,
            content_type="application/json",
        )


@app.post("/user/<int:user_id>/friend/<int:friend_id>/edit")
def friend_edit(user_id, friend_id):
    data = request.get_json()
    if User.is_valid_id(user_id):
        if Friend.is_valid_id(friend_id):
            friend = (
                db.session.execute(
                    db.select(Friend).where(
                        Friend.id == friend_id and User.id == user_id
                    )
                )
                .scalars()
                .all()[0]
            )
            for key in data:
                # we can't change id, user_id and rating of a friend, so we don't touch it
                if key != "id" and key != "user_id" and key != "rating":
                    if hasattr(
                        friend, key
                    ):  # check if friend has an attr, so we can change it
                        setattr(friend, key, data[key])
            db.session.commit()
            response_data = friend.to_dict()
            return Response(
                response=json.dumps(response_data),
                status=HTTPStatus.OK,
                content_type="application/json",
            )
        else:
            response_data = {"error": "No friend found with the provided ID"}
            return Response(
                response=json.dumps(response_data),
                status=HTTPStatus.NOT_FOUND,
                content_type="application/json",
            )
    else:
        response_data = {"error": "No user found with the provided ID"}
        return Response(
            response=json.dumps(response_data),
            status=HTTPStatus.NOT_FOUND,
            content_type="application/json",
        )


@app.delete("/user/<int:user_id>/friend/<int:friend_id>/delete")
def friend_delete(user_id, friend_id):
    if User.is_valid_id(user_id):
        if Friend.is_valid_id(friend_id):
            friend = (
                db.session.execute(
                    db.select(Friend).where(
                        Friend.id == friend_id and Friend.user_id == user_id
                    )
                )
                .scalars()
                .all()
            )
            db.session.delete(friend[0])
            db.session.commit()
            response_data = {"message": "User has been deleted successfully"}
            return Response(
                response=json.dumps(response_data),
                status=HTTPStatus.OK,
                content_type="application/json",
            )
        else:
            response_data = {"error": "No friend found with the provided ID"}
            return Response(
                response=json.dumps(response_data),
                status=HTTPStatus.NOT_FOUND,
                content_type="application/json",
            )
    else:
        response_data = {"error": "No user found with the provided ID"}
        return Response(
            response=json.dumps(response_data),
            status=HTTPStatus.NOT_FOUND,
            content_type="application/json",
        )
