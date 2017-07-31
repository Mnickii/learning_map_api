import uuid

from flask import request, jsonify
from flask_restful import Resource

from ..models import db, Contribution, ContributionType, Tag
try:
    from api.helpers import validate_type
except ModuleNotFoundError:
    from learning_map_api.api.helpers import validate_type

class ContributionsResource(Resource):

    def get(self):
        user_id = 'user_id'
        _user_contributions = Contribution.query.filter_by(user_id=user_id).all()
        if not _user_contributions:
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
    
    def post(self):
        user_id = 'user_id'
        if not request.json:
            return {"message": "Request must be a valid JSON"}, 400

        if not validate_type(user_id, str):
             return {"message": "user_id must be a valid string"}, 400

        if request.get_json():
            result = request.get_json()
            keys = ["title", "description", "tags", "type"]

            for key in keys:
                if key is not "tags" and key not in result:
                    return {"message": key + " cannot be null"}, 400
                elif (key in ["title", "description", "type"]) and not validate_type(result[key], str):
                    return {"message": key + " must be a valid string"}, 400
                elif (key is "tags" and key in result) and not validate_type(result[key], list):
                    return {"message": key + " must be a list"}, 400
        
            contribution_type = ContributionType.query.filter_by(id=result["type"]).first()           
            if not contribution_type:
                return {"message": "type must be of resource, idea or skill"}, 400
        
            contribution_type_id =  contribution_type.id

            generated_id = uuid.uuid4().hex

            new_contribution = Contribution(
                id=generated_id,
                title=result["title"],
                description=result["description"],
                user_id=user_id,
                contribution_type_id=contribution_type_id,
            )
            db.session.add(new_contribution)
            db.session.commit()

            contribution_serialized = new_contribution.serialize()
            
            if "tags" in result:
                for contribution_tag in result["tags"]:
                    valid_tag = Tag.query.filter_by(id=contribution_tag).first()
                    if not valid_tag:
                        return {"message": "{} is not a valid tag".format(contribution_tag)}, 400
                    new_contribution.tags.append(valid_tag)
                contribution_serialized["tags"] = [tag.serialize()
                                            for tag in new_contribution.tags]

            response = jsonify(dict(data=contribution_serialized))
            response.status_code = 201

            return response
