from flask import request, jsonify
from flask_restful import Resource

from ..models import db, Path


class PathResource(Resource):
    """
    Contains endpoints for path CRUD operations.
    """
        
    def post(self):
        """
        To create a learning path
        """
        payload = request.get_json()
        if payload:
            # check if the params named name and description exist
            if "name" not in payload.keys() or "description" not in payload.keys():
                return {"error": "The parameters name and description are required."}, 400

            name = payload["name"]
            description = payload["description"]

            # check if name or description are null
            if not name or not description:
                return {"error": "Name and description are required to create a path."}, 400

            if Path.query.filter_by(name=name).first():
                # prevent instances of duplicate path names
                return {"error": "A Path with the name {} exists.".format(name)}, 409
            path = Path(
                id=payload["id"],
                name=name.lower(),
                description=description
            )
            db.session.add(path)
            db.session.commit()
            return {
                "data": path.serialize(),
                "success": "Path succesfully created."
            }, 201
        else:
            return {"error": "The parameters name and description must be provided to create a path."}, 400

    def get(self, path_id=None):
        """
        To fetch all paths or a single one (if id is provided)
        """
        if path_id:
            # if an id is passed, query for path with that id
            path = Path.query.filter_by(id=path_id).first()
            if path:
                return jsonify({
                    "success": "Path fetched successfully.",
                    "data": path.serialize()
                })
            else:
                response = jsonify({"error": "Path does not exist."})
                response.status_code = 404
                return response
        else:
            # fetch all paths
            paths = Path.query.all()
            if paths:
                return jsonify({
                    "success": "All paths fetched successfully.",
                    "data": [path.serialize() for path in paths],
                    "count": len(paths)
                })
            else:
                return jsonify({
                    "data": [],
                    "count": 0
                })

    def put(self, path_id=None):
        """
        To update a path.
        """
        payload = request.get_json()

        if payload:    
            if not path_id:
                # if id is not passed
                return {"error": "Path id must be provided."}, 400

            # if an id is passed, query for path with that id
            path = Path.query.filter_by(id=path_id).first()
            if not payload["name"].strip():
                return jsonify({
                    "error": "Name cannot be empty"
                })
            if path:
                # if path exists update
                name = payload.get("name")
                description = payload.get("description")
                if name:
                    path.name = payload["name"].strip()
                if description:
                    path.description = payload["description"].strip()

                db.session.add(path)
                db.session.commit()
                
                response = jsonify({
                    "data": path.serialize(),
                    "success": "Path updated successfully."
                })
                response.status_code = 200
            else:
                response = jsonify({"error": "Path does not exist."})
                response.status_code = 404
            return response

    def delete(self, path_id=None):
        """
        To delete path
        """
        if not path_id:
            # if id is not passed
            return {"error": "Path id must be provided."}, 400
        
        path = Path.query.get(path_id)
        if path:
            db.session.delete(path)
            db.session.commit()
            response = jsonify({
                "success": "Path deleted successfully."
            })
        else:
            response = jsonify({"error": "Path does not exist."})
            response.status_code = 404
        return response
