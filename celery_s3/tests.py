from unittest import TestCase

from celery import Celery

from celery_s3.backends.s3 import S3Backend


class S3BackendTest(TestCase):

    def get_app(self, config):
        app = Celery('test')
        app.config_from_object(config)
        return app

    def test_s3_backend_instantiation(self):
        app = self.get_app({
            'CELERY_RESULT_BACKEND': 'celery_s3.backends.S3Backend',
            'CELERY_S3_BACKEND_SETTINGS': {
                'aws_access_key_id': 'test_key_id',
                'aws_secret_access_key': 'test_secret_access_key',
                'bucket': 'test_bucket',
            },
        })
        self.assertIsInstance(
            app.backend,
            S3Backend,
        )
        self.assertEqual(
            app.backend.aws_access_key_id,
            'test_key_id',
        )
        self.assertEqual(
            app.backend.aws_secret_access_key,
            'test_secret_access_key',
        )
        self.assertEqual(
            app.backend.bucket_name,
            'test_bucket',
        )
        self.assertEqual(
            app.backend.base_path,
            '',
        )

        app = self.get_app({
            'CELERY_RESULT_BACKEND': 'celery_s3.backends.S3Backend',
            'CELERY_S3_BACKEND_SETTINGS': {
                'aws_access_key_id': 'test_key_id',
                'aws_secret_access_key': 'test_secret_access_key',
                'bucket': 'test_bucket',
                'base_path': '/celery/',
            },
        })
        self.assertEqual(
            app.backend.base_path,
            '/celery/',
        )
