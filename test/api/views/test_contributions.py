import json

from learning_map_api.test.base import BaseTestCase
from learning_map_api.api.models import db, Path, Tag, Contribution, ContributionType

class ContributionsTestCase(BaseTestCase):
    contribution_type_id =  "-KA3Q0D45T6"
    python_tag_id = "-hjbjnjnnbhjbnn"
    javascript_tag_id = "-hjbjjhbmONMASS"
    
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.resource = ContributionType(
            id = self.contribution_type_id,
            name="resource",
        )
        db.session.add(self.resource)
        db.session.commit()
        self.first_tag = Tag(
            id = self.python_tag_id,
            name="python",
        )
        db.session.add(self.first_tag)
        db.session.commit()
        self.second_tag = Tag(
            id = self.javascript_tag_id,
            name="javascript",
        )
        db.session.add(self.second_tag)
        db.session.commit()

    def test_get_users_contributions(self):
        self.assertTrue(True)

    def test_contribution_created_successfully(self):
        """
        Tests the route '/api/v1/contributions'
        """
        res = self.client.post('/api/v1/contributions', data=json.dumps({
            "title": "usman",
            "type": self.contribution_type_id,
            "description": "usman baba",
            "tags": [self.python_tag_id, self.javascript_tag_id]
        }), content_type="application/json")
       
        self.assertEqual(res.status_code, 201)
        all_contributions = Contribution.query.all()
        self.assertEqual(len(all_contributions), 1)
          
    def test_request_is_a_valid_format(self):
        """
        Tests the response when a request is not JSON
        """
        res = self.client.post('/api/v1/contributions', data=json.dumps({
            "title": "usman",
            "type": self.contribution_type_id,
            "description": "usman baba",
            "tags": [self.python_tag_id, self.javascript_tag_id]
        }), content_type="Text(text/plain)")
        expected_response = "Request must be a valid JSON"
        generated_response = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(generated_response['message'], expected_response)

    def test_title_required_on_create(self):
        """
        Tests the response when the request does not contain 'title'
        """
        res = self.client.post('/api/v1/contributions', data=json.dumps({
            "type": self.contribution_type_id,
            "description": "usman baba",
            "tags": [self.python_tag_id, self.javascript_tag_id]
        }), content_type="application/json")
        expected_response = "title cannot be null"
        generated_response = json.loads(res.data)
    
        self.assertEqual(res.status_code, 400)
        self.assertEqual(generated_response['message'], expected_response)

    def test_description_required_on_create(self):
        """
        Tests the response when the request does not contain 'description'
        """
        res = self.client.post('/api/v1/contributions', data=json.dumps({
            "title": "usman",
            "type": self.contribution_type_id,
            "tags": [self.python_tag_id, self.javascript_tag_id]
        }), content_type="application/json")
        expected_response = "description cannot be null"
        generated_response = json.loads(res.data)
    
        self.assertEqual(res.status_code, 400)
        self.assertEqual(generated_response['message'], expected_response)
    
    def test_contribution_type_required_on_create(self):
        """
        Tests the response when the request does not contain 'type'
        """
        res = self.client.post('/api/v1/contributions', data=json.dumps({
            "description": "usman baba",
            "title": "usman",
            "tags": [self.python_tag_id, self.javascript_tag_id]
        }), content_type="application/json")
        expected_response = "type cannot be null"
        generated_response = json.loads(res.data)
    
        self.assertEqual(res.status_code, 400)
        self.assertEqual(generated_response['message'], expected_response)

    def test_title_is_string(self):
        """
        Tests the response when the 'title' is not a valid string
        """
        res = self.client.post('/api/v1/contributions', data=json.dumps({
            "title": 2,
            "type": self.contribution_type_id,
            "description": "usman baba",
            "tags": [self.python_tag_id, self.javascript_tag_id]
        }), content_type="application/json")
        expected_response = "title must be a valid string"
        generated_response = json.loads(res.data)
    
        self.assertEqual(res.status_code, 400)
        self.assertEqual(generated_response['message'], expected_response)

    def test_description_is_string(self):
        """
        Tests the response when the 'description' is not a valid string
        """
        res = self.client.post('/api/v1/contributions', data=json.dumps({
            "title": "usman",
            "type": self.contribution_type_id,
            "description": 3,
            "tags": [self.python_tag_id, self.javascript_tag_id]
        }), content_type="application/json")
        expected_response = "description must be a valid string"
        generated_response = json.loads(res.data)
    
        self.assertEqual(res.status_code, 400)
        self.assertEqual(expected_response, generated_response['message'])

    def test_contribution_type_is_string(self):
        """
        Tests the response when the 'type' is not a valid string
        """
        res = self.client.post('/api/v1/contributions', data=json.dumps({
            "title": "usman",
            "type": 4,
            "description": "usman baba",
            "tags": [self.python_tag_id, self.javascript_tag_id]
        }), content_type="application/json")
        expected_response = "type must be a valid string"
        generated_response = json.loads(res.data)
    
        self.assertEqual(res.status_code, 400)
        self.assertEqual(expected_response, generated_response['message'])
    
    def test_contribution_type_is_valid(self):
        """
        Tests the response when the 'type' is nt of resource, idea or skill
        """
        res = self.client.post('/api/v1/contributions', data=json.dumps({
            "title": "usman",
            "type": "not sure",
            "description": "usman baba",
            "tags": [self.python_tag_id, self.javascript_tag_id]
        }), content_type="application/json")
        expected_response = "type must be of resource, idea or skill"
        generated_response = json.loads(res.data)
    
        self.assertEqual(res.status_code, 400)
        self.assertEqual(expected_response, generated_response['message'])

    def test_tags_is_list(self):
        """
        Tests the response when the 'tags' is not a valid list
        """
        res = self.client.post('/api/v1/contributions', data=json.dumps({
            "title": "usman",
            "type": self.contribution_type_id,
            "description": "usman baba",
            "tags": "usman21e062",
        }), content_type="application/json")
        expected_response = "tags must be a list"
        generated_response = json.loads(res.data)
    
        self.assertEqual(res.status_code, 400)
        self.assertEqual(expected_response, generated_response['message'])

    def test_tag_id_exists(self):
        """
        Tests invalid tag ids
        """
        res = self.client.post('/api/v1/contributions', data=json.dumps({
            "title": "usman",
            "type": self.contribution_type_id,
            "description": "usman baba",
            "tags": ["usman21e062", "seun22e098"],
        }), content_type="application/json")
        expected_response = "usman21e062 is not a valid tag"
        generated_response = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(expected_response, generated_response["message"])

    def test_tag_not_required_on_create(self):
        """
        Tests the response when 'tags' is not in the request
        """
        res = self.client.post('/api/v1/contributions', data=json.dumps({
            "title": "usman",
            "type": self.contribution_type_id,
            "description": "usman baba"
        }), content_type="application/json")
        generated_response = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertNotIn("tags", generated_response["data"])
