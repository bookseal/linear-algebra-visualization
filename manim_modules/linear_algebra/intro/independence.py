from manim import *
import numpy as np

class IndependenceScene(ThreeDScene):
    """
    3D Scene to visualize Linear Independence concept.
    Shows how an independent vector escapes the 2D plane into 3D space.
    """
    def construct(self):
        # Read Config (Dependent vs Independent)
        try:
            with open("/tmp/independence_config.txt", "r") as f:
                content = f.read().strip()
                mode_val = float(content)
        except:
            mode_val = 1.0  # Default Independent

        is_independent = (mode_val > 0.5)
        
        # Set initial camera orientation
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)

        # Helper for subtitles (fixed to camera)
        def get_subtitle(text):
            t = Text(text, font_size=28).add_background_rectangle()
            self.add_fixed_in_frame_mobjects(t)
            t.to_edge(DOWN)
            return t

        # Step 1: Create 3D Axes
        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[-3, 3, 1],
            x_length=8,
            y_length=8,
            z_length=6
        )
        
        # 2D plane to represent the x-y span (using Polygon for compatibility)
        plane_corners = [
            axes.c2p(-3, -3, 0),
            axes.c2p(3, -3, 0),
            axes.c2p(3, 3, 0),
            axes.c2p(-3, 3, 0)
        ]
        xy_plane = Polygon(
            *plane_corners,
            fill_color=BLUE,
            fill_opacity=0.3,
            stroke_color=BLUE,
            stroke_width=1
        )
        
        title1 = get_subtitle("Step 1: The 2D Plane (x-y)")
        
        self.play(Create(axes), run_time=2.0)
        self.play(FadeIn(xy_plane), run_time=2.0)
        self.wait(1.0)

        # Step 2: Basis Vectors
        self.remove(title1)
        title2 = get_subtitle("Step 2: Existing Basis Vectors")
        
        vec_i = Arrow3D(
            start=axes.c2p(0, 0, 0),
            end=axes.c2p(2, 0, 0),
            color=RED,
            resolution=8
        )
        vec_j = Arrow3D(
            start=axes.c2p(0, 0, 0),
            end=axes.c2p(0, 2, 0),
            color=GREEN,
            resolution=8
        )
        
        label_i = MathTex(r"\hat{i}", color=RED).scale(0.8)
        label_j = MathTex(r"\hat{j}", color=GREEN).scale(0.8)
        self.add_fixed_orientation_mobjects(label_i, label_j)
        label_i.next_to(axes.c2p(2, 0, 0), RIGHT)
        label_j.next_to(axes.c2p(0, 2, 0), UP)
        
        self.play(Create(vec_i), Create(vec_j), Write(label_i), Write(label_j), run_time=2.0)
        self.wait(1.0)

        # Step 3: New Vector
        self.remove(title2)
        
        if is_independent:
            # Independent: Vector escapes into Z direction
            title3 = get_subtitle("Step 3: Independent - New Dimension!")
            
            vec_k = Arrow3D(
                start=axes.c2p(0, 0, 0),
                end=axes.c2p(1, 1, 2),  # Rising into z
                color=YELLOW,
                resolution=8
            )
            label_k = MathTex(r"\vec{w}", color=YELLOW).scale(0.8)
            self.add_fixed_orientation_mobjects(label_k)
            label_k.next_to(axes.c2p(1, 1, 2), UR)
            
            self.play(Create(vec_k), Write(label_k), run_time=2.5)
            
            # Dramatic camera rotation to show 3D
            self.remove(title3)
            title4 = get_subtitle("Step 4: Rotate to See 3D Space!")
            
            self.wait(0.5)
            self.move_camera(phi=30 * DEGREES, theta=45 * DEGREES, run_time=3.0)
            self.wait(0.5)
            self.move_camera(phi=70 * DEGREES, theta=-60 * DEGREES, run_time=3.0)
            
        else:
            # Dependent: Vector stays in xy plane
            title3 = get_subtitle("Step 3: Dependent - Stuck in 2D!")
            
            vec_dep = Arrow3D(
                start=axes.c2p(0, 0, 0),
                end=axes.c2p(2, 2, 0),  # Flat in xy plane
                color=ORANGE,
                resolution=8
            )
            label_dep = MathTex(r"\vec{w}", color=ORANGE).scale(0.8)
            self.add_fixed_orientation_mobjects(label_dep)
            label_dep.next_to(axes.c2p(2, 2, 0), UR)
            
            self.play(Create(vec_dep), Write(label_dep), run_time=2.5)
            
            # Show it's trapped in the plane
            self.remove(title3)
            title4 = get_subtitle("Step 4: No New Dimension")
            
            # Highlight the plane to show the vector is trapped
            self.play(xy_plane.animate.set_fill(ORANGE, opacity=0.4), run_time=2.0)
            
            # Small rotation to confirm
            self.move_camera(phi=75 * DEGREES, theta=-30 * DEGREES, run_time=2.0)

        self.wait(2.0)
