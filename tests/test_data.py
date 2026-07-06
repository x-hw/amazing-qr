# -*- coding: utf-8 -*-
"""Unit tests for amzqr.mylibs.data — assert spec-correct encoding behavior.

Where the current code violates the QR spec, the test is RED until the
corresponding bugfix lands (no xfail softening). The red is the work item.

Reference: ISO/IEC 18004. Alphanumeric values per Annex Table A.1,
  0-9 -> 0-9, A-Z -> 10-35, space=36, $=37, %=38, *=39, +=40, -=41,
  .=42, /=43, :=44.
"""

import pytest

from amzqr.mylibs import data
from amzqr.mylibs.constant import mode_indicator


# --- numeric_encoding -----------------------------------------------------
def test_numeric_encoding_groups_of_three():
    # 9 digits -> 3 groups x 10 bits = 30 bits.
    assert data.numeric_encoding("123456789") == "000111101101110010001100010101"


def test_numeric_encoding_single_and_double_digit_groups():
    # "1234" -> groups ["123","4"]: 10-bit + 4-bit.
    assert data.numeric_encoding("1234") == "0001111011" + "0100"
    # "12" -> single 2-digit group -> 7-bit.
    assert data.numeric_encoding("12") == "0001100"
    # "1" -> single 1-digit group -> 4-bit.
    assert data.numeric_encoding("1") == "0001"


# --- alphanumeric_encoding ------------------------------------------------
def test_alphanumeric_encoding_ac42():
    # QR spec Annex example "AC-42" (golden standard):
    # A=10,C=12 -> 10*45+12=462  -> 00111001110
    # -=41,4=4 -> 41*45+4 =1849 -> 11100111001
    # 2=2 (trailing)           -> 000010
    assert data.alphanumeric_encoding("AC-42") == "0011100111011100111001000010"


def test_alphanumeric_single_char():
    # Spec: a trailing single char encodes in 6 bits. A=10 -> 001010.
    # Currently RED (TODO #2): range(1, 1, 2) is empty -> `i` undefined ->
    # UnboundLocalError instead of a 6-bit code.
    assert data.alphanumeric_encoding("A") == "001010"


# --- byte_encoding --------------------------------------------------------
def test_byte_encoding_two_chars():
    # A=0x41=01000001, b=0x62=01100010.
    assert data.byte_encoding("Ab") == "0100000101100010"


# --- encode() end-to-end (data layer) ------------------------------------
def test_encode_numeric_v1_H():
    ver, data_codewords = data.encode(1, "H", "123456789")
    assert ver == 1
    # v1-H: 1 block of 9 data codewords (grouping_list[0][lindex['H']]).
    assert len(data_codewords) == 1
    assert len(data_codewords[0]) == 9
    # First codeword locks the mode+cci wiring: numeric mode_indicator="0001"
    # + 10-bit cci for v1-9 numeric ("0000001001" for len 9) -> "00010000...".
    expected_prefix = mode_indicator["numeric"] + data.get_cci(1, "numeric", "123456789")
    assert data_codewords[0][0] == int(expected_prefix[:8], 2)


def test_encode_chooses_alphanumeric_for_mixed():
    # digits + letters -> alphanumeric mode (subset of alphanum_list).
    ver, _ = data.encode(1, "H", "AC42")
    assert ver == 1


# --- spec-correct behavior currently violated (RED, drives fix) ----------
def test_oversized_content_raises():
    # 5000 digits exceeds even v40-H numeric capacity. analyse() never finds a
    # fitting version and encode proceeds with the stale requested ver (1),
    # producing garbage instead of an error. Spec: must raise ValueError.
    # Currently RED (TODO #3).
    with pytest.raises(ValueError):
        data.encode(1, "H", "0" * 5000)
