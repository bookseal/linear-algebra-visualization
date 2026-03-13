import streamlit as st
import os
import base64

def render():
    st.title("📘 Visual Linear Algebra for AI Engineers")
    st.markdown("### Master the Geometry of Data")
    st.markdown("This interactive guide is designed to give you the **visual intuition** needed for deep learning and data science.")
    
    st.write("---")
    st.markdown("### 🔥 Animation Demo (From Phase 1)")
    
    # Try to load the Phase 1 video if available
    demo_video_path = "/tmp/media/videos/basis/480p15/VectorBasisScene.mp4"
    if os.path.exists(demo_video_path):
        video_file = open(demo_video_path, 'rb')
        video_bytes = video_file.read()
        video_base64 = base64.b64encode(video_bytes).decode()
        
        video_html = f"""
        <video width="100%" autoplay loop muted playsinline style="border-radius: 8px;">
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
        </video>
        """
        st.markdown(video_html, unsafe_allow_html=True)
        st.caption("Example: Vector Basis Animation created in Phase 1")
    else:
        st.info("💡 **Tip**: Go to 'Phase 1' and click 'Viz Basis!' to generate the demo animation here!")

    st.write("---")
    st.subheader("🎓 Curriculum Roadmap")
    
    # Phase 1
    with st.container():
        col_text, col_btn = st.columns([4, 1])
        with col_text:
            st.markdown("#### **Phase 1: Vectors & Space**")
            st.markdown("""
            - **Step 1**: Basis Vectors - Standard Basis $\hat{i}$, $\hat{j}$ as atoms of space.
            - **Step 2**: Linear Combinations & Span - Filling the 2D plane.
            - **Step 3**: Linear Independence - Understanding dimensions.
            """)
        with col_btn:
             if st.button("Go to Phase 1", key="btn_phase1"):
                 st.session_state.page = "Phase 1"
                 st.query_params["page"] = "Phase 1"
                 st.rerun()
    st.divider()

    # Phase 2
    with st.container():
        col_text, col_btn = st.columns([4, 1])
        with col_text:
            st.markdown("#### **Phase 2: Matrix Transformation**")
            st.markdown("""
            - **Matrix as Function**: Input vector $\\to$ Output vector.
            - **Visualizing Transforms**: Scaling, Rotation, Shear.
            - **Determinant**: Area expansion/contraction factor.
            - **Determinant = 0**: Collapsing dimensions.
            """)
        with col_btn:
             if st.button("Go to Phase 2", key="btn_phase2"):
                 st.session_state.page = "Phase 2"
                 st.query_params["page"] = "Phase 2"
                 st.rerun()
    st.divider()

    # Phase 3
    with st.container():
        col_text, col_btn = st.columns([4, 1])
        with col_text:
            st.markdown("#### **Phase 3: Geometric Operations (Coming Soon)**")
            st.markdown("""
            - **Matrix Multiplication**: Composition of transformations.
            - **Inverse Matrix**: Rewinding time/space.
            - **Dot Product**: Projection and Similarity.
            """)
        with col_btn:
             if st.button("Go to Phase 3", key="btn_phase3"):
                 st.session_state.page = "Phase 3"
                 st.query_params["page"] = "Phase 3"
                 st.rerun()
    st.divider()
    
    # Phase 4
    with st.container():
        col_text, col_btn = st.columns([4, 1])
        with col_text:
            st.markdown("#### **Phase 4: Eigenvalues & SVD (Coming Soon)**")
            st.markdown("""
            - **Eigenvectors**: The invariant axes of rotation/scaling.
            - **Eigenvalues**: The scaling factor along those axes.
            - **SVD**: Decomposing complex matrices into Rotation-Scaling-Rotation.
            """)
        with col_btn:
             if st.button("Go to Phase 4", key="btn_phase4"):
                 st.session_state.page = "Phase 4"
                 st.query_params["page"] = "Phase 4"
                 st.rerun()
    st.divider()

    # Phase 5
    with st.container():
        col_text, col_btn = st.columns([4, 1])
        with col_text:
            st.markdown("#### **Phase 5: AI Applications (Coming Soon)**")
            st.markdown("""
            - **PCA**: Finding the principal axes of data.
            - **Neural Networks**: Layer-by-layer space warping using ReLU and Weights.
            - **Word Embeddings**: 'King - Man + Woman = Queen' as vector arithmetic.
            """)
        with col_btn:
             if st.button("Go to Phase 5", key="btn_phase5"):
                 st.session_state.page = "Phase 5"
                 st.query_params["page"] = "Phase 5"
                 st.rerun()
