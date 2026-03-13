from manim import *
import numpy as np
import sys

class LinearTransformationScene(Scene):
    def construct(self):
        # Default matrix (identity)
        matrix = [[1, 0], [0, 1]]
        
        # Parse arguments from command line if provided
        # We expect arguments like: -a 2.0,0.0,0.0,2.0 (comma separated flat list)
        # Usage: manim -qm transformations.py LinearTransformationScene --arg="2,0,0,2"
        # However, passing args to manim scripts can be tricky. 
        # Easier way: Use environment variable or config. 
        # But we can also parse argv if we are careful.
        
        # Let's read from a local file or env var for simplicity and reliability in automation.
        # Or simpler: The user generates a python file with the specific variables, then runs it.
        # OR: We just hardcode params in a template and overwrite the file. 
        # OR: We use Manim's config dictionary if accessible?
        
        # Let's try reading from a temp config file "matrix_config.txt" in the current directory
        try:
            with open("/tmp/matrix_config.txt", "r") as f:
                content = f.read().strip()
                # content format expected: "a,b,c,d" for [[a,b],[c,d]]

                parts = [float(x) for x in content.split(',')]
                matrix = [[parts[0], parts[1]], [parts[2], parts[3]]]
        except FileNotFoundError:
            pass # Use default

        # Display Setup
        # Add coordinates to the plane for better visibility
        plane = NumberPlane()
        plane.add_coordinates()
        
        matrix_tex = Matrix(matrix).add_background_to_entries()
        # Move it slightly away from the exact corner to avoid cropping
        matrix_tex.to_corner(UL, buff=0.5)
        
        text = Text("Linear Transformation", font_size=24)
        text.next_to(matrix_tex, RIGHT)
        
        # Add background rectangle to text for better contrast if needed, 
        # but default black background should be fine.

        self.add(plane, matrix_tex, text)
        self.wait(1)

        # Animation
        # Use ApplyMatrix for standard linear transformations (keeps lines straight)
        self.play(
            ApplyMatrix(matrix, plane),
            run_time=3
        )
        self.wait(1)
