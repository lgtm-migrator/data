# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import dials_data


def test_testing_framework():
    assert dials_data.__version__


def test_all_datasets_can_be_parsed():
    import dials_data.datasets

    assert dials_data.datasets.definition
