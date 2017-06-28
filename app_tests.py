import unittest
from unittest.mock import patch
from io import BytesIO
import json
import celery


import app


class Task(object):
    def __init__(self, id):
        self.id = id


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.app.test_client()

    def test_update_positiv(self):
        with patch('app.is_valid_image'),\
            patch('app.to_json'),\
            patch('app.transformation_task.delay',
                  return_value=Task("id_task")):

            data = dict(image=(BytesIO(b''), "test.jpg"),)
            rv = self.app.post("/image", data=data,
                               content_type='multipart/form-data',
                               follow_redirects=True)

            self.assertEqual(200, rv.status_code)
            self.assertEqual("id_task", json.loads(rv.data)['id'])

    def test_update_missing_file(self):
        rv = self.app.post("/image", data=dict(),
                           content_type='multipart/form-data',
                           follow_redirects=True)
        self.assertEqual(400, rv.status_code)

    def test_internal_server_error_raise_TypeError(self):
        with patch('app.is_valid_image'),\
            patch('app.to_json'),\
            patch('app.transformation_task.delay',
                  side_effect=TypeError("Mock object")):
            data = dict(image=(BytesIO(b''), "test.jpg"),)
            rv = self.app.post("/image", data=data,
                               content_type='multipart/form-data',
                               follow_redirects=True)

            self.assertEqual(500, rv.status_code)

    def test_internal_server_error_raise_CeleryError(self):
        with patch('app.is_valid_image'),\
            patch('app.to_json'),\
            patch('app.transformation_task.delay',
                  side_effect=celery.exceptions.CeleryError("Mock object")):
            data = dict(image=(BytesIO(b''), "test.jpg"),)
            rv = self.app.post("/image", data=data,
                               content_type='multipart/form-data',
                               follow_redirects=True)

            self.assertEqual(500, rv.status_code)

    def test_update_bad_format(self):
        data = dict(image=(BytesIO(b'this is not an jpg image'), "test.jpg"),)

        rv = self.app.post("/image", data=data,
                           content_type='multipart/form-data',
                           follow_redirects=True)
        self.assertEqual(400, rv.status_code)


if __name__ == '__main__':
    unittest.main()
