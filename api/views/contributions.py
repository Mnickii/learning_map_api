from flask import jsonify
from flask_restful import Resource

from ..models import Contribution


class ContributionsResource(Resource):

    def get(self):
        # fetch all contributions
        get_contributions = Contribution.query.order_by(
            Contribution.created_at.desc())

        if not get_contributions:
            return jsonify(dict(status=200,
                                message='You do not have any contributions yet'))

        # initialize empty list to append contributions
        contributions = []

        for contribution in get_contributions:

            # serialize all contributions
            all_contributions = contribution.serialize()

            # add contribution_type field
            all_contributions['contribution_type'] = contribution.contribution_type.name

            # add tags to resource and idea contributions
            if contribution.contribution_type.name.upper() in ['IDEA', 'RESOURCE']:
                all_contributions['tags'] = [tag.serialize()
                                             for tag in contribution.tags]

            # append serialized contributions to contributions list
            contributions.append(all_contributions)

        return jsonify(dict(status=200, contributions=contributions))
