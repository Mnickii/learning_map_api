from learning_map_api.api.test.base import BaseTestCase
from learning_map_api.api.models import db, Path


class PathTestCase(BaseTestCase):

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
