import streamlit as st
import subprocess
import os
import math

def render():
    st.title("Phase 2: Matrix as Space Transformation")
    st.markdown("### 🌀 Before & After: Watch space warp in real time")
    st.caption("The gray dashed lines (Ghost Grid) show the **original positions** before transformation.")

    # Define Tabs
    tabs = st.tabs([
        "1. Scaling",
        "2. Rotation",
        "3. Shear",
        "4. Linearity",
        "5. Inverse"
    ])

    # Helper for rendering
    def run_viz(step_num, config_str):
        # Write config file for Manim scene
        with open(f"/tmp/p2_s{step_num}_config.txt", "w") as f:
            f.write(config_str)

        cmd = [
            "manim", "-ql", "--media_dir", "/tmp/media",
            "manim_modules/linear_algebra/transformations/linear_transform.py",
            "LinearTransformationScene"
        ]

        with st.status("🎥 Transforming space... (~15 sec)", expanded=True) as status:
            st.write("Building ghost grid...")
            try:
                subprocess.run(cmd, check=True, capture_output=True, text=True)

                video_path = "/tmp/media/videos/linear_transform/480p15/LinearTransformationScene.mp4"
                if os.path.exists(video_path):
                    status.update(label="✅ Done!", state="complete", expanded=False)
                    return video_path
                else:
                    status.update(label="❌ Video not found", state="error")
                    st.error("Video file missing.")
                    return None
            except Exception as e:
                st.error(f"Render failed: {e}")
                status.update(label="❌ Failed", state="error")
                return None

    # -------------------------------------------------------------
    # Tab 1: Scaling
    # -------------------------------------------------------------
    with tabs[0]:
        st.header("Step 1: Scaling")
        st.info("Stretch or shrink space along each axis.")

        c1, c2 = st.columns(2)
        sx = c1.slider("x scale", 0.5, 3.0, 2.0, 0.5, key="p2_s1_sx")
        sy = c2.slider("y scale", 0.5, 3.0, 1.0, 0.5, key="p2_s1_sy")

        if st.button("🚀 Run (Scaling)", key="btn_p2_s1", type="primary"):
            vid = run_viz(1, f"{sx},0,0,{sy},scaling")
            if vid:
                st.video(open(vid, 'rb').read(), autoplay=True)

    # -------------------------------------------------------------
    # Tab 2: Rotation
    # -------------------------------------------------------------
    with tabs[1]:
        st.header("Step 2: Rotation")
        st.info("Rotate the entire space around the origin.")

        angle = st.slider("Angle (degrees)", -180, 180, 45, 15, key="p2_s2_angle")
        rad = math.radians(angle)
        a, b, c, d = math.cos(rad), -math.sin(rad), math.sin(rad), math.cos(rad)

        if st.button("🚀 Run (Rotation)", key="btn_p2_s2", type="primary"):
            vid = run_viz(2, f"{a},{b},{c},{d},rotation")
            if vid:
                st.video(open(vid, 'rb').read(), autoplay=True)

    # -------------------------------------------------------------
    # Tab 3: Shear
    # -------------------------------------------------------------
    with tabs[2]:
        st.header("Step 3: Shear (Sliding Layers)")
        st.info("Like sliding a deck of cards sideways. Area is preserved.")

        k = st.slider("Shear factor", -2.0, 2.0, 1.0, 0.5, key="p2_s3_k")

        if st.button("🚀 Run (Shear)", key="btn_p2_s3", type="primary"):
            vid = run_viz(3, f"1,{k},0,1,shear")
            if vid:
                st.video(open(vid, 'rb').read(), autoplay=True)

    # -------------------------------------------------------------
    # Tab 4: Linearity
    # -------------------------------------------------------------
    with tabs[3]:
        st.header("Step 4: Linearity Check")
        st.markdown("Verify the two rules of linear transforms: straight lines stay straight, origin stays fixed.")

        choice = st.radio("Select test:", [
            "✅ Linear (valid)",
            "❌ Non-Linear (origin shifts)",
            "❌ Non-Linear (grid curves)"
        ], key="p2_s4_rad")

        mode_map = {
            "✅ Linear (valid)": "linear_valid",
            "❌ Non-Linear (origin shifts)": "linearity_shift",
            "❌ Non-Linear (grid curves)": "linearity_curve"
        }

        if st.button("🚀 Run (Rule Check)", key="btn_p2_s4", type="primary"):
            vid = run_viz(4, f"0,0,0,0,{mode_map[choice]}")
            if vid:
                st.video(open(vid, 'rb').read(), autoplay=True)

    # -------------------------------------------------------------
    # Tab 5: Inverse
    # -------------------------------------------------------------
    with tabs[4]:
        st.header("Step 5: Inverse Matrix")
        st.markdown("Rewind the transformation back to the original space.")

        case = st.radio("Condition:", ["Invertible", "Collapsed (det=0)"], key="p2_s5_rad")

        conf = "1,1,0,1,inverse_ok" if case == "Invertible" else "1,1,1,1,inverse_fail"

        if st.button("🚀 Run (Inverse)", key="btn_p2_s5", type="primary"):
            vid = run_viz(5, conf)
            if vid:
                st.video(open(vid, 'rb').read(), autoplay=True)
