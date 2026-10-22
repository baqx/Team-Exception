import io
import re
from typing import Optional, Tuple
from PIL import Image
import matplotlib
matplotlib.use("Agg")  # Thread-safe headless raster backend for server environments
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class MathRenderer:
    """
    Renders LaTeX mathematical formulas and teacher chalk annotations
    into high-DPI transparent RGBA images using Matplotlib's MathText engine.
    Zero external LaTeX distribution required.
    """

    COLOR_MAP = {
        "yellow": "#E8D479",
        "cyan": "#709AD8",
        "white": "#F5F5F0",
        "muted": "#8E95A2",
    }

    @classmethod
    def is_math_expression(cls, text: str) -> bool:
        """
        Detects whether text contains mathematical notation, LaTeX symbols, or equations.
        """
        text_str = text.strip()
        if text_str.startswith("$") or text_str.startswith(r"\("):
            return True
        math_tokens = [
            "\\", "^", "_", "\\int", "\\frac", "\\ln", "\\boxed", "\\sum", "\\prod",
            "\\sqrt", "\\cdot", "\\times", "\\pm", "\\approx", "\\leq", "\\geq",
            "\\alpha", "\\beta", "\\gamma", "\\theta", "\\lambda", "\\mu", "\\Omega",
            "=", "+", "-"
        ]
        has_latex_cmd = bool(re.search(r"\\[a-zA-Z]+", text_str))
        has_equation = ("=" in text_str) and any(c in text_str for c in ["^", "_", "/", "\\", "+", "-", "*"])
        return has_latex_cmd or has_equation

    @classmethod
    def render_latex(
        cls,
        latex_str: str,
        color_name: str = "white",
        fontsize: int = 22,
        dpi: int = 140,
    ) -> Optional[Image.Image]:
        """
        Renders a LaTeX equation into a tightly cropped transparent PIL Image.
        """
        hex_color = cls.COLOR_MAP.get(color_name.lower(), "#F5F5F0")
        
        # Clean and sanitize LaTeX for Matplotlib mathtext compatibility
        clean = latex_str.strip()
        if clean.startswith(r"\boxed{") and clean.endswith("}"):
            clean = clean[7:-1]
        
        # Transform arrows with text above/below (\xrightarrow, \xleftarrow) into mathtext \overset
        clean = re.sub(r'\\xrightarrow\{(?:\s*\\text\{)?([^}]+)\}?\}', r'\\overset{\\mathrm{\1}}{\\longrightarrow}', clean)
        clean = re.sub(r'\\xrightarrow\{([^}]+)\}', r'\\overset{\\mathrm{\1}}{\\longrightarrow}', clean)
        clean = clean.replace(r'\xrightarrow', r'\longrightarrow')
        clean = re.sub(r'\\xleftarrow\{(?:\s*\\text\{)?([^}]+)\}?\}', r'\\overset{\\mathrm{\1}}{\\longleftarrow}', clean)
        clean = re.sub(r'\\xleftarrow\{([^}]+)\}', r'\\overset{\\mathrm{\1}}{\\longleftarrow}', clean)
        clean = clean.replace(r'\xleftarrow', r'\longleftarrow')

        # Translate \text{...} into \mathrm{...} while explicitly escaping spaces as '\ '
        # because LaTeX MathText mode otherwise discards all whitespace characters!
        def _preserve_text_spaces(match):
            inner = match.group(1)
            spaced = re.sub(r'\s+', r'\ ', inner)
            return r'\mathrm{' + spaced + '}'

        clean = re.sub(r'\\text\{([^}]+)\}', _preserve_text_spaces, clean)

        # Ensure spaces between numbers/symbols and following \mathrm blocks (e.g. "945\mathrm{" -> "945\ \mathrm{")
        clean = re.sub(r'(\d+)\s*(\\mathrm\{)', r'\1\\ \2', clean)

        # Replace non-standard macros with MathText equivalents
        clean = clean.replace(r"\implies", r"\rightarrow\ ")
        clean = clean.replace(r"\Big(", "(").replace(r"\Big)", ")")
        clean = clean.replace(r"\big(", "(").replace(r"\big)", ")")
        clean = clean.replace(r"\left.", "").replace(r"\right.", "")
        clean = clean.replace(r"\left|", "|").replace(r"\right|", "|")
        clean = clean.replace(r"\left(", "(").replace(r"\right)", ")")
        clean = clean.replace(r"\left[", "[").replace(r"\right]", "]")

        if not (clean.startswith("$") and clean.endswith("$")):
            clean = f"${clean}$"

        try:
            fig = plt.figure(figsize=(14, 2), dpi=dpi)
            fig.patch.set_alpha(0.0)
            ax = fig.add_axes([0, 0, 1, 1])
            ax.patch.set_alpha(0.0)
            ax.axis("off")

            ax.text(
                0.0, 0.5,
                clean,
                color=hex_color,
                fontsize=fontsize,
                va="center",
                ha="left",
                usetex=False,
            )

            buf = io.BytesIO()
            plt.savefig(
                buf,
                format="png",
                transparent=True,
                bbox_inches="tight",
                pad_inches=0.03,
                dpi=dpi,
            )
            plt.close(fig)
            buf.seek(0)
            rendered = Image.open(buf)
            # Crop tightly to the actual rendered glyphs to eliminate invisible margins
            bbox = rendered.getbbox()
            if bbox:
                pad = 4
                cropped_box = (
                    max(0, bbox[0] - pad),
                    max(0, bbox[1] - pad),
                    min(rendered.width, bbox[2] + pad),
                    min(rendered.height, bbox[3] + pad)
                )
                cropped = rendered.crop(cropped_box)
                # Auto-scale if wider than max blackboard width (1100px)
                if cropped.width > 1100:
                    scale = 1100.0 / cropped.width
                    new_w = 1100
                    new_h = max(24, int(cropped.height * scale))
                    return cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)
                return cropped
        except Exception as e:
            print(f"[MathRenderer Error] Failed to render '{latex_str}': {e}")
            plt.close("all")
            return None

    @classmethod
    def render_chalk_arrow(
        cls,
        width: int = 80,
        height: int = 40,
        direction: str = "right",
        color_name: str = "yellow",
        dpi: int = 120,
    ) -> Optional[Image.Image]:
        """
        Renders an authentic curved chalk arrow connecting setup terms to derivation terms.
        """
        hex_color = cls.COLOR_MAP.get(color_name.lower(), "#E8D479")
        try:
            fig, ax = plt.subplots(figsize=(width / 50, height / 50), dpi=dpi)
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.0)
            ax.axis("off")

            arrow = patches.FancyArrowPatch(
                (0.1, 0.5), (0.9, 0.5),
                arrowstyle="->,head_width=4,head_length=6",
                connectionstyle="arc3,rad=-0.15",
                color=hex_color,
                linewidth=2.5,
                mutation_scale=15,
            )
            ax.add_patch(arrow)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)

            buf = io.BytesIO()
            plt.savefig(buf, format="png", transparent=True, bbox_inches="tight", pad_inches=0.02, dpi=dpi)
            plt.close(fig)
            buf.seek(0)
            return Image.open(buf)
        except Exception:
            plt.close("all")
            return None

    @classmethod
    def render_strike_slash(
        cls,
        width: int = 60,
        height: int = 45,
        color_name: str = "cyan",
        dpi: int = 120,
    ) -> Optional[Image.Image]:
        """
        Renders a diagonal hand-drawn chalk cancelation slash.
        """
        hex_color = cls.COLOR_MAP.get(color_name.lower(), "#709AD8")
        try:
            fig, ax = plt.subplots(figsize=(width / 50, height / 50), dpi=dpi)
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.0)
            ax.axis("off")

            ax.plot([0.15, 0.85], [0.15, 0.85], color=hex_color, linewidth=2.8, solid_capstyle="round")
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)

            buf = io.BytesIO()
            plt.savefig(buf, format="png", transparent=True, bbox_inches="tight", pad_inches=0.02, dpi=dpi)
            plt.close(fig)
            buf.seek(0)
            return Image.open(buf)
        except Exception:
            plt.close("all")
            return None
