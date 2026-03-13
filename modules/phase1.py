import streamlit as st
import subprocess
import os
import time

def render():
    st.title("Phase 1: Vectors and Space")
    st.markdown("The birth of space — visualizing the fundamentals of vectors.")

    # Define Tabs
    tab1, tab2, tab3 = st.tabs(["Step 1: Basis Vectors", "Step 2: Linear Combo & Span", "Step 3: Linear Independence"])

    # Common Helper for Phase 1 Rendering
    def run_manim_p1(scene_file, scene_name, config_path, config_content, output_path):
        with open(config_path, "w") as f:
            f.write(config_content)

        cmd = [
            "manim", "-ql", "--media_dir", "/tmp/media",
            scene_file, scene_name
        ]

        with st.status("🎬 Rendering... (~15 sec)", expanded=True) as status:
            try:
                subprocess.run(cmd, check=True, capture_output=True, text=True)
                if os.path.exists(output_path):
                    status.update(label="✅ Done!", state="complete", expanded=False)
                    return True
                else:
                    status.update(label="❌ Video not found", state="error")
                    return False
            except subprocess.CalledProcessError as e:
                status.update(label="❌ Render error", state="error")
                st.code(e.stderr)
                return False

    # ==========================================
    # Tab 1: Basis Vectors
    # ==========================================
    with tab1:
        st.header("Step 1: Atoms of Space — Basis Vectors")
        st.markdown(r"""
        Every point in 2D space is a combination of two **standard basis vectors** ($\hat{i}$, $\hat{j}$).
        """)

        c1, c2 = st.columns(2)
        vx = c1.number_input("x component", value=3.0, step=0.5, key="p1_s1_x")
        vy = c2.number_input("y component", value=2.0, step=0.5, key="p1_s1_y")

        if st.button("🚀 Run (Basis Viz)", key="btn_p1_s1", type="primary"):
            success = run_manim_p1(
                "manim_modules/linear_algebra/intro/basis.py", "VectorBasisScene",
                "/tmp/basis_config.txt", f"{vx},{vy}",
                "/tmp/media/videos/basis/480p15/VectorBasisScene.mp4"
            )
            if success:
                st.markdown("#### 📺 Result")
                st.video(open("/tmp/media/videos/basis/480p15/VectorBasisScene.mp4", 'rb').read(), autoplay=True)

    # ==========================================
    # Tab 2: Span
    # ==========================================
    with tab2:
        st.header("Step 2: Linear Combination & Span")
        st.markdown(r"""
        The set of all points reachable by combining two vectors is called their **Span**.
        """)

        sc_a = st.slider("Scalar a", -3.0, 3.0, 1.5, 0.5, key="p1_s2_a")
        sc_b = st.slider("Scalar b", -3.0, 3.0, 1.0, 0.5, key="p1_s2_b")
        is_parallel = st.checkbox("Force parallel vectors (1D Line Span)", key="p1_s2_chk")

        if st.button("🚀 Run (Span Viz)", key="btn_p1_s2", type="primary"):
            c_val = 1.0 if is_parallel else 0.0
            success = run_manim_p1(
                "manim_modules/linear_algebra/intro/span.py", "LinearCombinationScene",
                "/tmp/span_config.txt", f"{sc_a},{sc_b},{c_val}",
                "/tmp/media/videos/span/480p15/LinearCombinationScene.mp4"
            )
            if success:
                st.markdown("#### 📺 Result")
                st.video(open("/tmp/media/videos/span/480p15/LinearCombinationScene.mp4", 'rb').read(), autoplay=True)

    # ==========================================
    # Tab 3: Linear Independence
    # ==========================================
    with tab3:
        st.header("Step 3: Linear Independence vs Dependence")
        st.markdown("""
        A new vector is **independent** if it escapes to a new dimension. Otherwise it's **dependent**.
        """)

        mode = st.radio("Select state", ["Dependent (trapped in 2D)", "Independent (escapes to 3D!)"], key="p1_s3_rad")

        if st.button("🚀 Run (3D Viz)", key="btn_p1_s3", type="primary"):
            val = 1.0 if "Independent" in mode else 0.0
            success = run_manim_p1(
                "manim_modules/linear_algebra/intro/independence.py", "IndependenceScene",
                "/tmp/independence_config.txt", str(val),
                "/tmp/media/videos/independence/480p15/IndependenceScene.mp4"
            )
            if success:
                st.markdown("#### 📺 Result")
                st.video(open("/tmp/media/videos/independence/480p15/IndependenceScene.mp4", 'rb').read(), autoplay=True)
