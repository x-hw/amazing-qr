# -*- coding: utf-8 -*-
"""Smoke tests for amzqr.amzqr.run — the public API.

These only exercise the no-picture path (base QR scaled 3x and saved), to
avoid depending on any image fixtures. They confirm the public contract
(returned tuple shape + output file existence) without pinning pixels.
"""

import os

import pytest

from amzqr import amzqr


def test_run_plain_writes_png(tmp_path):
    ver, level, name = amzqr.run("https://github.com", save_dir=str(tmp_path))
    out = os.path.join(str(tmp_path), os.path.basename(name))
    assert os.path.isfile(out)
    assert os.path.getsize(out) > 0
    assert ver >= 1
    assert level in ("L", "M", "Q", "H")


def test_run_rejects_unsupported_chars(tmp_path):
    with pytest.raises(ValueError):
        amzqr.run("你好", save_dir=str(tmp_path))


def test_run_rejects_bad_version(tmp_path):
    with pytest.raises(ValueError):
        amzqr.run("https://github.com", version=0, save_dir=str(tmp_path))
