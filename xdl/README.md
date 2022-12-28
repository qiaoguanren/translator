# XDL

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code_style-black-000000.svg)](https://github.com/psf/black)
[![Code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg)](https://github.com/prettier/prettier)

This package provides code relevant to the chemical description language (XDL) standard. It provides a XDL object which can be instantiated from a XDL file or from appropriate objects, then execute itself or write itself to a file.

More information can be found here: https://croningroup.gitlab.io/chemputer/xdl/

## Contributing

To contribute to this project, clone the repository and `cd` into it:

```shell
$ git clone https://gitlab.com/croningroup/chemputer/xdl.git
$ cd xdl
```

Next, install the tools required for development:

```shell
$ pip install -r requirements-dev.txt
```

Set up `pre-commit` to automatically lint the code and apply formatting where applicable
on each commit:

```
$ pre-commit install
```

Install the `xdl` package in editable mode:

```shell
$ pip install -e .[testing]
```

Before pushing to the remote, run `pytest`:

```shell
$ pytest
```

or alternatively `tox` for a full check across all supported python versions:

```shell
$ tox
```

Please also refer to the [Contribution Guidelines](https://gitlab.com/croningroup/chemputer/project-templates/contributing.git).
