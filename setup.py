import pathlib

from pkg_resources import parse_requirements
from setuptools import find_packages, setup

LIBRARY_NAME = "rubiks_cube"  # Rename according to the library folder

# List of requirements
with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement) for requirement in parse_requirements(requirements_txt)
    ]

setup(
    name=LIBRARY_NAME,
    packages=find_packages(include=[LIBRARY_NAME]),
    version="0.1.0",
    description="A library that allows to simulate a Rubik's Cube for research purposes.",
    author="Francisco Muñoz",
    license="MIT",
    install_requires=install_requires,
    setup_requires=["pytest-runner"],
    tests_requires=["pytest"],
    test_suite="tests",
)
