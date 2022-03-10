
import os
import re
from setuptools import setup, find_packages

with open(os.path.join('ddotkit', '__init__.py')) as ver_file:
    for line in ver_file:
        if line.startswith('__version__'):
            version = re.sub("'", "", line[line.index("'"):])

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'pandas>=0.20',
    'numpy',
    'scipy',
    'ndex2',
    'python-igraph',
    'networkx',
    'tulip-python'
]

setup(name='ddotkit',
      version=version,
      description='Data-Driven Ontology Toolkit v2',
      url='http://github.com/idekerlab/ddot',
      author='Christopher Churas',
      author_email='churas.camera@gmail.com',
      license='MIT',
      classifiers=[
          # How mature is this project? Common values are 
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 3',

          # Indicate who your project is intended for
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'Topic :: Scientific/Engineering :: Visualization',

          # Pick your license as you wish (should match "license" above)
          'License :: OSI Approved :: MIT License',

          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9'
      ],
      keywords='ontology hierarchy',
      packages=['ddotkit'],
      package_dir={'ddotkit': 'ddotkit'},
      data_files=[('style', ['ddotkit/ontology_style.cx',
                             'ddotkit/passthrough_style.cx'])],
      install_requires=requirements,
      include_package_data=True,
      test_suite='tests',
      zip_safe=False)
