#!/usr/bin/env python
"""Concept diagrams for the docs, as SVG in the project page style (Inter, light cards, DexSuite blue for the one
thing each diagram is about). Pages include them inline (``{raw} html`` with ``:file:``) so the text uses the page font.

The article column is about 700 px wide, so the canvases are 760 units wide and the text is sized for that: the
diagrams display close to 1:1 and stay readable.

    python3 tools/make_diagrams.py        -> docs/source/_static/diagrams/*.svg
"""
from __future__ import annotations

from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "docs/source/_static/diagrams"
INK, INK2, INK3, CARD, RULE, BLUE, DEEP = "#1d1d1f", "#6e6e73", "#86868b", "#f5f5f7", "#d2d2d7", "#289be4", "#1468b8"
FONT = "Inter, -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace"
W = 760


class Svg:
    def __init__(self, h, label):
        self.h, self.label, self.parts = h, label, []

    def add(self, s):
        self.parts.append(s)

    def card(self, x, y, w, h, fill=CARD, stroke=None, rx=14):
        st = f' stroke="{stroke}" stroke-width="1.5"' if stroke else ""
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{st}/>')

    def text(self, x, y, s, size=15, weight=400, fill=INK, anchor="start", mono=False):
        self.add(f'<text x="{x}" y="{y}" font-family="{MONO if mono else FONT}" font-size="{size}" font-weight="{weight}" '
                 f'fill="{fill}" text-anchor="{anchor}">{escape(s)}</text>')

    def arrow(self, x1, y1, x2, y2):
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#b7b7bd" stroke-width="1.8" marker-end="url(#ah)"/>')

    def path(self, d):
        self.add(f'<path d="{d}" fill="none" stroke="#b7b7bd" stroke-width="1.8" marker-end="url(#ah)"/>')

    def pill(self, x, y, w, h, s, size=17):
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="url(#ds)"/>')
        self.text(x + w / 2, y + h / 2 + size * 0.36, s, size, 600, "#ffffff", "middle", mono=True)

    def write(self, name):
        defs = (f'<defs><linearGradient id="ds" x1="0" y1="0" x2="1" y2="0.2"><stop offset="0" stop-color="{DEEP}"/>'
                f'<stop offset="0.6" stop-color="{BLUE}"/><stop offset="1" stop-color="#45b2ee"/></linearGradient>'
                '<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                '<path d="M0 0 L10 5 L0 10 z" fill="#b7b7bd"/></marker></defs>')
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" class="ds-diagram" viewBox="0 0 {W} {self.h}" role="img" '
               f'aria-label="{escape(self.label)}">{defs}' + "".join(self.parts) + "</svg>\n")
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / f"{name}.svg").write_text(svg)


def make_diagram():
    s = Svg(420, "ds.make combines a task, a robot, cameras and the simulator into one environment")
    rows = [("Task", '"lift"'), ("Robot", 'arm + end-effector'), ("Cameras", 'front, wrist'), ("Simulator", "Genesis, 20 Hz")]
    for i, (t, a) in enumerate(rows):
        y = 10 + i * 102
        s.card(0, y, 236, 86)
        s.text(22, y + 36, t, 19, 600)
        s.text(22, y + 64, a, 15, 400, INK2, mono=True)
        s.path(f"M236 {y + 43} C 262 {y + 43}, 262 206, 282 206")
    s.pill(286, 182, 150, 48, "ds.make", 18)
    s.arrow(438, 206, 470, 206)
    s.card(474, 96, 286, 220, fill="#ffffff", stroke=RULE, rx=18)
    s.text(498, 136, "Environment", 20, 700)
    s.text(498, 182, "reset(seed)", 15, 600, DEEP, mono=True)
    s.text(498, 206, "→ obs, info", 15, 400, INK, mono=True)
    s.text(498, 246, "step(action)", 15, 600, DEEP, mono=True)
    s.text(498, 270, "→ obs, reward, terminated,", 14, 400, INK, mono=True)
    s.text(498, 292, "   truncated, info", 14, 400, INK, mono=True)
    s.write("make")


def robot_diagram():
    s = Svg(300, "A modular robot: arm, mount, end-effector, joined at the arm's last link")
    boxes = [("Arm", 'manipulator="ur5"', ["fixed at its base pose", "home pose, gains", "ends at end_link"]),
             ("Mount", "adapter file", ["one entry per", "end-effector", "pose on end_link"]),
             ("End-effector", 'gripper="allegro"', ["welded to the mount", "joint limits", "tool point (TCP)"])]
    for i, (t, k, ls) in enumerate(boxes):
        x = i * 262
        hl = i == 1
        s.card(x, 10, 236, 200, fill="#ffffff" if hl else CARD, stroke=BLUE if hl else None, rx=16)
        s.text(x + 22, 50, t, 20, 700, DEEP if hl else INK)
        s.text(x + 22, 78, k, 14, 400, INK2, mono=True)
        for j, l in enumerate(ls):
            s.text(x + 22, 120 + j * 28, l, 16, 400, INK)
        if i < 2:
            s.arrow(x + 238, 110, x + 260, 110)
    s.text(0, 252, "Integrated robots carry their own gripper in one model.", 16, 400, INK2)
    s.text(0, 280, "The floating wrist replaces the arm with a 6-DoF virtual gantry.", 16, 400, INK2)
    s.write("robot")


