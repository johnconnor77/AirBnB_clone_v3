#!/usr/bin/python3
"""City module
"""
from flask import abort, jsonify, request
from flask.views import MethodView
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


class CityAPI(MethodView):
    """City Method View
    """

    def get(self, state_id=None, city_id=None):
        """Retrieves the list of all State objects
        or a single State object
        """
        if state_id:
            return jsonify(self.get_cities(state_id)), 200

        return jsonify(self.get_city(city_id)), 200

    def get_cities(self, state_id):
        """Retrieves the list of all City objects
        """
        cities_list = list()

        if storage.get(State, state_id) is None:
            abort(404)

        cities_state = storage.get(State, state_id).cities

        for city in cities_state:
            cities_list.append(city.to_dict())

        return cities_list

    def get_city(self, city_id):
        """Retrieves a City

        If the city_id is not linked to any City object,
        raise a 404 error
        """
        if city_id is not None:
            all_cities = storage.all(City)

            key = City.__name__ + "." + city_id

            if all_cities.get(key) is None:
                abort(404)
            city = all_cities.get(key).to_dict()

            return city
        

city_view = CityAPI.as_view('city_api')

app_views.add_url_rule('/states/<state_id>/cities',
                       view_func=city_view, methods=['GET'],
                       strict_slashes=False)

app_views.add_url_rule('/cities/<city_id>', view_func=city_view,
                       methods=['GET'], strict_slashes=False)


