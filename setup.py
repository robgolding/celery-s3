from setuptools import setup, find_packages

setup(
    name='celery-s3',
    version='0.2',
    description='An S3 result store backend for Celery',
    long_description=open('README.md').read(),
    author='Rob Golding',
    author_email='rob@robgolding.com',
    license='BSD',
    url='https://github.com/supericeboy/celery-s3',
    download_url='https://github.com/supericeboy/celery-s3/downloads',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'boto>=2.8.0,<3.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Distributed Computing',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
    ],
)
