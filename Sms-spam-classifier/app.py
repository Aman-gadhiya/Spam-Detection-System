# ==========================================================
# AI SPAM DETECTOR
# ==========================================================

import re
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils.helper import load_metadata, risk_level
from utils.predictor import SpamPredictor
from utils.styles import load_css

# ==========================================================
# PREDICTION HISTORY STORAGE
# ==========================================================

HISTORY_FILE = Path(__file__).parent / "history" / "predictions.csv"
HISTORY_COLUMNS = ["Timestamp", "Message", "Prediction", "Confidence", "Risk Level"]


def load_history():
    if HISTORY_FILE.exists():
        try:
            return pd.read_csv(HISTORY_FILE)
        except Exception:
            return pd.DataFrame(columns=HISTORY_COLUMNS)
    return pd.DataFrame(columns=HISTORY_COLUMNS)


def save_prediction(message, result):
    history_df = load_history()

    new_row = pd.DataFrame(
        [
            {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Message": message,
                "Prediction": result["label"],
                "Confidence": round(result["confidence"], 2) if result["confidence"] else "",
                "Risk Level": risk_level(result["confidence"]),
            }
        ]
    )

    history_df = pd.concat([history_df, new_row], ignore_index=True)
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    history_df.to_csv(HISTORY_FILE, index=False)


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

_logo_path = Path(__file__).parent / "asset" / "logo.png"
_page_icon = str(_logo_path) if _logo_path.exists() else "🛡️"

