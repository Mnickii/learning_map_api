from flask import jsonify, request
from flask_restful import Resource

from ..models import db, Contribution


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

    def put(self, id):
        if not request.json:
            response = jsonify(dict(
                status=400,
                message='Request must be valid JSON first')
                )
            response.status_code = 400
            return response

        data = request.get_json()

        if "status" in data:
            status = data["status"]
            if status.lower() not in ['approved', 'rejected']:
                    response = jsonify(dict(
                        status=400,
                        message='{} is not an acceptable status. '
                        'Status can only be approved or rejected'
                        .format(status))
                        )
                    response.status_code = 400
                    return response

        contribution = Contribution.query.get(id)

        if contribution:
            if "title" in data:
                contribution.title = data["title"]
            else:
                contribution.title = contribution.title
            if "description" in data:
                contribution.description = data["description"]
            else:
                contribution.description = contribution.description
            if "contribution_type_id" in data:
                contribution.contribution_type_id = (
                    data["contribution_type_id"])
            else:
                contribution.contribution_type_id = (contribution
                                                     .contribution_type_id)
            if "status" in data:
                contribution.status = data["status"]
            else:
                contribution.status = contribution.status

            db.session.add(contribution)
            db.session.commit()

            result = contribution.serialize()

            response = jsonify(dict(
                contribution=result,
                status=200,
                message='Contribution was successfully updated'))
            return response
        else:
            response = jsonify(dict(status=404,
                                    message='Contribution does not exist'))
            response.status_code = 404
            return response
