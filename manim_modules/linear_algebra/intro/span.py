from manim import *
import numpy as np

class LinearCombinationScene(Scene):
    def construct(self):
        # 1. Setup Plane
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-4, 4, 1],
            background_line_style={"stroke_opacity": 0.4}
        )
        self.add(plane)

        # 2. Read Config (a, b scalar values)
        try:
            with open("/tmp/span_config.txt", "r") as f:
                content = f.read().strip()
                a_val, b_val, is_parallel = map(float, content.split(","))
        except:
            a_val, b_val, is_parallel = 2.0, 1.0, 0.0

        # Define Basis Vectors
        i_vec = np.array([1, 0, 0])
        
        # Determine j_vec (Parallel or Independent)
        if is_parallel > 0.5: # Python bool from float
            j_vec = np.array([2, 0, 0]) # Parallel to i (Linear Dependent)
            j_color = ORANGE
            subtitle_text = "Linear Dependent: Span is a LINE"
        else:
            j_vec = np.array([0, 1, 0]) # Standard basis
            j_color = GREEN
            subtitle_text = "Linear Independent: Span is a PLANE"

        # Subtitle Helper
        def update_subtitle(text):
            new_title = Text(text, font_size=32).to_edge(DOWN).add_background_rectangle()
            return new_title

        # Step 1: Show Basis Vectors
        title1 = update_subtitle("Step 1: Standard Basis Vectors")
        self.add(title1)
        
        arrow_i = Vector(i_vec, color=RED)
        label_i = MathTex(r"\hat{i}", color=RED).next_to(arrow_i.get_end(), DOWN+RIGHT, buff=0.1)

        arrow_j = Vector(j_vec, color=j_color)
        label_j = MathTex(r"\hat{j}", color=j_color).next_to(arrow_j.get_end(), UP+LEFT, buff=0.1)

        self.play(GrowArrow(arrow_i), Write(label_i), GrowArrow(arrow_j), Write(label_j), run_time=2.0)
        self.wait(1.0)

        # Step 2: Scale Vectors (Linear Combination Components)
        title2 = update_subtitle(f"Step 2: Scale by scalars (a={a_val:.1f}, b={b_val:.1f})")
        
        # Scale i by a
        scaled_i = Vector(i_vec * a_val, color=RED_A)
        label_scaled_i = MathTex(f"{a_val:.1f}\\hat{{i}}", color=RED_A).next_to(scaled_i.get_end(), DOWN, buff=0.1)
        
        self.play(
            ReplacementTransform(title1, title2),
            Transform(arrow_i, scaled_i), 
            FadeIn(label_scaled_i), 
            run_time=2.5
        )
        
        # Scale j by b
        scaled_j = Vector(j_vec * b_val, color=GREEN_A)
        
        # Tip-to-Tail Animation: Move scaled j to tip of scaled i
        title3 = update_subtitle("Step 3: Tip-to-Tail Addition")
        
        scaled_j_shifted = Vector(j_vec * b_val, color=GREEN_A).shift(i_vec * a_val)
        label_scaled_j = MathTex(f"{b_val:.1f}\\hat{{j}}", color=GREEN_A).next_to(scaled_j_shifted.get_end(), UP, buff=0.1)

        self.play(
            ReplacementTransform(title2, title3),
            Transform(arrow_j, scaled_j_shifted),
            FadeIn(label_scaled_j),
            run_time=2.5
        )
        self.wait(0.5)

        # Step 4: Resultant Vector
        title4 = update_subtitle("Step 4: Resultant Vector (Linear Combination)")
        
        final_vec = (i_vec * a_val) + (j_vec * b_val)
        result_arrow = Vector(final_vec, color=YELLOW, stroke_width=6)
        label_result = MathTex(r"\vec{v}", color=YELLOW).next_to(result_arrow.get_end(), UR, buff=0.1)

        self.play(
            ReplacementTransform(title3, title4),
            GrowArrow(result_arrow), 
            Write(label_result),
            run_time=2.0
        )
        self.wait(1.0)
        
        # Step 5: Show Span (Dynamic Grid Visualization)
        if is_parallel > 0.5:
             span_text = "Step 5: Span is a LINE (Grid Collapses)"
             grid_color = ORANGE
             is_line = True
        else:
             span_text = "Step 5: Span is the Entire PLANE (Grid Expands)"
             grid_color = BLUE_D
             is_line = False

        title5 = update_subtitle(span_text)
        self.play(ReplacementTransform(title4, title5))

        # Clean up previous specific scaling vectors to focus on the span
        self.play(
            FadeOut(scaled_i), FadeOut(label_scaled_i),
            FadeOut(scaled_j_shifted), FadeOut(label_scaled_j),
            FadeOut(result_arrow), FadeOut(label_result),
            run_time=1.0
        )

        # Create the Span Grid
        # We draw logic lines parallel to i_vec and j_vec
        grid_group = VGroup()
        
        # Grid range
        r_min, r_max = -6, 6
        
        # 1. Lines based on i_vec (sweeping along j)
        for s in range(r_min, r_max + 1):
            if s == 0: continue # Skip origin line to avoid clutter
            
            # Start and end points for the line
            start = (i_vec * r_min) + (j_vec * s)
            end   = (i_vec * r_max) + (j_vec * s)
            
            line = Line(start, end, color=grid_color).set_stroke(opacity=0.5, width=2)
            grid_group.add(line)

        # 2. Lines based on j_vec (sweeping along i)
        for s in range(r_min, r_max + 1):
            if s == 0: continue
            
            start = (j_vec * r_min) + (i_vec * s)
            end   = (j_vec * r_max) + (i_vec * s)
            
            line = Line(start, end, color=grid_color).set_stroke(opacity=0.5, width=2)
            grid_group.add(line)

        # Animation: "Grow" the grid from the center
        self.play(Create(grid_group, lag_ratio=0.1), run_time=3.0)
        
        # Final Highlight
        if is_line:
            # Highlight the single line intensely
            span_line = Line(start=i_vec * -10, end=i_vec * 10, color=YELLOW, stroke_width=8)
            label_span = Text("Span: 1D Line", color=YELLOW, font_size=24).next_to(ORIGIN, UP*2)
            self.play(Create(span_line), Write(label_span))
        else:
            # Highlight the whole plane
            rect = Rectangle(width=16, height=10, color=BLUE, fill_opacity=0.2, stroke_width=0)
            label_span = Text("Span: 2D Plane", color=BLUE, font_size=36).to_edge(UP)
            self.play(FadeIn(rect), Write(label_span))
            
        self.wait(2)
