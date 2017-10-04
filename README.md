# Celery-S3

[![Build Status](https://travis-ci.org/robgolding/celery-s3.svg?branch=master)](https://travis-ci.org/robgolding/celery-s3)
[![Coverage Status](https://coveralls.io/repos/github/robgolding/celery-s3/badge.svg?branch=master)](https://coveralls.io/github/robgolding/celery-s3?branch=master)

Celery-S3 is a simple S3 result backend for Celery.

If used in conjunction with the SQS broker, it allows for Celery deployments
that use only distributed AWS services -- with no dependency on individual
machines within your infrastructure.

This backend probably isn't suitable for particularly high-traffic Celery
deployments, but it works just fine in general -- and imposes no limits on the
number of workers in the pool.

## Installation

Install via pip:

`pip install celery-s3`

Then configure Celery to use the `S3Backend`:

    CELERY_RESULT_BACKEND = 'celery_s3.backends.S3Backend'

    CELERY_S3_BACKEND_SETTINGS = {
        'aws_access_key_id': '<your_aws_access_key_id>',
        'aws_secret_access_key': '<your_aws_secret_access_key>',
        'bucket': '<your_bucket_name>',
    }

## Configuration

To use a folder within the specified bucket, set the `base_path` in your
`CELERY_S3_BACKEND_SETTINGS`:


    CELERY_S3_BACKEND_SETTINGS = {
        ...
        'base_path': '/celery/',
        ...
    }

To use a region other than the default (`us-east-1`), set the `aws_region`
parameter:

    CELERY_S3_BACKEND_SETTINGS = {
        ...
        'aws_region': 'us-east-1',
        ...
    }

To use [reduced redundancy storage](https://aws.amazon.com/s3/reduced-redundancy/),
set the `reduced_redundancy` parameter:

    CELERY_S3_BACKEND_SETTINGS = {
        ...
        'reduced_redundancy': True,
        ...
    }

## Notes

Storing Celery results with this backend will obviously result in API calls
being made to Amazon S3.  For each result, at least one `PUT` request will be
made (priced at $0.01 per 1,000 requests at the time of writing).  Also, the
data contained within the result object will be stored indefinitely, unless
otherwise specified.

To fetch a result for a task that has already finished, at least two requests
will be made (one `HEAD` and one `GET`).  If you use Celery's `result.get()` to
wait for a task to finish, S3 will be polled continuously until the task has
finished.

By default, the poll interval is set to 0.5 seconds, which could result in
a lot of requests (two `HEAD` requests per second until the task has finished,
then one `GET` request to fetch the result).  If you need to use
`result.get()`, consider increasing the interval and using a timeout to prevent
polling forever: `result.get(interval=5, timeout=600)`.

Also, for tasks whose result you don't need, be sure to use `ignore_result`:

    @celery.task(ignore_result=True)
    def process_data(obj):
        obj.do_processing()

Once task results have been used and are no longer needed, be sure to call
`result.forget()` to delete the corresponding S3 key.  Otherwise, old results
will remain forever and contribute to storage costs (storage is priced at
$0.095 per GB per month at the time of writing).

Also, the S3 lifecycle can be used to archive or delete old keys after
a certain period of time.
