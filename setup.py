import os
import shutil
import sys

from setuptools import setup, find_packages

src_dir = 'main'
package_directory = 'orange_datashare'
package_name = 'orange-datashare'

__version__ = None
version_file = '%s/%s/__init__.py' % (src_dir, package_directory)
with open(version_file, 'r') as f:
    for line in f.readlines():
        if line.find('__version__') >= 0:
            exec(line)

if __version__ is None:
    raise AssertionError('Failed to load version from %s' % version_file)


def purge_sub_dir(path):
    shutil.rmtree(os.path.join(os.path.dirname(__file__), path))

requirements = [requirement.rstrip(' \r\n') for requirement in open('requirements.txt').readlines()]
if sys.version_info.major == 2:
    requirements.append("enum34==1.1.6")

setup(name=package_name,
      version=__version__,
      zip_safe=False,
      packages=find_packages(where=src_dir),
      author='Team Datasahre',
      author_email='soda.dev@orange.com',
      description='A client library for Orange Datashare',
      long_description=open('README.rst').read(),
      url='http://github.com/datashare/client-python',
      classifiers=[
          "Programming Language :: Python",
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Topic :: Communications",
      ],
      entry_points={
          'console_scripts': [
              'orange_datashare = %s.main:main' % package_directory,
          ]
      },
      package_dir={package_directory: '%s/%s' % (src_dir, package_directory)},
      install_requires=[requirement.rstrip(' \r\n') for requirement in open('requirements.txt').readlines()],
      tests_require=[
          'mock==2.0.0',
      ],
      test_suite='test',
      )
