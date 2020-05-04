#!/usr/bin/python3
"""Review module
"""
from flask import abort, jsonify, request
from flask.views import MethodView
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


class ReviewAPI(MethodView):
    """Review Method View
    """
    def get(self, place_id=None, review_id=None):
        """Retrieves the list of all Review objects
        or a single Review object
        """
        if place_id:
            return jsonify(self.get_reviews(place_id)), 200

        return jsonify(self.get_review(review_id)), 200

    def get_reviews(self, place_id):
        """Retrieves the list of all Reviews objects
        of a Place
        """
        reviews_list = list()
        place = storage.get(Place, place_id)

        if place is None:
            abort(404)

        reviews_place = place.reviews

        for review in reviews_place:
            reviews_list.append(review.to_dict())

        return reviews_list

    def get_review(self, review_id):
        """Retrieves a Review

        If the review_id is not linked to any Place object,
        raise a 404 error
        """
        review = storage.get(Review, review_id)

        if review is None:
            abort(404)

        return review.to_dict()

    def post(self, place_id):
        """Creates a new Review
        """
        place = self.get_place(place_id)
        req = self.check_request_format(request)

        if 'user_id' not in req:
            abort(400, 'Missing user_id')

        user = self.get_user(req.get('user_id'))

        if 'text' not in req:
            abort(400, 'Missing text')

        review = Review(**req)
        review.place_id = place_id
        review.user_id = user.id
        review.save()
        return jsonify(review.to_dict()), 201

    def get_place(self, place_id):
        """Get a Place
        """
        place = storage.get(Place, place_id)

        if place is None:
            abort(404)

        return place

    def get_user(self, user_id):
        """Get an User
        """
        user = storage.get(User, user_id)

        if user is None:
            abort(404)

        return user

    def check_request_format(self, request):
        """Checks the format of the request
        """
        req_data = request.get_json()

        if not req_data:
            abort(400, 'Not a JSON')

        return req_data

    def put(self, review_id):
        """Update a Review
        """
        review = storage.get(Review, review_id)

        if review is None:
            abort(404)

        req = self.check_request_format(request)
        req_text = req.get('text')

        if req_text is not None:
            review.text = req_text

        review.save()
        return jsonify(review.to_dict()), 200

    def delete(self, review_id):
        """Deletes a Review
        """
        json_reviews = storage.get(Review, review_id)

        if json_reviews is None:
            abort(404)

        storage.delete(json_reviews)
        storage.save()
        return jsonify({}), 200


review_view = ReviewAPI.as_view('review_api')
app_views.add_url_rule('/places/<place_id>/reviews',
                       view_func=review_view, methods=['GET'],
                       strict_slashes=False)
app_views.add_url_rule('/places/<place_id>/reviews', view_func=review_view,
                       methods=['POST'], strict_slashes=False)
app_views.add_url_rule('/reviews/<review_id>', view_func=review_view,
                       methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
