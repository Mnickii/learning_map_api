from flask import jsonify
from flask_restful import Resource

from ..models import Contribution


class ContributionsResource(Resource):

    def get(self, user_id):

        _user_contributions = Contribution.query.filter_by(user_id=user_id).all()
        if not user_contributions:
            return jsonify(dict(status=200,
                                    message='You do not have any '
                                    'contributions yet'))

        user_contributions = [c.serialize for c in _user_contributions]
        # for resource in user_resources:
        #     # serialize resource
        #     user_resource_serialized = resource.serialize()
        #
        #     # add extra keys to serialized resource
        #     user_resource_serialized['category'] = 'resource'
        #     user_resource_serialized['tags'] = [
        #         tag.serialize() for tag in resource.tags]
        #     user_resource_serialized['links'] = [
        #         link.serialize() for link in resource.links]
        #
        #     # append resource to contributions list
        #     contributions.append(user_resource_serialized)
        return jsonify(dict(status=200, contributions=contributions))
