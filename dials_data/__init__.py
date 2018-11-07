# -*- coding: utf-8 -*-

"""Top-level package for DIALS Regression Data."""

__author__ = """Markus Gerstel"""
__email__ = "dials-support@lists.sourceforge.net"
__version__ = "0.1.0"


def pytest_addoption(parser):
    """Adds '--regression' option to pytest exactly once."""
    if not hasattr(pytest_addoption, "done"):
        parser.addoption(
            "--regression",
            action="store_true",
            default=False,
            help="run regression tests. Download data for those tests if required",
        )
    setattr(pytest_addoption, "done", True)
