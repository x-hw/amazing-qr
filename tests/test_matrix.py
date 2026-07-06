# -*- coding: utf-8 -*-
"""Unit tests for amzqr.mylibs.matrix — structure of a fresh QR matrix.

These tests build the matrix from synthetic final-bits input and assert
structural invariants (size, finder patterns, timing patterns) that any
correct QR matrix must satisfy. They are intentionally decoupled from the
data/ECC/structure layers so a regression in matrix.py is caught directly.
"""

from amzqr.mylibs import matrix


def _matrix(ver, bits):
    # get_qrmatrix expects a final-bits string; pad whatever we pass so
    # place_bits doesn't run dry for larger versions.
    return matrix.get_qrmatrix(ver, "H", bits)


def _bits_for(ver):
    n = (ver - 1) * 4 + 21
    # total modules minus reserved-function modules is roughly n*n; place_bits
    # uses next(bit) lazily and would StopIteration if we under-supply, but for
    # structural tests we only need *enough* bits — feed n*n of them.
    return "1" * (n * n)


def test_matrix_size_v1():
    m = _matrix(1, _bits_for(1))
    assert len(m) == 21
    assert all(len(row) == 21 for row in m)


def test_matrix_size_scales_with_version():
    for ver in (2, 5, 10):
        m = _matrix(ver, _bits_for(ver))
        assert len(m) == (ver - 1) * 4 + 21


def test_finder_pattern_top_left():
    m = _matrix(1, _bits_for(1))
    # 7x7 finder border at (0,0): outer ring of 1s.
    for j in range(7):
        assert m[0][j] == 1 and m[6][j] == 1
    for i in range(7):
        assert m[i][0] == 1 and m[i][6] == 1
    # separator ring (row/col 7) is 0.
    for j in range(8):
        assert m[7][j] == 0 and m[j][7] == 0


def test_three_finder_patterns():
    m = _matrix(1, _bits_for(1))
    n = len(m)
    # Finders occupy 7x7 at top-left, top-right (cols n-7..n-1), bottom-left
    # (rows n-7..n-1). The 8th row/col is the 0-separator.
    corners = [(0, 0), (0, n - 7), (n - 7, 0)]
    for r, c in corners:
        assert m[r][c] == 1, (r, c)
        assert m[r][c + 6] == 1, (r, c + 6)
        assert m[r + 6][c] == 1, (r + 6, c)


def test_timing_pattern_row_and_col_6():
    m = _matrix(1, _bits_for(1))
    n = len(m)
    for i in range(8, n - 8):
        assert m[6][i] == (1 if i % 2 == 0 else 0)
        assert m[i][6] == (1 if i % 2 == 0 else 0)


def test_dark_module_is_fixed_dark():
    # ISO/IEC 18004 §7.3.4: the module at (4*ver+9, 8) == (13, 8) for v1 is a
    # fixed dark module, always 1, never masked. Regression guard for the
    # matrix.py:128 bug (mm[-8][8] = None) that was fixed in 76f07c8 — if that
    # line ever returns, the dark module flips with the winning mask.
    m = _matrix(1, _bits_for(1))
    assert m[-8][8] == 1
