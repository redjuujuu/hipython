import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Telco Churn Story Dashboard",
    page_icon="📶",
    layout="wide"
)



from utils import (
    load_data, apply_filters,
    inject_style, apply_plotly_theme,
    render_top_logo, render_sidebar_logo_fixed
)

inject_style()
apply_plotly_theme()

render_sidebar_logo_fixed("assets/logo.png", link_to="./", max_width_px=280, top_px=10, nav_pad_px=160)



# ✅ 4) 로고 렌더 (파일 경로는 실제 있는지 확인)
render_top_logo("assets/logo.png", "Telco_dashboard")




st.markdown("""
<style>
.main .block-container{ padding-top: 6rem !important; padding-bottom: 2rem !important; }
header[data-testid="stHeader"]{ height: 3.2rem !important; }
h1{ padding-top: 0.2rem !important; margin-top: 0.2rem !important; line-height: 1.15 !important; }
</style>
""", unsafe_allow_html=True)

# ✅ Plotly 기본 템플릿
pio.templates.default = "plotly_white"

INTERNET_COLOR_MAP = {
    "DSL": "#9ED0FF",
    "Fiber optic": "#A7E8D6",
    "No": "#C7B3FF"
}
CONTRACT_COLOR_MAP = {
    "Month-to-month": "#FFD6A5",
    "One year": "#9ED0FF",
    "Two year": "#A7E8D6"
}

# ----------------------------
# 1) 데이터 로드 (원본 저장)
# ----------------------------
@st.cache_data
def get_df():
    return load_data()

df = get_df()
st.session_state["df_raw"] = df  # ✅ 여기 딱 1번만!

# ChurnFlag 없으면 생성
if "ChurnFlag" not in df.columns:
    df["ChurnFlag"] = (df["Churn"] == "Yes").astype(int)

# ----------------------------
# 2) 사이드바 필터
# ----------------------------
st.sidebar.markdown("### 🎛️ Control Center")




tenure_min = int(df["tenure"].min())
tenure_max = int(df["tenure"].max())
tenure_range = st.sidebar.slider("Tenure (months)", tenure_min, tenure_max, (tenure_min, tenure_max))

contracts_all = sorted(df["Contract"].dropna().unique().tolist())
internet_all = sorted(df["InternetService"].dropna().unique().tolist())
pay_all = sorted(df["PaymentMethod"].dropna().unique().tolist())

contracts = st.sidebar.multiselect("Contract", contracts_all, default=contracts_all)
internet_services = st.sidebar.multiselect("InternetService", internet_all, default=internet_all)
payment_methods = st.sidebar.multiselect("PaymentMethod", pay_all, default=pay_all)

include_unknown = st.sidebar.toggle("Include Unknown (Missing)", value=True)

filtered = apply_filters(df, tenure_range, contracts, internet_services, payment_methods, include_unknown)

# ✅ 전역 공유(모든 pages가 이걸 씀)
st.session_state["df_filtered"] = filtered
st.session_state["filters"] = {
    "tenure_range": tenure_range,
    "contracts": contracts,
    "internet_services": internet_services,
    "payment_methods": payment_methods,
    "include_unknown": include_unknown
}

st.sidebar.markdown("---")
st.sidebar.caption("✅ Filters apply to all pages.")

# ----------------------------
# 3) 메인(Overview 내용은 pages/1_Overview.py로 옮기는 게 베스트)
#    지금은 app.py는 '랜딩' 정도만
# ----------------------------
st.markdown(
    '<div class="fadein"><div class="h1">Overview</div>'
    '<div class="sub">왼쪽 Control Center에서 필터를 바꿔가며 페이지별 분석을 확인하세요.</div></div>',
    unsafe_allow_html=True
)

df_view = st.session_state["df_filtered"]

# ---- KPI: Customers / Churn rate (Count-up) ----
n = int(len(df_view))
cr = float(df_view["ChurnFlag"].mean() * 100) if n > 0 else 0.0

kpi_html = f"""
<div class="card fadein" style="display:flex; gap:18px; align-items:center; margin-top:10px;">
  <div style="flex:1;">
    <div style="font-size:12px; color:#6b6b6b;">Customers (filtered)</div>
    <div id="kpi_n" style="font-size:34px; font-weight:900; letter-spacing:-0.3px;">0</div>
  </div>
  <div style="flex:1;">
    <div style="font-size:12px; color:#6b6b6b;">Churn rate</div>
    <div id="kpi_cr" style="font-size:34px; font-weight:900; letter-spacing:-0.3px;">0%</div>
  </div>
</div>

<script>
function animateNumber(id, start, end, duration, isPercent=false) {{
  const el = document.getElementById(id);
  const startTime = performance.now();
  function step(now) {{
    const t = Math.min((now - startTime) / duration, 1);
    const v = start + (end - start) * t;
    if (isPercent) {{
      el.textContent = v.toFixed(1) + "%";
    }} else {{
      el.textContent = Math.floor(v).toLocaleString();
    }}
    if (t < 1) requestAnimationFrame(step);
  }}
  requestAnimationFrame(step);
}}
animateNumber("kpi_n", 0, {n}, 650, false);
animateNumber("kpi_cr", 0, {cr}, 850, true);
</script>
"""

components.html(kpi_html, height=120)


df_view = st.session_state["df_filtered"]

c1, c2 = st.columns(2)
with c1:
    tmp = df_view.groupby("InternetService", dropna=False)["ChurnFlag"].mean().mul(100).reset_index(name="churn_rate")
    fig = px.bar(
        tmp, x="InternetService", y="churn_rate", text=tmp["churn_rate"].round(1),
        color="InternetService", color_discrete_map=INTERNET_COLOR_MAP,
        title="Churn rate by InternetService"
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    tmp = df_view.groupby("Contract", dropna=False)["ChurnFlag"].mean().mul(100).reset_index(name="churn_rate")
    fig = px.bar(
        tmp, x="Contract", y="churn_rate", text=tmp["churn_rate"].round(1),
        color="Contract", color_discrete_map=CONTRACT_COLOR_MAP,
        title="Churn rate by Contract"
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig, use_container_width=True)
