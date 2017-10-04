# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from unittest import TestCase

from celery import Celery
from mock import Mock, patch

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
            app.backend.aws_region,
            'us-east-1',
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
        self.assertEqual(
            app.backend.reduced_redundancy,
            False,
        )

        # test region, base path and rr config
        app = self.get_app({
            'CELERY_RESULT_BACKEND': 'celery_s3.backends.S3Backend',
            'CELERY_S3_BACKEND_SETTINGS': {
                'aws_region': 'us-west-1',
                'aws_access_key_id': 'test_key_id',
                'aws_secret_access_key': 'test_secret_access_key',
                'bucket': 'test_bucket',
                'base_path': '/celery/',
                'reduced_redundancy': True,
            },
        })
        self.assertEqual(
            app.backend.aws_region,
            'us-west-1',
        )
        self.assertEqual(
            app.backend.base_path,
            '/celery/',
        )
        self.assertEqual(
            app.backend.reduced_redundancy,
            True,
        )

        # test base path config with unicode
        app = self.get_app({
            'CELERY_RESULT_BACKEND': 'celery_s3.backends.S3Backend',
            'CELERY_S3_BACKEND_SETTINGS': {
                'aws_access_key_id': 'test_key_id',
                'aws_secret_access_key': 'test_secret_access_key',
                'bucket': 'test_bucket',
                'base_path': '/celery/hellø/',
            },
        })
        self.assertEqual(
            app.backend.base_path,
            '/celery/hellø/',
        )

    @patch('celery_s3.backends.s3.Key')
    def test_s3_backend_bucket_region(self, mock_key_cls):
        app = self.get_app({
            'CELERY_RESULT_BACKEND': 'celery_s3.backends.S3Backend',
            'CELERY_S3_BACKEND_SETTINGS': {
                'aws_region': 'us-west-1',
                'aws_access_key_id': 'test_key_id',
                'aws_secret_access_key': 'test_secret_access_key',
                'bucket': 'test_bucket',
                'base_path': '/celery/',
            },
        })
        mock_key_instance = Mock()
        mock_key_instance.get_contents_as_string.return_value = 'TEST VALUE'
        mock_key_cls.return_value = mock_key_instance
        self.assertEqual(
            app.backend.get('teßt'),
            'TEST VALUE',
        )
        self.assertEqual(
            len(mock_key_cls.call_args_list),
            1,
        )
        call = mock_key_cls.call_args_list[0]
        bucket = call[0][0]
        self.assertEqual(
            bucket.connection.host,
            's3-us-west-1.amazonaws.com',
        )

    @patch('celery_s3.backends.s3.Key')
    def test_s3_backend_get(self, mock_key_cls):
        app = self.get_app({
            'CELERY_RESULT_BACKEND': 'celery_s3.backends.S3Backend',
            'CELERY_S3_BACKEND_SETTINGS': {
                'aws_region': 'us-west-1',
                'aws_access_key_id': 'test_key_id',
                'aws_secret_access_key': 'test_secret_access_key',
                'bucket': 'test_bucket',
                'base_path': '/celery/',
            },
        })
        mock_key_instance = Mock()
        mock_key_instance.get_contents_as_string.return_value = 'TEST VALUE'
        mock_key_cls.return_value = mock_key_instance
        self.assertEqual(
            app.backend.get('teßt'),
            'TEST VALUE',
        )
        self.assertEqual(
            len(mock_key_cls.call_args_list),
            1,
        )
        call = mock_key_cls.call_args_list[0]
        bucket = call[0][0]
        self.assertEqual(
            bucket.name,
            'test_bucket',
        )
        self.assertEqual(
            mock_key_instance.key,
            '/celery/teßt',
        )

    @patch('celery_s3.backends.s3.Key')
    def test_s3_backend_set(self, mock_key_cls):
        app = self.get_app({
            'CELERY_RESULT_BACKEND': 'celery_s3.backends.S3Backend',
            'CELERY_S3_BACKEND_SETTINGS': {
                'aws_access_key_id': 'test_key_id',
                'aws_secret_access_key': 'test_secret_access_key',
                'bucket': 'test_bucket',
                'base_path': '/celery/',
            },
        })
        mock_key_instance = Mock()
        mock_key_cls.return_value = mock_key_instance
        app.backend.set('teßt', 'TEßT VALUE')
        self.assertEqual(
            len(mock_key_cls.call_args_list),
            1,
        )
        call = mock_key_cls.call_args_list[0]
        args, kwargs = call
        bucket = args[0]
        self.assertEqual(
            bucket.name,
            'test_bucket',
        )
        self.assertEqual(
            mock_key_instance.key,
            '/celery/teßt',
        )
        calls = mock_key_instance.set_contents_from_string.call_args_list
        self.assertEqual(
            len(calls),
            1,
        )
        args, kwargs = calls[0]
        self.assertEqual(args[0], 'TEßT VALUE')
        self.assertEqual(
            kwargs,
            {
                'reduced_redundancy': False,
            },
        )

        app = self.get_app({
            'CELERY_RESULT_BACKEND': 'celery_s3.backends.S3Backend',
            'CELERY_S3_BACKEND_SETTINGS': {
                'aws_access_key_id': 'test_key_id',
                'aws_secret_access_key': 'test_secret_access_key',
                'bucket': 'test_bucket',
                'base_path': '/celery/',
                'reduced_redundancy': True,
            },
        })
        app.backend.set('teßt', 'TEßT VALUE')

        calls = mock_key_instance.set_contents_from_string.call_args_list
        self.assertEqual(
            len(calls),
            2,
        )
        args, kwargs = calls[1]
        self.assertEqual(args[0], 'TEßT VALUE')
        self.assertEqual(
            kwargs,
            {
                'reduced_redundancy': True,
            },
        )

    @patch('celery_s3.backends.s3.Key')
    def test_s3_backend_delete(self, mock_key_cls):
        app = self.get_app({
            'CELERY_RESULT_BACKEND': 'celery_s3.backends.S3Backend',
            'CELERY_S3_BACKEND_SETTINGS': {
                'aws_access_key_id': 'test_key_id',
                'aws_secret_access_key': 'test_secret_access_key',
                'bucket': 'test_bucket',
                'base_path': '/celery/',
            },
        })
        mock_key_instance = Mock()
        mock_key_cls.return_value = mock_key_instance
        app.backend.delete('teßt')
        self.assertEqual(
            len(mock_key_cls.call_args_list),
            1,
        )
        call = mock_key_cls.call_args_list[0]
        bucket = call[0][0]
        self.assertEqual(
            bucket.name,
            'test_bucket',
        )
        self.assertEqual(
            mock_key_instance.key,
            '/celery/teßt',
        )
        self.assertEqual(
            len(mock_key_instance.delete.call_args_list),
            1,
        )
