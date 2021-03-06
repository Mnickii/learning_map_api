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
        if request.get_json():
            result = request.get_json()
            if Path.query.filter_by(name=result["name"]).first():
                # prevent instances of duplicate path names
                return {"error": "A Path with same name exists."}, 409
            path = Path(
                id=result["id"],
                name=result["name"].lower(),
                description=result["description"]
            )
            db.session.add(path)
            db.session.commit()
            return {
                "data": path.serialize(),
                "success": "Path succesfully created."
            }, 201
        else:
            return {"error": "No data was sent to the server"}, 400

    def get(self, id=None):
        """
        To fetch all/a single path
        """
        if id:
            # if an id is passed, query for path with that id
            path = Path.query.filter_by(id=id).first()
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
            paths = db.session.query(Path).all()
            if paths:
                return jsonify({
                    "success": "All paths fetched successfully.",
                    "data": [path.serialize() for path in paths]
                })
            else:
                return jsonify({
                    "warning": "There are no paths yet."
                })

    def put(self, id):
        """
        To update a path.
        """
        if request.get_json():
            result = request.get_json()
            # if an id is passed, query for path with that id
            path = Path.query.filter_by(id=id).first()
            if not result["name"].strip():
                return jsonify({
                    "error": "Name cannot be empty"
                })
            if path:
                # if path exists update
                name = result.get("name")
                description = result.get("description")
                if name:
                    path.name = result["name"].strip()
                if description:
                    path.description = result["description"].strip()

                db.session.add(path)
                db.session.commit()

                return jsonify({
                    "data": path.serialize(),
                    "success": "Path updated successfully."
                })
            else:
                response = jsonify({"error": "Path does not exist."})
                response.status_code = 404
                return response

    def delete(self, id):
        """
        To delete path
        """
        path = Path.query.get(id)
        if path:
            db.session.delete(path)
            db.session.commit()
            return jsonify({
                "success": "Path deleted successfully."
            })
        else:
            response = jsonify({"error": "Path does not exist."})
            response.status_code = 404
            return response
