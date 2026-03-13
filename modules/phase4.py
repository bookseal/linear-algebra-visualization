# Purpose: Streamlit UI for Phase 4 — Eigenvalues & SVD
# Scope: Interactive eigenvector and SVD decomposition visualizations
# Notes: Renders via EigenSVDScene in manim_modules/linear_algebra/eigen/eigen_svd.py

import streamlit as st
import subprocess
import os


def render() -> None:
    """Renders the Phase 4 interactive page."""
    st.title("Phase 4: Eigenvalues & SVD")
    st.markdown("The **skeleton** of a matrix — directions that survive any transformation.")

    tabs = st.tabs(["1. Eigenvectors & Eigenvalues", "2. SVD Decomposition"])

    def run_viz(step_num: int, config_str: str) -> str | None:
        """Writes config and runs Manim scene, returns video path or None."""
        with open(f"/tmp/p4_s{step_num}_config.txt", "w") as f:
            f.write(config_str)

        cmd = [
            "manim", "-ql", "--media_dir", "/tmp/media",
            "manim_modules/linear_algebra/eigen/eigen_svd.py",
            "EigenSVDScene"
        ]

        with st.status("🎬 Rendering... (~15 sec)", expanded=True) as status:
            try:
                subprocess.run(cmd, check=True, capture_output=True, text=True)
                video_path = "/tmp/media/videos/eigen_svd/480p15/EigenSVDScene.mp4"
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
    # Tab 1: Eigenvectors
    # ------------------------------------------------------------------
    with tabs[0]:
        st.header("Eigenvectors & Eigenvalues")
        st.info("Eigenvectors are the special directions that only **stretch**, never rotate.")
        st.markdown(r"""
        For matrix $A = \begin{bmatrix}3&1\\0&2\end{bmatrix}$:
        - $\vec{e}_1 = [1, 0]$ → eigenvalue $\lambda_1 = 3$ (stretches 3×)
        - $\vec{e}_2 = [1, 1]$ → eigenvalue $\lambda_2 = 2$ (stretches 2×)

        All other vectors rotate. Only the gold ones stay on their line.
        """)

        if st.button("🚀 Run (Eigenvectors)", key="btn_p4_s1", type="primary"):
            vid = run_viz(1, "eigenvector")
            if vid:
                st.video(open(vid, "rb").read(), autoplay=True)

    # ------------------------------------------------------------------
    # Tab 2: SVD
    # ------------------------------------------------------------------
    with tabs[1]:
        st.header("SVD — Singular Value Decomposition")
        st.info("Any matrix can be broken into three simple steps: Rotate → Scale → Rotate.")
        st.markdown(r"""
        $$A = U \Sigma V^T$$

        | Symbol | Meaning |
        |--------|---------|
        | $V^T$ | Rotate input to align with singular directions |
        | $\Sigma$ | Stretch/compress along each axis (singular values) |
        | $U$ | Rotate to final output orientation |

        Used in: image compression, PCA, recommendation systems.
        """)

        if st.button("🚀 Run (SVD)", key="btn_p4_s2", type="primary"):
            vid = run_viz(2, "svd")
            if vid:
                st.video(open(vid, "rb").read(), autoplay=True)
