import json

from learning_map_api.test.base import BaseTestCase
from learning_map_api.api.models import db, Path


class PathsTestCase(BaseTestCase):

    def setUp(self):
        db.drop_all()
        db.create_all()

        self.path1 = Path(
            id = "-KA345D5FG6",
            name="Blockchain Developer",
            description="Leading software platform for digital assets."
        )

        self.path2 = dict(
            id = "-KA345D5FG1",
            name="Quality Assurance Engineer",
            description="Ensure apps run with no glitch."
        )
        db.session.add(self.path1)

    def test_create_path(self):
        """
        To test that path is created successfully.
        """
        old_all_paths = Path.query.all()
        response = self.client.post(
            '/api/v1/paths',
            data=json.dumps(self.path2),
            content_type='application/json'
        )
        self.assertEqual(
            json.loads(response.data)["success"],
            "Path succesfully created."
        )
        new_all_paths = Path.query.all()
        self.assertEqual(len(new_all_paths), len(old_all_paths) + 1)
        self.assertEqual(response.status_code, 201)

    def test_path_name_is_required_on_create(self):
        """
        To test that path name is a required field.
        """
        old_all_paths = Path.query.all()
        response = self.client.post(
            '/api/v1/paths',
            data=json.dumps({
                "name": "",
                "description": "path description"
            }),
            content_type='application/json'
        )
        self.assertEqual(
            json.loads(response.data)["error"],
            "Name and description are required to create a path."
        )
        new_all_paths = Path.query.all()
        # confirm that the invald path is not created
        self.assertEqual(len(new_all_paths), len(old_all_paths))
        self.assertEqual(response.status_code, 400)

    def test_description_is_required_on_create(self):
        """
        To test that path description is a required field.
        """
        old_all_paths = Path.query.all()
        response = self.client.post(
            '/api/v1/paths',
            data=json.dumps({
                "name": "Path name",
                "description": ""
            }),
            content_type='application/json'
        )
        self.assertEqual(
            json.loads(response.data)["error"],
            "Name and description are required to create a path."
        )
        new_all_paths = Path.query.all()
        # confirm that the invald path is not created
        self.assertEqual(len(new_all_paths), len(old_all_paths))
        self.assertEqual(response.status_code, 400)

    def test_no_duplicate_path_names(self):
        """
        To test path with same name cannot be recreated.
        """
        name="Blockchain Developer"
        response = self.client.post(
            '/api/v1/paths',
            data=json.dumps(dict(
                name=name,
                description="To become a leading blockchain developer"
            )),
            content_type='application/json'
        )
        self.assertEqual(
            json.loads(response.data)["error"],
            "A Path with the name {} exists.".format(name)
        )
        self.assertEqual(response.status_code, 409)

    def test_fetch_single_path(self):
        """
        Test for fetching single path.
        """
        path = Path.query.all()[0]
        response = self.client.get(
            '/api/v1/paths/{}'.format(path.id),
            content_type='application/json'
        )
        self.assertEqual(
            json.loads(response.data)["success"],
            "Path fetched successfully."
        )
        self.assert200(response)

    def test_fetch_all_paths(self):
        """
        Test for fetching all paths.
        """
        path = Path.query.all()
        response = self.client.get(
            '/api/v1/paths/',
            content_type='application/json'
        )
        self.assertEqual(
            json.loads(response.data)["success"],
            "All paths fetched successfully."
        )
        self.assert200(response)

    def test_fetch_all_paths(self):
        """
        Attempt to fetch all when no path exists.
        """
        # delete all existing paths
        db.session.query(Path).delete()
        paths = Path.query.all()
        response = self.client.get(
            '/api/v1/paths/',
            content_type='application/json'
        )
        # confirm that path count is zero
        self.assertEqual(
            json.loads(response.data)["count"],
            0
        )
        self.assert200(response)

    def test_fetch_path_with_invalid_id(self):
        """
        Test that fetch fails when given invalid id.
        """
        path = Path.query.all()[0]
        response = self.client.get(
            '/api/v1/paths/-invalid-id-1234',
            content_type='application/json'
        )
        self.assertEqual(
            json.loads(response.data)["error"], "Path does not exist."
        )
        self.assert404(response)

    def test_path_id_required_on_update(self):
        """
        Test that fetch fails when given invalid id.
        """
        path = Path.query.all()[0]
        response = self.client.put(
            '/api/v1/paths/',
            data=json.dumps(self.path2),
            content_type='application/json'
        )
        print(response.__dict__)
        self.assertEqual(
            json.loads(response.data)["error"], "Path id must be provided."
        )
        self.assert400(response)

    def test_update_path(self):
        """
        To test update works successfully.
        """
        # fetch single path
        path = Path.query.all()[0]
        response = self.client.put(
            '/api/v1/paths/{}'.format(path.id),
            data=json.dumps({'name': 'Robotics'}),
            content_type='application/json'
        )
        self.assertEqual(
            json.loads(response.data)["success"],
            "Path updated successfully."
        )
        self.assert200(response)

    def test_update_path_with_invalid_id(self):
        """
        To test update works successfully.
        """
        response = self.client.put(
            '/api/v1/paths/-invalid-id-123',
            data=json.dumps({'name': 'Robotics'}),
            content_type='application/json'
        )
        self.assertEqual(
            json.loads(response.data)["error"],
            "Path does not exist."
        )
        self.assert404(response)

    def test_delete_path(self):
        """
        To test delete works successfully.
        """
        path = Path.query.all()[0]
        response = self.client.delete(
            '/api/v1/paths/{}'.format(path.id),
            content_type='application/json'
        )
        self.assertEqual(
            json.loads(response.data)["success"],
            "Path deleted successfully."
        )

    def test_path_id_required_on_delete(self):
        """
        To test delete operation doesnt work without path id.
        """
        path = Path.query.all()[0]
        response = self.client.delete(
            '/api/v1/paths/',
            content_type='application/json'
        )
        self.assertEqual(
            json.loads(response.data)["error"],
            "Path id must be provided."
        )

    def test_delete_path_with_invalid_id(self):
        """
        To test delete fails given invalid id.
        """
        old_all_paths = Path.query.all()
        response = self.client.delete(
            '/api/v1/paths/-invalid-id-1234',
            content_type='application/json'
        )
        self.assertEqual(
            json.loads(response.data)["error"],
            "Path does not exist."
        )
        self.assert404(response)
        new_all_paths = Path.query.all()
        self.assertEqual(len(old_all_paths), len(new_all_paths))
