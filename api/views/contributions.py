from flask import jsonify
from flask_restful import Resource

from ..models import Resource as Resources, Skill, Idea


class UserContributionsResource(Resource):

    def get(self, user_id):

        # fetch user contributions from database
        user_resources = Resources.query.filter_by(
            owner_id=user_id).all()
        user_ideas = Idea.query.filter_by(owner_id=user_id).all()
        user_skills = Skill.query.filter_by(owner_id=user_id).all()

        # return message if user does not have contributions
        if (not user_resources and not user_ideas and not user_skills):
            response = jsonify(dict(status=200,
                                    message='You do not have any '
                                    'contributions yet'))
            return response

        # initialize contributions list
        contributions = []

        for resource in user_resources:
            # serialize resource
            user_resource_serialized = resource.serialize()

            # add extra keys to serialized resource
            user_resource_serialized['category'] = 'resource'
            user_resource_serialized['tags'] = [
                tag.serialize() for tag in resource.tags]
            user_resource_serialized['links'] = [
                link.serialize() for link in resource.links]

            # append resource to contributions list
            contributions.append(user_resource_serialized)

        for idea in user_ideas:
            # serialize idea
            user_idea_serialized = idea.serialize()

            # add extra keys to serialized idea
            user_idea_serialized['category'] = 'idea'
            user_idea_serialized['tags'] = [
                tag.serialize() for tag in idea.tags]

            # append idea to contributions list
            contributions.append(user_idea_serialized)

        for skill in user_skills:
            # serialize skill
            user_skill_serialized = skill.serialize()

            # add category key to serialized skill
            user_skill_serialized['category'] = 'skill'

            # append skill to contributions list
            contributions.append(user_skill_serialized)

        # format response
        response = jsonify(dict(status=200, contributions=contributions))

        return response
