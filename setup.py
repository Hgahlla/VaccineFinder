from setuptools import setup

setup(
      name='VaccineFinder',
      version='1.0',
      description='An automation tool that notifies users by text messages of CVS pharmacies within a certain drive time that have available appointments for the COVID-19 vaccine',
      url='',
      author='Harmohan Gahlla',
      author_email='harmohangahlla@gmail.com',
      license='MIT',
      packages=['vaccine_finder'],
      zip_safe=False,
      install_requires=[
            'certifi',
            'charset - normalizer',
            'geographiclib',
            'geopy',
            'idna',
            'psycopg2',
            'PyJWT',
            'python - dotenv',
            'pytz',
            'requests',
            'twilio',
            'urllib3'
      ]
)