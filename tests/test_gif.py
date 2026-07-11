# -*- coding: utf-8 -*-
"""Tests for GIF per-frame duration preservation.

Before the fix, amzqr.run() only captured the first frame's duration
and applied it to all output frames.  After the fix, each frame's
duration is preserved individually.
"""

import os

from PIL import Image

from amzqr import amzqr


def _make_test_gif(path, durations_ms):
    """Create a multi-frame GIF with per-frame durations.

    durations_ms: list of int, one duration (in ms) per frame.
    """
    frames = []
    for i, dur in enumerate(durations_ms):
        # Each frame is a solid colour so we can tell them apart.
        im = Image.new("RGB", (20, 20), color=(min(i * 80, 255), 0, 0))
        frames.append(im)
    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=durations_ms,
        loop=0,
    )


def _read_durations(path):
    """Return a list of per-frame durations (ms) from a GIF."""
    im = Image.open(path)
    result = []
    for frame in range(im.n_frames):
        im.seek(frame)
        result.append(im.info.get("duration", 0))
    return result


def test_gif_per_frame_duration_preserved(tmp_path):
    """Output GIF must preserve each frame's original duration."""
    input_durations = [100, 500, 200]
    gif_in = os.path.join(str(tmp_path), "in.gif")
    _make_test_gif(gif_in, input_durations)

    save_name = "out.gif"
    amzqr.run(
        "https://github.com",
        picture=gif_in,
        save_dir=str(tmp_path),
        save_name=save_name,
    )

    out_path = os.path.join(str(tmp_path), save_name)
    assert os.path.isfile(out_path)
    out_durations = _read_durations(out_path)
    assert out_durations == input_durations, (
        f"Expected durations {input_durations}, got {out_durations}"
    )
