# @todo #/DEV Rename main project *.md to lower case (e.g. `readme.md` -> `readme.md`)
"""Python setup.py for g2w package"""
import io
import os
from setuptools import find_packages, setup
# @todo #/DEV Apply readme.md format like dgroup/lazylead


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("g2w", "VERSION")
    '0.2.0'
    >>> read("readme.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="g2w",
    version=read("g2w", "VERSION"),
    description="Awesome g2w created by dgroup",
    url="https://github.com/dgroup/g2w/",
    long_description=read("readme.md"),
    long_description_content_type="text/markdown",
    author="lazylead",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        "console_scripts": ["g2w = g2w.__main__:main"]
    },
    extras_require={"test": read_requirements("requirements-test.txt")},
)
