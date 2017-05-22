from setuptools import setup

setup(
    name='myproject',
    author='Kumar Pratik',
    description='Nginx server for Flask',
    author_email='kumar.pratik73@yahoo.com',
    packages=['myproject'],
    include_package_data=True,
    install_requires=[
        'flask','flask-sqlalchemy',
    ],
    scripts=['bin/myproject-shell','bin/postgres-shell']
)
