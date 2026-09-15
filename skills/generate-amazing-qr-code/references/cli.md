# amzqr CLI reference

Source: [x-hw/amazing-qr](https://github.com/x-hw/amazing-qr) and the
`amzqr.run` implementation. Confirm details against the installed version when
behavior differs.

## Command

```sh
amzqr Words
  [-v {1,2,...,40}]
  [-l {L,M,Q,H}]
  [-n output-filename]
  [-d output-directory]
  [-p picture_file]
  [-c]
  [-con contrast]
  [-bri brightness]
  [-V]
```

## Parameters

| Parameter | Meaning | Values and defaults |
|---|---|---|
| positional `Words` | URL or text to encode | Required string; see supported characters |
| `-v` | QR version / symbol size | `1` through `40`; default `1` |
| `-l` | error-correction level | `L`, `M`, `Q`, `H`; default `H` |
| `-n` | output filename | `.jpg`, `.jpeg`, `.png`, `.bmp`, `.gif`; default `qrcode.png` |
| `-d` | output directory | Existing directory; default current directory |
| `-p` | background image | Existing `.jpg`, `.jpeg`, `.png`, `.bmp`, or `.gif` file |
| `-c` | colorize background | Flag; default is black and white |
| `-con` | background contrast | Float; default `1.0` |
| `-bri` | background brightness | Float; default `1.0` |
| `-V` | print version | Flag |

With no `-n`, an artistic output is named from the background basename plus
`_qrcode`, using `.png` for a still background and `.gif` for an animated one.

## Payload

`amzqr` accepts only these characters:

- `0-9`
- `a-z`, `A-Z`
- `· , . : ; + - * / \ ~ ! @ # $ % ^ & \` ' = < > [ ] ( ) ? _ { } |` and space

Reject or transform unsupported Unicode (for example non-ASCII characters,
newline, and tab) before calling the tool. For URLs, percent-encoding with
supported ASCII characters is appropriate.

## Backgrounds and troubleshooting

- Use a nearly square background. The tool scales it to cover the QR data area
  and center-crops the excess.
- Large backgrounds or payloads may need a larger `-v`; however, a larger
  version can reduce visual appeal.
- Transparent regions are treated as background. Flatten transparency to a
  suitable color (usually white) before generation if scanning fails.
- A GIF background produces an animated GIF; with `-n`, that name must end in
  `.gif`.
- If a generated code does not scan, raise `-l` (prefer `H`), reduce background
  complexity or opacity, adjust `-con`/`-bri`, or increase `-v` if capacity or
  module size requires it.
