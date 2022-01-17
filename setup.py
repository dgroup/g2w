# @todo #/DEV Rename main project *.md to lower case (e.g. `readme.md` -> `readme.md`)
"""Python setup.py for g2w package"""
import io
import os
from setuptools import find_packages, setup
from distutils.util import convert_path

# @todo #/DEV Apply readme.md format like dgroup/lazylead


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
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

main_ns = {}
ver_path = convert_path('g2w/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setup(
    name="g2w",
    version=main_ns['__version__'],
    description="Gateway to notify Worksection tasks about events from Grafana, Gitlab (e.g commits)",
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
