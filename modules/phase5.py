# Purpose: Streamlit UI for Phase 5 — AI Applications of Linear Algebra
# Scope: PCA, neural network warping, and word embedding visualizations
# Notes: Renders via AIAppsScene in manim_modules/linear_algebra/ai/ai_apps.py

import streamlit as st
import subprocess
import os


def render() -> None:
    """Renders the Phase 5 interactive page."""
    st.title("Phase 5: AI Applications")
    st.markdown("Where linear algebra **meets** deep learning — the geometry behind AI.")

    tabs = st.tabs(["1. PCA", "2. Neural Net Space Warping", "3. Word Embeddings"])

    def run_viz(step_num: int, config_str: str) -> str | None:
        """Writes config and runs Manim scene, returns video path or None."""
        with open(f"/tmp/p5_s{step_num}_config.txt", "w") as f:
            f.write(config_str)

        cmd = [
            "manim", "-ql", "--media_dir", "/tmp/media",
            "manim_modules/linear_algebra/ai/ai_apps.py",
            "AIAppsScene"
        ]

        with st.status("🎬 Rendering... (~15 sec)", expanded=True) as status:
            try:
                subprocess.run(cmd, check=True, capture_output=True, text=True)
                video_path = "/tmp/media/videos/ai_apps/480p15/AIAppsScene.mp4"
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
    # Tab 1: PCA
    # ------------------------------------------------------------------
    with tabs[0]:
        st.header("PCA — Principal Component Analysis")
        st.info("Find the axes of maximum variance and compress data with minimal loss.")
        st.markdown(r"""
        PCA uses **eigenvectors** of the covariance matrix:
        - **PC1** = direction of greatest spread → keep this
        - **PC2** = perpendicular direction → drop this to compress to 1D

        Used in: face recognition, image compression, noise reduction.
        """)

        if st.button("🚀 Run (PCA)", key="btn_p5_s1", type="primary"):
            vid = run_viz(1, "pca")
            if vid:
                st.video(open(vid, "rb").read(), autoplay=True)

    # ------------------------------------------------------------------
    # Tab 2: Neural Net
    # ------------------------------------------------------------------
    with tabs[1]:
        st.header("Neural Net — Layer-by-Layer Space Warping")
        st.info("Each layer transforms space until classes become linearly separable.")
        st.markdown(r"""
        A neural network layer does two things:
        1. **Linear transform** $W\vec{x}$ — rotate, stretch, shear the space
        2. **ReLU** $\max(0, x)$ — fold the negative half to zero (non-linearity)

        Repeat this enough times and even tangled data can be separated by a flat plane.
        """)

        if st.button("🚀 Run (Neural Net)", key="btn_p5_s2", type="primary"):
            vid = run_viz(2, "neuralnet")
            if vid:
                st.video(open(vid, "rb").read(), autoplay=True)

    # ------------------------------------------------------------------
    # Tab 3: Word Embeddings
    # ------------------------------------------------------------------
    with tabs[2]:
        st.header("Word Embeddings — Vector Arithmetic in Semantic Space")
        st.info("Words are vectors. Relationships are vector differences.")
        st.markdown(r"""
        The famous equation:
        $$\text{King} - \text{Man} + \text{Woman} \approx \text{Queen}$$

        - The **gender direction** ($\vec{Woman} - \vec{Man}$) is a consistent vector in embedding space.
        - Adding it to King lands near Queen — geometry encodes meaning.

        Used in: Word2Vec, GloVe, and every modern LLM tokenizer.
        """)

        if st.button("🚀 Run (Word Embeddings)", key="btn_p5_s3", type="primary"):
            vid = run_viz(3, "embedding")
            if vid:
                st.video(open(vid, "rb").read(), autoplay=True)
