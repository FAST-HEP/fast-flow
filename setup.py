import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fast-flow",
    version="0.0.1",
    author="Ben Krikler",
    author_email="fast-hep@cern.ch",
    description="YAML-based analysis flow description language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.cern.ch/fast-hep/public/fast-flow",
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=['six', 'pyyaml'],
    #setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    classifiers=(
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Development Status :: 3 - Alpha",
    ),
)
