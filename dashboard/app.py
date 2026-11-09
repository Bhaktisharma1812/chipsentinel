import streamlit as st
import pandas as pd
import pickle
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

st.set_page_config(page_title="ChipSentinel", page_icon="🛡️", layout="wide")

st.markdown("""<style>
html, body, [class*="css"], .stMarkdown, p, li, label {font-size:18px !important; line-height:1.6;}
h1 {font-size:2.6rem !important;} h2 {font-size:2rem !important;} h3 {font-size:1.5rem !important;}
[data-testid="stMetricValue"] {font-size:2.4rem !important;}
[data-testid="stMetricLabel"] p {font-size:1.1rem !important;}
[data-testid="stCaptionContainer"] p {font-size:15px !important;}
section[data-testid="stSidebar"] * {font-size:17px !important;}
.block-container {padding-top:2rem; max-width:1300px;}
</style>""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🛡️ ChipSentinel")
    st.caption("Bhakti Sharma | M25AI2173 | IIT Jodhpur")
    st.divider()
    page = st.radio("Navigate", [
        "📋 Executive Brief",
        "🎯 Pillar 1: Validation Risk",
        "💬 Pillar 2: Blocker Detection",
        "🔗 Pillar 3: Dependency Graph",
        "🧪 Joint Results (Ablation)",
    ], label_visibility="collapsed")
    st.divider()
    st.caption("MTP 2 — In Progress")
    st.caption("Supervised by Dr. Binod Kumar")

@st.cache_resource
def load_p2():
    with open('pillar2_model.pkl','rb') as f: return pickle.load(f)
@st.cache_resource
def load_p3():
    with open('pillar3_scores.pkl','rb') as f: return pickle.load(f)
@st.cache_data
def load_issues():
    return pd.read_csv('opentitan_issues.csv')

p2_model  = load_p2()
p3_scores = load_p3()
issues_df = load_issues()

# ── Team data ─────────────────────────────────────────
teams = {
    "Architecture":    {"completion":100, "delay":0,  "blockers":0, "status":"green"},
    "RTL Design":      {"completion":85,  "delay":3,  "blockers":1, "status":"amber"},
    "DV":              {"completion":72,  "delay":3,  "blockers":2, "status":"amber"},
    "DFT":             {"completion":45,  "delay":12, "blockers":3, "status":"red"},
    "Synthesis":       {"completion":60,  "delay":2,  "blockers":1, "status":"amber"},
    "Physical Design": {"completion":50,  "delay":4,  "blockers":1, "status":"amber"},
    "Timing Closure":  {"completion":30,  "delay":4,  "blockers":0, "status":"red"},
    "DRC/LVS":         {"completion":20,  "delay":4,  "blockers":0, "status":"red"},
}
gates = {
    ("RTL Design","DFT"):     {"delay":12,"label":"GATED"},
    ("Physical Design","Timing Closure"): {"delay":4,"label":"GATED"},
}
status_color = {"green":"#2ecc71","amber":"#f39c12","red":"#e74c3c"}

# ── Spotlight findings ────────────────────────────────
findings = [
    {"team":"DFT",           "icon":"🔴","msg":"DFT is 12 days behind — gated on RTL Design freeze. Critical path to tape-out."},
    {"team":"RTL Design",    "icon":"🟡","msg":"RTL Design has 1 open blocker causing a cascade: DFT and Synthesis both waiting."},
    {"team":"DRC/LVS",       "icon":"🔴","msg":"Physical verification at 20% — needs to accelerate immediately for tape-out."},
    {"team":"Timing Closure","icon":"🔴","msg":"Timing Closure at 30% with no assigned blockers — resourcing gap likely."},
]

st.title("🛡️ ChipSentinel")
st.caption("AI-driven program health & early-warning for chip design programs")
st.divider()

c1,c2,c3,c4 = st.columns(4)
with c1: st.markdown(f"**Tape-out Readiness**\n## {p3_scores['total']}/100\n🔴 RED — At Risk")
with c2: st.markdown(f"**Pillar 1 — Risk Model**\n## F1: 0.915\n✅ Excellent")
with c3: st.markdown(f"**Pillar 2 — Blockers**\n## F1: 0.799\n✅ Good")
with c4: st.markdown(f"**Red Dependencies**\n## {p3_scores['red_deps']}\n⚠️ {p3_scores['total_delay']} days delay")
st.divider()

# ════════════════════════════════════════════════════════
if page == "📋 Executive Brief":
    st.subheader("60-Second Program Health Brief")

    # ── Spotlight ──────────────────────────────────────
    st.markdown("### 🔦 Spotlight Findings")
    for f in findings:
        color = "#fde8e8" if f["icon"]=="🔴" else "#fdf0dc"
        border = "#e74c3c" if f["icon"]=="🔴" else "#f39c12"
        st.markdown(f"""<div style='background:{color};border-left:4px solid {border};
        padding:10px 14px;border-radius:4px;margin-bottom:8px;font-size:17px;color:#1a1a1a'>
        {f["icon"]} <b>{f["team"]}</b> — {f["msg"]}</div>""", unsafe_allow_html=True)

    st.divider()
    col_a, col_b = st.columns([1, 1.4])
    with col_a:
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=p3_scores['total'],
            title={'text':"Tape-out Readiness",'font':{'size':14}},
            gauge={'axis':{'range':[0,100]},'bar':{'color':"#e74c3c"},
                   'steps':[{'range':[0,60],'color':'#fde8e8'},
                             {'range':[60,80],'color':'#fdf0dc'},
                             {'range':[80,100],'color':'#dff0e4'}]}))
        fig.update_layout(height=280,margin=dict(t=60,b=10,l=30,r=30),paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    with col_b:
        st.error("**🔴 AT RISK — Readiness 36.8/100**\n\n"
                 "1. **DFT critically behind** — 45% complete, 12-day delay.\n"
                 "2. **DRC/LVS barely started** — 20% complete.\n"
                 "3. **Dependency health zero** — 55 total delay days.\n\n"
                 "**Action:** Escalate DFT resourcing immediately.")
        st.info("**Working well:** DV coverage at 21.6/30. Architecture and RTL on track.")

    # ── Trend chart ────────────────────────────────────
    st.divider()
    st.markdown("### 📈 Readiness Score Trend (Simulated)")
    weeks = [f"W{i+1}" for i in range(8)]
    scores = [62, 58, 54, 50, 46, 42, 39, 36.8]
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=weeks, y=scores, mode='lines+markers',
        line=dict(color='#e74c3c', width=3),
        marker=dict(size=8, color=['#2ecc71']+['#f39c12']*3+['#e74c3c']*4),
        fill='tozeroy', fillcolor='rgba(231,76,60,0.1)'))
    fig2.add_hline(y=60, line_dash='dash', line_color='#f39c12',
                   annotation_text='Amber threshold (60)')
    fig2.add_hline(y=80, line_dash='dash', line_color='#2ecc71',
                   annotation_text='Green threshold (80)')
    fig2.update_layout(height=260, yaxis_range=[0,100],
                       yaxis_title='Readiness Score',
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)',
                       margin=dict(t=20,b=20,l=20,r=20))
    st.plotly_chart(fig2, use_container_width=True)

    # ── Team scorecards ────────────────────────────────
    st.divider()
    st.markdown("### 👥 Team Health Scorecards")
    cols = st.columns(4)
    for i, (team, data) in enumerate(teams.items()):
        with cols[i % 4]:
            sc = status_color[data["status"]]
            st.markdown(f"""<div style='background:#f8f9fa;border-left:4px solid {sc};
            padding:10px;border-radius:4px;margin-bottom:10px'>
            <div style='font-size:16px;font-weight:600;color:#1a1a1a'>{team}</div>
            <div style='font-size:30px;font-weight:700;color:{sc}'>{data["completion"]}%</div>
            <div style='font-size:14px;color:#555'>Delay: {data["delay"]}d &nbsp;|&nbsp; 
            Blockers: {data["blockers"]}</div></div>""", unsafe_allow_html=True)

    # ── Breakdown chart ────────────────────────────────
    st.divider()
    st.markdown("### 📊 Readiness Score Breakdown")
    components = ['DV Coverage (30)','DFT Sign-off (25)','Dependency Health (25)','DRC/LVS (20)']
    scores_b   = [p3_scores['dv_score'],p3_scores['dft_score'],p3_scores['dep_score'],p3_scores['drc_score']]
    maximums   = [30,25,25,20]
    gaps       = [m-s for s,m in zip(scores_b,maximums)]
    bar_colors = ['#2ecc71' if s/m>=0.8 else '#f39c12' if s/m>=0.6 else '#e74c3c'
                  for s,m in zip(scores_b,maximums)]
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(name='Score',x=components,y=scores_b,marker_color=bar_colors,
                          text=[f"{s}" for s in scores_b],textposition='inside'))
    fig3.add_trace(go.Bar(name='Remaining',x=components,y=gaps,marker_color='rgba(200,200,200,0.3)'))
    fig3.update_layout(barmode='stack',height=300,paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)',margin=dict(t=10,b=20,l=20,r=20),
                       legend=dict(orientation='h',y=1.1))
    st.plotly_chart(fig3, use_container_width=True)

# ════════════════════════════════════════════════════════
elif page == "🎯 Pillar 1: Validation Risk":
    st.subheader("Validation Gap Risk Scorer")
    st.write("Gradient Boosting on 500 real OpenTitan issues. **F1 Score: 0.915**")

    # Action panel
    st.markdown("""<div style='background:#fde8e8;border-left:4px solid #e74c3c;
    padding:12px 16px;border-radius:4px;margin-bottom:16px'>
    <b>🔴 Action Required</b> — 9 high/medium risk issues identified. 
    Top risk: security + DV component bugs with 10+ comments unresolved.
    Assign owners to issues #30144, #29817, #28968 immediately.</div>""",
    unsafe_allow_html=True)

    col_a,col_b = st.columns(2)
    with col_a:
        st.write("**Risk distribution across 500 issues**")
        low=len(issues_df[issues_df['risk_score_v2']<=1])
        med=len(issues_df[issues_df['risk_score_v2']==2])
        high=len(issues_df[issues_df['risk_score_v2']==3])
        fig=go.Figure(go.Bar(x=['Low','Medium','High'],y=[low,med,high],
            marker_color=['#2ecc71','#f39c12','#e74c3c'],
            text=[low,med,high],textposition='outside'))
        fig.update_layout(height=300,showlegend=False,paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)',margin=dict(t=10,b=20,l=20,r=20))
        st.plotly_chart(fig,use_container_width=True)
    with col_b:
        st.write("**Model comparison (CV F1)**")
        fig2=go.Figure(go.Bar(x=['Logistic\nRegression','Random\nForest','Gradient\nBoosting'],
            y=[0.429,0.727,0.915],marker_color=['#95a5a6','#3498db','#2ecc71'],
            text=['0.429','0.727','0.915'],textposition='outside'))
        fig2.add_hline(y=0.9,line_dash='dash',line_color='red',annotation_text='0.9 threshold')
        fig2.update_layout(height=300,showlegend=False,yaxis_range=[0,1.1],
                           paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
                           margin=dict(t=10,b=20,l=20,r=20))
        st.plotly_chart(fig2,use_container_width=True)

    st.write("**Feature importance**")
    feats=['has_bug_label','has_risk_keyword','has_security','has_dv','has_rtl',
           'has_silicon_val','comment_count','label_count','body_length']
    imps=[0.220,0.201,0.140,0.138,0.101,0.100,0.041,0.037,0.021]
    fig3=go.Figure(go.Bar(x=imps,y=feats,orientation='h',
        marker_color=['#e74c3c' if i>0.1 else '#3498db' if i>0.03 else '#95a5a6' for i in imps],
        text=[f"{i:.3f}" for i in imps],textposition='outside'))
    fig3.update_layout(height=320,paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)',margin=dict(t=10,b=20,l=20,r=20))
    st.plotly_chart(fig3,use_container_width=True)

    st.write("**High-risk issues identified**")
    hr=issues_df[issues_df['risk_score_v2']>=2][['id','title']].head(10)
    md="| ID | Issue Title |\n|---|---|\n"
    for _,row in hr.iterrows():
        md+=f"| #{row['id']} | {str(row['title'])[:75]} |\n"
    st.markdown(md)

