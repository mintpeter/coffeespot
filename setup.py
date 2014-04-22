import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_mako',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'markdown',
    'passlib',
    'py-bcrypt',
    'pyyaml',
    'wtforms',
    ]

setup(name='coffeespot',
      version='0.1.0',
      description='coffeespot',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Zack Marvel',
      author_email='zpmarvel@gmail.com',
      url='http://zackmarvel.com',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='coffeespot',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = coffeespot:main
      [console_scripts]
      initialize_coffeespot_db = coffeespot.scripts.initializedb:main
      coffeespot = coffeespot.scripts.new_post:main
      """,
      )
