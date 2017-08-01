from flask import jsonify, request
from flask_restful import Resource

from ..models import Contribution


class ContributionsResource(Resource):

    def get(self):

        if request.args.get('user'):
            user_id = request.args.get('user', type=str)

            # fetch user contributions from database
            user_contributions = Contribution.query.filter_by(
                user_id=user_id).all()
            if not user_contributions:
                return jsonify(dict(status=200,
                                    message='You do not have any '
                                    'contributions yet'))

            # initialize user contributions list
            user_contributions_serialized = []

            for contribution in user_contributions:
                # serialize contribution
                user_contribution_serialized = contribution.serialize()

                # add contribution_type key to contribution
                user_contribution_serialized['contribution_type'] = \
                    contribution.contribution_type.name

                # add tags key to contribution if contribution is resource or
                # idea
                if contribution.contribution_type.name.upper() in \
                        ['IDEA', 'RESOURCE']:
                    user_contribution_serialized['tags'] = [
                        tag.serialize() for tag in contribution.tags
                    ]

                # append to serialized user_contributions list
                user_contributions_serialized.append(
                    user_contribution_serialized)

            return jsonify(dict(status=200,
                                contributions=user_contributions_serialized))
