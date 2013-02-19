celery-s3
=========

celery-s3 is an S3 backend for Celery.

Requirements
------------

* boto
* celery

Installation
------------

Install via pip:

`pip install celery-s3`

Then configure Celery to use the `S3Backend`:

    CELERY_RESULT_BACKEND = 'celery_s3.backends.S3Backend'

    CELERY_S3_BACKEND_SETTINGS = {
        'aws_access_key_id': '<your_aws_access_key_id>',
        'aws_secret_access_key': '<your_aws_secret_access_key>',
        'bucket': '<your_bucket_name>',
    }

Notes
-----

This backend isn't the fastest in the world (obviously, it's fastest if you use
it from an EC2 server) but it allows task results to be retrieved from machines
that are logically separate from the worker(s).

To prevent files being left in S3 forever, use the lifecycle configuation to
ensure they are deleted after a certain period of time. Also, use
`result.forget()` once a result has been used and is no longer needed (this
deletes the key from S3).