# ════════════════════════════════════════════════════════
elif page == "💬 Pillar 2: Blocker Detection":
    st.subheader("Buried Blocker Detection — Live Demo")

    st.markdown("""<div style='background:#fdf0dc;border-left:4px solid #f39c12;
    padding:12px 16px;border-radius:4px;margin-bottom:16px'>
    <b>⚠️ 2 threads going quiet</b> — DFT sign-off thread silent for 12 days. 
    RTL freeze dependency thread silent for 8 days. Both need escalation today.</div>""",
    unsafe_allow_html=True)

    samples={
        "🚨 Blocker — DFT delay"       :"Blocked on DFT sign-off for 2 weeks. No response from team.",
        "🚨 Blocker — no owner"        :"No owner assigned to this P0 bug. Sitting unresolved for 3 weeks.",
        "🚨 Blocker — escalation"      :"Escalate now. This is on the critical path to tape-out.",
        "✅ Normal — progress update"  :"Coverage closure progressing well. On track for Friday.",
        "✅ Normal — sign-off complete":"DFT insertion complete for this IP. Moving to sign-off phase.",
    }
    choice=st.radio("Pick a comment:",list(samples.keys()),label_visibility="collapsed")
    selected=samples[choice]
    st.write(f"**Comment:** _{selected}_")
    pred=p2_model.predict([selected])[0]
    probs=p2_model.predict_proba([selected])[0]
    conf=max(probs)*100
    col_a,col_b=st.columns([1,1])
    with col_a:
        if pred==1: st.error(f"🚨 BLOCKER DETECTED — Confidence: {conf:.0f}%")
        else:       st.success(f"✅ Normal Update — Confidence: {conf:.0f}%")
        fig=go.Figure(go.Indicator(mode="gauge+number",value=conf,
            title={'text':"Confidence %"},
            gauge={'axis':{'range':[0,100]},'bar':{'color':'#e74c3c' if pred==1 else '#2ecc71'}}))
        fig.update_layout(height=240,paper_bgcolor='rgba(0,0,0,0)',margin=dict(t=40,b=10,l=20,r=20))
        st.plotly_chart(fig,use_container_width=True)
    with col_b:
        st.write("**Top predictive terms**")
        terms=['waiting','blocked','team','weeks','blocking','dependency','needs','bug']
        imps2=[0.039,0.035,0.033,0.020,0.017,0.009,0.009,0.008]
        fig2=go.Figure(go.Bar(x=imps2,y=terms,orientation='h',
            marker_color=['#e74c3c' if i>0.02 else '#3498db' for i in imps2],
            text=[f"{i:.3f}" for i in imps2],textposition='outside'))
        fig2.update_layout(height=280,paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)',margin=dict(t=10,b=20,l=20,r=20))
        st.plotly_chart(fig2,use_container_width=True)
    st.write("**Random Forest + TF-IDF | 203 synthetic examples | F1: 0.799**")

