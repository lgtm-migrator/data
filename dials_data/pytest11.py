# -*- coding: utf-8 -*-

"""
pytest plugin functions
"""

from __future__ import absolute_import, division, print_function

import pytest
from .download import DataFetcher


def pytest_addoption(parser):
    parser.addoption(
        "--regression",
        action="store_true",
        default=False,
        help="run regression tests. Download data for those tests if required",
    )


@pytest.fixture(scope="session")
def dials_data(request):
    """
    Return the location of a regression dataset as py.path object.
    Download the files if they are not on disk already.
    Skip the test if the dataset can not be downloaded.
    """
    if not request.config.getoption("--regression"):
        pytest.skip("Test requires --regression option to run.")
    df = DataFetcher()

    def skip_test_if_lookup_failed(result, dials_data_too_old=False):
        if dials_data_too_old:
            pytest.skip(
                "Test requires a newer version of dials_data (v%s)" % dials_data_too_old
            )
        if not result:
            pytest.skip(
                "Automated download of test data failed. Download manually using dials.data"
            )
        return result

    setattr(df, "result_filter", skip_test_if_lookup_failed)
    return df
