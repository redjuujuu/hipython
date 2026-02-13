import streamlit as st
import pandas as pd

from utils import (
    load_data, apply_filters,
    inject_style, apply_plotly_theme,
    render_top_logo, render_sidebar_logo_fixed
)

inject_style()
apply_plotly_theme()

render_sidebar_logo_fixed("assets/logo.png", link_to="./", max_width_px=280, top_px=10, nav_pad_px=160)



# ✅ 3) 공통 스타일/테마는 1번만


# ✅ 4) 로고 렌더 (파일 경로는 실제 있는지 확인)
render_top_logo("assets/logo.png", "Telco_dashboard")

# ✅ 5) 로고에 그림자 같은 CSS는 'style 태그'로

import streamlit as st

# ✅ Playbook 페이지에서만 위쪽 여백 추가
st.markdown("""
<style>
/* ✅ Playbook: 메인 컨텐츠 위/좌/우 여백 확보 */
section.main > div.block-container,
[data-testid="stAppViewContainer"] .main .block-container,
.stApp .main .block-container{
  padding-top: 6.8rem !important;     /* 위 여백 */
  padding-left: 4.2rem !important;    /* 좌 여백 */
  padding-right: 4.2rem !important;   /* 우 여백 */
  padding-bottom: 2.4rem !important;
}

/* ✅ 화면 작아지면 좌우 여백 자동 축소 */
@media (max-width: 1200px){
  section.main > div.block-container,
  [data-testid="stAppViewContainer"] .main .block-container,
  .stApp .main .block-container{
    padding-left: 2.0rem !important;
    padding-right: 2.0rem !important;
  }
}
@media (max-width: 700px){
  section.main > div.block-container,
  [data-testid="stAppViewContainer"] .main .block-container,
  .stApp .main .block-container{
    padding-left: 1.0rem !important;
    padding-right: 1.0rem !important;
  }
}
</style>
""", unsafe_allow_html=True)




st.markdown("""
<style>
.telco-logo-img{
  filter: drop-shadow(0 10px 18px rgba(0,0,0,0.18));
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 1) df 가져오기 (없으면 안전하게 생성)
# -----------------------------
df = st.session_state.get("df_filtered")

if df is None:
    # app.py를 안 거치고 Playbook만 단독 실행될 때 대비
    df_raw = st.session_state.get("df_raw")
    if df_raw is None:
        df_raw = load_data()
        st.session_state["df_raw"] = df_raw

    # 필터 정보가 있으면 그걸로, 없으면 전체 범위로
    filters = st.session_state.get("filters", {})
    tenure_range = filters.get("tenure_range", (int(df_raw["tenure"].min()), int(df_raw["tenure"].max())))
    contracts = filters.get("contracts", sorted(df_raw["Contract"].dropna().unique().tolist()))
    internet_services = filters.get("internet_services", sorted(df_raw["InternetService"].dropna().unique().tolist()))
    payment_methods = filters.get("payment_methods", sorted(df_raw["PaymentMethod"].dropna().unique().tolist()))
    include_unknown = filters.get("include_unknown", True)

    df = apply_filters(df_raw, tenure_range, contracts, internet_services, payment_methods, include_unknown)
    st.session_state["df_filtered"] = df

df = df.copy()

# ChurnFlag 없으면 생성 (안전)
if "ChurnFlag" not in df.columns:
    df["ChurnFlag"] = (df["Churn"] == "Yes").astype(int)

# -----------------------------
# 2) Target segment builder (옵션도 안전하게)
# -----------------------------
st.markdown("### 🎯 Target segment builder")
c1, c2, c3 = st.columns(3)

internet_options = ["Fiber optic", "DSL", "No"]
contract_options = sorted(df["Contract"].dropna().unique().tolist()) if "Contract" in df.columns else []
tenure_options = ["0–6", "7–12", "13–24", "25–48", "49+"]

with c1:
    internet = st.selectbox("InternetService", internet_options, index=0)

with c2:
    if len(contract_options) == 0:
        st.warning("Contract 컬럼/값이 없어서 선택할 수 없어요.")
        st.stop()
    contract = st.selectbox("Contract", contract_options, index=0)

with c3:
    tenure_band = st.selectbox("Tenure band", tenure_options, index=0)

def band_filter(d):
    if tenure_band=="0–6":   return d[d["tenure"].between(0,6)]
    if tenure_band=="7–12":  return d[d["tenure"].between(7,12)]
    if tenure_band=="13–24": return d[d["tenure"].between(13,24)]
    if tenure_band=="25–48": return d[d["tenure"].between(25,48)]
    return d[d["tenure"]>=49]

seg = df[(df["InternetService"]==internet) & (df["Contract"]==contract)]
seg = band_filter(seg)

seg_n = len(seg)
seg_churn = round(seg["ChurnFlag"].mean()*100, 1) if seg_n else None
st.markdown(f"<div class='card fadein'><b>Segment size</b>: {seg_n:,} &nbsp;&nbsp; "
            f"<b>Churn rate</b>: {seg_churn if seg_churn is not None else 'NA'}%</div>", unsafe_allow_html=True)

st.markdown("### 🧾 Proposed offers")
discount = st.slider("Discount (Month-to-month → 1Y/2Y conversion)", 0, 20, 10, 1)
bundle_os = st.checkbox("Bundle: OnlineSecurity free (limited 기간)", value=True)
bundle_ts = st.checkbox("Bundle: TechSupport trial (limited 기간)", value=True)

st.markdown('<div class="card fadein"><b>제안</b><br>'
            f'- 월단위 고객이 1년 이상 계약으로 전환 시 <b>{discount}%</b> 할인(한정 기간/조건부) 제공<br>'
            f'- 전환 고객에게 OnlineSecurity/TechSupport를 “무제한 무료”가 아닌 <b>기간/횟수 한도형</b>으로 제공해 가치 체감 강화<br>'
            '</div>', unsafe_allow_html=True)

st.markdown("### ✅ 핵심 지표 ")
core_metrics = pd.DataFrame([
    {"핵심 지표": "Conversion rate (Month→1Y/2Y)", "Why": "락인으로 churn 구조를 낮춤"},
    {"핵심 지표": "0–6 months churn rate", "Why": "초기 방어 성과를 바로 확인"},
    {"핵심 지표": "Auto-pay adoption rate", "Why": "결제 마찰(전자수표) 리스크 완화"},
    {"핵심 지표": "ARPU / Margin guardrail", "Why": "할인으로 수익 훼손 방지"},
    {"핵심 지표": "Support ticket resolution time", "Why": "품질/지원 체감 개선 측정"},
])
st.dataframe(core_metrics, use_container_width=True)