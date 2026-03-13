from manim import *

class VectorBasisScene(Scene):
    def construct(self):
        # 1. Setup Plane
        plane = NumberPlane()
        plane.add_coordinates()
        self.add(plane)
        
        # 2. Define Basis Vectors (i_hat, j_hat)
        i_hat = Vector([1, 0], color=GREEN)
        j_hat = Vector([0, 1], color=RED)
        
        i_label = MathTex("\\hat{i}").next_to(i_hat.get_end(), DOWN)
        j_label = MathTex("\\hat{j}").next_to(j_hat.get_end(), LEFT)
        
        # 3. Read target vector from config or default to (3, 2)
        target_x, target_y = 3, 2
        try:
            with open("/tmp/basis_config.txt", "r") as f:
                content = f.read().strip()
                target_x, target_y = map(float, content.split(','))
        except:
            pass
            
        target_vec = Vector([target_x, target_y], color=YELLOW)
        vec_label = MathTex(f"\\vec{{v}} = {target_x}\\hat{{i}} + {target_y}\\hat{{j}}").next_to(target_vec.get_end(), RIGHT)
        vec_label.add_background_rectangle()

        # Animation Sequence
        
        # Show Basis Vectors first
        # Subtitle: "Step 1: Standard Basis Vectors"
        title1 = Text("Step 1: Standard Basis Vectors", font_size=32).to_edge(DOWN)
        self.add(title1)
        self.play(GrowArrow(i_hat), Write(i_label), run_time=1.5)
        self.play(GrowArrow(j_hat), Write(j_label), run_time=1.5)
        self.wait(1)
        
        # Show scaling of basis vectors
        # Subtitle: "Step 2: Scale them by coordinates"
        title2 = Text("Step 2: Scale by Coordinates", font_size=32).to_edge(DOWN)
        self.play(Transform(title1, title2))
        
        scaled_i = Vector([target_x, 0], color=GREEN_A)
        # Start scaled_j from origin first for clarity, then shift? 
        # Or standard vector addition visualization: tail-to-head method.
        # Let's show scaling in place first.
        
        self.play(TransformFromCopy(i_hat, scaled_i), run_time=2.0)
        
        # For j, let's show it scaling on the y-axis first, then moving?
        # Or just show it at the tip of x.
        # Manim's Vector addition is usually shown by placing vectors tip-to-tail.
        scaled_j_origin = Vector([0, target_y], color=RED_A)
        self.play(TransformFromCopy(j_hat, scaled_j_origin), run_time=2.0)
        self.wait(0.5)
        
        # Subtitle: "Step 3: Add them tip-to-tail"
        title3 = Text("Step 3: Vector Addition (Tip-to-Tail)", font_size=32).to_edge(DOWN)
        self.play(Transform(title1, title3))
        
        # Move scaled J to tip of scaled I
        scaled_j = Vector([0, target_y], color=RED_A).shift(RIGHT * target_x) 
        self.play(Transform(scaled_j_origin, scaled_j), run_time=2.0)
        
        # Show resultant vector
        # Subtitle: "Step 4: Resultant Vector"
        title4 = Text("Step 4: Resultant Vector", font_size=32).to_edge(DOWN)
        self.play(Transform(title1, title4))
        self.play(GrowArrow(target_vec), Write(vec_label), run_time=2.0)
        self.wait(3)
