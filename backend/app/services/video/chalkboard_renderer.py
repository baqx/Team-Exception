import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import VideoClip, AudioFileClip
from typing import List, Dict, Any, Optional, Tuple
from app.core.models import ScenePlan, ChalkAction
from app.services.video.math_renderer import MathRenderer
from app.services.video.schematic_renderer import SchematicRenderer

class ChalkboardRenderer:
    """
    Renders authentic digital blackboard explainer videos in the direct style of
    "The Organic Chemistry Tutor" (Julio on YouTube).

    Key Characteristics:
    - Pure pitch-black canvas (#000000) with ZERO digital title bars, app UI chrome, or grid lines.
    - Cumulative Blackboard: previous steps remain visible on the board as new steps are written below,
      so the student can always reference prior results without them being wiped off prematurely.
    - Character-by-Character Glyph Writing: equations write briskly at natural human handwriting speed (~1.5-3.0s),
      with the chalk tip tracing vertical handwriting arcs rather than a slow digital horizontal crop.
    - Pedagogical Audio Alignment:
        * 'write_first': Problem setups, initial formulas, and diagrams are written immediately at the start
          of the scene as a visual anchor so the student can study the equation while the tutor explains it.
        * 'synchronous': Intermediate steps write in flow with the derivation.
        * 'write_last': Boxed results & final conclusions are drawn after the verbal derivation as the climax.
    - In-place hand-drawn diagonal chalk cancelation slashes across canceled terms.
    - Yellow chalk boxed final answers drawn by the chalk stick.
    - Authentic Chalk Schematics: full support for biological cycles (e.g. Nitrogen Cycle), circuits, and flowcharts.
    """

    def __init__(self, width: int = 1280, height: int = 720, fps: int = 24):
        self.width = width
        self.height = height
        self.fps = fps
        
        # Authentic Chalk Colors
        self.color_bg = (0, 0, 0)               # Pure pitch black #000000
        self.color_white = (245, 245, 240)      # Chalk white
        self.color_yellow = (235, 215, 115)     # Yellow chalk
        self.color_cyan = (112, 160, 230)       # Cyan/blue chalk
        self.color_green = (130, 220, 150)      # Green chalk
        self.color_muted = (110, 118, 130)      # Muted slate/grey

        # Load fonts
        self.font_body = self._load_font(["segoeui.ttf", "arial.ttf"], 20)
        self.font_bold = self._load_font(["segoeuib.ttf", "arialbd.ttf"], 20)
        self.font_small = self._load_font(["segoeui.ttf", "arial.ttf"], 13)
        self.font_cancel = self._load_font(["segoeuib.ttf", "arialbd.ttf"], 16)
        self.font_tag = self._load_font(["segoeuib.ttf", "arialbd.ttf"], 14)

    def _load_font(self, font_names: List[str], size: int) -> ImageFont.ImageFont:
        for name in font_names:
            try:
                return ImageFont.truetype(name, size)
            except Exception:
                continue
        try:
            return ImageFont.load_default()
        except Exception:
            return None

    def _get_color(self, name: Optional[str]):
        if not name:
            return self.color_white
        n = name.lower()
        if "yellow" in n:
            return self.color_yellow
        elif "cyan" in n or "blue" in n:
            return self.color_cyan
        elif "green" in n:
            return self.color_green
        elif "muted" in n or "grey" in n:
            return self.color_muted
        return self.color_white

    def _extract_glyph_clusters(self, math_img: Image.Image) -> List[dict]:
        """
        Decomposes a rendered math image into individual character/glyph clusters
        by analyzing column-wise alpha projection. Enables authentic character-by-character
        handwriting animation.
        """
        alpha = np.array(math_img)[:, :, 3]
        col_sums = alpha.sum(axis=0)
        is_active = (col_sums > 0).astype(int)
        diff = np.diff(np.pad(is_active, (1, 1), 'constant'))
        starts = np.where(diff == 1)[0]
        ends = np.where(diff == -1)[0]

        clusters = []
        for s, e in zip(starts, ends):
            glyph_alpha = alpha[:, s:e]
            row_sums = glyph_alpha.sum(axis=1)
            nz = np.where(row_sums > 0)[0]
            if len(nz) > 0:
                clusters.append({
                    "x0": int(s),
                    "x1": int(e),
                    "y0": int(nz[0]),
                    "y1": int(nz[-1]),
                    "cy": int((nz[0] + nz[-1]) // 2)
                })
        return clusters

    def _draw_chalk_stick(self, draw: ImageDraw.ImageDraw, tip_x: int, tip_y: int, color_tuple: tuple):
        """
        Draws a realistic chalk stick angled at 45 degrees with tip contact glow and chalk dust.
        """
        stick_len = 15
        stick_w = 6
        draw.polygon([
            (tip_x, tip_y),
            (tip_x + stick_len, tip_y - stick_len),
            (tip_x + stick_len + stick_w, tip_y - stick_len + stick_w),
            (tip_x + stick_w, tip_y + stick_w)
        ], fill=color_tuple)
        # Bright chalk tip contact point
        draw.ellipse([tip_x - 2, tip_y - 2, tip_x + 2, tip_y + 2], fill=(255, 255, 255))
        # Micro chalk dust specks
        draw.point((tip_x - 2, tip_y + 2), fill=(220, 220, 220))
        draw.point((tip_x - 1, tip_y + 4), fill=(190, 190, 190))

    def render_scene_clip(
        self,
        scene: ScenePlan,
        audio_path: str,
        output_path: str,
        persistent_items: Optional[List[dict]] = None,
        start_y: Optional[int] = None,
    ) -> Tuple[str, List[dict], int]:
        """
        Renders a chalkboard clip synced to audio.
        Supports cumulative blackboard retention, intelligent pedagogical timing,
        diagram drawing, dynamic strike-throughs, and overflow protection.
        """
        audio_clip = AudioFileClip(audio_path)
        duration = float(audio_clip.duration)

        # Base Slate Image: Pure pitch black #000000
        base_img = Image.new("RGB", (self.width, self.height), color=self.color_bg)

        # Inherit completed items from previous scenes
        inherited_items = list(persistent_items or [])
        
        # Actions for this scene
        actions = scene.chalk_actions or []
        new_items: List[dict] = []
        margin_x = 80

        # Calculate starting Y coordinate
        curr_y = start_y if start_y is not None else 50

        # Board clear conditions:
        # 1. Start of a schematic diagram scene (needs clean chalkboard)
        # 2. Transitioning away from a schematic diagram scene (equations need clean chalkboard)
        # 3. Y-overflow (exceeds y=560)
        has_schematic = any(a.action_type == "draw_schematic" for a in actions)
        prev_was_schematic = any(it.get("action_type") == "draw_schematic" for it in inherited_items)
        if has_schematic or prev_was_schematic or curr_y > 560:
            inherited_items = []
            curr_y = 50

        # Draw already-completed inherited items onto the base blackboard
        draw_base = ImageDraw.Draw(base_img)
        for prev in inherited_items:
            self._draw_completed_item(base_img, draw_base, prev)

        # Side-by-side layout is ONLY permitted for short two-variable definitions (e.g. u = ... and dv = ...)
        is_by_parts_split = (
            len(actions) == 2 
            and actions[0].action_type == "write_latex" 
            and actions[1].action_type == "write_latex"
            and any(term in actions[0].content for term in ["u =", "u ="])
            and any(term in actions[1].content for term in ["dv =", "dv ="])
        )

        for idx, action in enumerate(actions):
            raw_text = action.content.strip()
            color_name = action.color or "white"
            col_tuple = self._get_color(color_name)
            a_type = action.action_type

            # CASE A: Strike-Through Cancellation
            if a_type == "strike_through":
                target = new_items[-1] if new_items else (inherited_items[-1] if inherited_items else None)
                item_data = {
                    "action_type": "strike_through",
                    "action": action,
                    "target_item": target,
                    "color": self.color_yellow,
                    "cancel_label": getattr(action, "cancel_label", None),
                }
                new_items.append(item_data)
                continue

            # CASE B: Schematic / Cycle / Circuit Diagram
            if a_type == "draw_schematic":
                diag_w = min(1100, self.width - 160)
                diag_h = 320
                diag_img, trace_path = SchematicRenderer.render_schematic(raw_text, width=diag_w, height=diag_h, progress=1.0)
                
                # Check for board overflow
                if curr_y + diag_h > 620:
                    inherited_items = []
                    curr_y = 50
                    base_img = Image.new("RGB", (self.width, self.height), color=self.color_bg)
                    draw_base = ImageDraw.Draw(base_img)

                item_x = (self.width - diag_w) // 2
                item_y = curr_y
                curr_y += diag_h + 25

                item_data = {
                    "action_type": "draw_schematic",
                    "action": action,
                    "schematic_img": diag_img,
                    "trace_path": trace_path,
                    "color": col_tuple,
                    "x": item_x,
                    "y": item_y,
                    "w": diag_w,
                    "h": diag_h,
                    "is_boxed": False,
                }
                new_items.append(item_data)
                continue

            # CASE C: Circle Term
            if a_type == "circle_term":
                target = new_items[-1] if new_items else (inherited_items[-1] if inherited_items else None)
                item_data = {
                    "action_type": "circle_term",
                    "action": action,
                    "target_item": target,
                    "color": self.color_yellow,
                }
                new_items.append(item_data)
                continue

            # CASE D: Standard LaTeX Formula or Text
            math_img = None
            if MathRenderer.is_math_expression(raw_text):
                math_img = MathRenderer.render_latex(raw_text, color_name=color_name, fontsize=21, dpi=130)

            clean_text = raw_text
            for tag in [r"\text{", r"\boxed{", r"\Big(", r"\Big)", r"\,", r"\;", "}"]:
                clean_text = clean_text.replace(tag, " " if tag in [r"\,", r"\;"] else "")
            clean_text = clean_text.strip()

            item_h = math_img.size[1] if math_img else 45
            item_w = math_img.size[0] if math_img else int(len(clean_text) * 11)
            is_boxed = (action.action_type == "box_answer")

            # Check if side-by-side positioning is safe and fits on board
            fits_side_by_side = False
            if is_by_parts_split and idx == 1 and new_items:
                prev_item = new_items[0]
                cand_x = prev_item["x"] + prev_item["w"] + 60
                if cand_x + item_w <= self.width - margin_x:
                    fits_side_by_side = True
                    item_x = cand_x
                    item_y = prev_item["y"]

            if not fits_side_by_side:
                # Intra-scene blackboard overflow protection
                if curr_y + item_h + (30 if is_boxed else 15) > 630:
                    inherited_items = []
                    curr_y = 50
                    base_img = Image.new("RGB", (self.width, self.height), color=self.color_bg)
                    draw_base = ImageDraw.Draw(base_img)

                item_x = margin_x
                if is_boxed:
                    curr_y += 15
                item_y = curr_y

            clusters = self._extract_glyph_clusters(math_img) if math_img else []

            item_data = {
                "action_type": action.action_type,
                "action": action,
                "math_img": math_img,
                "clusters": clusters,
                "clean_text": clean_text,
                "color": col_tuple,
                "x": item_x,
                "y": item_y,
                "w": item_w,
                "h": item_h,
                "is_boxed": is_boxed,
            }
            new_items.append(item_data)

            # Advance Y only if not side-by-side
            if not fits_side_by_side:
                spacing = 28 if not is_boxed else 36
                curr_y += item_h + spacing

        # -------------------------------------------------------------
        # Pedagogical Pacing & Audio-Visual Alignment:
        # 'write_first': Visual is drawn early (~t=0.35s) so the student
        # has the equation on board to look at while the teacher explains it.
        # 'write_last': Boxed final answer is drawn towards the end of the scene.
        # 'synchronous': Derivations proceed in logical order.
        # -------------------------------------------------------------
        total_new = max(1, len(new_items))
        buffer_start = 0.35
        buffer_end = 0.8
        usable_time = max(1.0, duration - buffer_start - buffer_end)
        slot_time = usable_time / total_new

        for i, item in enumerate(new_items):
            action_obj = item.get("action")
            user_timing = getattr(action_obj, "timing", "synchronous") if action_obj else "synchronous"

            # Determine handwriting duration (1.4s - 3.2s)
            if item["action_type"] == "strike_through":
                w_dur = 1.4
            elif item["action_type"] == "circle_term":
                w_dur = 1.6
            elif item["action_type"] == "draw_schematic":
                w_dur = min(4.5, max(2.5, slot_time * 0.85))
            elif item.get("is_boxed"):
                w_dur = min(3.8, max(2.0, (item["w"] / 130.0) + 1.2))
            else:
                n_clust = len(item.get("clusters") or [])
                w_dur = min(3.2, max(1.4, n_clust * 0.22 if n_clust > 0 else item["w"] / 130.0))

            w_dur = min(w_dur, slot_time * 0.88)

            # Assign t_start based on pedagogical timing intent
            if user_timing == "write_first" or (i == 0 and item["action_type"] in ["write_latex", "draw_schematic"]):
                # Write immediately at the start of the scene as a visual anchor
                t_start = buffer_start
            elif user_timing == "write_last" or item.get("is_boxed"):
                # Boxed answer / final summary drawn towards end of scene after explanation
                t_start = max(buffer_start + i * (slot_time * 0.5), duration - w_dur - buffer_end)
            else:
                # Synchronous intermediate derivation step
                t_start = buffer_start + i * slot_time

            # Ensure non-overlapping monotonicity
            if i > 0 and t_start < new_items[i - 1]["t_end_write"]:
                t_start = new_items[i - 1]["t_end_write"] + 0.2

            item["t_start"] = t_start
            item["t_end_write"] = min(duration - 0.2, t_start + w_dur)

        # -------------------------------------------------------------
        # Frame Generation Function
        # -------------------------------------------------------------
        def make_frame(t: float):
            img = base_img.copy()
            draw = ImageDraw.Draw(img)

            # Global timeline progress
            progress = min(1.0, max(0.0, t / max(0.001, duration)))

            for item in new_items:
                t_start = item["t_start"]
                t_end_write = item["t_end_write"]
                a_type = item["action_type"]

                if t < t_start:
                    continue

                is_writing = (t < t_end_write)
                write_p = 1.0 if not is_writing else min(1.0, max(0.0, (t - t_start) / max(0.001, t_end_write - t_start)))

                # 1. In-place Cancelation Strike-Through
                if a_type == "strike_through":
                    target = item.get("target_item")
                    if target:
                        tx, ty, tw, th = target["x"], target["y"], target["w"], target["h"]
                        # Check if specific calculus pattern or generic cancellation
                        action_content = getattr(item.get("action"), "content", "")
                        if "cancel_integrand" in action_content:
                            # Specific x cancellation in (x^2/2)(1/x)
                            s1_x0, s1_y0 = tx + int(tw * 0.65), ty + int(th * 0.72)
                            s1_x1, s1_y1 = tx + int(tw * 0.73), ty + int(th * 0.20)
                            s2_x0, s2_y0 = tx + int(tw * 0.78), ty + int(th * 0.72)
                            s2_x1, s2_y1 = tx + int(tw * 0.84), ty + int(th * 0.20)

                            if write_p <= 0.5:
                                p1 = write_p / 0.5
                                cur_x = s1_x0 + int((s1_x1 - s1_x0) * p1)
                                cur_y = s1_y0 + int((s1_y1 - s1_y0) * p1)
                                draw.line([(s1_x0, s1_y0), (cur_x, cur_y)], fill=self.color_yellow, width=3)
                                if is_writing:
                                    self._draw_chalk_stick(draw, cur_x, cur_y, self.color_yellow)
                            else:
                                draw.line([(s1_x0, s1_y0), (s1_x1, s1_y1)], fill=self.color_yellow, width=3)
                                draw.text((s1_x0 + 4, s1_y1 - 18), "x", font=self.font_cancel, fill=self.color_yellow)

                                p2 = (write_p - 0.5) / 0.5
                                cur_x = s2_x0 + int((s2_x1 - s2_x0) * p2)
                                cur_y = s2_y0 + int((s2_y1 - s2_y0) * p2)
                                draw.line([(s2_x0, s2_y0), (cur_x, cur_y)], fill=self.color_yellow, width=3)
                                if write_p > 0.8:
                                    draw.text((s2_x0 + 2, s2_y0 + 4), "1", font=self.font_cancel, fill=self.color_yellow)
                                if is_writing:
                                    self._draw_chalk_stick(draw, cur_x, cur_y, self.color_yellow)
                        else:
                            # Dynamic Generic Strike-Through across target
                            sx0 = tx + 10
                            sy0 = ty + th - 6
                            sx1 = tx + tw - 10
                            sy1 = ty + 6
                            cur_x = sx0 + int((sx1 - sx0) * write_p)
                            cur_y = sy0 + int((sy1 - sy0) * write_p)
                            draw.line([(sx0, sy0), (cur_x, cur_y)], fill=self.color_yellow, width=3)
                            
                            lbl = item.get("cancel_label")
                            if lbl and write_p > 0.6:
                                draw.text((sx1 + 4, sy1 - 12), str(lbl), font=self.font_cancel, fill=self.color_yellow)
                            if is_writing:
                                self._draw_chalk_stick(draw, cur_x, cur_y, self.color_yellow)
                    continue

                # 2. Circle Term
                if a_type == "circle_term":
                    target = item.get("target_item")
                    if target:
                        tx, ty, tw, th = target["x"], target["y"], target["w"], target["h"]
                        pad = 14
                        oval_img = SchematicRenderer.render_chalk_oval_term(tw + pad * 2, th + pad * 2, self.color_yellow)
                        if write_p >= 1.0:
                            img.paste(oval_img, (tx - pad, ty - pad), oval_img)
                        else:
                            # Progressive oval reveal
                            vis_h = max(1, int((th + pad * 2) * write_p))
                            sub_oval = oval_img.crop((0, 0, tw + pad * 2, vis_h))
                            img.paste(sub_oval, (tx - pad, ty - pad), sub_oval)
                            if is_writing:
                                self._draw_chalk_stick(draw, tx + tw + pad - 4, ty + vis_h - pad, self.color_yellow)
                    continue

                # 3. Authentic Chalkboard Schematic (Cycles, Circuits, Diagrams)
                if a_type == "draw_schematic":
                    sch_img = item["schematic_img"]
                    ix, iy, iw, ih = item["x"], item["y"], item["w"], item["h"]
                    trace_path = item.get("trace_path") or []

                    if not is_writing:
                        img.paste(sch_img, (ix, iy), sch_img)
                    else:
                        # Progressive component slice reveal
                        vis_w = max(1, min(iw, int(iw * write_p)))
                        crop_slice = sch_img.crop((0, 0, vis_w, ih))
                        img.paste(crop_slice, (ix, iy), crop_slice)

                        # Chalk stick traces active outline
                        if trace_path:
                            pt_idx = min(len(trace_path) - 1, int(write_p * len(trace_path)))
                            tp = trace_path[pt_idx]
                            self._draw_chalk_stick(draw, ix + tp[0], iy + tp[1], self.color_yellow)
                        else:
                            self._draw_chalk_stick(draw, ix + vis_w, iy + ih // 2, self.color_yellow)
                    continue

                # 4. Boxed Final Answer
                if item.get("is_boxed"):
                    math_img = item["math_img"]
                    ix, iy, iw, ih = item["x"], item["y"], item["w"], item["h"]

                    if write_p < 0.65:
                        fp = write_p / 0.65
                        if math_img:
                            vis_w = max(1, int(iw * fp))
                            crop_slice = math_img.crop((0, 0, vis_w, ih))
                            img.paste(crop_slice, (ix, iy), crop_slice)
                            if is_writing:
                                self._draw_chalk_stick(draw, ix + vis_w, iy + ih // 2, self.color_yellow)
                    else:
                        if math_img:
                            img.paste(math_img, (ix, iy), math_img)
                        else:
                            draw.text((ix, iy), item["clean_text"], font=self.font_bold, fill=self.color_yellow)

                        # Draw yellow chalk box around formula
                        bp = (write_p - 0.65) / 0.35
                        pad = 12
                        bx0, by0 = ix - pad, iy - pad
                        bx1, by1 = ix + iw + pad, iy + ih + pad
                        w_side = bx1 - bx0
                        h_side = by1 - by0
                        perim = 2 * (w_side + h_side)
                        drawn_len = perim * bp

                        # Top
                        d_top = min(drawn_len, w_side)
                        draw.line([(bx0, by0), (bx0 + d_top, by0)], fill=self.color_yellow, width=3)
                        cur_pt = (bx0 + d_top, by0)

                        # Right
                        if drawn_len > w_side:
                            d_right = min(drawn_len - w_side, h_side)
                            draw.line([(bx1, by0), (bx1, by0 + d_right)], fill=self.color_yellow, width=3)
                            cur_pt = (bx1, by0 + d_right)

                        # Bottom
                        if drawn_len > w_side + h_side:
                            d_bot = min(drawn_len - (w_side + h_side), w_side)
                            draw.line([(bx1, by1), (bx1 - d_bot, by1)], fill=self.color_yellow, width=3)
                            cur_pt = (bx1 - d_bot, by1)

                        # Left
                        if drawn_len > 2 * w_side + h_side:
                            d_left = min(drawn_len - (2 * w_side + h_side), h_side)
                            draw.line([(bx0, by1), (bx0, by1 - d_left)], fill=self.color_yellow, width=3)
                            cur_pt = (bx0, by1 - d_left)

                        if is_writing:
                            self._draw_chalk_stick(draw, int(cur_pt[0]), int(cur_pt[1]), self.color_yellow)
                    continue

                # 5. Character-by-Character Glyph Writing
                math_img = item["math_img"]
                col = item["color"]
                ix, iy, iw, ih = item["x"], item["y"], item["w"], item["h"]
                clusters = item.get("clusters") or []

                if not is_writing:
                    if math_img:
                        img.paste(math_img, (ix, iy), math_img)
                    else:
                        draw.text((ix, iy), item["clean_text"], font=self.font_body, fill=col)
                else:
                    if math_img and len(clusters) > 0:
                        n_c = len(clusters)
                        c_idx = min(n_c - 1, int(write_p * n_c))
                        c_prog = (write_p * n_c) - c_idx
                        cur_cluster = clusters[c_idx]

                        vis_w = cur_cluster["x0"] + int((cur_cluster["x1"] - cur_cluster["x0"]) * c_prog)
                        vis_w = max(1, min(iw, vis_w))
                        crop_slice = math_img.crop((0, 0, vis_w, ih))
                        img.paste(crop_slice, (ix, iy), crop_slice)

                        bob = int(math.sin(c_prog * 2 * math.pi) * 5)
                        tip_x = ix + vis_w
                        tip_y = iy + cur_cluster["cy"] + bob
                        self._draw_chalk_stick(draw, tip_x, tip_y, col)
                    elif math_img:
                        vis_w = max(1, int(iw * write_p))
                        crop_slice = math_img.crop((0, 0, vis_w, ih))
                        img.paste(crop_slice, (ix, iy), crop_slice)
                        self._draw_chalk_stick(draw, ix + vis_w, iy + ih // 2, col)
                    else:
                        vis_chars = max(1, int(len(item["clean_text"]) * write_p))
                        text_part = item["clean_text"][:vis_chars]
                        draw.text((ix, iy), text_part, font=self.font_body, fill=col)
                        self._draw_chalk_stick(draw, ix + int(len(text_part) * 11), iy + 10, col)

            # Minimalist 2px Bottom Timeline
            bar_y = self.height - 10
            bar_w = int((self.width - 80) * progress)
            draw.line([(40, bar_y), (self.width - 40, bar_y)], fill=(28, 30, 36), width=2)
            if bar_w > 0:
                draw.line([(40, bar_y), (40 + bar_w, bar_y)], fill=self.color_yellow, width=2)

            return np.array(img)

        # Create VideoClip from make_frame function using MoviePy v2
        video_clip = VideoClip(make_frame, duration=duration)
        video_clip = video_clip.with_audio(audio_clip)

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        video_clip.write_videofile(
            output_path,
            fps=self.fps,
            codec="libx264",
            audio_codec="aac",
            preset="ultrafast",
            ffmpeg_params=["-movflags", "+faststart"],
            logger=None
        )

        audio_clip.close()
        video_clip.close()

        # Combine all items for persistence to next scene
        all_completed = inherited_items + new_items
        return output_path, all_completed, curr_y

    def _draw_completed_item(self, base_img: Image.Image, draw: ImageDraw.ImageDraw, item: dict):
        """
        Draws an already-completed item in its finalized state onto the blackboard.
        """
        a_type = item.get("action_type")
        if a_type == "strike_through":
            target = item.get("target_item")
            if target:
                tx, ty, tw, th = target["x"], target["y"], target["w"], target["h"]
                action_content = getattr(item.get("action"), "content", "")
                if "cancel_integrand" in action_content:
                    s1_x0, s1_y0 = tx + int(tw * 0.65), ty + int(th * 0.72)
                    s1_x1, s1_y1 = tx + int(tw * 0.73), ty + int(th * 0.20)
                    s2_x0, s2_y0 = tx + int(tw * 0.78), ty + int(th * 0.72)
                    s2_x1, s2_y1 = tx + int(tw * 0.84), ty + int(th * 0.20)

                    draw.line([(s1_x0, s1_y0), (s1_x1, s1_y1)], fill=self.color_yellow, width=3)
                    draw.text((s1_x0 + 4, s1_y1 - 18), "x", font=self.font_cancel, fill=self.color_yellow)
                    draw.line([(s2_x0, s2_y0), (s2_x1, s2_y1)], fill=self.color_yellow, width=3)
                    draw.text((s2_x0 + 2, s2_y0 + 4), "1", font=self.font_cancel, fill=self.color_yellow)
                else:
                    sx0 = tx + 10
                    sy0 = ty + th - 6
                    sx1 = tx + tw - 10
                    sy1 = ty + 6
                    draw.line([(sx0, sy0), (sx1, sy1)], fill=self.color_yellow, width=3)
                    lbl = item.get("cancel_label")
                    if lbl:
                        draw.text((sx1 + 4, sy1 - 12), str(lbl), font=self.font_cancel, fill=self.color_yellow)
            return

        if a_type == "circle_term":
            target = item.get("target_item")
            if target:
                tx, ty, tw, th = target["x"], target["y"], target["w"], target["h"]
                pad = 14
                oval_img = SchematicRenderer.render_chalk_oval_term(tw + pad * 2, th + pad * 2, self.color_yellow)
                base_img.paste(oval_img, (tx - pad, ty - pad), oval_img)
            return

        if a_type == "draw_schematic":
            sch_img = item.get("schematic_img")
            if sch_img:
                base_img.paste(sch_img, (item["x"], item["y"]), sch_img)
            return

        ix, iy, iw, ih = item["x"], item["y"], item["w"], item["h"]
        math_img = item.get("math_img")
        col = item.get("color", self.color_white)

        if math_img:
            base_img.paste(math_img, (ix, iy), math_img)
        else:
            draw.text((ix, iy), item.get("clean_text", ""), font=self.font_body, fill=col)

        if item.get("is_boxed"):
            pad = 12
            bx0, by0 = ix - pad, iy - pad
            bx1, by1 = ix + iw + pad, iy + ih + pad
            draw.rectangle([bx0, by0, bx1, by1], outline=self.color_yellow, width=3)
            draw.text((bx1 + 16, iy + (ih // 2) - 8), "★ FINAL ANSWER", font=self.font_tag, fill=self.color_yellow)
