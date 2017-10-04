from setuptools import setup, find_packages

requirements = [
    'boto>=2.8.0,<3.0',
]

setup(
    name='celery-s3',
    version='1.0.0',
    description='An S3 result store backend for Celery',
    long_description=open('README.md').read(),
    author='Rob Golding',
    author_email='rob@robgolding.com',
    license='BSD',
    url='https://github.com/robgolding63/celery-s3',
    download_url='https://github.com/robgolding63/celery-s3/downloads',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    tests_require=requirements + [
        'celery==4.1.0',
    ],
    test_suite='celery_s3.tests',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Distributed Computing',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
    ],
)
