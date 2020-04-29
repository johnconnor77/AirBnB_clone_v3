#!/usr/bin/python3
"""States module
"""
from flask import abort, jsonify
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


state_view = StateAPI.as_view('state_api')
app_views.add_url_rule('/states/', defaults={'state_id': None},
                       view_func=state_view, methods=['GET'])
app_views.add_url_rule('/states/<state_id>', view_func=state_view,
                       methods=['GET'])
