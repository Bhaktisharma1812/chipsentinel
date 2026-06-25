import streamlit as st
import pandas as pd
import pickle

st.set_page_config(page_title="ChipSentinel", page_icon="🛡️", layout="wide")

st.title("🛡️ ChipSentinel")
st.caption("AI-driven program health & early-warning for chip design programs  |  Bhakti Sharma, M25AI2173, IIT Jodhpur")
st.divider()

@st.cache_resource
def load_pillar2():
    with open('pillar2_model.pkl', 'rb') as f:
        return pickle.load(f)

@st.cache_resource
def load_pillar3_scores():
    with open('pillar3_scores.pkl', 'rb') as f:
        return pickle.load(f)

@st.cache_data
def load_issues():
    return pd.read_csv('opentitan_issues.csv')

p2_model  = load_pillar2()
p3_scores = load_pillar3_scores()
issues_df = load_issues()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"**Tape-out Readiness**\n## {p3_scores['total']}/100\n🔴 RED — At Risk")
with col2:
    st.markdown(f"**Pillar 1 — Risk Model**\n## F1: 0.915\n✅ Excellent")
with col3:
    st.markdown(f"**Pillar 2 — Blocker Detection**\n## F1: 0.799\n✅ Good")
with col4:
    st.markdown(f"**Red Dependencies**\n## {p3_scores['red_deps']}\n⚠️ {p3_scores['total_delay']} days delay")

st.divider()
tab1, tab2, tab3, tab4 = st.tabs(["📋 Executive Brief", "🎯 Pillar 1", "💬 Pillar 2", "🔗 Pillar 3"])

with tab1:
    st.subheader("60-Second Program Health Brief")
    st.error(f"""
    ** OVERALL STATUS: AT RISK — Tape-out Readiness {p3_scores['total']}/100**

    1. **DFT is critically behind schedule** — only 45% complete, RTL→DFT dependency has 12-day delay.
    2. **DRC/LVS signoff barely started** — 20% complete, 4.0/20 points.
    3. **Dependency health at zero** — 2 critical dependencies red, 55 total delay days.

    **Recommended action:** Escalate DFT resourcing immediately.
    """)
    st.info("**What's working well:** DV coverage at 21.6/30. Architecture and RTL on track.")

# TAB 2 — pure markdown table, no raw HTML
with tab2:
    st.subheader("Validation Gap Risk Scorer")
    st.write("Model trained on 500 real OpenTitan issues. **F1 Score: 0.915**")

    high_risk = issues_df[issues_df['risk_score_v2'] >= 2][['id','title']].head(10)

    md_table = "| ID | Title |\n|---|---|\n"
    for _, row in high_risk.iterrows():
        title_clean = str(row['title']).replace("|", "-")[:65]
        md_table += f"| #{row['id']} | {title_clean} |\n"
    st.markdown(md_table)

    st.divider()
    low  = len(issues_df[issues_df['risk_score_v2']<=1])
    med  = len(issues_df[issues_df['risk_score_v2']==2])
    high = len(issues_df[issues_df['risk_score_v2']==3])
    st.write(f"**Risk distribution:** Low: {low}  |  Medium: {med}  |  High: {high}")

# TAB 3 — radio buttons, no selectbox/text_area/button
with tab3:
    st.subheader("Buried Blocker Detection — Live Demo")
    st.write("Pick a comment to see the model's prediction instantly:")

    sample_comments = {
        "Blocker — DFT delay"        : "Blocked on DFT sign-off for 2 weeks. No response from team.",
        "Blocker — no owner"         : "No owner assigned to this P0 bug. Sitting unresolved for 3 weeks.",
        "Blocker — escalation"       : "Escalate now. This is on the critical path to tape-out.",
        "Normal — progress update"   : "Coverage closure progressing well. On track for Friday.",
        "Normal — sign-off complete" : "DFT insertion complete for this IP. Moving to sign-off phase.",
    }

    choice = st.radio("", list(sample_comments.keys()), label_visibility="collapsed")
    selected_text = sample_comments[choice]

    st.write(f"**Comment:** _{selected_text}_")

    pred = p2_model.predict([selected_text])[0]
    prob = p2_model.predict_proba([selected_text])[0]
    confidence = max(prob) * 100

    if pred == 1:
        st.error(f" BLOCKER DETECTED — Confidence: {confidence:.0f}%")
    else:
        st.success(f" Normal Update — Confidence: {confidence:.0f}%")

    st.divider()
    st.write("**Model trained on 203 synthetic Jira comments. F1 Score: 0.799**")
    st.write("Top predictive words: *waiting, blocked, weeks, dependency, escalate*")

with tab4:
    st.subheader("Cross-Team Dependency Graph")
    st.write(f"**DV Coverage:** {p3_scores['dv_score']}/30")
    st.write(f"**DFT Sign-off:** {p3_scores['dft_score']}/25")
    st.write(f"**Dependency Health:** {p3_scores['dep_score']}/25")
    st.write(f"**DRC/LVS:** {p3_scores['drc_score']}/20")
    st.divider()
    st.markdown(f"### TOTAL READINESS: {p3_scores['total']}/100")
    st.write("Full dependency graph diagram available in MTP 1 report (Figure 3).")

st.divider()
st.caption("ChipSentinel MTP 1 | Supervised by Dr. Binod Kumar, IIT Jodhpur")
