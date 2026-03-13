import streamlit as st

# Import page modules
from modules import overview, phase1, phase2, phase3, phase4, phase5

st.set_page_config(page_title="Linear Algebra Viz", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for better sidebar styling
st.markdown("""
<style>
    /* Sidebar Navigation Styling */
    section[data-testid="stSidebar"] .stRadio > label {
        display: none; /* Hide default label "Navigation" */
    }
    div[dataclass="stRadio"] div[role="radiogroup"] > label > div:first-child {
        display: none; /* Hide radio button circle */
    }
    div[dataclass="stRadio"] div[role="radiogroup"] > label {
        padding: 10px 15px;
        border-radius: 8px;
        margin-bottom: 5px;
        transition: background-color 0.3s;
        cursor: pointer;
    }
    div[dataclass="stRadio"] div[role="radiogroup"] > label:hover {
        background-color: rgba(255, 75, 75, 0.1);
    }
    /* Active State Highlight */
    div[dataclass="stRadio"] div[role="radiogroup"] > label[data-checked="true"] {
        background-color: rgba(255, 75, 75, 0.2);
        border-left: 4px solid #FF4B4B;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State for Navigation
# Check URL query params first
query_params = st.query_params
url_page = query_params.get("page", "Overview")

if 'page' not in st.session_state:
    st.session_state.page = url_page
else:
    # If URL changed externally, sync session state
    if url_page != st.session_state.page:
        st.session_state.page = url_page

# Check for sub-step query param (e.g. ?page=Phase+1&step=2)
url_step = query_params.get("step", "1")
if 'phase1_step' not in st.session_state:
    st.session_state.phase1_step = int(url_step) if url_step.isdigit() else 1
else:
    if url_step.isdigit() and int(url_step) != st.session_state.phase1_step:
        st.session_state.phase1_step = int(url_step)

# Define Curriculum Structure (Phases)
CURRICULUM = {
    "Overview": "🏠  Overview",
    "Phase 1": "1️⃣  Vectors & Space",
    "Phase 2": "2️⃣  Matrix Transformation",
    "Phase 3": "3️⃣  Geometric Operations",
    "Phase 4": "4️⃣  Eigenvalues & SVD",
    "Phase 5": "5️⃣  AI Applications"
}

# Sidebar Navigation
st.sidebar.title("Curriculum Map")
st.sidebar.markdown("---")
# Sync sidebar with session state
selected_phase = st.sidebar.radio(
    "Navigation", 
    list(CURRICULUM.values()), 
    index=list(CURRICULUM.values()).index(CURRICULUM.get(st.session_state.page, CURRICULUM["Overview"])),
    label_visibility="collapsed"
)

# Update session state if sidebar changes
if selected_phase != CURRICULUM.get(st.session_state.page):
    # Reverse lookup to find key
    for key, value in CURRICULUM.items():
        if value == selected_phase:
            st.session_state.page = key
            # Update URL query params
            st.query_params["page"] = key
            st.rerun()

# Route to appropriate page
if st.session_state.page == "Overview":
    overview.render()
elif st.session_state.page == "Phase 1":
    phase1.render()
elif st.session_state.page == "Phase 2":
    phase2.render()
elif st.session_state.page == "Phase 3":
    phase3.render()
elif st.session_state.page == "Phase 4":
    phase4.render()
elif st.session_state.page == "Phase 5":
    phase5.render()
