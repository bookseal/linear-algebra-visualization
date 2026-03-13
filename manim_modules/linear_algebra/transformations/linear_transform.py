from manim import *
import numpy as np
import glob
import os

class LinearTransformationScene(Scene):
    def construct(self):
        # 0. Read Config with Mode
        try:
            # Find latest config file
            files = glob.glob("/tmp/p2_s*_config.txt")
            if not files:
                 raise Exception("No config found")
            latest_file = max(files, key=os.path.getmtime)
            
            with open(latest_file, "r") as f:
                content = f.read().strip()
                parts = content.split(",")
                a, b, c, d = map(float, parts[:4])
                mode = parts[4] if len(parts) > 4 else "default"
                
        except Exception as e:
            # Default fallback
            a, b, c, d = 2.0, 0.0, 0.0, 1.0 # Scaling example
            mode = "default"
            print(f"Config Error: {e}")

        matrix = [[a, b], [c, d]]
        
        # Helper: Highlighted Subtitle
        subtitle_group = VGroup()
        self.add(subtitle_group)
        
        def set_subtitle(text, color=WHITE, wait_time=1.0):
            # Clear previous subtitles properly
            for sub in subtitle_group:
                self.remove(sub)
            subtitle_group.submobjects = []
            
            # Create new subtitle with better visibility
            t = Text(text, font_size=36, color=color).to_edge(DOWN, buff=0.5).add_background_rectangle(opacity=0.9, color=BLACK, buff=0.2)
            subtitle_group.add(t)
            self.add(t)
            self.wait(wait_time)

        # ==========================================
        # 1. The "Before" World (Original Grid)
        # ==========================================
        
        # Create a "Ghost" grid that will stay behind to show the "Before" state
        ghost_grid = NumberPlane(
            x_range=[-8, 8, 1],
            y_range=[-5, 5, 1],
            background_line_style={"stroke_color": GREY_C, "stroke_width": 1, "stroke_opacity": 0.3},
            axis_config={"stroke_opacity": 0.3} # Dim axes too
        )
        self.add(ghost_grid)
        
        # Main Grid to be transformed
        grid = NumberPlane(
            x_range=[-8, 8, 1],
            y_range=[-5, 5, 1],
            background_line_style={"stroke_color": GREY_A, "stroke_width": 2, "stroke_opacity": 0.8}
        )
        
        # Basis Vectors
        i_hat = Vector([1, 0, 0], color=RED, stroke_width=6)
        j_hat = Vector([0, 1, 0], color=GREEN, stroke_width=6)
        
        label_i = MathTex(r"\hat{i}", color=RED).next_to(i_hat.get_end(), DOWN+RIGHT, buff=0.1)
        label_j = MathTex(r"\hat{j}", color=GREEN).next_to(j_hat.get_end(), UP+LEFT, buff=0.1)

        # Intro
        set_subtitle("Phase 2: Matrix Transformation", wait_time=0.5)
        
        if "linearity" not in mode:
            self.play(Create(grid, run_time=2.0, lag_ratio=0.1))
            self.play(GrowArrow(i_hat), Write(label_i), GrowArrow(j_hat), Write(label_j))
            set_subtitle("Original Space (Before)", wait_time=1.5)
        else:
            self.add(grid, i_hat, j_hat, label_i, label_j)

        # ==========================================
        # 2. Transformation
        # ==========================================
        
        # Group objects to transform together
        moving_parts = VGroup(grid, i_hat, j_hat, label_i, label_j)
        
        if mode == "scaling":
            set_subtitle(f"Step 1: Scaling (x*{a}, y*{d})", color=YELLOW, wait_time=1)
            
            # Dramatic Pause
            self.play(Indicate(i_hat, color=RED), Indicate(j_hat, color=GREEN))
            
            set_subtitle("Watch the vectors stretch...", wait_time=0.5)
            self.play(
                ApplyMatrix(matrix, moving_parts),
                run_time=3.0 # Slow
            )
            set_subtitle("Compare: Ghost Grid (Before) vs New Grid (After)", wait_time=2)
            
        elif mode == "rotation":
            set_subtitle("Step 2: Rotation (Spinning Space)", color=YELLOW, wait_time=1)
            
            # Show rotation arc hint
            arc = Arc(radius=1.5, angle=np.arctan2(c, a), color=YELLOW, start_angle=0)
            self.play(Create(arc))
            
            self.play(
                ApplyMatrix(matrix, moving_parts),
                Rotate(arc, 0), # just to update it if needed, or fade it out
                run_time=3.5
            )
            self.play(FadeOut(arc))
            set_subtitle("The Origin (0,0) stays fixed!", wait_time=2)
            
        elif mode == "shear":
            set_subtitle("Step 3: Shear (Sliding Layers)", color=YELLOW, wait_time=1)
            
            # Height marker before
            h_line = DashedLine([-4, 1, 0], [4, 1, 0], color=BLUE_B)
            h_text = Text("Height level", font_size=20, color=BLUE_B).next_to(h_line, UP)
            self.play(Create(h_line), FadeIn(h_text))
            
            set_subtitle("x-axis is stuck, y-axis slides...", wait_time=1)
            
            self.play(
                ApplyMatrix(matrix, moving_parts),
                run_time=4.0 # Very Slow for Shear
            )
            
            set_subtitle("Notice: All points on the yellow line stayed at height=1", wait_time=2)
            self.play(Indicate(h_line))
            
        elif mode.startswith("linearity"):
            submode = mode.split("_")[1]
            if "valid" in submode:
                set_subtitle("Linear check: Lines remain straight & parallel", wait_time=1)
                self.play(ApplyMatrix([[1, 0.5], [0, 1]], moving_parts), run_time=3)
                
            elif "shift" in submode:
                set_subtitle("Checking Linearity... (Origin Shift)", color=RED, wait_time=1)
                self.play(moving_parts.animate.shift(RIGHT*2 + UP*1), run_time=2.5)

                # Show ghost origin vs new origin
                origin_dot = Dot(ORIGIN, color=GREY)
                new_dot = Dot([2,1,0], color=RED)
                self.add(origin_dot, new_dot)
                self.play(TransformFromCopy(origin_dot, new_dot))
                set_subtitle("FAIL: Origin moved! (Not Linear)", color=RED, wait_time=2)

            elif "curve" in submode:
                set_subtitle("Checking Linearity... (Curving)", color=RED, wait_time=1)
                def nonlinear_func(point):
                    x, y, z = point
                    return [x, y + 0.5 * np.sin(x*1.5), z]
                self.play(moving_parts.animate.apply_function(nonlinear_func), run_time=4.0)
                set_subtitle("FAIL: Lines are curved! (Not Linear)", color=RED, wait_time=2)

        elif mode.startswith("inverse"):
            set_subtitle("Transforming...", wait_time=0.5)
            self.play(ApplyMatrix(matrix, moving_parts), run_time=2.0)
            
            if "ok" in mode:
                set_subtitle("Now, let's Rewind (Inverse Matrix)", color=BLUE, wait_time=1.0)
                inv_matrix = np.linalg.inv(matrix)
                
                # Highlight recovery
                self.play(
                    ApplyMatrix(inv_matrix, moving_parts), # Apply inverse to the ALREADY transformed group
                    run_time=3.0
                )
                set_subtitle("Back to the Ghost Grid! (Perfect Match)", color=GREEN, wait_time=2)
                
            else:
                set_subtitle("Collapsed to 1D Line...", wait_time=1.0)
                self.play(Indicate(moving_parts, color=RED))
                set_subtitle("Impossible to recover original 2D positions! ❌", color=RED, wait_time=2)

        self.wait(1)
