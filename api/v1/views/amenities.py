#!/usr/bin/python3
"""Amenity module
"""
from flask import abort, jsonify, request
from flask.views import MethodView
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


class AmenityAPI(MethodView):
    """Amenity Method View
    """

    def get(self, amenity_id):
        """Retrieves the list of all Amenity objects
        or a single Amenity object
        """
        if amenity_id:
            return jsonify(self.get_amenity(amenity_id)), 200

        return jsonify(self.get_amenities()), 200

    def get_amenities(self):
        """Retrieves the list of all Amenity objects
        """
        amenities_list = list()
        amenities = storage.all(Amenity).values()

        for amenity in amenities:
            amenities_list.append(amenity.to_dict())

        return amenities_list

    def get_amenity(self, amenity_id):
        """Retrieves an Amenity

        If the amenity_id is not linked to any Amenity object,
        raise a 404 error
        """
        amenity = storage.get(Amenity, amenity_id)

        if amenity is None:
            abort(404)

        return amenity.to_dict()

    def post(self):
        """Creates an Amenity
        """
        req_data = request.get_json()

        if not req_data:
            abort(400, 'Not a JSON')

        if 'name' not in req_data:
            abort(400, 'Missing name')

        amenity = Amenity(**req_data)
        amenity.save()
        return jsonify(amenity.to_dict()), 201

    def put(self, amenity_id):
        """Update an Amenity
        """
        req_data = request.get_json()

        if not req_data:
            abort(400, 'Not a JSON')

        key = Amenity.__name__ + "." + amenity_id
        all_amenities = storage.all(Amenity)
        amenity_update = all_amenities.get(key)

        if amenity_update is None:
            abort(404)

        amenity_update.name = req_data.get('name')
        storage.save()
        return jsonify(amenity_update.to_dict()), 200

    def delete(self, amenity_id):
        """Deletes an Amenity
        """
        json_amenities = storage.get(Amenity, amenity_id)

        if json_amenities is None:
            abort(404)

        storage.delete(json_amenities)
        storage.save()
        return jsonify({}), 200


amenity_view = AmenityAPI.as_view('amenity_api')
app_views.add_url_rule('/amenities/', defaults={'amenity_id': None},
                       view_func=amenity_view, methods=['GET'],
                       strict_slashes=False)
app_views.add_url_rule('/amenities/', view_func=amenity_view, methods=['POST'],
                       strict_slashes=False)
app_views.add_url_rule('/amenities/<amenity_id>', view_func=amenity_view,
                       methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
