import re

import setuptools

with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

# Inspiration: https://stackoverflow.com/a/7071358/6064135
with open('muffinscript/_version.py', 'r') as version_file:
    version_groups = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    if version_groups:
        version = version_groups.group(1)
    else:
        raise RuntimeError('Unable to find version string!')


DEV_REQUIREMENTS = [
    'bandit == 1.8.*',
    'black == 25.*',
    'flake8 == 7.*',
    'isort == 6.*',
    'mypy == 1.15.*',
    'pyinstaller == 6.*',
    'pytest == 8.*',
    'pytest-cov == 6.*',
]

setuptools.setup(
    name='muffinscript',
    version=version,
    description='Delectable little programming language.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/justintime50/muffinscript',
    author='justintime50',
    license='MIT',
    packages=setuptools.find_packages(
        exclude=[
            'test',
        ]
    ),
    package_data={
        'muffinscript': [
            'py.typed',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    extras_require={
        'dev': DEV_REQUIREMENTS,
    },
    entry_points={
        'console_scripts': [
            'muffinscript=muffinscript.muffin:main',
        ]
    },
    python_requires='==3.13.*',
)
