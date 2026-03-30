#!/usr/bin/env python3
"""
generate_cover.py — Create book cover for "Proving Nothing"
Design: Classical painting with overlaid title text, dark gradients for readability.
"""

from PIL import Image, ImageDraw, ImageFont
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, "assets")
COVER_ART = os.path.join(SCRIPT_DIR, "coverart.jpeg")

TITLE_LINES = ["PROVING", "NOTHING"]
SUBTITLE = "A Layered Guide to Zero-Knowledge Proof Systems"
AUTHOR = "Charles Hoskinson"

W, H = 1600, 2560


def load_font(name, size):
    font_map = {
        "bold": "Outfit-Bold.ttf",
        "semibold": "Outfit-SemiBold.ttf",
        "medium": "Outfit-Medium.ttf",
        "regular": "Outfit-Regular.ttf",
    }
    path = os.path.join(ASSETS_DIR, font_map.get(name, "Outfit-Regular.ttf"))
    try:
        return ImageFont.truetype(path, size)
    except (OSError, IOError):
        for fb in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
            try:
                return ImageFont.truetype(fb, size)
            except (OSError, IOError):
                continue
        return ImageFont.load_default()


def draw_gradient_line(draw, x1, y1, x2, y2, height=4):
    width = x2 - x1
    for i in range(width):
        ratio = i / width
        r = int(20 + (150 - 20) * ratio)
        g = int(40 + (90 - 40) * ratio)
        b = int(240 + (255 - 240) * ratio)
        for h in range(height):
            draw.point((x1 + i, y1 + h), fill=(r, g, b))


def generate_cover():
    # Load and scale painting to fill cover
    art = Image.open(COVER_ART).convert("RGB")
    scale = W / art.width
    art_scaled = art.resize((W, int(art.height * scale)), Image.LANCZOS)

    if art_scaled.height > H:
        top = (art_scaled.height - H) // 2
        art_scaled = art_scaled.crop((0, top, W, top + H))
    elif art_scaled.height < H:
        canvas = Image.new("RGB", (W, H), (10, 10, 15))
        canvas.paste(art_scaled, (0, 0))
        art_scaled = canvas

    cover = art_scaled.copy().convert("RGBA")

    # Top gradient overlay — softer, lets painting show through
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    for y in range(int(H * 0.38)):
        ratio = 1.0 - (y / (H * 0.38))
        alpha = int(210 * ratio * ratio)
        overlay_draw.line([(0, y), (W, y)], fill=(8, 10, 20, alpha))

    # Bottom gradient — for author name
    for y in range(H - int(H * 0.18), H):
        progress = (y - (H - int(H * 0.18))) / (H * 0.18)
        alpha = int(220 * progress ** 1.5)
        overlay_draw.line([(0, y), (W, y)], fill=(8, 10, 20, alpha))

    cover = Image.alpha_composite(cover, overlay).convert("RGB")
    draw = ImageDraw.Draw(cover)

    # Title — large, bold, white with shadow
    font_title = load_font("bold", 160)
    title_y = int(H * 0.06)
    for line in TITLE_LINES:
        bbox = draw.textbbox((0, 0), line, font=font_title)
        lw = bbox[2] - bbox[0]
        lh = bbox[3] - bbox[1]
        # Shadow
        draw.text(((W - lw) // 2 + 3, title_y + 3), line, fill=(0, 0, 0), font=font_title)
        # Text
        draw.text(((W - lw) // 2, title_y), line, fill=(255, 255, 255), font=font_title)
        title_y += lh + 15

    # Gradient accent line below title
    line_margin = int(W * 0.18)
    draw_gradient_line(draw, line_margin, title_y + 20, W - line_margin, title_y + 20, height=4)

    # Subtitle — medium weight, brighter than before, with shadow
    font_sub = load_font("medium", 48)
    sub_bbox = draw.textbbox((0, 0), SUBTITLE, font=font_sub)
    sub_w = sub_bbox[2] - sub_bbox[0]
    sub_y = title_y + 42
    draw.text(((W - sub_w) // 2 + 2, sub_y + 2), SUBTITLE, fill=(10, 12, 20), font=font_sub)
    draw.text(((W - sub_w) // 2, sub_y), SUBTITLE, fill=(195, 198, 215), font=font_sub)

    # Author name — lower area, white, bold
    font_author = load_font("semibold", 60)
    author_bbox = draw.textbbox((0, 0), AUTHOR, font=font_author)
    author_w = author_bbox[2] - author_bbox[0]
    author_y = int(H * 0.90)
    draw.text(((W - author_w) // 2 + 2, author_y + 2), AUTHOR, fill=(0, 0, 0), font=font_author)
    draw.text(((W - author_w) // 2, author_y), AUTHOR, fill=(255, 255, 255), font=font_author)

    return cover


def main():
    print("Generating covers...")

    cover = generate_cover()

    # Portrait (print/PDF/EPUB internal)
    portrait_path = os.path.join(ASSETS_DIR, "cover_print.jpg")
    cover.save(portrait_path, "JPEG", quality=95, dpi=(300, 300))
    print(f"  Portrait: {portrait_path} ({W}x{H})")

    # Internal EPUB
    internal_path = os.path.join(ASSETS_DIR, "cover_internal.jpg")
    cover.save(internal_path, "JPEG", quality=95, dpi=(300, 300))
    print(f"  Internal: {internal_path}")

    # Kindle marketing (landscape 2560x1600)
    kw, kh = 2560, 1600
    kindle = Image.new("RGB", (kw, kh), (11, 14, 26))
    k_scale = kh / cover.height
    k_sw = int(cover.width * k_scale)
    cover_scaled = cover.resize((k_sw, kh), Image.LANCZOS)
    kindle.paste(cover_scaled, ((kw - k_sw) // 2, 0))
    kindle_path = os.path.join(ASSETS_DIR, "cover_kindle.jpg")
    kindle.save(kindle_path, "JPEG", quality=95, dpi=(300, 300))
    print(f"  Kindle:   {kindle_path} ({kw}x{kh})")

    print("Done.")


if __name__ == "__main__":
    main()
