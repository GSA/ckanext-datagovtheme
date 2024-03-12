from setuptools import setup, find_packages
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ckanext-datagovtheme",
    version="0.2.14",
    description="CKAN Extension to manage data.gov theme",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords="",
    author="Data.gov",
    author_email="datagovhelp@gsa.gov",
    url="https://github.com/GSA/ckanext-datagovtheme/",
    license="Public Domain",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    namespace_packages=["ckanext"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    setup_requires=["wheel"],
    entry_points="""
        [ckan.plugins]
        datagovtheme=ckanext.datagovtheme.plugin:DatagovTheme
    """,
)
