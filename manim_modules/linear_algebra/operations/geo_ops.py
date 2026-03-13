# Purpose: Manim scenes for Phase 3 — Geometric Operations
# Scope: Matrix multiplication (composition), dot product & projection
# Notes: Config file /tmp/p3_config.txt — format: "mode[,extra_params]"

from manim import *
import numpy as np
import glob
import os


class GeoOpsScene(Scene):
    """Renders Phase 3 geometric operation scenes based on config mode."""

    def construct(self) -> None:
        # Read config file
        mode = "compose"
        params: list[str] = []
        try:
            files = glob.glob("/tmp/p3_*_config.txt")
            latest = max(files, key=os.path.getmtime)
            with open(latest) as f:
                parts = f.read().strip().split(",")
                mode = parts[0]
                params = parts[1:]
        except Exception:
            pass

        if mode == "compose":
            self._scene_compose(params)
        elif mode == "dotproduct":
            self._scene_dot_product(params)

    # ------------------------------------------------------------------
    # Helper
    # ------------------------------------------------------------------
    def _subtitle(self, text: str, color: ManimColor = WHITE, wait: float = 1.5) -> None:
        """Displays a subtitle at the bottom of the scene."""
        t = Text(text, font_size=34, color=color).to_edge(DOWN, buff=0.4)
        t.add_background_rectangle(opacity=0.85, color=BLACK, buff=0.15)
        self.add(t)
        self.wait(wait)
        self.remove(t)

    # ------------------------------------------------------------------
    # Scene 1: Matrix Multiplication = Composition
    # ------------------------------------------------------------------
    def _scene_compose(self, params: list[str]) -> None:
        """Shows AB as applying B first, then A on top of the result."""
        ghost = NumberPlane(
            background_line_style={"stroke_color": GREY_C, "stroke_width": 1, "stroke_opacity": 0.3},
            axis_config={"stroke_opacity": 0.3},
        )
        self.add(ghost)

        grid = NumberPlane(
            background_line_style={"stroke_color": GREY_A, "stroke_width": 2, "stroke_opacity": 0.8}
        )
        i_hat = Vector([1, 0, 0], color=RED, stroke_width=6)
        j_hat = Vector([0, 1, 0], color=GREEN, stroke_width=6)
        label_i = MathTex(r"\hat{i}", color=RED).next_to(i_hat.get_end(), DR, buff=0.1)
        label_j = MathTex(r"\hat{j}", color=GREEN).next_to(j_hat.get_end(), UL, buff=0.1)

        self.play(Create(grid, run_time=1.5, lag_ratio=0.1))
        self.play(GrowArrow(i_hat), Write(label_i), GrowArrow(j_hat), Write(label_j))
        self._subtitle("Matrix Multiplication = Composition of Transforms", wait=1.5)

        moving = VGroup(grid, i_hat, j_hat, label_i, label_j)

        # Matrix B — shear
        mat_b = [[1, 1], [0, 1]]
        b_tex = MathTex(r"B = \begin{bmatrix}1&1\\0&1\end{bmatrix}", color=YELLOW).to_corner(UL)
        self.play(FadeIn(b_tex))
        self._subtitle("Step 1: Apply B (Shear)", color=YELLOW, wait=1.0)
        self.play(ApplyMatrix(mat_b, moving), run_time=2.5)
        self._subtitle("Space after B — parallelogram grid", wait=1.5)

        # Matrix A — rotation 45°
        theta = np.pi / 4
        mat_a = [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]]
        a_tex = MathTex(r"A = \begin{bmatrix}\cos45°&-\sin45°\\\sin45°&\cos45°\end{bmatrix}", color=BLUE).to_corner(UR)
        self.play(FadeIn(a_tex))
        self._subtitle("Step 2: Apply A (Rotation 45°)", color=BLUE, wait=1.0)
        self.play(ApplyMatrix(mat_a, moving), run_time=2.5)
        self._subtitle("AB ≠ BA  —  Order matters!", color=RED, wait=2.0)

    # ------------------------------------------------------------------
    # Scene 2: Dot Product & Projection
    # ------------------------------------------------------------------
    def _scene_dot_product(self, params: list[str]) -> None:
        """Visualizes dot product as projection (shadow) of one vector onto another."""
        plane = NumberPlane(background_line_style={"stroke_opacity": 0.3})
        self.add(plane)
        self._subtitle("Dot Product = Shadow (Projection)", wait=1.5)

        # Two vectors from config or defaults
        ax = float(params[0]) if len(params) > 0 else 3.0
        ay = float(params[1]) if len(params) > 1 else 1.0
        bx = float(params[2]) if len(params) > 2 else 2.0
        by = float(params[3]) if len(params) > 3 else 2.5

        vec_a = np.array([ax, ay, 0])
        vec_b = np.array([bx, by, 0])

        arrow_a = Vector(vec_a, color=RED, stroke_width=6)
        arrow_b = Vector(vec_b, color=GREEN, stroke_width=6)
        label_a = MathTex(r"\vec{a}", color=RED).next_to(arrow_a.get_end(), RIGHT)
        label_b = MathTex(r"\vec{b}", color=GREEN).next_to(arrow_b.get_end(), UP)

        self.play(GrowArrow(arrow_a), Write(label_a), GrowArrow(arrow_b), Write(label_b))
        self._subtitle("Two vectors in 2D space", wait=1.5)

        # Projection of b onto a
        unit_a = vec_a / np.linalg.norm(vec_a)
        proj_len = np.dot(vec_b, unit_a)
        proj_vec = proj_len * unit_a

        # Dashed perpendicular drop
        drop_start = np.array([bx, by, 0])
        drop_end = proj_vec
        drop_line = DashedLine(drop_start, drop_end, color=YELLOW)
        proj_arrow = Vector(proj_vec, color=YELLOW, stroke_width=6)
        proj_label = MathTex(r"\text{proj}_{\vec{a}}\vec{b}", color=YELLOW).next_to(proj_arrow.get_end(), DR)

        dot_val = np.dot(vec_a[:2], vec_b[:2])
        dot_tex = MathTex(
            rf"\vec{{a}} \cdot \vec{{b}} = {dot_val:.1f}",
            color=WHITE
        ).to_corner(UR).add_background_rectangle(opacity=0.8)

        self.play(Create(drop_line), GrowArrow(proj_arrow), Write(proj_label))
        self.play(FadeIn(dot_tex))
        self._subtitle(f"Dot product = {dot_val:.1f}  (larger → more aligned)", color=YELLOW, wait=2.0)
        self.wait(1)
