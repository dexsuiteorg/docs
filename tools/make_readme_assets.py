#!/usr/bin/env python
"""Images for the DexSuite code README, in the project page's look: Inter, DexSuite blue, renders on soft cards.

    python tools/make_readme_assets.py [--only hero track1 ...]

Writes <Dexsuite>/docs/readme/. Every image reads on GitHub's light and dark themes alike, so the README needs no
<picture> switch: text sits inside light cards, and what sits on the page itself (stat labels, logos) is a mid grey.
Inputs:

- the project page's hero frames and Track 1 clips (dexsuite_website/v2/assets) and teleop footage (static/videos),
- the docs' catalog and task renders (docs/source/_static), produced by render_catalog.py and render_tasks.py,
- the paper's Table II (paper_ol/Dexsuite/imitation_results.tex) for the benchmark chart,
- the project page's single-ink logos.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

DOCS = Path(__file__).resolve().parents[1]
STATIC = DOCS / "docs/source/_static"
sys.path.insert(0, str(Path(__file__).parent))
from paths import DEXSUITE, FONTS, PAPER, SITE  # noqa: E402

OUT = DEXSUITE / "docs/readme"
sys.path.insert(0, str(Path(__file__).parent))
import catalog_data as cat  # noqa: E402

BLUE = [(0x1f, 0x7c, 0xcc), (0x2e, 0xa0, 0xe8), (0x52, 0xb9, 0xf0)]   # the wordmark gradient, lifted to read on dark too
INK, SUB, CARD = (29, 29, 31), (110, 110, 115), (245, 245, 247)       # inside cards
MUTED = (133, 141, 151)                                                # on the page: 3.5:1 on white, 5.6:1 on #0d1117
GRID = (226, 226, 231)
GRIP, HAND = (0xeb, 0x68, 0x34), (0x2a, 0x78, 0xd6)                    # the project page's series, validator-checked
W_PAGE = 1786                                                          # 2x GitHub's content width


def font(weight, size):
    return ImageFont.truetype(str(FONTS / f"Inter-{weight}.ttf"), size)


def gradient(w, h):
    x = np.linspace(0, 1, w)[None, :, None]
    a, b, c = (np.array(v, float) for v in BLUE)
    g = np.where(x < 0.6, a + (b - a) * (x / 0.6), b + (c - b) * ((x - 0.6) / 0.4))
    return Image.fromarray(np.repeat(g, h, 0).astype(np.uint8))


def text_w(s, f):
    return f.getbbox(s)[2] - f.getbbox(s)[0]


def draw_gradient_text(img, xy, s, f, anchor="la"):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).text(xy, s, font=f, fill=255, anchor=anchor)
    bb = mask.getbbox()
    g = Image.new("RGBA", img.size, (0, 0, 0, 0))
    g.paste(gradient(bb[2] - bb[0], bb[3] - bb[1]), (bb[0], bb[1]))
    g.putalpha(mask)
    img.alpha_composite(g)


def rounded(im, r):
    """im with its corners cut to radius r (alpha)."""
    im = im.convert("RGBA")
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255)
    im.putalpha(Image.fromarray(np.minimum(np.asarray(im.getchannel("A")), np.asarray(m))))
    return im


def ink_box(im, thr=10):
    return im.getchannel("A").point(lambda v: 255 if v > thr else 0).getbbox()


def fit(im, w, h, fill=0.9):
    """Scale an RGBA render so its ink fills `fill` of a w x h box, centred."""
    im = im.crop(ink_box(im))
    s = min(w * fill / im.width, h * fill / im.height)
    im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.alpha_composite(im, ((w - im.width) // 2, (h - im.height) // 2))
    return out


def save(im, name, quality=90):
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / name
    im.save(p, "WEBP", quality=quality, alpha_quality=95, method=6)
    print(f"{name}: {im.width}x{im.height}, {p.stat().st_size / 1e6:.2f} MB")


def save_anim(frames, durations, name, quality=78):
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / name
    frames[0].save(p, "WEBP", save_all=True, append_images=frames[1:], duration=durations, loop=0,
                   quality=quality, alpha_quality=90, method=4)
    print(f"{name}: {frames[0].width}x{frames[0].height}, {len(frames)} frames, {p.stat().st_size / 1e6:.2f} MB")


def decode(path, w, h, every=1):
    """Frames of a video as RGB images, scaled to w x h, keeping every `every`-th."""
    vf = f"select=not(mod(n\\,{every})),scale={w}:{h}:flags=lanczos"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", vf, "-fps_mode", "passthrough", "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    return [Image.fromarray(f) for f in np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)]


def card(w, h, render, box, fill, title=None, sub=None, r=28):
    """A light rounded card: the render fitted into `box` (x, y, w, h) and an optional title and subtitle below it."""
    c = Image.new("RGBA", (w, h), (*CARD, 255))
    bx, by, bw, bh = box
    c.alpha_composite(fit(render, bw, bh, fill), (bx, by))
    d = ImageDraw.Draw(c)
    if title:
        d.text((w / 2, h - (64 if sub else 34)), title, font=font("SemiBold", 27), fill=INK, anchor="ms")
    if sub:
        d.text((w / 2, h - 30), sub, font=font("Regular", 22), fill=SUB, anchor="ms")
    return rounded(c, r)


# ---------------------------------------------------------------------------------------------------------- assets
def hero():
    frames = [Image.open(f).convert("RGBA") for f in sorted((SITE / "v2/assets/hero/scene").glob("f*.webp"))]
    boxes = np.array([ink_box(im) for im in frames[::4]])
    pad = 24
    box = (max(0, boxes[:, 0].min() - pad), max(0, boxes[:, 1].min() - pad),
           min(1200, boxes[:, 2].max() + pad), min(1200, boxes[:, 3].max() + pad))
    frames = [im.crop(box) for im in frames]
    w = 960
    h = round(frames[0].height * w / frames[0].width)
    frames = [im.resize((w, h), Image.LANCZOS) for im in frames]
    durs = [50] * len(frames)
    durs[0], durs[-1] = 700, 2200
    save_anim(frames, durs, "hero.webp", quality=80)


def stats():
    items = [("26", "tasks"), ("10", "arms"), ("11", "end-effectors"), ("16", "benchmark pairs"), ("4,700", "episodes")]
    img = Image.new("RGBA", (1800, 230), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    fb, fl = font("Bold", 104), font("Medium", 30)
    col = img.width / len(items)
    for i, (n, lab) in enumerate(items):
        cx = col * (i + 0.5)
        draw_gradient_text(img, (cx, 120), n, fb, anchor="ms")
        d.text((cx, 180), lab, font=fl, fill=MUTED, anchor="ms")
    save(img, "stats.webp")


def track1():
    tasks = [("reach", "Reach", "Robotiq 2F-85"), ("lift", "Lift", "UMI gripper"), ("push", "Push", "UMI gripper"),
             ("pickplace", "Pick & Place", "UMI gripper"), ("stack", "Stack", "UMI gripper")]
    cw, ch, gap = 688, 387, 24
    ft, fe = font("SemiBold", 30), font("Medium", 25)
    out = []
    for key, name, grip in tasks:
        a = decode(SITE / f"v2/assets/clips/t1_{key}_grip.mp4", cw, ch, every=2)   # every other frame: 2x speed
        b = decode(SITE / f"v2/assets/clips/t1_{key}_hand.mp4", cw, ch, every=2)
        for i in range(max(len(a), len(b))):
            fr = Image.new("RGBA", (2 * cw + gap, ch), (0, 0, 0, 0))
            for x, clip, emb in ((0, a, grip), (cw + gap, b, "Allegro hand")):
                c = clip[min(i, len(clip) - 1)].convert("RGBA")
                d = ImageDraw.Draw(c)
                d.text((30, 26), name, font=ft, fill=INK)
                d.text((30, ch - 26), emb, font=fe, fill=SUB, anchor="ls")
                fr.alpha_composite(rounded(c, 26), (x, 0))
            out.append(fr)
        out.append(out[-1])                                                         # a beat on the last frame
    save_anim(out, [50] * len(out), "track1.webp", quality=72)


def gallery(name, items, cols=4, w=430, h=500):
    """items: [(render file, title, subtitle)] as cards, rows centred."""
    gap = 22
    rows = [items[i:i + cols] for i in range(0, len(items), cols)]
    W = cols * w + (cols - 1) * gap
    img = Image.new("RGBA", (W, len(rows) * (h + gap) - gap), (0, 0, 0, 0))
    for r, row in enumerate(rows):
        x0 = (W - (len(row) * w + (len(row) - 1) * gap)) // 2
        for j, (f, title, sub) in enumerate(row):
            c = card(w, h, Image.open(f).convert("RGBA"), (0, 0, w, h - 100), 0.84, title, sub)
            img.alpha_composite(c, (x0 + j * (w + gap), r * (h + gap)))
    save(img, f"{name}.webp")


def arms():
    c = STATIC / "catalog"
    items = [(c / f"arm_{a['key']}.webp", a["name"], f"{a['maker']}, {a['dof']} DoF") for a in cat.ARMS]
    items += [(c / f"robot_{r['key']}.webp", r["name"].replace(" with Franka Hand", " + Hand"), f"{r['dof']} DoF, integrated")
              for r in cat.INTEGRATED]
    gallery("arms", items)


def hands():
    c = STATIC / "catalog"
    gallery("hands", [(c / f"ee_{e['key']}.webp", e["name"], f"{e['fingers']} fingers, {e['dof']} DoF")
                      for e in cat.END_EFFECTORS])


def task_grid(name, groups):
    """groups: [(heading, task group, columns)]; tiles fill the width of each group's row."""
    gap, head_h = 22, 84
    fh, fn = font("SemiBold", 28), font("Medium", 25)
    layout, y = [], 0
    for title, g, cols in groups:
        ts = [x for x in cat.TASKS if x["group"] == g]
        tw = (W_PAGE - (cols - 1) * gap) // cols
        th = round(tw * 0.62) + 56
        layout.append((title, ts, cols, tw, th, y))
        y += head_h + -(-len(ts) // cols) * (th + gap)
    img = Image.new("RGBA", (W_PAGE, y - gap), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for title, ts, cols, tw, th, y in layout:
        d.text((4, y + 52), title, font=fh, fill=BLUE[1], anchor="ls")
        for i, x in enumerate(ts):
            r, c = divmod(i, cols)
            tile = Image.new("RGBA", (tw, th), (*CARD, 255))
            tile.alpha_composite(fit(Image.open(STATIC / "tasks" / f"{x['key']}.webp").convert("RGBA"), tw, th - 56, 0.92))
            ImageDraw.Draw(tile).text((24, th - 26), x["name"], font=fn, fill=INK, anchor="ls")
            img.alpha_composite(rounded(tile, 26), (c * (tw + gap), y + head_h + r * (th + gap)))
    save(img, f"{name}.webp")


def tasks():
    task_grid("tasks-benchmark", [("Track 1  ·  same task, gripper or hand", "track1", 5),
                                  ("Track 2  ·  dexterous capability", "track2", 3)])
    task_grid("tasks-more", [("Single arm", "single", 4), ("Bimanual", "bimanual", 4)])


def table2():
    """Track 1 best success per task and embodiment, from the paper's Table II (same parse as the project page)."""
    tex = (PAPER / "Dexsuite/imitation_results.tex").read_text(encoding="utf-8")
    panels = []
    for block in re.findall(r"\\begin\{tabular\*\}.*?\\end\{tabular\*\}", tex, re.S):
        lines = [x.strip() for x in block.splitlines()]
        head = next(x for x in lines if x.startswith("\\textbf{Model"))
        names = [re.sub(r"\\textbf\{(.*?)\}", r"\1", c).replace("\\&", "&").strip() for c in re.split(r"(?<!\\)&", head.rstrip("\\"))[1:]]
        rows = [[float(re.search(r"(\d+(?:\.\d+)?)", c).group(1)) for c in x.rstrip("\\").split("&")[1:]]
                for x in lines if re.match(r"(BC-G|BC-GMM|BC-T|Diffusion|ACT) \(", x)]
        panels.append((names, rows))
    (n1, grip), (_, hand) = panels
    return [(n1[j], max(r[j] for r in grip), max(r[j] for r in hand)) for j in range(5)]


def chart():
    """Best Track 1 success per task, gripper vs Allegro hand, on a light card."""
    data = table2()
    W, H = 1786, 760
    left, right, top, bottom = 140, 60, 170, 110
    img = Image.new("RGBA", (W, H), (*CARD, 255))
    d = ImageDraw.Draw(img)
    fa, fv, fl = font("Regular", 24), font("Medium", 24), font("Medium", 27)
    ph = H - top - bottom
    y_of = lambda v: top + ph * (1 - v / 100)  # noqa: E731
    for v in (0, 25, 50, 75, 100):
        d.line((left, y_of(v), W - right, y_of(v)), fill=GRID, width=2)
        d.text((left - 18, y_of(v)), f"{v}", font=fa, fill=SUB, anchor="rm")
    d.text((left - 18, top - 46), "success rate, %", font=fa, fill=SUB, anchor="ls")
    gw = (W - left - right) / len(data)
    bw, inner = 92, 4                                                        # 2 px surface gap between the pair
    for i, (name, g, h) in enumerate(data):
        cx = left + gw * (i + 0.5)
        for v, col, x in ((g, GRIP, cx - inner / 2 - bw), (h, HAND, cx + inner / 2)):
            if v > 0:
                d.rounded_rectangle((x, y_of(v), x + bw, y_of(0)), 8, fill=col, corners=(True, True, False, False))
            d.text((x + bw / 2, y_of(v) - 14), f"{v:g}", font=fv, fill=INK, anchor="ms")
        d.text((cx, H - bottom + 52), name, font=fl, fill=INK, anchor="ms")
    labs = (("Parallel-jaw gripper", GRIP), ("Allegro hand", HAND))
    lx = W - right - sum(40 + text_w(lab, fl) for lab, _ in labs) - 56
    for lab, col in labs:
        d.rounded_rectangle((lx, 62, lx + 26, 88), 6, fill=col)
        d.text((lx + 40, 75), lab, font=fl, fill=INK, anchor="lm")
        lx += 40 + text_w(lab, fl) + 56
    save(rounded(img, 30), "benchmark.webp")


def logos():
    spec = [("mcgill", 80), ("mila", 64), ("amazon", 60), ("hf", 60), ("kinova", 34), ("manus", 32)]   # 2x the page's heights
    ims = []
    for k, h in spec:
        im = Image.open(SITE / f"v2/assets/logos/{k}.png").convert("RGBA")
        im = im.resize((round(im.width * h / im.height), h), Image.LANCZOS)
        ink = Image.new("RGBA", im.size, (*MUTED, 255))
        ink.putalpha(im.getchannel("A"))
        ims.append(ink)
    gap = 84
    img = Image.new("RGBA", (sum(i.width for i in ims) + gap * (len(ims) - 1), max(i.height for i in ims)), (0, 0, 0, 0))
    x = 0
    for im in ims:
        img.alpha_composite(im, (x, (img.height - im.height) // 2))
        x += im.width + gap
    save(img, "logos.webp")


def teleop():
    v = SITE / "static/videos"
    a = decode(v / "manusretarget.mp4", 800, 266, every=2)              # 25 fps footage, kept at 12.5 fps
    b = decode(v / "vivecontroller.mp4", 534, 266, every=2)
    gap = 18
    out = []
    for i in range(len(a)):
        fr = Image.new("RGBA", (800 + gap + 534, 266), (0, 0, 0, 0))
        fr.alpha_composite(rounded(a[i], 18), (0, 0))
        fr.alpha_composite(rounded(b[i % len(b)], 18), (800 + gap, 0))
        out.append(fr)
    save_anim(out, [80] * len(out), "teleop.webp", quality=74)


def wordmark():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "wordmark.svg").write_text((STATIC / "brand/wordmark.svg").read_text())
    print("wordmark.svg")


JOBS = {"wordmark": wordmark, "hero": hero, "stats": stats, "track1": track1, "arms": arms, "hands": hands,
        "tasks": tasks, "chart": chart, "teleop": teleop, "logos": logos}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", choices=list(JOBS))
    for k in ap.parse_args().only or list(JOBS):
        JOBS[k]()


if __name__ == "__main__":
    main()