# ════════════════════════════════════════════════════════
elif page == "🔗 Pillar 3: Dependency Graph":
    st.subheader("Cross-Team Dependency Graph & Tape-out Readiness")

    # Action panel
    st.markdown("""<div style='background:#fde8e8;border-left:4px solid #e74c3c;
    padding:12px 16px;border-radius:4px;margin-bottom:16px'>
    <b>🔴 2 Critical Gates Identified</b><br>
    🔒 <b>RTL Design → DFT</b>: DFT is GATED on RTL freeze. 12-day accumulated delay.<br>
    🔒 <b>Physical Design → Timing Closure</b>: Timing Closure GATED on PD completion. 4-day delay.
    </div>""", unsafe_allow_html=True)

    node_pos={
        "Architecture":(0,2),"RTL Design":(1,2),"DV":(2,3),
        "DFT":(2,1),"Synthesis":(2,2),"Physical Design":(3,2),
        "Timing Closure":(4,3),"DRC/LVS":(4,1),"Tape-out":(5,2),
    }
    node_pct={"Architecture":100,"RTL Design":85,"DV":72,"DFT":45,
              "Synthesis":60,"Physical Design":50,"Timing Closure":30,"DRC/LVS":20,"Tape-out":0}
    edges=[
        ("Architecture","RTL Design",0,"green",False),
        ("Architecture","DFT",5,"amber",False),
        ("RTL Design","DV",3,"amber",False),
        ("RTL Design","DFT",12,"red",True),
        ("RTL Design","Synthesis",2,"amber",False),
        ("DV","Tape-out",3,"amber",False),
        ("DFT","Tape-out",12,"red",True),
        ("Synthesis","Physical Design",2,"amber",False),
        ("Physical Design","Timing Closure",4,"red",True),
        ("Physical Design","DRC/LVS",4,"amber",False),
        ("Timing Closure","Tape-out",4,"amber",False),
        ("DRC/LVS","Tape-out",4,"amber",False),
    ]
    cmap={"green":"#2ecc71","amber":"#f39c12","red":"#e74c3c"}
    edge_traces=[]
    for n1,n2,delay,status,gated in edges:
        x0,y0=node_pos[n1]; x1,y1=node_pos[n2]
        lbl=f"{'🔒 GATED — ' if gated else ''}{n1}→{n2}: +{delay}d"
        edge_traces.append(go.Scatter(x=[x0,x1,None],y=[y0,y1,None],mode='lines',
            line=dict(width=5 if status=="red" else 2,color=cmap[status]),
            hoverinfo='text',text=lbl,showlegend=False))
        if gated:
            mx,my=(x0+x1)/2,(y0+y1)/2
            edge_traces.append(go.Scatter(x=[mx],y=[my],mode='text',
                text=['🔒'],textfont=dict(size=16),showlegend=False,hoverinfo='skip'))

    node_colors=['#2ecc71' if node_pct[n]>=80 else '#f39c12' if node_pct[n]>=50
                 else '#e74c3c' for n in node_pos]
    node_trace=go.Scatter(
        x=[node_pos[n][0] for n in node_pos],
        y=[node_pos[n][1] for n in node_pos],
        mode='markers+text',text=list(node_pos.keys()),textposition="top center",
        textfont=dict(size=10,color='#1a1a1a'),
        marker=dict(size=38,color=node_colors,line=dict(width=2,color='white')),
        hovertext=[f"{n}: {node_pct[n]}% complete" for n in node_pos],
        hoverinfo='text',showlegend=False)
    fig=go.Figure(data=edge_traces+[node_trace])
    fig.update_layout(height=420,xaxis=dict(visible=False,range=[-0.5,5.8]),
                      yaxis=dict(visible=False,range=[0.3,3.8]),
                      paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='white',
                      margin=dict(t=10,b=10,l=10,r=10),hovermode='closest')
    st.plotly_chart(fig,use_container_width=True)
    st.caption("🟢 ≥80% complete  🟡 50–79%  🔴 <50%  |  🔒 = GATED dependency  |  Thick red = critical delay")

    st.divider()
    ca,cb,cc,cd=st.columns(4)
    ca.markdown(f"**DV Coverage**\n### {p3_scores['dv_score']}/30")
    cb.markdown(f"**DFT Sign-off**\n### {p3_scores['dft_score']}/25")
    cc.markdown(f"**Dependency Health**\n### {p3_scores['dep_score']}/25")
    cd.markdown(f"**DRC/LVS**\n### {p3_scores['drc_score']}/20")

    fig2=go.Figure(go.Indicator(mode="gauge+number",value=p3_scores['total'],
        title={'text':"Composite Tape-out Readiness Score"},
        gauge={'axis':{'range':[0,100]},'bar':{'color':'#e74c3c'},
               'steps':[{'range':[0,60],'color':'#fde8e8'},
                        {'range':[60,80],'color':'#fdf0dc'},
                        {'range':[80,100],'color':'#dff0e4'}]}))
    fig2.update_layout(height=300,paper_bgcolor='rgba(0,0,0,0)',margin=dict(t=60,b=10,l=30,r=30))
    st.plotly_chart(fig2,use_container_width=True)

