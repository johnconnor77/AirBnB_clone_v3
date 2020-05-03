#!/usr/bin/python3
"""Place module
"""
from flask import abort, jsonify, request
from flask.views import MethodView
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


class PlaceAPI(MethodView):
    """Place Method View
    """

    def get(self, city_id=None, place_id=None):
        """Retrieves the list of all Places objects
        or a single Place object
        """
        if city_id:
            return jsonify(self.get_places(city_id)), 200

        return jsonify(self.get_place(place_id)), 200

    def get_places(self, city_id):
        """Retrieves the list of all Place objects
           at a certain city
        """
        places_list = list()

        if storage.get(City, city_id) is None:
            abort(404)

        places_city = storage.get(City, city_id).places

        for place in places_city:
            places_list.append(place.to_dict())

        return places_list

    def get_place(self, place_id):
        """Retrieves a Place

        If the place_id is not linked to any Place object,
        raise a 404 error
        """

        if place_id is not None:
            all_places = storage.all(Place)

            key = Place.__name__ + "." + place_id

            if all_places.get(key) is None:
                abort(404)

            place = all_places.get(key).to_dict()

            return place

    def post(self, city_id):
        """ Creates a new Place
        """
        req_data = request.get_json()

        is_city = storage.get(City, city_id)

        if is_city is None:
            abort(404)

        if not req_data:
            abort(400, 'Not a JSON')

        if 'user_id' not in req_data:
            abort(400, 'Missing user_id')

        is_user = storage.get(User, req_data.get('user_id'))

        if is_user is None:
            abort(404)

        if 'name' not in req_data:
            abort(400, 'Missing name')

        place = Place(**req_data)
        place.city_id = city_id
        place.save()
        return jsonify(place.to_dict()), 201

    def put(self, place_id):
        """Update a Place
        """
        req_data = request.get_json()

        if not req_data:
            abort(400, 'Not a JSON')

        place_update = storage.get(Place, place_id)

        if place_update is None:
            abort(404)

        check_update = Place(**req_data)
        check_update_dict = check_update.to_dict()

        not_to_update = ["id", "user_id", "city_id", "created_at",
                         "updated_at", "__class__", "__len__"]

        for key, val in check_update_dict.items():
            if key not in not_to_update:
                if val is not None:
                    setattr(place_update, key, val)

        place_update.save()

        return jsonify(place_update.to_dict()), 200

    def delete(self, place_id):
        """Deletes a Place
        """
        json_place = storage.get(Place, place_id)

        if json_place is None:
            abort(404)

        storage.delete(json_place)
        storage.save()
        return jsonify({}), 200


place_view = PlaceAPI.as_view('place_api')

app_views.add_url_rule('/cities/<city_id>/places',
                       view_func=place_view, methods=['GET'],
                       strict_slashes=False)
app_views.add_url_rule('/cities/<city_id>/places', view_func=place_view,
                       methods=['POST'], strict_slashes=False)
app_views.add_url_rule('/places/<place_id>', view_func=place_view,
                       methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
