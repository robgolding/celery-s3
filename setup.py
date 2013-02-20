from setuptools import setup, find_packages

setup(
    name='celery-s3',
    version='0.1',
    description='An S3 result store backend for Celery',
    long_description=open('README.md').read(),
    author='Rob Golding',
    author_email='rob@robgolding.com',
    license='BSD',
    url='https://github.com/robgolding63/celery-s3',
    download_url='https://github.com/robgolding63/celery-s3/downloads',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Topic :: System :: Distributed Computing',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
    ],
)
