# -*- coding: utf-8 -*-
"""Coupling test: draw.py layout <-> combine() compositing.

draw.py and combine() share a "3 pixels per module + 4-module quiet zone"
layout; this test catches drift between them.

Approach: composite a solid-red background onto a QR via the public API
amzqr.run(picture=..., colorized=True). combine() paints red onto
non-reserved data modules (except the center sampling sub-pixel of each
module) and skips reserved modules entirely. So in the final 3x-upscaled
output, a data module's 9x9 pixel block is mostly red, while a reserved
module's block is not. Module positions are computed from the shared
constant.* layout constants and the output image's actual geometry -- if
draw.py and combine() disagree on layout, a reserved module turns red or
a data module stays un-red, and the assertion fails.
"""

from PIL import Image

from amzqr import amzqr
from amzqr.mylibs import constant, theqrmodule


def _is_red(px):
    # RGBA pixel; bg is solid red (255,0,0,255). Tolerate BICUBIC edge bleed.
    return px[0] > 200 and px[1] < 50 and px[2] < 50


def _count_red_in_module(out, mx, my, modules_per_unit, qz_modules):
    # Final image: each matrix module spans `modules_per_unit` pixels.
    # Module (mx, my) top-left pixel = (qz_modules + mx) * modules_per_unit.
    x0 = (qz_modules + mx) * modules_per_unit
    y0 = (qz_modules + my) * modules_per_unit
    n = modules_per_unit
    return sum(1 for dx in range(n) for dy in range(n) if _is_red(out.getpixel((x0 + dx, y0 + dy))))


def _reserved_modules(ver, n):
    """Return a set of (mx, my) module coords that are QR-spec reserved:
    finder+separator (3 corners, 8x8 each), timing row/col 6, and
    alignment-pattern 5x5 blocks (ver > 1). This is the spec notion of
    'must not be overwritten by the background'."""
    fr = constant.FINDER_REGION_MODULES  # 8: finder(7) + separator(1)
    t = constant.TIMING_MODULE  # 6
    reserved = set()

    # Finder + separator: 3 corners, fr x fr modules each.
    for cmx, cmy in [(0, 0), (0, n - fr), (n - fr, 0)]:
        for mx in range(cmx, cmx + fr):
            for my in range(cmy, cmy + fr):
                reserved.add((mx, my))

    # Timing pattern: row t and column t (within the matrix interior).
    for k in range(n):
        reserved.add((k, t))
        reserved.add((t, k))

    # Alignment patterns: 5x5 around each non-finder-adjacent center.
    if ver > 1:
        aloc = constant.alig_location[ver - 2]
        L = len(aloc)
        for a in range(L):
            for b in range(L):
                if (a == b == 0) or (a == L - 1 and b == 0) or (a == 0 and b == L - 1):
                    continue  # finder-adjacent, already covered
                cx, cy = aloc[a], aloc[b]
                for mx in range(cx - 2, cx + 3):
                    for my in range(cy - 2, cy + 3):
                        reserved.add((mx, my))
    return reserved


def test_combine_respects_reserved_modules(tmp_path):
    words = "https://github.com"
    # Determine the resolved version the same way test_pipeline does.
    ver, _ = theqrmodule.get_qrcode(1, "H", words, str(tmp_path))
    n = (ver - 1) * 4 + 21  # matrix side length in modules

    # Solid-red background; combine() resizes it to the data area, so any
    # size works. Use a non-square size to also exercise the resize branch.
    bg_path = tmp_path / "bg.png"
    Image.new("RGBA", (100, 80), (255, 0, 0, 255)).save(bg_path)

    out_name = "out.png"
    rver, rlevel, out_path = amzqr.run(
        words,
        level="H",
        picture=str(bg_path),
        colorized=True,
        save_name=out_name,
        save_dir=str(tmp_path),
    )
    assert rver == ver
    out = Image.open(out_path).convert("RGBA")

    # Derive final pixels-per-module from the actual output geometry:
    # output side = (n + 2*quiet) * ppm * upscale; ppm*upscale = side/(n+2*qz).
    qz = constant.QUIET_ZONE_MODULES
    total_modules = n + 2 * qz
    assert out.width % total_modules == 0, (out.width, total_modules)
    modules_per_unit = out.width // total_modules
    assert modules_per_unit == constant.PIXELS_PER_MODULE * 3  # 3x upscale in run()

    reserved = _reserved_modules(ver, n)

    # Reserved modules: few red pixels (block skipped by combine()).
    # Sample a handful across finder / timing / alignment regions.
    reserved_samples = sorted(reserved)[:40]
    for mx, my in reserved_samples:
        red = _count_red_in_module(out, mx, my, modules_per_unit, qz)
        assert red <= 30, f"reserved module ({mx},{my}) painted red: {red}/81"

    # Data modules (not reserved), surrounded by other data modules so
    # BICUBIC edge bleed is bounded. For ver=3 (n=29) these are unreserved.
    data_samples = [(15, 15), (10, 20), (20, 10), (12, 12)]
    for mx, my in data_samples:
        assert (mx, my) not in reserved, (mx, my)
        red = _count_red_in_module(out, mx, my, modules_per_unit, qz)
        assert red >= 50, f"data module ({mx},{my}) not painted red: {red}/81"


