# pylint-hexagonal

[![PyPI - Version](https://img.shields.io/pypi/v/pylint-hexagonal.svg)](https://pypi.org/project/pylint-hexagonal)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pylint-hexagonal.svg)](https://pypi.org/project/pylint-hexagonal)

-----

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [License](#license)

## Introduction
This is a pylint plugin for use with a with a package structure as follows:

```
example/
├── adapters
│   ├── api
│   │   └── api.py
│   └── db
│       └── db.py
└── core
    ├── application
    │   └── service.py
    ├── domain
    │   └── aggregate.py
    └── ports
        ├── primary
        │   └── serviceport.py
        └── secondary
            └── daoport.py
```

The checker validates the following hexagonal architecure rules:

1. Core modules must not import from adapters
1. Adapter modules must not import from other adapters
1. Adapter modules modules should only import from the ports subpackage of the core.
1. Ports should not include any logic (abstract classes and methods only)


## Installation

```console
pip install pylint-hexagonal
```

## License

`pylint-hexagonal` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

