"""Generate the trainer's original ambient loop and native app icons."""

from math import pi, sin
from pathlib import Path
import struct
import wave
import zlib


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)


def make_ambient() -> None:
    rate = 11025
    seconds_per_chord = 2
    chords = (
        (130.81, 164.81, 196.00, 246.94),
        (110.00, 130.81, 164.81, 196.00),
        (87.31, 110.00, 130.81, 174.61),
        (98.00, 123.47, 146.83, 196.00),
    )
    sample_count = rate * seconds_per_chord * len(chords)
    samples = bytearray()
    for index in range(sample_count):
        t = index / rate
        chord_index = min(int(t // seconds_per_chord), len(chords) - 1)
        within = t % seconds_per_chord
        envelope = min(1.0, within / 0.24, (seconds_per_chord - within) / 0.24)
        envelope = max(0.0, envelope)
        chord = chords[chord_index]
        tone = sum(sin(2 * pi * frequency * t) for frequency in chord) / len(chord)
        tone += 0.24 * sin(2 * pi * (chord[0] / 2) * t)
        amplitude = int(max(-1, min(1, tone * envelope * 0.12)) * 127 + 128)
        samples.append(max(0, min(255, amplitude)))

    with wave.open(str(ASSETS / "ambient.wav"), "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(1)
        output.setframerate(rate)
        output.writeframes(samples)


def _chunk(kind: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)


def _icon_pixels(output_size: int) -> bytes:
    scale = 2
    source_size = 512 * scale
    raw = bytearray(source_size * source_size * 4)
    colors = {
        "background": (23, 36, 59, 255), "rail": (217, 228, 247, 255),
        "blue": (118, 167, 255, 255), "green": (128, 214, 177, 255),
        "gold": (255, 209, 122, 255), "clear": (0, 0, 0, 0),
    }
    beads = ((204, 158, "blue"), (302, 158, "green"), (252, 256, "gold"), (204, 354, "green"), (302, 354, "blue"))
    for py in range(source_size):
        y = (py + 0.5) / scale
        for px in range(source_size):
            x = (px + 0.5) / scale
            color = colors["clear"]
            if 20 <= x < 492 and 20 <= y < 492:
                cx = min(max(x, 136), 376)
                cy = min(max(y, 136), 376)
                if (x - cx) ** 2 + (y - cy) ** 2 <= 116 ** 2:
                    color = colors["background"]
                    if any(142 <= x <= 370 and abs(y - rail) <= 9 for rail in (158, 256, 354)):
                        color = colors["rail"]
                    for bx, by, bead_color in beads:
                        if (x - bx) ** 2 + (y - by) ** 2 <= 29 ** 2:
                            color = colors[bead_color]
            offset = (py * source_size + px) * 4
            raw[offset:offset + 4] = bytes(color)

    factor = source_size // output_size
    result = bytearray(output_size * output_size * 4)
    sample_count = factor * factor
    for y in range(output_size):
        for x in range(output_size):
            sums = [0, 0, 0, 0]
            for dy in range(factor):
                start = (((y * factor + dy) * source_size) + x * factor) * 4
                for dx in range(factor):
                    for channel in range(4):
                        sums[channel] += raw[start + dx * 4 + channel]
            offset = (y * output_size + x) * 4
            result[offset:offset + 4] = bytes(value // sample_count for value in sums)
    return bytes(result)


def _png(size: int, pixels: bytes) -> bytes:
    rows = b"".join(b"\0" + pixels[y * size * 4:(y + 1) * size * 4] for y in range(size))
    header = struct.pack(">2I5B", size, size, 8, 6, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", header) + _chunk(b"IDAT", zlib.compress(rows, 9)) + _chunk(b"IEND", b"")


def _ico(size: int, rgba: bytes) -> bytes:
    xor = bytearray()
    for y in range(size - 1, -1, -1):
        for x in range(size):
            offset = (y * size + x) * 4
            red, green, blue, alpha = rgba[offset:offset + 4]
            xor.extend((blue, green, red, alpha))
    mask_row_size = ((size + 31) // 32) * 4
    mask = bytes(mask_row_size * size)
    dib = struct.pack("<IiiHHIIiiII", 40, size, size * 2, 1, 32, 0, len(xor) + len(mask), 0, 0, 0, 0) + xor + mask
    entry = struct.pack("<BBBBHHII", 0, 0, 0, 0, 1, 32, len(dib), 22)
    return struct.pack("<HHH", 0, 1, 1) + entry + dib


def make_icon() -> None:
    png_pixels = _icon_pixels(512)
    (ASSETS / "icon.png").write_bytes(_png(512, png_pixels))
    ico_pixels = _icon_pixels(256)
    (ASSETS / "icon.ico").write_bytes(_ico(256, ico_pixels))
    png = (ASSETS / "icon.png").read_bytes()
    chunk = b"ic09" + struct.pack(">I", len(png) + 8) + png
    icns = b"icns" + struct.pack(">I", len(chunk) + 8) + chunk
    (ASSETS / "icon.icns").write_bytes(icns)


if __name__ == "__main__":
    make_ambient()
    make_icon()
