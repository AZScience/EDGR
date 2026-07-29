"""Replace English subtitle on quy-trinh-a-z.png with Vietnamese topic."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "public" / "quy-trinh-a-z.png"

VI = (
    "Thuật toán truy hồi đồ thị động dựa trên bằng chứng để giảm ảo giác "
    "trong LLM cho phát hiện xâm nhập và tình báo mối đe dọa mạng"
)

FONT_PATHS = [
    r"C:\Windows\Fonts\segoeui.ttf",
    r"C:\Windows\Fonts\arial.ttf",
    r"C:\Windows\Fonts\tahoma.ttf",
    r"C:\Windows\Fonts\calibri.ttf",
]


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for fp in FONT_PATHS:
        try:
            return ImageFont.truetype(fp, size)
        except OSError:
            continue
    return ImageFont.load_default()


def wrap(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.ImageFont,
    max_width: int,
) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for word in words:
        trial = (cur + " " + word).strip()
        bbox = draw.textbbox((0, 0), trial, font=font)
        if bbox[2] - bbox[0] <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def main() -> None:
    im = Image.open(SRC).convert("RGB")
    w, h = im.size
    draw = ImageDraw.Draw(im)
    bg = im.getpixel((w // 2, 55))

    # Keep Vietnamese main title; cover English subtitle band.
    y0, y1 = 36, 78
    draw.rectangle([40, y0, w - 40, y1], fill=bg)

    size = 13
    font = load_font(size)
    lines = wrap(draw, VI, font, w - 100)
    while len(lines) > 2 and size > 10:
        size -= 1
        font = load_font(size)
        lines = wrap(draw, VI, font, w - 100)

    color = (30, 58, 95)
    metrics: list[tuple[str, int, int]] = []
    total_h = 0
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        lw = bbox[2] - bbox[0]
        lh = bbox[3] - bbox[1]
        metrics.append((line, lw, lh))
        total_h += lh + 2

    y = y0 + max(0, (y1 - y0 - total_h) // 2)
    for line, lw, lh in metrics:
        x = (w - lw) // 2
        draw.text((x, y), line, font=font, fill=color)
        y += lh + 2

    bak = SRC.with_suffix(".bak.png")
    if not bak.exists():
        Image.open(SRC).save(bak)

    im.save(SRC, optimize=True)
    im.crop((0, 0, w, 90)).save(ROOT / "public" / "_top_band.png")
    print("patched", SRC)
    print("lines:", lines)


if __name__ == "__main__":
    main()
