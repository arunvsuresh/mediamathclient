from distutils.core import setup

setup(
  name='mediamathclient',
  version='0.0.1',
  author='Arun Suresh',
  author_email='arun@me.com',
  packages=['mediamathclient', 'tests'],
  install_requires=[
    'pytest',
    'requests'
  ],
  scripts=[],
  url='https://github.com/arunvsuresh/mediamathclient',
  license='LICENSE',
  description='A client for interacting with the MediaMath Platform.',
  long_description=open('README.md').read(),
)

