import os
import sys
from setuptools import setup

install_requires = [
    'numpy>=1.10.0',
    'scipy>=0.18.0',
    'scikit-learn>=0.19.1',
    'future',
    'pandas',
    'decorator',
]

test_requires = [
    'nose',
    'nose2',
    'fcsparser',
    'tables',
    'h5py',
    'matplotlib',
    'coverage',
    'coveralls',
]

doc_requires = [
    'sphinx',
    'sphinxcontrib-napoleon',
    'autodocsumm',
]

if sys.version_info[:2] < (2, 7) or (3, 0) <= sys.version_info[:2] < (3, 5):
    raise RuntimeError("Python version 2.7 or >=3.5 required.")

version_py = os.path.join(os.path.dirname(
    __file__), 'scprep', 'version.py')
version = open(version_py).read().strip().split(
    '=')[-1].replace('"', '').strip()

readme = open('README.rst').read()

setup(name='scprep',
      version=version,
      description='scprep',
      author='Jay Stanley, Scott Gigante, and Daniel Burkhardt, Krishnaswamy Lab, Yale University',
      author_email='krishnaswamylab@gmail.com',
      packages=['scprep', ],
      license='GNU General Public License Version 2',
      install_requires=install_requires,
      extras_require={'test': test_requires,
                      'doc': doc_requires},
      test_suite='nose2.collector.collector',
      long_description=readme,
      url='https://github.com/KrishnaswamyLab/scprep',
      download_url="https://github.com/KrishnaswamyLab/scprep/archive/v{}.tar.gz".format(
          version),
      keywords=['big-data',
                'computational-biology',
                ],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Framework :: Jupyter',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Natural Language :: English',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
      ]
      )
