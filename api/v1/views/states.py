#!/usr/bin/python3
"""States module
"""
from flask import abort, jsonify, request
from flask.views import MethodView
from api.v1.views import app_views
from models import storage
from models.state import State


class StateAPI(MethodView):
    """State Method View
    """

    def get(self, state_id):
        """Retrieves the list of all State objects
        or a single State object
        """
        if state_id:
            return jsonify(self.get_state(state_id)), 200

        return jsonify(self.get_states()), 200

    def get_states(self):
        """Retrieves the list of all State objects
        """
        states_list = list()
        states = storage.all(State).values()

        for state in states:
            states_list.append(state.to_dict())

        return states_list

    def get_state(self, state_id):
        """Retrieves a State

        If the state_id is not linked to any State object,
        raise a 404 error
        """
        state = storage.get(State, state_id)

        if state is None:
            abort(404)

        return state.to_dict()

    def post(self):
        """Creates a State
        """
        req_data = request.get_json()

        if not req_data:
            abort(400, 'Not a JSON')

        if 'name' not in req_data:
            abort(400, 'Missing name')

        state = State(**req_data)
        state.save()
        return jsonify(state.to_dict()), 201

    def put(self, state_id):
        """Update a State
        """
        req_data = request.get_json()

        if not req_data:
            abort(400, 'Not a JSON')

        key = State.__name__ + "." + state_id
        all_states = storage.all(State)
        state_update = all_states.get(key)

        if state_update is None:
            abort(404)

        state_update.name = req_data.get('name')
        storage.save()
        return jsonify(state_update.to_dict()), 200

    def delete(self, state_id):
        """Deletes a State
        """
        json_states = storage.get(State, state_id)

        if json_states is None:
            abort(404)

        storage.delete(json_states)
        storage.save()
        return jsonify(empty_dict), 200


state_view = StateAPI.as_view('state_api')
app_views.add_url_rule('/states/', defaults={'state_id': None},
                       view_func=state_view, methods=['GET'],
                       strict_slashes=False)
app_views.add_url_rule('/states/', view_func=state_view, methods=['POST'],
                       strict_slashes=False)