elif page == "🧪 Joint Results (Ablation)":
    st.header("Joint Model vs Single Pillars")
    st.caption("Temporal split: train pre-freeze, test post-freeze (freeze = median date, assumed). 43 post-freeze defects.")
    ab = pd.DataFrame({
        "Feature set":["P1 only","P2 only","P3 only","P1+P2","P1+P3","P2+P3","Joint P1+P2+P3"],
        "Average precision":[0.285,0.134,0.221,0.213,0.288,0.146,0.222]})
    ab = ab.dropna()
    fig = px.bar(ab, x="Feature set", y="Average precision", text="Average precision", color="Average precision", color_continuous_scale="Blues")
    fig.add_hline(y=0.17, line_dash="dot", annotation_text="Chance = 0.17")
    fig.update_layout(height=380, paper_bgcolor='rgba(0,0,0,0)', coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)
    c1,c2,c3 = st.columns(3)
    c1.metric("Best single (P1)","0.285")
    c2.metric("Joint","0.222")
    c3.metric("Defect F1 (baseline)","0.25")
    st.info("Honest finding: the joint model did not beat P1 alone. P2 was trained on synthetic data, so it transfers poorly to real GitHub comments. Wide CIs; small sample.")

st.divider()
st.caption("ChipSentinel MTP 2 | IIT Jodhpur | Supervised by Dr. Binod Kumar")
