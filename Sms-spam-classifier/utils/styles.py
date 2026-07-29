import streamlit as st


def load_css():
    st.markdown(
        """
<style>

/* ============================================================
   GLOBAL
============================================================ */
html, body, [data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top left, #EEF3FC 0%, #F5F7FB 40%, #F5F7FB 100%);
    font-family: 'Segoe UI', 'Inter', sans-serif;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

/* ============================================================
   HERO
============================================================ */
.hero {
    background: linear-gradient(135deg, #2563EB 0%, #4F46E5 50%, #1E3A8A 100%);
    padding: 42px 50px;
    border-radius: 24px;
    color: white;
    text-align: center;
    margin-bottom: 22px;
    box-shadow: 0 25px 50px rgba(37, 99, 235, .25);
    position: relative;
    overflow: hidden;
}

.hero h1 {
    font-size: 40px;
    font-weight: 800;
    margin-bottom: 6px;
    letter-spacing: -0.5px;
}

.hero p {
    font-size: 17px;
    opacity: .92;
    margin: 0;
}

/* ============================================================
   FEATURE STRIP (compact, replaces bulky feature cards)
============================================================ */
.feature-strip {
    display: flex;
    justify-content: space-around;
    background: white;
    border-radius: 18px;
    padding: 16px 10px;
    box-shadow: 0 8px 22px rgba(0,0,0,.06);
    margin-bottom: 26px;
    flex-wrap: wrap;
}

.feature-strip .feature-item {
    text-align: center;
    padding: 6px 14px;
    font-size: 14.5px;
    font-weight: 600;
    color: #1E293B;
}

.feature-strip .feature-item span.icon {
    font-size: 20px;
    display: block;
    margin-bottom: 2px;
}

/* ============================================================
   SECTION CARD WRAPPER
============================================================ */
.section-card {
    background: #fff;
    margin-bottom: 20px;
    border-bottom: 1px solid #000000;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
    border-radius: 0;
}

.section-card h2, .section-card h3 {
    margin-top: 0;
}

/* ============================================================
   METRICS
============================================================ */
[data-testid="stMetric"] {
    background: white;
    border-radius: 16px;
    padding: 16px 18px;
    box-shadow: 0 8px 20px rgba(0,0,0,.06);
    border: 1px solid #EEF1F6;
}

/* ============================================================
   SIDEBAR
============================================================ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827 0%, #1F2937 100%);
}

[data-testid="stSidebar"] * {
    color: #F1F5F9 !important;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,.12);
}

/* ============================================================
   TABS
============================================================ */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: white;
    padding: 8px;
    border-radius: 16px;
    box-shadow: 0 6px 18px rgba(0,0,0,.05);
}

.stTabs [data-baseweb="tab"] {
    height: 46px;
    border-radius: 12px;
    padding: 0 20px;
    font-weight: 600;
    color: #475569;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #2563EB, #4F46E5) !important;
    color: white !important;
}

/* ============================================================
   BUTTONS
============================================================ */
.stButton > button {
    width: 100%;
    height: 56px;
    border-radius: 14px;
    font-size: 17px;
    font-weight: 700;
    border: none;
    background: linear-gradient(135deg, #2563EB, #4F46E5);
    color: white;
    transition: .25s;
    box-shadow: 0 10px 22px rgba(37,99,235,.25);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 28px rgba(37,99,235,.35);
}

/* ============================================================
   TEXTAREA
============================================================ */
textarea {
    font-size: 17px !important;
    border-radius: 16px !important;
}

/* ============================================================
   RESULT BANNERS
============================================================ */
.spam-card {
    background: linear-gradient(135deg, #FEE2E2, #FECACA);
    padding: 32px;
    border-radius: 20px;
    font-size: 26px;
    font-weight: 800;
    text-align: center;
    color: #991B1B;
    border-left: 8px solid #DC2626;
    box-shadow: 0 14px 30px rgba(220,38,38,.15);
}

.safe-card {
    background: linear-gradient(135deg, #DCFCE7, #BBF7D0);
    padding: 32px;
    border-radius: 20px;
    font-size: 26px;
    font-weight: 800;
    text-align: center;
    color: #166534;
    border-left: 8px solid #22C55E;
    box-shadow: 0 14px 30px rgba(34,197,94,.15);
}

/* ============================================================
   BADGES (model status, quick signals)
============================================================ */
.badge-good {
    background: #DCFCE7;
    color: #000000 !important;
    padding: 10px 16px;
    border-radius: 12px;
    font-weight: 700;
    text-align: center;
}

.badge-bad {
    background: #FEE2E2;
    color: #000000 !important;
    padding: 10px 16px;
    border-radius: 12px;
    font-weight: 700;
    text-align: center;
}

/* ============================================================
   EXPANDERS
============================================================ */
.streamlit-expanderHeader {
    font-size: 16px;
    font-weight: 600;
}

/* ============================================================
   PLOTLY / TABLES
============================================================ */
.js-plotly-plot, [data-testid="stDataFrame"] {
    border-radius: 16px;
    overflow: hidden;
}

/* ============================================================
   FOOTER
============================================================ */
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }

.app-footer {
    text-align: center;
    color: #94A3B8;
    font-size: 13.5px;
    margin-top: 30px;
}

</style>
""",
        unsafe_allow_html=True,
    )