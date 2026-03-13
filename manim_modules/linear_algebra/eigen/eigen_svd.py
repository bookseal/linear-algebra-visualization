# Purpose: Manim scenes for Phase 4 — Eigenvalues & SVD
# Scope: Eigenvector visualization and SVD decomposition steps
# Notes: Config /tmp/p4_config.txt — format: "mode[,params]"

from manim import *
import numpy as np
import glob
import os


class EigenSVDScene(Scene):
    """Renders Phase 4 eigenvector and SVD scenes based on config mode."""

    def construct(self) -> None:
        mode = "eigenvector"
        params: list[str] = []
        try:
            files = glob.glob("/tmp/p4_*_config.txt")
            latest = max(files, key=os.path.getmtime)
            with open(latest) as f:
                parts = f.read().strip().split(",")
                mode = parts[0]
                params = parts[1:]
        except Exception:
            pass

        if mode == "eigenvector":
            self._scene_eigenvector(params)
        elif mode == "svd":
            self._scene_svd(params)

    # ------------------------------------------------------------------
    def _subtitle(self, text: str, color: ManimColor = WHITE, wait: float = 1.5) -> None:
        t = Text(text, font_size=34, color=color).to_edge(DOWN, buff=0.4)
        t.add_background_rectangle(opacity=0.85, color=BLACK, buff=0.15)
        self.add(t)
        self.wait(wait)
        self.remove(t)

    # ------------------------------------------------------------------
    # Scene 1: Eigenvectors
    # ------------------------------------------------------------------
    def _scene_eigenvector(self, params: list[str]) -> None:
        """Shows that eigenvectors only scale, never rotate, under a transformation."""
        # Build ghost + live grid
        ghost = NumberPlane(
            background_line_style={"stroke_color": GREY_C, "stroke_width": 1, "stroke_opacity": 0.3},
            axis_config={"stroke_opacity": 0.3},
        )
        self.add(ghost)

        grid = NumberPlane(
            background_line_style={"stroke_color": GREY_A, "stroke_width": 2, "stroke_opacity": 0.7}
        )
        self.play(Create(grid, run_time=1.5, lag_ratio=0.1))
        self._subtitle("A transformation is about to happen...", wait=1.0)

        # Transformation matrix (has real eigenvectors: shear-scale combo)
        matrix = [[3, 1], [0, 2]]
        mat_tex = MathTex(
            r"A = \begin{bmatrix}3&1\\0&2\end{bmatrix}", color=WHITE
        ).to_corner(UL).add_background_rectangle(opacity=0.8)
        self.play(FadeIn(mat_tex))

        # Several random vectors
        random_vecs = [
            Vector([2, 1, 0], color=BLUE_B, stroke_width=4),
            Vector([1, 2, 0], color=TEAL, stroke_width=4),
            Vector([-1, 1, 0], color=PURPLE_A, stroke_width=4),
        ]
        for v in random_vecs:
            self.add(v)
        self._subtitle("Most vectors rotate AND stretch", wait=1.0)

        # Eigenvectors of A = [[3,1],[0,2]]: eigenvalues 3,2; eigenvecs [1,0],[1,1]
        eig1 = Vector([2, 0, 0], color=GOLD, stroke_width=7)
        eig2 = Vector([1, 1, 0], color=GOLD, stroke_width=7)
        e_label1 = MathTex(r"\vec{e}_1", color=GOLD).next_to(eig1.get_end(), DR, buff=0.1)
        e_label2 = MathTex(r"\vec{e}_2", color=GOLD).next_to(eig2.get_end(), UR, buff=0.1)

        self.play(GrowArrow(eig1), Write(e_label1), GrowArrow(eig2), Write(e_label2))
        self._subtitle("Gold arrows = Eigenvectors (special directions)", color=GOLD, wait=1.5)

        # Apply transformation to everything
        moving = VGroup(grid, *random_vecs, eig1, eig2, label := VGroup(e_label1, e_label2))
        self.play(ApplyMatrix(matrix, moving), run_time=3.0)

        self._subtitle("Random vectors changed direction — eigenvectors only scaled!", color=GOLD, wait=2.5)

        # Show eigenvalue annotations
        ev1 = MathTex(r"\lambda_1 = 3", color=GOLD).next_to(eig1.get_end(), UP)
        ev2 = MathTex(r"\lambda_2 = 2", color=GOLD).next_to(eig2.get_end(), RIGHT)
        self.play(Write(ev1), Write(ev2))
        self._subtitle("Eigenvalue = how much the eigenvector stretched", color=YELLOW, wait=2.0)
        self.wait(1)

    # ------------------------------------------------------------------
    # Scene 2: SVD Decomposition
    # ------------------------------------------------------------------
    def _scene_svd(self, params: list[str]) -> None:
        """Visualizes SVD as three sequential steps: Rotate → Scale → Rotate."""
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
        self.play(Create(grid, run_time=1.5, lag_ratio=0.1))
        self.play(GrowArrow(i_hat), GrowArrow(j_hat))

        self._subtitle("SVD: Any matrix = Rotate → Scale → Rotate", wait=1.5)

        svd_tex = MathTex(r"A = U \Sigma V^T", color=WHITE).to_corner(UR).add_background_rectangle(opacity=0.8)
        self.play(FadeIn(svd_tex))

        moving = VGroup(grid, i_hat, j_hat)

        # Step 1: V^T — first rotation
        theta1 = np.pi / 6
        vt = [[np.cos(theta1), -np.sin(theta1)], [np.sin(theta1), np.cos(theta1)]]
        vt_tex = MathTex(r"V^T \text{ — Rotate input axes}", color=BLUE).to_corner(UL).add_background_rectangle(opacity=0.8)
        self.play(FadeIn(vt_tex))
        self._subtitle("Step 1: V^T — Rotate to singular vector basis", color=BLUE, wait=0.8)
        self.play(ApplyMatrix(vt, moving), run_time=2.5)
        self._subtitle("Input space aligned to singular directions", wait=1.5)
        self.play(FadeOut(vt_tex))

        # Step 2: Σ — scaling along axes
        sigma = [[2.5, 0], [0, 0.8]]
        sig_tex = MathTex(r"\Sigma \text{ — Scale each axis}", color=YELLOW).to_corner(UL).add_background_rectangle(opacity=0.8)
        self.play(FadeIn(sig_tex))
        self._subtitle("Step 2: Σ — Stretch/compress along each axis", color=YELLOW, wait=0.8)
        self.play(ApplyMatrix(sigma, moving), run_time=2.5)
        self._subtitle("Singular values show how much each direction stretches", wait=1.5)
        self.play(FadeOut(sig_tex))

        # Step 3: U — second rotation
        theta2 = np.pi / 4
        u = [[np.cos(theta2), -np.sin(theta2)], [np.sin(theta2), np.cos(theta2)]]
        u_tex = MathTex(r"U \text{ — Rotate output axes}", color=RED).to_corner(UL).add_background_rectangle(opacity=0.8)
        self.play(FadeIn(u_tex))
        self._subtitle("Step 3: U — Rotate to output orientation", color=RED, wait=0.8)
        self.play(ApplyMatrix(u, moving), run_time=2.5)
        self._subtitle("Any matrix = just Rotate → Scale → Rotate!", color=GREEN, wait=2.0)
        self.wait(1)
