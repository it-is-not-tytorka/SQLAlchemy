from app import app
from app.db import db
from app.models import User, Friend
from flask import request, Response
from sqlalchemy import desc, case
from http import HTTPStatus
import json


@app.post("/user/<int:user_id>/friend/create")
def friend_create(user_id):
    if User.is_valid_id(user_id):
        data = request.get_json()
        name = data["name"]
        description = data["description"]
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
        response_data = {"error": "No user found with the provided ID"}
        return Response(
            response=json.dumps(response_data),
            status=HTTPStatus.NOT_FOUND,
            content_type="application/json",
        )


@app.get("/friend/<int:friend_id>")
def friend_get(friend_id):
    if Friend.is_valid_id(friend_id):
        friend = (
            db.session.execute(
                db.select(Friend).where(
                    (Friend.id == friend_id) & (Friend.deleted == 0)
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
            response_data = {"error": "Friend with the provided ID was deleted"}
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


@app.get("/user/<int:user_id>/friend/all")
def friend_get_all(user_id):
    if User.is_valid_id(user_id):
        data = request.get_json()
        order_method = ""
        if "order_by" in data:
            if data["order_by"] == "name":
                order_method = Friend.name
            elif data["order_by"] == "count_notes":
                order_method = Friend.count_notes
        # if we got request 'order_by': name or count_notes we send query to database
        if order_method:
            friends = (
                db.session.execute(
                    db.select(Friend)
                    .where((Friend.user_id == user_id) & (Friend.deleted == 0))
                    .order_by(
                        order_method
                        if order_method == Friend.name
                        else desc(order_method)
                    )
                )
                .scalars()
                .all()
            )
        # default method if user didn't choose order by name or count_notes
        # order by rating. rating = sum_of_notes/count_notes if count_notes > 0. if a friend doesn't have notes,
        # count_notes = 0 we can't divide on 0, so, we just return 0. because of this we use CASE
        else:
            rating = case(
                ((Friend.count_notes > 0, Friend.sum_of_notes / Friend.count_notes)),
                else_=0,
            ).label("rating")
            friends = (
                db.session.execute(
                    db.select(Friend, rating.label("rating"))
                    .where((Friend.user_id == user_id) & (Friend.deleted == 0))
                    .order_by(desc(rating))
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


@app.patch("/friend/<int:friend_id>/edit")
def friend_edit(friend_id):
    data = request.get_json()
    if Friend.is_valid_id(friend_id):
        friend = (
            db.session.execute(db.select(Friend).where(Friend.id == friend_id))
            .scalars()
            .all()[0]
        )
        if friend.deleted == 0:
            for key in data:
                # we can change only user's description and his name
                if key == "description":
                    setattr(friend, key, data[key])
                elif key == "name":
                    setattr(friend, key, data[key])
            db.session.commit()
            response_data = friend.to_dict()
            return Response(
                response=json.dumps(response_data),
                status=HTTPStatus.OK,
                content_type="application/json",
            )
        else:
            response_data = {"error": "Friend with the provided ID was deleted"}
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


@app.delete("/friend/<int:friend_id>/delete")
def friend_delete(friend_id):
    if Friend.is_valid_id(friend_id):
        friend = (
            db.session.execute(db.select(Friend).where(Friend.id == friend_id))
            .scalars()
            .all()
        )[0]
        if friend.deleted == 0:
            friend.remove()
            db.session.commit()
            response_data = {"message": "Friend has been deleted successfully"}
            return Response(
                response=json.dumps(response_data),
                status=HTTPStatus.OK,
                content_type="application/json",
            )
        else:
            response_data = {"error": "Friend with the provided ID was deleted"}
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


@app.put("/friend/<int:friend_id>/restore")
def friend_restore(friend_id):
    if Friend.is_valid_id(friend_id):
        friend = (
            db.session.execute(db.select(Friend).where(Friend.id == friend_id))
            .scalars()
            .all()[0]
        )
        friend.restore()
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
