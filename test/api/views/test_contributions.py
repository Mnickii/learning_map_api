import json

from learning_map_api.test.base import BaseTestCase
from learning_map_api.api.models import db, Path, Contribution


class ContributionsTestCase(BaseTestCase):
    def test_get_users_contributions(self):
        self.assertTrue(True)

    def setUp(self):
        db.drop_all()
        db.create_all()

        contrib = Contribution(
            id="-KA3Q0D45T6",
            title="AI",
            user_id="-KJKcv0D",
            contribution_type_id="-KSDQcv0D",
        )

    def test_json_request(self):
        data = {"status": "approved"}
        response = self.client.put(
            'api/v1/contributions/1',
            data=json.dumps(data),
            content_type='text'
        )

        expected_message = "Request must be valid JSON first"
        generated_response = json.loads(response.data)

        self.assertEqual(response.status_code, 400),
        self.assertEqual(expected_message,
                         generated_response['message'])

    def test_approved_rejected_status(self):
        data = {"status": "accepted"}
        response = self.client.put(
            'api/v1/contributions/1?type=idea',
            data=json.dumps(data),
            content_type='application/json'
        )

        status = data["status"]
        expected_message = ('{} is not an acceptable status. '
                            'Status can only be approved or rejected'
                            .format(status))
        generated_response = json.loads(response.data)

        self.assertEqual(response.status_code, 400),
        self.assertEqual(expected_message,
                         generated_response['message'])

        def test_update_status(self):
            data = {"status": "approved"}
            response = self.client.put(
                'api/v1/contributions/-KA3Q0D45T6',
                data=json.dumps(data),
                content_type='application/json'
            )

            old_contribution = Contribution.query.all()
            db.session.add(contrib)
            db.session.commit()
            new_contribution = Contribution.query.all()
            expected_message = "Status was successfully updated"
            generated_response = json.loads(response.data)

            self.assertEqual(response.status_code, 200),
            self.assertEqual(expected_message,
                             generated_response['message'])
            self.assertEqual(new_contrbution["status"], "approved")

        def test_existing_contribution(self):
            data = {"status": "approved"}
            response = self.client.put(
                'api/v1/contributions/2',
                data=json.dumps(data),
                content_type='application/json'
            )

            expected_message = "Contribution does not exist"

            generated_response = json.loads(response.data)

            self.assertEqual(response.status_code, 404),
            self.assertEqual(expected_message,
                             generated_response['message'])

        def test_empty_request_data(self):
            data = None
            response = self.client.put(
                'api/v1/contributions/1?type=idea',
                data=json.dumps(data),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 400)
