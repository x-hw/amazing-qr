# -*- coding: utf-8 -*-
"""End-to-end tests for amzqr.mylibs.theqrmodule.

Asserts spec-correct invariants on the full pipeline output for a fixed real
input ('https://github.com', H).

Invariants pinned here (ISO/IEC 18004):
  - version / size scale as (ver-1)*4+21
  - three finder patterns at the canonical corners, each a 7x7 border
  - timing patterns on row/col 6 alternate
  - the fixed dark module at (4*ver+9, 8) == m[-8][8] is ALWAYS 1
"""

from amzqr.mylibs import ECC, data, matrix, structure, theqrmodule


def _rebuild_matrix(words, requested_ver, ecl):
    """Replicate theqrmodule.get_qrcode's pipeline up to the matrix (no drawing)."""
    ver, data_codewords = data.encode(requested_ver, ecl, words)
    ecc = ECC.encode(ver, ecl, data_codewords)
    final_bits = structure.structure_final_bits(ver, ecl, data_codewords, ecc)
    qrmatrix = matrix.get_qrmatrix(ver, ecl, final_bits)
    return ver, qrmatrix


def test_pipeline_version_and_size():
    ver, m = _rebuild_matrix("https://github.com", 1, "H")
    assert ver == 3
    assert len(m) == (3 - 1) * 4 + 21
    assert all(len(row) == len(m) for row in m)


def test_pipeline_finder_patterns():
    _, m = _rebuild_matrix("https://github.com", 1, "H")
    n = len(m)
    corners = [(0, 0), (0, n - 7), (n - 7, 0)]
    for r, c in corners:
        assert m[r][c] == 1, (r, c)
        assert m[r][c + 6] == 1, (r, c + 6)
        assert m[r + 6][c] == 1, (r + 6, c)


def test_pipeline_timing_patterns():
    _, m = _rebuild_matrix("https://github.com", 1, "H")
    n = len(m)
    for i in range(8, n - 8):
        assert m[6][i] == (1 if i % 2 == 0 else 0)
        assert m[i][6] == (1 if i % 2 == 0 else 0)


def test_pipeline_dark_module_is_fixed_dark():
    # ISO/IEC 18004 §7.3.4: the module at (4*ver+9, 8) is a fixed dark module,
    # always 1, never masked.
    _, m = _rebuild_matrix("https://github.com", 1, "H")
    assert m[-8][8] == 1


def test_get_qrcode_writes_png(tmp_path):
    # draw_qrcode treats save_place as a *directory* and writes qrcode.png in it.
    ver, name = theqrmodule.get_qrcode(1, "H", "https://github.com", str(tmp_path))
    import os

    assert os.path.isfile(name)
    assert os.path.getsize(name) > 0
    assert ver >= 1


def test_pipeline_is_deterministic():
    v1, m1 = _rebuild_matrix("https://github.com", 1, "H")
    v2, m2 = _rebuild_matrix("https://github.com", 1, "H")
    assert (v1, m1) == (v2, m2)
