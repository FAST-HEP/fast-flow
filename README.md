[![pypi package](https://img.shields.io/pypi/v/fast-flow.svg)](https://pypi.org/project/fast-flow/)
[![pipeline status](https://gitlab.cern.ch/fast-hep/public/fast-flow/badges/master/pipeline.svg)](https://gitlab.cern.ch/fast-hep/public/fast-flow/commits/master)
[![coverage report](https://gitlab.cern.ch/fast-hep/public/fast-flow/badges/master/coverage.svg)](https://gitlab.cern.ch/fast-hep/public/fast-flow/commits/master)


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
In addition, the [`fast-carpenter`](https://gitlab.cern.ch/fast-hep/public/fast-carpenter) package makes use of this, so it might be helpful to see how this is used there.
