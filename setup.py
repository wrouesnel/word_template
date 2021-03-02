#!/usr/bin/env python3
# type: ignore

from setuptools import setup, find_packages

# TODO: check python version before allowing install.

# Read the requirements out of requirements.txt which makes more tools happy.
install_requires = []
with open("requirements.txt", "rt") as f:
    for line in f:
        if line == "":
            continue
        if line.startswith("#"):
            continue
        if line.startswith("-") or line.startswith("--"):
            continue
        split_line = line.split()
        if len(split_line) > 0:
            install_requires.append(split_line[0])

setup(
    name="word_template",
    version="0.0.0",
    description="DOCX templated from YAML and directories",
    author="Will Rouesnel <wrouesnel@wrouesnel.com>",
    py_modules=find_packages("."),
    setup_requires=[],
    install_requires=install_requires,
    include_package_data=True,
    classifiers=[
        "License :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={"console_scripts": ["word-template=word_template.cmd.__main__:entry",],},
)