st.set_page_config(
    page_title="AI Spam Detector",
    page_icon=_page_icon,
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

SPAM_KEYWORDS = [
    "free", "winner", "claim", "click", "urgent", "offer",
    "money", "cash", "loan", "bonus", "gift", "prize",
]


def message_statistics(text):
    characters = len(text)
    words = len(text.split())
    sentences = len(re.findall(r"[.!?]+", text)) if text.strip() else 0
    reading_time = max(1, round(words / 200)) if words else 0

    return {
        "characters": characters,
        "words": words,
        "sentences": sentences,
        "reading_time": reading_time,
    }


def explain_prediction(message):
    """Return a short list of human-readable signals behind the prediction."""
    explanation = []
    text = message.lower()

    found = [word for word in SPAM_KEYWORDS if word in text]
    if found:
        explanation.append(f"Contains common spam keywords: {', '.join(found)}")

    if "http://" in text or "https://" in text or "www." in text:
        explanation.append("Contains a website link")

    uppercase = sum(1 for c in message if c.isupper())
    if uppercase > 10:
        explanation.append("Unusually high amount of capital letters")

    if message.count("!") >= 3:
        explanation.append("Multiple exclamation marks")

    if sum(c.isdigit() for c in message) >= 3:
        explanation.append("Contains several numbers")

    if len(message) < 30:
        explanation.append("Message is very short")

    return explanation, found


def confidence_message(confidence):
    if confidence is None:
        return ("Unknown", "⚪", "Confidence score unavailable.")
    elif confidence >= 95:
        return ("Very High", "🟢", "The AI model is extremely confident about this prediction.")
    elif confidence >= 80:
        return ("High", "🔵", "The prediction is highly reliable.")
    elif confidence >= 60:
        return ("Medium", "🟡", "The prediction is reasonably reliable.")
    else:
        return ("Low", "🔴", "The prediction should be interpreted carefully.")


def render_analytics_dashboard(result):
    """A single, polished dashboard: metrics + donut chart + gradient bars."""
    spam_prob = result["probabilities"][1] * 100
    safe_prob = result["probabilities"][0] * 100
    is_spam = result["prediction"] == 1

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 📊 AI Analytics Dashboard")
    st.caption("A quick visual breakdown of how confident the model is, and why.")

    m1, m2, m3 = st.columns(3)
    m1.metric("🟢 Safe Probability", f"{safe_prob:.1f}%")
    m2.metric("🔴 Spam Probability", f"{spam_prob:.1f}%")
    m3.metric("🎯 Model Confidence", f"{result['confidence']:.1f}%" if result["confidence"] else "N/A")

    chart_col, bar_col = st.columns([1, 1])

    with chart_col:
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=["Safe", "Spam"],
                    values=[safe_prob, spam_prob],
                    hole=0.68,
                    marker=dict(colors=["#22C55E", "#EF4444"], line=dict(color="white", width=3)),
                    textinfo="percent",
                    textfont=dict(size=15, color="white"),
                    sort=False,
                )
            ]
        )
        fig.update_layout(
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
            margin=dict(l=10, r=10, t=10, b=10),
            height=300,
            annotations=[
                dict(
                    text=f"<b>{result['label']}</b>",
                    x=0.5, y=0.5,
                    font=dict(size=20, color="#DC2626" if is_spam else "#16A34A"),
                    showarrow=False,
                )
            ],
        )
        st.plotly_chart(fig, use_container_width=True)

    with bar_col:
        st.markdown(
            f"""
            <div style="padding-top: 18px;">
                <p style="margin-bottom:6px;font-weight:600;color:#166534;">🟢 Safe &nbsp; {safe_prob:.1f}%</p>
                <div style="background:#E5E7EB;border-radius:10px;height:20px;overflow:hidden;margin-bottom:22px;">
                    <div style="width:{safe_prob}%;background:linear-gradient(90deg,#4ADE80,#16A34A);height:100%;"></div>
                </div>
                <p style="margin-bottom:6px;font-weight:600;color:#991B1B;">🔴 Spam &nbsp; {spam_prob:.1f}%</p>
                <div style="background:#E5E7EB;border-radius:10px;height:20px;overflow:hidden;">
                    <div style="width:{spam_prob}%;background:linear-gradient(90deg,#F87171,#DC2626);height:100%;"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        level, icon, description = confidence_message(result["confidence"])
        st.info(f"{icon} **{level} confidence** — {description}")

    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================================
# LOAD MODEL
# ==========================================================

metadata = {}
model_loaded = False
model_error = None

try:
    predictor = SpamPredictor("spam_detector_pipeline.pkl")
    metadata = load_metadata()
    model_loaded = True
except Exception as e:
    model_error = str(e)


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:
    if _logo_path.exists():
        st.image(str(_logo_path), width=90)

    st.markdown("## 🛡️ AI Spam Detector")
    st.caption("Enterprise Email & SMS Security")
    st.markdown("---")

    if model_loaded:
        st.markdown('<div class="badge-good">✅ AI Model Ready</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="badge-bad">❌ Model Not Loaded</div>', unsafe_allow_html=True)
        if model_error:
            st.caption(model_error)

    st.markdown("---")
    st.markdown(
        """
        **Navigate**
        🔍 Analyze a message
        📜 View prediction history
        """
    )
    st.markdown("---")
    st.caption("Your messages are analyzed in real time and are not shared with third parties.")


# ==========================================================
# HERO
# ==========================================================

st.markdown(
    """
    <div class="hero">
    <h1>🛡️ AI Email & SMS Spam Detector</h1>
    <p>Paste a message below and let AI tell you instantly if it's safe or spam.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="feature-strip">
        <div class="feature-item"><span class="icon">⚡</span>Instant Results</div>
        <div class="feature-item"><span class="icon">🎯</span>AI-Powered Accuracy</div>
        <div class="feature-item"><span class="icon">🔒</span>Privacy Friendly</div>
        <div class="feature-item"><span class="icon">📈</span>Visual Insights</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# TABS
# ==========================================================

tab_analyze, tab_history = st.tabs(["🔍 Analyze Message", "📜 Prediction History"])

# ----------------------------------------------------------
# TAB 1 — ANALYZE
# ----------------------------------------------------------
with tab_analyze:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("📩 Message Analyzer")

    message = st.text_area(
        "Paste your Email or SMS",
        height=200,
        placeholder=(
            "Example:\n"
            "Congratulations! You have won a FREE iPhone.\n"
            "Click the link below to claim."
        ),
        label_visibility="collapsed",
    )

    with st.expander("📚 See example messages"):
        ex1, ex2 = st.columns(2)
        with ex1:
            st.caption("Spam example")
            st.code("Congratulations!\nYou have won a FREE iPhone.\nClaim your prize now.")
        with ex2:
            st.caption("Safe example")
            st.code("Hey,\nAre we still meeting tomorrow at 6 PM?\nLet me know.")

    stats = message_statistics(message)
    s1, s2, s3, s4 = st.columns(4)
    s1.caption(f"🔤 {stats['characters']} characters")
    s2.caption(f"📝 {stats['words']} words")
    s3.caption(f"📄 {stats['sentences']} sentences")
    s4.caption(f"⏱ ~{stats['reading_time']} min read")

    button1, button2 = st.columns(2)
    with button1:
        predict = st.button("🚀 Analyze Message", use_container_width=True, type="primary")
    with button2:
        clear = st.button("🗑 Clear", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    if clear:
        st.rerun()

    if predict:
        if not model_loaded:
            st.error("AI Model is not loaded. Please check that `spam_detector_pipeline.pkl` is present.")
            st.stop()

        if message.strip() == "":
            st.warning("Please enter a message to analyze.")
            st.stop()

        with st.spinner("🧠 Running AI Analysis..."):
            result = predictor.analyze(message)
            explanation, detected_words = explain_prediction(message)
            save_prediction(message, result)

        is_spam = result["prediction"] == 1

        # --- Result banner ---
        if is_spam:
            st.markdown(
                '<div class="spam-card">🚨 SPAM DETECTED<br>'
                '<span style="font-size:16px;font-weight:500;">This message shows patterns commonly seen in spam.</span></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="safe-card">✅ MESSAGE IS SAFE<br>'
                '<span style="font-size:16px;font-weight:500;">No significant spam indicators were detected.</span></div>',
                unsafe_allow_html=True,
            )

        st.write("")

        # --- AI recommendation ---
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 💡 AI Recommendation")
        confidence = result["confidence"] or 0

        if is_spam:
            if confidence >= 90:
                st.error(
                    "This message is **very likely spam**.\n\n"
                    "- Avoid clicking any links\n"
                    "- Never share passwords or OTPs\n"
                    "- Verify the sender before responding"
                )
            elif confidence >= 70:
                st.warning("This message looks suspicious — verify the sender before taking any action.")
            else:
                st.info("A few spam characteristics were detected. Review the message carefully.")
        else:
            if confidence >= 90:
                st.success("This message appears safe. No obvious spam indicators were detected.")
            else:
                st.info("This message appears safe, but always verify messages from unknown senders.")

        if explanation:
            with st.expander("🔎 Why did the AI decide this?"):
                for reason in explanation:
                    st.write(f"• {reason}")
        st.markdown("</div>", unsafe_allow_html=True)

        # --- Analytics dashboard ---
        if result["probabilities"] is not None:
            render_analytics_dashboard(result)

# ----------------------------------------------------------
# TAB 2 — HISTORY
# ----------------------------------------------------------
with tab_history:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("📜 Prediction History")

    history_df = load_history()

    if history_df.empty:
        st.info("No predictions available yet — analyze a message to get started.")
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Predictions", len(history_df))
        c2.metric("Spam Messages", int((history_df["Prediction"] == "Spam").sum()))
        c3.metric("Safe Messages", int((history_df["Prediction"] == "Safe").sum()))

        history_df = history_df.sort_values(by="Timestamp", ascending=False)

        search = st.text_input("🔍 Search messages", placeholder="Type to filter...")
        if search:
            history_df = history_df[
                history_df["Message"].str.contains(search, case=False, na=False)
            ]

        st.dataframe(history_df, use_container_width=True, hide_index=True)

        dl_col, clear_col = st.columns(2)
        with dl_col:
            if not history_df.empty:
                csv = history_df.to_csv(index=False)
                st.download_button(
                    "📥 Download History", csv, "prediction_history.csv", "text/csv",
                    use_container_width=True,
                )
        with clear_col:
            if st.button("🗑 Clear History", use_container_width=True):
                pd.DataFrame(columns=HISTORY_COLUMNS).to_csv(HISTORY_FILE, index=False)
                st.success("History cleared.")
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================================
# FOOTER
# ==========================================================

st.markdown(
    """
    <div class="app-footer">
    🛡 <b>AI Spam Detector</b> · Built with Python, Streamlit & Scikit-Learn<br>
    © 2026 All Rights Reserved
    </div>
    """,
    unsafe_allow_html=True,
)