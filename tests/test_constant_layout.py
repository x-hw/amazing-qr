# -*- coding: utf-8 -*-
"""Sanity checks for the rendering-layout constants in constant.py.

These guard against typos in the derived values; the coupling test
(test_combine_layout.py) guards the actual draw<->combine relationship.
"""

from amzqr.mylibs import constant


def test_layout_constants_values():
    assert constant.PIXELS_PER_MODULE == 3
    assert constant.QUIET_ZONE_MODULES == 4
    assert constant.PASTE_OFFSET_PX == 12
    assert constant.DATA_OFFSET_PX == 24
    assert constant.FINDER_REGION_MODULES == 8
    assert constant.FINDER_REGION_PX == 24
    assert constant.TIMING_MODULE == 6


def test_layout_constants_derive_from_roots():
    ppm = constant.PIXELS_PER_MODULE
    qz = constant.QUIET_ZONE_MODULES
    assert constant.PASTE_OFFSET_PX == qz * ppm
    assert constant.DATA_OFFSET_PX == 2 * qz * ppm
    assert constant.FINDER_REGION_PX == constant.FINDER_REGION_MODULES * ppm
