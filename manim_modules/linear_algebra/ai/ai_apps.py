# Purpose: Manim scenes for Phase 5 — AI Applications of Linear Algebra
# Scope: PCA, neural network space warping, word embedding arithmetic
# Notes: Config /tmp/p5_config.txt — format: "mode[,params]"

from manim import *
import numpy as np
import glob
import os


class AIAppsScene(Scene):
    """Renders Phase 5 AI application scenes based on config mode."""

    def construct(self) -> None:
        mode = "pca"
        params: list[str] = []
        try:
            files = glob.glob("/tmp/p5_*_config.txt")
            latest = max(files, key=os.path.getmtime)
            with open(latest) as f:
                parts = f.read().strip().split(",")
                mode = parts[0]
                params = parts[1:]
        except Exception:
            pass

        if mode == "pca":
            self._scene_pca()
        elif mode == "neuralnet":
            self._scene_neural_net()
        elif mode == "embedding":
            self._scene_word_embedding()

    # ------------------------------------------------------------------
    def _subtitle(self, text: str, color: ManimColor = WHITE, wait: float = 1.5) -> None:
        t = Text(text, font_size=32, color=color).to_edge(DOWN, buff=0.4)
        t.add_background_rectangle(opacity=0.85, color=BLACK, buff=0.15)
        self.add(t)
        self.wait(wait)
        self.remove(t)

    # ------------------------------------------------------------------
    # Scene 1: PCA
    # ------------------------------------------------------------------
    def _scene_pca(self) -> None:
        """Shows PCA as finding the axis of maximum variance in a data cloud."""
        plane = NumberPlane(background_line_style={"stroke_opacity": 0.3})
        self.add(plane)
        self._subtitle("PCA: Find the axis of maximum variance", wait=1.5)

        # Generate correlated 2D data cloud
        np.random.seed(42)
        n = 40
        raw = np.random.randn(n, 2)
        # Stretch and rotate to create correlation
        cov_transform = np.array([[2.0, 1.2], [0.3, 0.8]])
        data = (cov_transform @ raw.T).T

        dots = VGroup(*[
            Dot(point=[x, y, 0], radius=0.07, color=BLUE_B)
            for x, y in data
        ])
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.05), run_time=2.0)
        self._subtitle("A cloud of data points in 2D", wait=1.0)

        # Compute PCA via SVD
        centered = data - data.mean(axis=0)
        _, _, vt = np.linalg.svd(centered, full_matrices=False)
        pc1 = vt[0]  # First principal component

        # Draw PC1 axis
        pc1_arrow = Arrow(
            start=[-pc1[0] * 3.5, -pc1[1] * 3.5, 0],
            end=[pc1[0] * 3.5, pc1[1] * 3.5, 0],
            color=GOLD, stroke_width=6, buff=0
        )
        pc1_label = MathTex(r"\text{PC}_1", color=GOLD).next_to(pc1_arrow.get_end(), UR)
        self.play(GrowArrow(pc1_arrow), Write(pc1_label))
        self._subtitle("PC1 = direction of greatest spread (eigenvector)", color=GOLD, wait=1.5)

        # Draw PC2 axis (perpendicular)
        pc2 = vt[1]
        pc2_arrow = Arrow(
            start=[-pc2[0] * 2, -pc2[1] * 2, 0],
            end=[pc2[0] * 2, pc2[1] * 2, 0],
            color=TEAL, stroke_width=4, buff=0
        )
        pc2_label = MathTex(r"\text{PC}_2", color=TEAL).next_to(pc2_arrow.get_end(), UL)
        self.play(GrowArrow(pc2_arrow), Write(pc2_label))
        self._subtitle("Dropping PC2 → compress to 1D with minimal info loss", color=TEAL, wait=2.0)

        # Fade PC2 to show dimensionality reduction
        self.play(FadeOut(pc2_arrow), FadeOut(pc2_label))

        # Project all dots onto PC1
        projected_dots = VGroup(*[
            Dot(
                point=[np.dot([x, y], pc1) * pc1[0], np.dot([x, y], pc1) * pc1[1], 0],
                radius=0.07, color=GOLD
            )
            for x, y in centered
        ])
        self.play(Transform(dots, projected_dots), run_time=2.5)
        self._subtitle("Data projected onto PC1 — dimensionality reduced!", color=GOLD, wait=2.0)

    # ------------------------------------------------------------------
    # Scene 2: Neural Net Space Warping
    # ------------------------------------------------------------------
    def _scene_neural_net(self) -> None:
        """Shows how a linear layer + ReLU folds and warps the input space."""
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-4, 4, 1],
            background_line_style={"stroke_color": GREY_A, "stroke_width": 2, "stroke_opacity": 0.7}
        )
        self.add(plane)
        self._subtitle("Neural Network = Space Transformation", wait=1.5)

        # Draw two clusters (not linearly separable)
        np.random.seed(7)
        cluster_a = np.random.randn(12, 2) * 0.5 + np.array([1.5, 1.0])
        cluster_b = np.random.randn(12, 2) * 0.5 + np.array([-1.5, -1.0])

        dots_a = VGroup(*[Dot([x, y, 0], color=RED, radius=0.1) for x, y in cluster_a])
        dots_b = VGroup(*[Dot([x, y, 0], color=BLUE, radius=0.1) for x, y in cluster_b])

        self.play(LaggedStart(*[FadeIn(d) for d in dots_a + dots_b], lag_ratio=0.05), run_time=1.5)
        self._subtitle("Two classes mixed in input space", wait=1.2)

        # Layer 1: linear transform (rotation + scale)
        weight_label = MathTex(r"W_1 = \begin{bmatrix}1.5&0.8\\-0.5&1.2\end{bmatrix}",
                               color=YELLOW).to_corner(UL).add_background_rectangle(opacity=0.8)
        self.play(FadeIn(weight_label))
        self._subtitle("Layer 1: Linear transform W₁ (rotate & stretch)", color=YELLOW, wait=1.0)

        matrix = [[1.5, 0.8], [-0.5, 1.2]]
        moving = VGroup(plane, dots_a, dots_b)
        self.play(ApplyMatrix(matrix, moving), run_time=2.5)
        self._subtitle("Space warped — but still not separable by a line", wait=1.5)
        self.play(FadeOut(weight_label))

        # ReLU: fold negative-y values to 0 (simulate fold)
        relu_label = Text("ReLU: max(0, x) — fold negative half to zero",
                          font_size=28, color=GREEN).to_corner(UL).add_background_rectangle(opacity=0.8)
        self.play(FadeIn(relu_label))
        self._subtitle("ReLU folds the negative half of space", color=GREEN, wait=1.0)

        # Animate: move dots with negative y to y=0
        relu_anims = []
        for dot in dots_a:
            if dot.get_center()[1] < 0:
                relu_anims.append(dot.animate.move_to([dot.get_center()[0], 0, 0]))
        for dot in dots_b:
            if dot.get_center()[1] < 0:
                relu_anims.append(dot.animate.move_to([dot.get_center()[0], 0, 0]))
        if relu_anims:
            self.play(*relu_anims, run_time=2.0)

        self._subtitle("After ReLU: classes begin to separate!", color=GREEN, wait=2.0)
        self.play(FadeOut(relu_label))
        self.wait(1)

    # ------------------------------------------------------------------
    # Scene 3: Word Embeddings
    # ------------------------------------------------------------------
    def _scene_word_embedding(self) -> None:
        """Visualizes word vector arithmetic: King - Man + Woman ≈ Queen."""
        plane = NumberPlane(
            x_range=[-2, 7, 1],
            y_range=[-2, 6, 1],
            background_line_style={"stroke_opacity": 0.3}
        )
        self.add(plane)
        self._subtitle("Word Embeddings: Words as vectors in space", wait=1.5)

        # Simplified 2D word vectors
        words = {
            "Man":   np.array([1.0, 1.0]),
            "Woman": np.array([1.0, 3.5]),
            "King":  np.array([4.5, 1.0]),
            "Queen": np.array([4.5, 3.5]),
        }
        colors = {"Man": BLUE, "Woman": RED, "King": GOLD, "Queen": GREEN}

        dots = {}
        labels_mob = {}
        for word, pos in words.items():
            d = Dot([pos[0], pos[1], 0], radius=0.12, color=colors[word])
            lbl = Text(word, font_size=28, color=colors[word]).next_to(d, UR, buff=0.1)
            dots[word] = d
            labels_mob[word] = lbl
            self.play(FadeIn(d), Write(lbl), run_time=0.5)

        self._subtitle("Each word = a point in high-dimensional space (shown in 2D)", wait=1.5)

        # Show gender vector: Woman - Man
        gender_vec = words["Woman"] - words["Man"]
        gender_arrow = Arrow(
            start=[*words["Man"], 0],
            end=[*words["Woman"], 0],
            color=PURPLE_A, stroke_width=5, buff=0
        )
        gender_label = Text("gender", font_size=24, color=PURPLE_A).next_to(gender_arrow, LEFT, buff=0.1)
        self.play(GrowArrow(gender_arrow), Write(gender_label))
        self._subtitle("Woman - Man = 'gender' direction vector", color=PURPLE_A, wait=1.5)

        # Show same vector applied to King → Queen
        royal_arrow = Arrow(
            start=[*words["King"], 0],
            end=[*words["Queen"], 0],
            color=PURPLE_A, stroke_width=5, buff=0
        )
        self.play(GrowArrow(royal_arrow))
        self._subtitle("King + gender vector = Queen!", color=GREEN, wait=1.5)

        # Highlight the equation
        eq = MathTex(
            r"\text{King} - \text{Man} + \text{Woman} \approx \text{Queen}",
            color=YELLOW
        ).to_edge(UP).add_background_rectangle(opacity=0.85)
        self.play(Write(eq))
        self._subtitle("Vector arithmetic works in semantic space", color=YELLOW, wait=2.0)
        self.wait(1)
