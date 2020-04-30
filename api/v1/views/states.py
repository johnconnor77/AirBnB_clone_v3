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
            return jsonify(self.get_state(state_id))

        return jsonify(self.get_states())

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

    def delete(self, state_id):
        """Deletes a State
        """
        empty_dict = {}
        print("Entre al delete")

        try:
            json_states = storage.get(State, state_id)
            storage.delete(json_states)
            storage.save()
            return jsonify(empty_dict), 200
        except Exception:
            abort(404)

    def put(self, state_id):
        """Update a State
        """
        print("Entre al put")
        req_data = request.get_json()

        if not req_data:
            abort(400, 'Not a JSON')

        print("Put entra")
        key = State.__name__ + "." + state_id
        print(key)
        all_states = storage.all(State)
        state_update = all_states.get(key)

        if state_update is None:
            abort(404)

        state_update.name = req_data['name']
        state_update.save()
        return jsonify(state_update.to_dict()), 200


state_view = StateAPI.as_view('state_api')
app_views.add_url_rule('/states/', defaults={'state_id': None},
                       view_func=state_view, methods=['GET'])
app_views.add_url_rule('/states/<state_id>', view_func=state_view,
                       methods=['GET', 'PUT', 'DELETE'])
