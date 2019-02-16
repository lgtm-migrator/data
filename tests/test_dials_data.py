# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import dials_data


def test_all_datasets_can_be_parsed():
    import dials_data.datasets

    assert dials_data.datasets.definition


def test_repository_location():
    import dials_data.datasets

    rl = dials_data.datasets.repository_location()
    assert rl.check(dir=1)


def test_fetching_undefined_datasets_does_not_crash():
    import dials_data.download

    df = dials_data.download.DataFetcher(read_only=True)
    assert df("aardvark") is False
