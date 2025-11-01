"""Setuptools configuration for the converters package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="file-converters",
    version="0.2.0",
    author="File Converters Maintainers",
    author_email="opensource@example.com",
    description="A collection of polished file format converters",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lazarev-Cloud/converters",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "file-converters=converters.cli:main",
        ],
    },
)
