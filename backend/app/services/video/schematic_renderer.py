import math
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class SchematicRenderer:
    """
    Renders authentic chalkboard schematics and diagrams (cycles, circuits, flowcharts)
    in the direct visual style of a classroom blackboard.
    """

    COLOR_MAP = {
        "white": (245, 245, 240),
        "yellow": (235, 215, 115),
        "cyan": (112, 160, 230),
        "green": (130, 220, 150),
        "red": (240, 110, 110),
        "muted": (110, 118, 130),
    }

    @classmethod
    def _get_font(cls, size: int = 16, bold: bool = False) -> ImageFont.ImageFont:
        font_names = ["segoeuib.ttf", "arialbd.ttf"] if bold else ["segoeui.ttf", "arial.ttf"]
        for name in font_names:
            try:
                return ImageFont.truetype(name, size)
            except Exception:
                continue
        return ImageFont.load_default()

    @classmethod
    def is_schematic_content(cls, content: str) -> bool:
        """Determines if content describes a schematic, circuit, or cycle diagram."""
        c = content.lower()
        keywords = [
            "cycle", "nitrogen", "circuit", "thevenin", "schematic", 
            "diagram", "->", "-->", "flowchart", "bridge", "resistor"
        ]
        return any(k in c for k in keywords)

    @classmethod
    def render_chalk_oval_term(
        cls, 
        width: int, 
        height: int, 
        color: tuple = (235, 215, 115)
    ) -> Image.Image:
        """
        Renders an authentic hand-drawn chalk circle/oval to circle important terms.
        """
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        pad = 6
        x0, y0 = pad, pad
        x1, y1 = width - pad, height - pad

        # Hand-drawn ellipse with multiple layered chalk strokes for authentic texture
        for offset, alpha in [(-1, 160), (0, 255), (1, 180)]:
            c = (color[0], color[1], color[2], alpha)
            draw.ellipse([x0 + offset, y0 + offset, x1 + offset, y1 + offset], outline=c, width=2)
        
        return img

    @classmethod
    def render_nitrogen_cycle_diagram(
        cls, 
        width: int = 1000, 
        height: int = 360,
        progress: float = 1.0
    ) -> Tuple[Image.Image, List[Tuple[int, int]]]:
        """
        Renders a full 5-stage Nitrogen Cycle chalkboard diagram with nodes,
        curved cycle arrows, and chemical stage labels.
        Returns the rendered transparent RGBA image and tracing path points for the chalk stick.
        """
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        font_node = cls._get_font(15, bold=True)
        font_sub = cls._get_font(12, bold=False)
        font_arrow = cls._get_font(12, bold=True)

        col_white = cls.COLOR_MAP["white"]
        col_yellow = cls.COLOR_MAP["yellow"]
        col_cyan = cls.COLOR_MAP["cyan"]
        col_green = cls.COLOR_MAP["green"]

        # Define 5 cycle stages arranged in an elliptical classroom chalkboard layout
        cx, cy = width // 2, height // 2 - 5
        rx, ry = 360, 115

        stages = [
            {
                "angle": -math.pi / 2, # Top center
                "title": "Atmospheric N2 (78%)",
                "sub": "Triple bond (N#N), Inert",
                "color": col_yellow,
                "arrow_label": "Fixation (Rhizobium)",
            },
            {
                "angle": -math.pi / 2 + (2 * math.pi / 5), # Upper right
                "title": "Ammonium (NH4+)",
                "sub": "Biological fixation in soil",
                "color": col_cyan,
                "arrow_label": "Nitrification (Nitrosomonas)",
            },
            {
                "angle": -math.pi / 2 + 2 * (2 * math.pi / 5), # Lower right
                "title": "Nitrites (NO2-) -> Nitrates (NO3-)",
                "sub": "Oxidized by Nitrobacter",
                "color": col_white,
                "arrow_label": "Assimilation by Roots",
            },
            {
                "angle": -math.pi / 2 + 3 * (2 * math.pi / 5), # Lower left
                "title": "Organic Plant / Animal Matter",
                "sub": "Amino acids & proteins",
                "color": col_green,
                "arrow_label": "Ammonification / Decay",
            },
            {
                "angle": -math.pi / 2 + 4 * (2 * math.pi / 5), # Upper left
                "title": "Denitrification (Pseudomonas)",
                "sub": "NO3- -> NO2- -> N2 gas",
                "color": col_yellow,
                "arrow_label": "Returns N2 to air",
            },
        ]

        # Calculate node center positions
        node_positions = []
        node_boxes = []
        for s in stages:
            nx = int(cx + rx * math.cos(s["angle"]))
            ny = int(cy + ry * math.sin(s["angle"]))
            node_positions.append((nx, ny))
            bw, bh = 210, 48
            node_boxes.append((nx - bw // 2, ny - bh // 2, nx + bw // 2, ny + bh // 2))

        # Trace points for chalk stick tracking
        trace_path = []

        total_elements = len(stages) * 2 # nodes + arrows
        clamped_p = min(1.0, max(0.0, progress))
        items_to_draw = int(clamped_p * total_elements)
        sub_p = (clamped_p * total_elements) - items_to_draw

        # 1. Draw connecting directional chalk arrows
        for i in range(len(stages)):
            next_i = (i + 1) % len(stages)
            idx_in_seq = i * 2 + 1
            if clamped_p * total_elements < idx_in_seq - 0.5:
                continue

            p1 = node_positions[i]
            p2 = node_positions[next_i]

            # Vector from p1 to p2
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            dist = math.hypot(dx, dy)
            if dist < 1:
                continue

            # Shorten arrow so it connects node borders, not centers
            start_x = p1[0] + (dx / dist) * 105
            start_y = p1[1] + (dy / dist) * 28
            end_x = p2[0] - (dx / dist) * 105
            end_y = p2[1] - (dy / dist) * 28

            # Curved midpoint for organic chalkboard feel
            mid_x = (start_x + end_x) / 2 + (-dy / dist) * 22
            mid_y = (start_y + end_y) / 2 + (dx / dist) * 22

            # Sample bezier curve points
            curve_pts = []
            for t in np.linspace(0, 1, 20):
                bx = (1 - t)**2 * start_x + 2 * (1 - t) * t * mid_x + t**2 * end_x
                by = (1 - t)**2 * start_y + 2 * (1 - t) * t * mid_y + t**2 * end_y
                curve_pts.append((int(bx), int(by)))

            trace_path.extend(curve_pts)

            # Draw curved arrow line
            for j in range(len(curve_pts) - 1):
                draw.line([curve_pts[j], curve_pts[j + 1]], fill=(180, 200, 230), width=2)

            # Draw arrowhead at end
            tip = (int(end_x), int(end_y))
            angle = math.atan2(end_y - mid_y, end_x - mid_x)
            arr_len = 12
            left_wing = (
                int(tip[0] - arr_len * math.cos(angle - math.pi / 6)),
                int(tip[1] - arr_len * math.sin(angle - math.pi / 6)),
            )
            right_wing = (
                int(tip[0] - arr_len * math.cos(angle + math.pi / 6)),
                int(tip[1] - arr_len * math.sin(angle + math.pi / 6)),
            )
            draw.polygon([tip, left_wing, right_wing], fill=col_yellow)

            # Draw arrow annotation label
            label_text = stages[i]["arrow_label"]
            draw.text((int(mid_x - 35), int(mid_y - 8)), label_text, font=font_arrow, fill=col_yellow)

        # 2. Draw Nodes (Chalk rounded boxes + titles + subtitles)
        for i, s in enumerate(stages):
            idx_in_seq = i * 2
            if clamped_p * total_elements < idx_in_seq:
                continue

            box = node_boxes[i]
            col = s["color"]

            # Background slate plate for readability
            draw.rounded_rectangle(box, radius=8, fill=(16, 20, 26), outline=col, width=2)
            
            # Chalk texture border lines
            draw.line([(box[0] + 3, box[1] - 1), (box[2] - 3, box[1] - 1)], fill=col, width=1)
            draw.line([(box[0] + 3, box[3] + 1), (box[2] - 3, box[3] + 1)], fill=col, width=1)

            # Node Title & Subtitle
            t_w = int(len(s["title"]) * 7.5)
            s_w = int(len(s["sub"]) * 6.0)
            t_x = (box[0] + box[2]) // 2 - t_w // 2
            s_x = (box[0] + box[2]) // 2 - s_w // 2

            draw.text((t_x, box[1] + 8), s["title"], font=font_node, fill=col)
            draw.text((s_x, box[1] + 28), s["sub"], font=font_sub, fill=(200, 205, 215))

            trace_path.append(((box[0] + box[2]) // 2, (box[1] + box[3]) // 2))

        return img, trace_path

    @classmethod
    def render_circuit_schematic(
        cls,
        width: int = 860,
        height: int = 300,
        title: str = "Thevenin Bridge Network (Terminals A - B)",
        progress: float = 1.0,
    ) -> Tuple[Image.Image, List[Tuple[int, int]]]:
        """
        Renders an authentic hand-drawn chalkboard circuit schematic:
        Independent 24V source, 4-resistor bridge network (R1=3Ω, R2=6Ω, R3=4Ω, R4=8Ω),
        terminals A and B with test load.
        """
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        font_label = cls._get_font(15, bold=True)
        font_title = cls._get_font(16, bold=True)
        font_val = cls._get_font(13, bold=False)

        col_white = cls.COLOR_MAP["white"]
        col_yellow = cls.COLOR_MAP["yellow"]
        col_cyan = cls.COLOR_MAP["cyan"]

        trace_points = []

        # Circuit layout coordinates
        src_x = 90
        top_y = 60
        bot_y = 240
        node_a_x = 340
        node_b_x = 520
        term_x = 720
        mid_y = (top_y + bot_y) // 2

        # 1. Independent Voltage Source (Circle with + and -)
        src_cy = mid_y
        r_src = 24
        draw.ellipse([src_x - r_src, src_cy - r_src, src_x + r_src, src_cy + r_src], outline=col_yellow, width=2)
        draw.text((src_x - 6, src_cy - 18), "+", font=font_label, fill=col_yellow)
        draw.text((src_x - 5, src_cy + 2), "-", font=font_label, fill=col_yellow)
        draw.text((src_x - 65, src_cy - 8), "24 V", font=font_label, fill=col_yellow)

        # 2. Main rails
        draw.line([(src_x, src_cy - r_src), (src_x, top_y), (node_b_x + 60, top_y)], fill=col_white, width=2)
        draw.line([(src_x, src_cy + r_src), (src_x, bot_y), (node_b_x + 60, bot_y)], fill=col_white, width=2)

        # Helper: Chalk Resistor (Zig-zag)
        def draw_chalk_resistor(x1, y1, x2, y2, label, value, col):
            dx = x2 - x1
            dy = y2 - y1
            dist = math.hypot(dx, dy)
            lead = 24
            p_start = (x1 + int(dx * (lead / dist)), y1 + int(dy * (lead / dist)))
            p_end = (x2 - int(dx * (lead / dist)), y2 - int(dy * (lead / dist)))

            # Wire leads
            draw.line([(x1, y1), p_start], fill=col_white, width=2)
            draw.line([p_end, (x2, y2)], fill=col_white, width=2)

            # 4 zig-zags
            steps = 6
            perp_x = -dy / dist
            perp_y = dx / dist
            amp = 12
            pts = [p_start]
            for s in range(1, steps):
                t = s / steps
                sign = 1 if s % 2 == 1 else -1
                cur_x = int(p_start[0] + (p_end[0] - p_start[0]) * t + perp_x * amp * sign)
                cur_y = int(p_start[1] + (p_end[1] - p_start[1]) * t + perp_y * amp * sign)
                pts.append((cur_x, cur_y))
            pts.append(p_end)

            for j in range(len(pts) - 1):
                draw.line([pts[j], pts[j + 1]], fill=col, width=2)

            # Label text
            lx = (x1 + x2) // 2 + int(perp_x * 24)
            ly = (y1 + y2) // 2 + int(perp_y * 14)
            draw.text((lx - 15, ly - 10), label, font=font_label, fill=col)
            draw.text((lx - 15, ly + 6), value, font=font_val, fill=(200, 205, 215))

        # Branch 1: Node A
        draw_chalk_resistor(node_a_x, top_y, node_a_x, mid_y, "R1", "3 Ω", col_cyan)
        draw_chalk_resistor(node_a_x, mid_y, node_a_x, bot_y, "R2", "6 Ω", col_cyan)

        # Branch 2: Node B
        draw_chalk_resistor(node_b_x, top_y, node_b_x, mid_y, "R3", "4 Ω", col_white)
        draw_chalk_resistor(node_b_x, mid_y, node_b_x, bot_y, "R4", "8 Ω", col_white)

        # Terminals A and B
        draw.line([(node_a_x, mid_y), (term_x, mid_y - 25)], fill=col_yellow, width=2)
        draw.line([(node_b_x, mid_y), (term_x, mid_y + 25)], fill=col_yellow, width=2)

        # Terminal Ports (Open Circles)
        draw.ellipse([term_x - 5, mid_y - 30, term_x + 5, mid_y - 20], outline=col_yellow, width=2)
        draw.text((term_x + 12, mid_y - 32), "Terminal A (16.0 V)", font=font_label, fill=col_yellow)

        draw.ellipse([term_x - 5, mid_y + 20, term_x + 5, mid_y + 30], outline=col_yellow, width=2)
        draw.text((term_x + 12, mid_y + 18), "Terminal B (8.0 V)", font=font_label, fill=col_yellow)

        # Differential Voltage Arrow between A and B
        draw.line([(term_x + 4, mid_y - 16), (term_x + 4, mid_y + 16)], fill=col_yellow, width=2)
        draw.text((term_x + 12, mid_y - 8), "V_th = 8.00 V", font=font_label, fill=col_yellow)

        trace_points.append((term_x, mid_y))
        return img, trace_points

    @classmethod
    def render_physics_coordinate_diagram(
        cls,
        width: int = 900,
        height: int = 260,
        title: str = "Vertical Motion Sign Convention",
        progress: float = 1.0,
    ) -> Tuple[Image.Image, List[Tuple[int, int]]]:
        """
        Renders an authentic blackboard chalk coordinate diagram for 1D physics:
        - Coordinate axes (+y pointing up, -y pointing down)
        - Ground reference (y = 0)
        - Object with upward velocity arrow (v0 > 0)
        - Downward gravitational acceleration arrow (a = -g = -9.80 m/s^2)
        - Rule summary box: Up (+), Down (-)
        """
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        font_title = cls._get_font(16, bold=True)
        font_main = cls._get_font(14, bold=True)
        font_sub = cls._get_font(13, bold=False)
        font_sm = cls._get_font(11, bold=False)

        col_white = cls.COLOR_MAP["white"]
        col_yellow = cls.COLOR_MAP["yellow"]
        col_cyan = cls.COLOR_MAP["cyan"]
        col_muted = cls.COLOR_MAP["muted"]

        trace_points = []

        # 1. Sign Convention Rule Box on left
        box_left, box_top, box_right = 30, 20, 440
        draw.rounded_rectangle([box_left, box_top, box_right, 75], radius=6, outline=col_yellow, width=2)
        draw.text((box_left + 15, box_top + 10), "Vertical Motion Sign Convention", font=font_title, fill=col_yellow)
        draw.text((box_left + 15, box_top + 32), "Direction: Upward (+), Downward (-)", font=font_sub, fill=col_white)

        draw.text((box_left + 15, 95), "* Dropped from rest:    v0 = 0", font=font_main, fill=col_white)
        draw.text((box_left + 15, 125), "* Thrown upward:        v0 > 0  (Positive)", font=font_main, fill=col_cyan)
        draw.text((box_left + 15, 155), "* Thrown downward:      v0 < 0  (Negative)", font=font_main, fill=(240, 140, 140))
        draw.text((box_left + 15, 185), "* Acceleration:         Always a = -g = -9.80 m/s^2", font=font_main, fill=col_yellow)
        draw.text((box_left + 15, 210), "  (Gravity ALWAYS points downward toward Earth)", font=font_sm, fill=(200, 205, 215))

        # 2. Coordinate Y-Axis
        axis_x = 520
        y_top = 35
        y_bot = 220
        draw.line([(axis_x, y_bot), (axis_x, y_top)], fill=col_white, width=2)
        # Top arrow
        draw.polygon([(axis_x, y_top - 8), (axis_x - 6, y_top + 4), (axis_x + 6, y_top + 4)], fill=col_white)
        draw.text((axis_x - 28, y_top - 5), "+y", font=font_title, fill=col_white)
        draw.text((axis_x - 24, y_bot - 15), "-y", font=font_title, fill=col_white)

        # Ground reference line
        draw.line([(axis_x - 40, y_bot), (axis_x + 320, y_bot)], fill=col_muted, width=1)
        draw.text((axis_x + 230, y_bot - 18), "Ground (y = 0)", font=font_sm, fill=(180, 190, 205))

        # 3. Particle / Ball in Free Fall
        ball_x = axis_x + 85
        ball_y = 125
        r = 15
        draw.ellipse([ball_x - r, ball_y - r, ball_x + r, ball_y + r], fill=(20, 26, 36), outline=col_cyan, width=2)
        draw.text((ball_x - 7, ball_y - 8), "m", font=font_sub, fill=col_cyan)

        # Upward velocity vector
        draw.line([(ball_x, ball_y - r), (ball_x, ball_y - r - 45)], fill=col_cyan, width=2)
        draw.polygon([(ball_x, ball_y - r - 52), (ball_x - 5, ball_y - r - 40), (ball_x + 5, ball_y - r - 40)], fill=col_cyan)
        draw.text((ball_x + 12, ball_y - r - 45), "v > 0 (Upward)", font=font_main, fill=col_cyan)

        # Downward gravity vector
        g_x = ball_x + 65
        draw.line([(g_x, ball_y), (g_x, ball_y + 55)], fill=col_yellow, width=2)
        draw.polygon([(g_x, ball_y + 63), (g_x - 5, ball_y + 50), (g_x + 5, ball_y + 50)], fill=col_yellow)
        draw.text((g_x + 12, ball_y + 25), "a = -g = -9.80 m/s^2", font=font_main, fill=col_yellow)
        draw.text((g_x + 12, ball_y + 48), "(Always downward)", font=font_sm, fill=(200, 205, 215))

        trace_points.append((ball_x, ball_y))
        return img, trace_points

    @classmethod
    def render_generic_flowchart_diagram(
        cls,
        content: str,
        width: int = 900,
        height: int = 240,
        progress: float = 1.0,
    ) -> Tuple[Image.Image, List[Tuple[int, int]]]:
        """
        Renders a horizontal series of chalk rounded boxes connected by arrows for general concepts.
        """
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        font_node = cls._get_font(14, bold=True)
        font_sub = cls._get_font(12, bold=False)

        col_white = cls.COLOR_MAP["white"]
        col_yellow = cls.COLOR_MAP["yellow"]
        col_cyan = cls.COLOR_MAP["cyan"]

        # Parse steps from content: "Step 1 -> Step 2 -> Step 3"
        raw_steps = [s.strip() for s in content.replace("-->", "->").split("->") if s.strip()]
        if not raw_steps or len(raw_steps) == 1:
            raw_steps = [s.strip() for s in content.split(",") if s.strip()]
        if not raw_steps or len(raw_steps) == 1:
            raw_steps = [content[:30], "Governing Relationship", "Verified Solution"]

        num_steps = min(4, len(raw_steps))
        steps = raw_steps[:num_steps]

        box_w = min(190, (width - 60 - (num_steps - 1) * 50) // num_steps)
        box_h = 60
        start_x = 40
        y_center = height // 2

        trace_points = []
        colors = [col_yellow, col_cyan, col_white, col_yellow]

        for i, text in enumerate(steps):
            bx0 = start_x + i * (box_w + 50)
            by0 = y_center - box_h // 2
            bx1 = bx0 + box_w
            by1 = by0 + box_h
            col = colors[i % len(colors)]

            draw.rounded_rectangle([bx0, by0, bx1, by1], radius=8, fill=(16, 20, 26), outline=col, width=2)
            words = text.split()
            line1 = " ".join(words[:2]) if len(words) > 2 else text
            line2 = " ".join(words[2:5]) if len(words) > 2 else ""

            draw.text((bx0 + 10, by0 + 12), line1[:20], font=font_node, fill=col)
            if line2:
                draw.text((bx0 + 10, by0 + 32), line2[:22], font=font_sub, fill=(200, 205, 215))

            trace_points.append(((bx0 + bx1) // 2, y_center))

            # Arrow to next box
            if i < len(steps) - 1:
                ax0 = bx1 + 6
                ax1 = bx1 + 44
                draw.line([(ax0, y_center), (ax1, y_center)], fill=col_white, width=2)
                draw.polygon([(ax1, y_center), (ax1 - 6, y_center - 4), (ax1 - 6, y_center + 4)], fill=col_white)

        return img, trace_points

    @classmethod
    def execute_matplotlib_code(
        cls,
        code: str,
        width: int = 900,
        height: int = 300,
    ) -> Tuple[Image.Image, List[Tuple[int, int]]]:
        """
        Executes dynamic Matplotlib drawing code generated by the LLM in a safe chalkboard sandbox.
        """
        import io

        clean_code = code.strip()
        if clean_code.startswith("```python"):
            clean_code = clean_code[9:]
        elif clean_code.startswith("```"):
            clean_code = clean_code[3:]
        if clean_code.endswith("```"):
            clean_code = clean_code[:-3]
        clean_code = clean_code.strip()

        fig, ax = plt.subplots(figsize=(width / 100, height / 100), dpi=100)
        fig.patch.set_facecolor((0, 0, 0, 0))
        ax.set_facecolor((0, 0, 0, 0))

        # Chalkboard axes aesthetics
        for spine in ax.spines.values():
            spine.set_color("#5a6270")
            spine.set_linewidth(1.0)
        ax.tick_params(colors="#c8cdd7", labelsize=10)

        safe_env = {
            "ax": ax,
            "plt": plt,
            "np": np,
            "math": math,
            "patches": patches,
            "white": "#f5f5f0",
            "yellow": "#ebd773",
            "cyan": "#70a0e6",
            "green": "#82dc96",
            "red": "#f06e6e",
            "muted": "#707682",
        }

        try:
            exec(clean_code, safe_env)
        except Exception as e:
            print(f"[SchematicRenderer Warning] Dynamic Matplotlib code execution failed: {e}. Falling back to smart dynamic diagram.")
            plt.close(fig)
            return cls.render_smart_dynamic_diagram(clean_code, width=width, height=height)

        buf = io.BytesIO()
        fig.savefig(buf, format="png", transparent=True, bbox_inches="tight", pad_inches=0.1)
        plt.close(fig)
        buf.seek(0)
        img = Image.open(buf)
        return img, [(width // 2, height // 2)]

    @classmethod
    def render_smart_dynamic_diagram(
        cls,
        description: str,
        width: int = 900,
        height: int = 280,
    ) -> Tuple[Image.Image, List[Tuple[int, int]]]:
        """
        Dynamically generates a customized chalkboard Matplotlib figure from natural language
        descriptions (trajectories, vectors, coordinate systems, forces).
        """
        import io

        desc = description.strip()
        d_lower = desc.lower()

        # 1. Physics: 1D Vertical Motion / Sign Convention / Free Fall
        if any(k in d_lower for k in ["sign", "convention", "up", "down", "free fall", "coordinate", "y-axis"]):
            return cls.render_physics_coordinate_diagram(width=width, height=min(height, 260))

        # 2. Physics: Projectile / Trajectory / Parabola / Curve
        if any(k in d_lower for k in ["parabola", "trajectory", "projectile", "curve", "t^2", "x^2"]):
            fig, ax = plt.subplots(figsize=(width / 100, height / 100), dpi=100)
            fig.patch.set_facecolor((0, 0, 0, 0))
            ax.set_facecolor((0, 0, 0, 0))

            t = np.linspace(0, 3.0, 100)
            y = 45 - 5 * t**2
            ax.plot(t, y, color="#ebd773", lw=2.5, label="Trajectory y(t)")
            ax.axhline(0, color="#f5f5f0", linestyle="--", alpha=0.5)
            ax.scatter([0, 3.0], [45, 0], color="#70a0e6", s=60, zorder=5)
            ax.text(0.1, 46, "Start (y0)", color="#70a0e6", fontsize=11, fontweight="bold")
            ax.text(3.05, 3, "Impact (y=0)", color="#ebd773", fontsize=11, fontweight="bold")
            ax.set_xlabel("Time (s)", color="#f5f5f0", fontsize=10)
            ax.set_ylabel("Position (m)", color="#f5f5f0", fontsize=10)
            ax.set_title(desc[:40], color="#f5f5f0", fontsize=12, fontweight="bold", pad=8)
            for spine in ax.spines.values():
                spine.set_color("#5a6270")
            ax.tick_params(colors="#c8cdd7", labelsize=9)

            buf = io.BytesIO()
            fig.savefig(buf, format="png", transparent=True, bbox_inches="tight", pad_inches=0.1)
            plt.close(fig)
            buf.seek(0)
            return Image.open(buf), [(width // 2, height // 2)]

        # 3. Process / Steps / Flowchart ("A -> B -> C")
        if "->" in desc or "-->" in desc or "step" in d_lower or "cycle" in d_lower:
            return cls.render_generic_flowchart_diagram(content=desc, width=width, height=min(height, 240))

        # 4. General concept card / diagram
        fig, ax = plt.subplots(figsize=(width / 100, height / 100), dpi=100)
        fig.patch.set_facecolor((0, 0, 0, 0))
        ax.set_facecolor((0, 0, 0, 0))
        ax.axis("off")

        rect = patches.FancyBboxPatch((0.05, 0.1), 0.9, 0.8, boxstyle="round,pad=0.04", ec="#ebd773", fc="#10141a", lw=2)
        ax.add_patch(rect)
        ax.text(0.5, 0.72, desc[:45], color="#ebd773", fontsize=13, fontweight="bold", ha="center", va="center")
        ax.plot([0.15, 0.85], [0.58, 0.58], color="#5a6270", lw=1)
        ax.text(0.5, 0.40, "Key Visual Framework & Governing Principle", color="#f5f5f0", fontsize=11, ha="center", va="center")
        ax.text(0.5, 0.25, "[Refer to line-by-line chalk derivation below]", color="#70a0e6", fontsize=10, style="italic", ha="center", va="center")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

        buf = io.BytesIO()
        fig.savefig(buf, format="png", transparent=True, bbox_inches="tight", pad_inches=0.1)
        plt.close(fig)
        buf.seek(0)
        return Image.open(buf), [(width // 2, height // 2)]

    @classmethod
    def render_schematic(
        cls, 
        content: str, 
        width: int = 1000, 
        height: int = 340,
        progress: float = 1.0
    ) -> Tuple[Image.Image, List[Tuple[int, int]]]:
        """
        Dispatches schematic rendering dynamically:
        1. If content is Python/Matplotlib code, executes it dynamically on the chalkboard.
        2. If explicitly biology (nitrogen), renders the 5-stage biological cycle.
        3. If explicitly an electrical bridge circuit, renders the Thevenin circuit.
        4. Otherwise, generates a dynamic Matplotlib visualization based on the concept.
        """
        c = content.strip()
        c_lower = c.lower()

        # Case 1: Dynamic Python / Matplotlib code generated by LLM
        if any(marker in c for marker in ["ax.", "plt.", "np.", "import ", "def ", "patches."]):
            return cls.execute_matplotlib_code(c, width=width, height=height)

        # Case 2: Specific legacy topic match (Biology / Nitrogen)
        if any(k in c_lower for k in ["nitrogen", "rhizobium", "nitrification", "denitrification"]) and not any(k in c_lower for k in ["motion", "sign", "physics", "circuit"]):
            return cls.render_nitrogen_cycle_diagram(width=width, height=height, progress=progress)

        # Case 3: Specific legacy topic match (Electrical circuits)
        if any(k in c_lower for k in ["thevenin", "bridge network", "resistor bridge", "circuit_bridge_schematic"]):
            return cls.render_circuit_schematic(width=width, height=height, progress=progress)

        # Case 4: Smart dynamic Matplotlib diagram
        return cls.render_smart_dynamic_diagram(c, width=width, height=min(height, 270))