def action_diagram():
    s = Svg(300, "Action layout: arm slice then end-effector slice; for two arms, left then right")
    s.text(0, 24, "One arm", 17, 600)
    s.card(0, 40, 240, 60, fill="url(#ds)", rx=12)
    s.text(120, 77, "arm · 6", 17, 600, "#ffffff", "middle", mono=True)
    s.card(248, 40, 512, 60, fill=CARD, rx=12)
    s.text(504, 77, "end-effector · 1 to 24", 17, 500, INK, "middle", mono=True)
    s.text(0, 130, "osc_pose: dx dy dz droll dpitch dyaw", 14, 400, INK2, mono=True)
    s.text(760, 130, "joint_position: one per joint", 14, 400, INK2, "end", mono=True)
    s.text(0, 186, "Two arms", 17, 600)
    x = 0
    for i, (ww, lb) in enumerate(zip([140, 236, 140, 236], ["left arm", "left hand", "right arm", "right hand"])):
        arm = i % 2 == 0
        s.card(x, 202, ww - 8, 56, fill="url(#ds)" if arm else CARD, rx=12)
        s.text(x + (ww - 8) / 2, 237, lb, 16, 600 if arm else 500, "#ffffff" if arm else INK, "middle", mono=True)
        x += ww + 2
    s.write("action")


def obs_diagram():
    s = Svg(400, "The observation dictionary: state (manipulator, gripper, other) and cameras")
    s.pill(0, 176, 84, 46, "obs", 17)
    groups = [("state", 14, [("manipulator", "qpos, qvel, eef_pos ..."), ("gripper", "qpos, tcp_pos, tactile ..."),
                             ("other", "task values, last action")]),
              ("cameras", 248, [("front", "rgb, depth ..."), ("wrist", "rgb, depth ...")])]
    for name, y0, rows in groups:
        mid = y0 + (len(rows) * 62 - 8) / 2
        s.path(f"M84 199 C 110 199, 110 {mid}, 134 {mid}")
        s.card(136, mid - 23, 124, 46, fill="#ffffff", stroke=RULE, rx=12)
        s.text(198, mid + 6, name, 16, 600, INK, "middle", mono=True)
        for j, (k, v) in enumerate(rows):
            y = y0 + j * 62
            s.path(f"M260 {mid} C 282 {mid}, 282 {y + 27}, 302 {y + 27}")
            s.card(304, y, 456, 54, fill=CARD, rx=12)
            s.text(324, y + 33, k, 16, 600, DEEP, mono=True)
            s.text(470, y + 33, v, 14.5, 400, INK2, mono=True)
    s.write("obs")


def teleop_diagram():
    s = Svg(380, "Teleoperation and recording: device, controller, environment, LeRobot dataset")
    devs = ["Keyboard", "SpaceMouse", "Vive tracker", "Manus glove"]
    for i, d in enumerate(devs):
        y = 10 + i * 64
        s.card(0, y, 170, 50)
        s.text(85, y + 31, d, 16, 600, INK, "middle")
        s.path(f"M170 {y + 25} C 196 {y + 25}, 196 128, 216 128")
    steps = [("controller", "pose and joints"), ("env.step", "any task, any robot"), ("LeRobotLogger", "each step")]
    x = 220
    for i, (a, b) in enumerate(steps):
        hl = i == 2
        s.card(x, 92, 168, 72, fill="#ffffff" if hl else CARD, stroke=BLUE if hl else None)
        s.text(x + 84, 124, a, 15, 600, DEEP if hl else INK, "middle", mono=True)
        s.text(x + 84, 148, b, 13, 400, INK2, "middle")
        if i < 2:
            s.arrow(x + 168, 128, x + 178, 128)
        x += 180
    s.arrow(676, 166, 676, 212)
    s.card(512, 216, 248, 64, fill="#ffffff", stroke=RULE)
    s.text(636, 244, "LeRobot dataset", 16, 600, INK, "middle")
    s.text(636, 266, "→ robomimic HDF5", 13.5, 400, INK2, "middle", mono=True)
    s.text(0, 340, "The glove's finger angles come from GeoRT retargeting.", 15, 400, INK2)
    s.write("teleop")


def protocol_diagram():
    s = Svg(290, "Benchmark protocol: select the best checkpoint by rollouts, then evaluate it on three new seeds")
    steps = [("Train", "on the demos"), ("Roll out", "50 episodes,", "every 50 epochs"), ("Select", "the best", "checkpoint"),
             ("Evaluate", "3 new seeds", "× 50 episodes"), ("Report", "mean ± std")]
    x = 0
    for i, st in enumerate(steps):
        hl = i == 3
        s.card(x, 10, 140, 124, fill="#ffffff" if hl else CARD, stroke=BLUE if hl else None, rx=16)
        s.text(x + 18, 48, st[0], 18, 700, DEEP if hl else INK)
        for j, l in enumerate(st[1:]):
            s.text(x + 18, 80 + j * 22, l, 14.5, 400, INK2)
        if i < 4:
            s.arrow(x + 140, 72, x + 154, 72)
        x += 155
    s.text(0, 186, "Re-testing on new seeds keeps the number honest: the best of many", 16, 400, INK2)
    s.text(0, 212, "noisy in-training rollouts is optimistic, by about 7 points for ACT", 16, 400, INK2)
    s.text(0, 238, "on this benchmark.", 16, 400, INK2)
    s.write("protocol")


if __name__ == "__main__":
    for f in (make_diagram, robot_diagram, action_diagram, obs_diagram, teleop_diagram, protocol_diagram):
        f()
    print(sorted(p.name for p in OUT.glob("*.svg")))
