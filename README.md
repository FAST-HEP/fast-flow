[![pypi package](https://img.shields.io/pypi/v/fast-flow.svg)](https://pypi.org/project/fast-flow/)
[![Build Status](https://travis-ci.com/FAST-HEP/fast-flow.svg?branch=master)](https://travis-ci.com/FAST-HEP/fast-flow)
[![codecov](https://codecov.io/gh/FAST-HEP/fast-flow/branch/master/graph/badge.svg)](https://codecov.io/gh/FAST-HEP/fast-flow)
[![DOI](https://zenodo.org/badge/187254541.svg)](https://zenodo.org/badge/latestdoi/187254541)


fast-flow: A YAML-based processing configuration
================================================
Provides a simple interface to describe a processing chain, where a user names
the stages and type of stage they want to run and then provides specific
parameters for each stage.

## Installing
```
pip install --user fast-flow
```

## Documentation
While better documentation is on its way, you might want to look at the examples directory to see how this can be used.
In addition, the [`fast-carpenter`](https://github.com/fast-hep/fast-carpenter) package makes use of this, so it might be helpful to see how this is used there.
