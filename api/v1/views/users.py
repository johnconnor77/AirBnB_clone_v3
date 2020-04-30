#!/usr/bin/python3
"""Users module
"""
from flask import abort, jsonify, request
from flask.views import MethodView
from api.v1.views import app_views
from models import storage
from models.user import User


class UserAPI(MethodView):
    """User Method View
    """

    def get(self, user_id):
        """Retrieves the list of all User objects
        or a single User object
        """
        if user_id:
            return jsonify(self.get_user(user_id)), 200

        return jsonify(self.get_users()), 200

    def get_users(self):
        """Retrieves the list of all User objects
        """
        users_list = list()
        users = storage.all(User).values()

        for user in users:
            users_list.append(user.to_dict())

        return users_list

    def get_user(self, user_id):
        """Retrieves an User

        If the user_id is not linked to any User object,
        raise a 404 error
        """
        user = storage.get(User, user_id)

        if user is None:
            abort(404)

        return user.to_dict()

    def post(self):
        """Creates an User
        """
        req_data = request.get_json()

        if not req_data:
            abort(400, 'Not a JSON')

        if 'email' not in req_data:
            abort(400, 'Missing email')

        if 'password' not in req_data:
            abort(400, 'Missing password')

        user = User(**req_data)
        user.save()
        return jsonify(user.to_dict()), 201

    def put(self, user_id):
        """Update an User
        """
        req_data = request.get_json()

        if not req_data:
            abort(400, 'Not a JSON')

        key = User.__name__ + "." + user_id
        all_users = storage.all(User)
        user_update = all_users.get(key)

        if user_update is None:
            abort(404)

        user_update.email = req_data.get('email')
        user_update.password = req_data.get('password')
        storage.save()
        return jsonify(user_update.to_dict()), 200

    def delete(self, user_id):
        """Deletes an User
        """
        json_users = storage.get(User, user_id)

        if json_users is None:
            abort(404)

        storage.delete(json_users)
        storage.save()
        return jsonify({}), 200


user_view = UserAPI.as_view('user_api')
app_views.add_url_rule('/users/', defaults={'user_id': None},
                       view_func=user_view, methods=['GET'],
                       strict_slashes=False)
app_views.add_url_rule('/users/', view_func=user_view, methods=['POST'],
                       strict_slashes=False)
app_views.add_url_rule('/users/<user_id>', view_func=user_view,
                       methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