def test_combine_scaling_preserves_aspect_ratio(tmp_path):
    """Non-square backgrounds should retain their aspect ratio after scaling.

    Uses a two-tone background (red top half, blue bottom half) so the
    vertical split is visible after center-crop. For a portrait bg, the
    top and bottom are cropped equally; the red/blue boundary should
    remain near the vertical center of the data area.
    """
    words = "https://github.com"
    ver, _ = theqrmodule.get_qrcode(1, "H", words, str(tmp_path))
    n = (ver - 1) * 4 + 21

    # Create a portrait bg (width < height) with distinct top/bottom colors.
    # Red top half, blue bottom half — boundary at h/2.
    bg_w, bg_h = 80, 160
    bg = Image.new("RGBA", (bg_w, bg_h))
    for y in range(bg_h):
        color = (255, 0, 0, 255) if y < bg_h // 2 else (0, 0, 255, 255)
        for x in range(bg_w):
            bg.putpixel((x, y), color)
    bg_path = tmp_path / "two_tone_portrait.png"
    bg.save(bg_path)

    out_name = "out.png"
    rver, rlevel, out_path = amzqr.run(
        words,
        level="H",
        picture=str(bg_path),
        colorized=True,
        save_name=out_name,
        save_dir=str(tmp_path),
    )
    assert rver == ver

    out = Image.open(out_path).convert("RGBA")
    qz = constant.QUIET_ZONE_MODULES
    total_modules = n + 2 * qz
    assert out.width % total_modules == 0, (out.width, total_modules)
    modules_per_unit = out.width // total_modules
    assert modules_per_unit == constant.PIXELS_PER_MODULE * 3

    # Verify sample modules are not in the reserved set before asserting
    # colors, so a version change doesn't produce a misleading failure.
    reserved = _reserved_modules(ver, n)

    # Sample a data module near the TOP of the QR (module (10, 10)) —
    # should be RED because the portrait bg's top half is red.
    # Use the top-left sub-pixel (i%3=0, j%3=0) to avoid the combine()
    # center-sub-pixel skip (i%3==1 and j%3==1).
    top_mx, top_my = 10, 10
    assert (top_mx, top_my) not in reserved, f"top sample module ({top_mx},{top_my}) is reserved"
    top_x = (qz + top_mx) * modules_per_unit
    top_y = (qz + top_my) * modules_per_unit
    top_px = out.getpixel((top_x, top_y))
    assert _is_red(top_px), (
        f"top module ({top_mx},{top_my}) should be red (center-cropped portrait bg), got {top_px}"
    )

    # Sample a data module near the BOTTOM of the QR (module (10, n-10)) —
    # should be BLUE because the portrait bg's bottom half is blue.
    bottom_mx, bottom_my = 10, n - 10
    assert (bottom_mx, bottom_my) not in reserved, (
        f"bottom sample module ({bottom_mx},{bottom_my}) is reserved"
    )
    bottom_x = (qz + bottom_mx) * modules_per_unit
    bottom_y = (qz + bottom_my) * modules_per_unit
    bottom_px = out.getpixel((bottom_x, bottom_y))
    assert bottom_px[2] > 200 and bottom_px[0] < 50 and bottom_px[1] < 50, (
        f"bottom module ({bottom_mx},{bottom_my}) should be blue (center-cropped portrait bg), got {bottom_px}"
    )

    # Also verify reserved modules are still skipped (not colored over).
    # Top-left finder area should be mostly untouched (not red/blue).
    finder_x0 = qz * modules_per_unit + modules_per_unit // 2
    finder_y0 = qz * modules_per_unit + modules_per_unit // 2
    fp = out.getpixel((finder_x0, finder_y0))
    # Finder center should be dark (black module), not red or blue.
    assert fp[0] < 50 and fp[1] < 50 and fp[2] < 50, f"finder should be dark, got {fp}"
