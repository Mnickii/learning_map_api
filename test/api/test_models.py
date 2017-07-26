from datetime import datetime

from flask import json
import unittest

from learning_map_api.test.base import BaseTestCase
from learning_map_api.api.models import(
    db, Path, Contribution, ContributionType, Tag
)


class TestPath(BaseTestCase):

    def setUp(self):
        db.drop_all()
        db.create_all()

        self.path1 = Path(
            id = "-KA3Q0D45T6",
            name="Blockchain Developer",
            description="Leading software platform for digital assets."
        )
        self.path2 = Path(
            id = "-KQ0X2FG8V",
            name="Quality Assurance Engineer",
            description="Ensure apps run with no glitch."
        )
        db.session.add(self.path1)

    def test_create_path(self):
        """
        to test that path is created successfully.
        """
        # get original number of paths
        old_all_paths = Path.query.all()
        db.session.add(self.path2)
        db.session.commit()
        new_app_paths = Path.query.all()
        self.assertEqual(len(new_app_paths), (len(old_all_paths) + 1))


    def test_update_path(self):
        """
        To test successful path update.
        """
        # fetch a path
        path = Path.query.filter_by(name="Blockchain Developer").first()
        # save original name
        old_path_name = path.name
        new_path_name = "AI Engineer"
        # update path name
        path.name = new_path_name
        db.session.commit()
        self.assertNotEqual(old_path_name, new_path_name)

    def test_delete_path(self):
        """
        To test successful path deletion.
        """
        # fetch a path
        path = Path.query.all()[0]
        old_path_name = path.name
        path_id = path.id
        new_name = "UI Developer"
        path.name = new_name
        updated_path = Path.query.get(path_id)
        self.assertNotEqual(new_name, old_path_name)
        self.assertEqual(new_name, updated_path.name)


class TestContribution(BaseTestCase):

    def setUp(self):
        db.drop_all()
        db.create_all()

    def test_successful_contribution_creation(self):
        contrib = Contribution(
            id="-KA3Q0D45T6",
            title="AI",
            user_id="-KJKcv0D",
            contribution_type_id="-KSDQcv0D"
        )

        initial_contribs = Contribution.query.all()
        db.session.add(contrib)
        db.session.commit()
        new_contribs = Contribution.query.all()
        self.assertEqual(len(new_contribs), (len(initial_contribs) + 1))

    def test_create_contribution_sets_created_at(self):
        contrib_id = "-KA3Q0D45T6"
        contrib = Contribution(
            id=contrib_id,
            title="AI",
            user_id="-KJKcv0D",
            contribution_type_id="-KSDQcv0D"
        )
        db.session.add(contrib)
        db.session.commit()
        retrieved_contrib = Contribution.query.filter_by(id=contrib_id).first()
        self.assertIsNotNone(retrieved_contrib.created_at)
        self.assertIsInstance(retrieved_contrib.created_at, datetime)

    def test_default_status_is_pending(self):
        contrib_id = "-KA3Q0D45T6"
        contrib = Contribution(
            id=contrib_id,
            title="AI",
            user_id="-KJKcv0D",
            contribution_type_id="-KSDQcv0D"
        )
        db.session.add(contrib)
        db.session.commit()
        retrieved_contrib = Contribution.query.filter_by(id=contrib_id).first()
        self.assertIsNotNone(retrieved_contrib.status)
        self.assertEqual(retrieved_contrib.status, "pending")

    def test_tags_empty_on_creation(self):
        contrib_id = "-KA3Q0D45T6"
        contrib = Contribution(
            id=contrib_id,
            title="AI",
            user_id="-KJKcv0D",
            contribution_type_id="-KSDQcv0D"
        )
        db.session.add(contrib)
        db.session.commit()
        retrieved_contrib = Contribution.query.filter_by(id=contrib_id).first()
        self.assertIsNotNone(retrieved_contrib.created_at)
        self.assertEqual(len(retrieved_contrib.tags.all()), 0)

    def test_tags_relation_successful(self):
        tag1 = Tag(id="-KA3Q0D45T6", name="devOps")
        tag2 = Tag(id="-KA3Q32144", name="Core platform")
        all_tags = [tag1, tag2]
        contrib_id = "-KA3Q0D45T6"
        contrib = Contribution(
            id=contrib_id,
            title="AI",
            user_id="-KJKcv0D",
            contribution_type_id="-KSDQcv0D"
        )
        for t in all_tags: contrib.tags.append(t)
        db.session.add(contrib)
        db.session.commit()
        retrieved_tags = Tag.query.filter(Tag.contributions.any(id=contrib_id)).all()
        self.assertIsNotNone(retrieved_tags)
        self.assertEqual(len(retrieved_tags), len(all_tags))

    def test_contribution_type_relation(self):
        contrib_type_id = "-KSDQcv0D"
        contrib_type = ContributionType(
            id=contrib_type_id,
            name="Skill"
        )
        contrib_id = "-KA3Q0D45T6"
        contrib = Contribution(
            id=contrib_id,
            title="AI",
            user_id="-KJKcv0D",
            contribution_type_id=contrib_type_id
        )
        for c in [contrib, contrib_type]: db.session.add(c)
        db.session.commit()
        retrieved_contrib = Contribution.query.filter_by(id=contrib_id).first()
        retrieved_contrib_type = ContributionType.query.filter_by(id=contrib_type_id).first()
        retrieved_contrib_type2 = ContributionType.query.filter_by(
            id=retrieved_contrib.contribution_type_id
        ).first()
        self.assertIsNotNone(retrieved_contrib_type)
        self.assertEqual(retrieved_contrib_type, retrieved_contrib_type2)
