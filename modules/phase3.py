# Purpose: Streamlit UI for Phase 3 — Geometric Operations
# Scope: Matrix composition and dot product visualization
# Notes: Renders via GeoOpsScene in manim_modules/linear_algebra/operations/geo_ops.py

import streamlit as st
import subprocess
import os


def render() -> None:
    """Renders the Phase 3 interactive page."""
    st.title("Phase 3: Geometric Operations")
    st.markdown("How transformations **compose**, and what the dot product really means.")

    tabs = st.tabs(["1. Matrix Multiplication", "2. Dot Product & Projection"])

    def run_viz(step_num: int, config_str: str) -> str | None:
        """Writes config and runs Manim scene, returns video path or None."""
        with open(f"/tmp/p3_s{step_num}_config.txt", "w") as f:
            f.write(config_str)

        cmd = [
            "manim", "-ql", "--media_dir", "/tmp/media",
            "manim_modules/linear_algebra/operations/geo_ops.py",
            "GeoOpsScene"
        ]

        with st.status("🎬 Rendering... (~15 sec)", expanded=True) as status:
            try:
                subprocess.run(cmd, check=True, capture_output=True, text=True)
                video_path = "/tmp/media/videos/geo_ops/480p15/GeoOpsScene.mp4"
                if os.path.exists(video_path):
                    status.update(label="✅ Done!", state="complete", expanded=False)
                    return video_path
                status.update(label="❌ Video not found", state="error")
                return None
            except subprocess.CalledProcessError as e:
                status.update(label="❌ Render error", state="error")
                st.code(e.stderr)
                return None

    # ------------------------------------------------------------------
    # Tab 1: Matrix Multiplication
    # ------------------------------------------------------------------
    with tabs[0]:
        st.header("Matrix Multiplication = Composition")
        st.info("AB means: apply B first, then apply A to the result.")
        st.markdown(r"""
        - **B** = Shear $\begin{bmatrix}1&1\\0&1\end{bmatrix}$ → slide the grid sideways
        - **A** = Rotation 45° → then spin it
        - Watch how the order of operations shapes the final space.
        """)

        if st.button("🚀 Run (Compose)", key="btn_p3_s1", type="primary"):
            vid = run_viz(1, "compose")
            if vid:
                st.video(open(vid, "rb").read(), autoplay=True)

    # ------------------------------------------------------------------
    # Tab 2: Dot Product
    # ------------------------------------------------------------------
    with tabs[1]:
        st.header("Dot Product & Projection")
        st.info("The dot product measures how much two vectors point in the same direction.")

        c1, c2 = st.columns(2)
        ax = c1.number_input("a · x", value=3.0, step=0.5, key="p3_ax")
        ay = c2.number_input("a · y", value=1.0, step=0.5, key="p3_ay")
        bx = c1.number_input("b · x", value=2.0, step=0.5, key="p3_bx")
        by = c2.number_input("b · y", value=2.5, step=0.5, key="p3_by")

        dot = ax * bx + ay * by
        st.metric("Dot product  a·b", f"{dot:.2f}")

        if st.button("🚀 Run (Dot Product)", key="btn_p3_s2", type="primary"):
            vid = run_viz(2, f"dotproduct,{ax},{ay},{bx},{by}")
            if vid:
                st.video(open(vid, "rb").read(), autoplay=True)
