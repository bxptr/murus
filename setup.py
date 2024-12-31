from setuptools import setup, find_packages

with open("requirements.txt") as handler:
    requirements = handler.readlines()

setup(
    name = "murus",
    packages = find_packages(),
    install_requires = requirements
)
