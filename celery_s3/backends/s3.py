import os

from boto.s3 import connect_to_region
from boto.s3.bucket import Bucket
from boto.s3.connection import S3Connection
from boto.s3.connection import OrdinaryCallingFormat
from boto.s3.key import Key
from kombu.utils import cached_property

from celery.backends.base import KeyValueStoreBackend
from celery.exceptions import ImproperlyConfigured


class S3Backend(KeyValueStoreBackend):
    """
    An S3 task result store.
    """
    supports_native_join = False
    implements_incr = False

    aws_region = 'us-east-1'
    aws_access_key_id = None
    aws_secret_access_key = None
    bucket_name = None
    base_path = ''
    use_ssl = True
    use_rr = False

    def __init__(self, **kwargs):
        super(S3Backend, self).__init__(**kwargs)
        config = self.app.conf.get('CELERY_S3_BACKEND_SETTINGS', None)
        if config is not None:
            if not isinstance(config, dict):
                raise ImproperlyConfigured(
                    'S3 backend settings should be grouped in a dict')
            self.aws_region = config.get('aws_region', self.aws_region)
            self.aws_access_key_id = config.get('aws_access_key_id',
                                            self.aws_access_key_id)
            self.aws_secret_access_key = config.get('aws_secret_access_key',
                                            self.aws_secret_access_key)
            self.bucket_name = config.get('bucket', self.bucket_name)
            self.base_path = config.get('base_path', self.base_path)
            self.use_ssl = config.get('use_ssl', self.use_ssl)
            self.use_rr = config.get('use_rr', self.use_rr)

    def _get_key(self, key):
        k = Key(self. s3_bucket)
        if self.base_path:
            key = os.path.join(self.base_path, key)
        k.key = key
        return k

    def get(self, key):
        k = self._get_key(key)
        if k.exists():
            return k.get_contents_as_string()
        return None

    def set(self, key, value):
        return self._get_key(key).set_contents_from_string(value, reduced_redundancy=self.use_rr)

    def delete(self, key):
        self._get_key(key).delete()

    @cached_property
    def s3_bucket(self):
        conn = connect_to_region(
            self.aws_region,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            is_secure=self.use_ssl,
        )
        return Bucket(connection=conn, name=self.bucket_name)
