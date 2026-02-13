import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from utils import (
    load_data, apply_filters,
    inject_style, apply_plotly_theme,
    render_top_logo, render_sidebar_logo_fixed
)

inject_style()
apply_plotly_theme()

render_sidebar_logo_fixed("assets/logo.png", link_to="./", max_width_px=280, top_px=10, nav_pad_px=160)


# ✅ 3) 공통 스타일/테마는 1번만
inject_style()
apply_plotly_theme()



# ✅ 4) 로고 렌더 (파일 경로는 실제 있는지 확인)
render_top_logo("assets/logo.png", "Telco_dashboard")

# ✅ 5) 로고에 그림자 같은 CSS는 'style 태그'로
st.markdown("""
<style>
.telco-logo-img{
  filter: drop-shadow(0 10px 18px rgba(0,0,0,0.18));
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# 0) 데이터 가져오기 (필터 적용본 우선)
# ----------------------------
df = st.session_state.get("df_filtered")
if df is None:
    # df_filtered가 아직 없으면 원본 df를 가져오도록(너 app.py에서 df를 session_state에 넣어둬야 함)
    df = st.session_state.get("df_raw")
    if df is None:
        st.error("df_filtered / df_raw가 없습니다. app.py에서 데이터를 st.session_state['df_raw']에 저장해주세요.")
        st.stop()

df = df.copy()

# ChurnFlag 없으면 생성 (Yes=1, No=0)
if "ChurnFlag" not in df.columns:
    df["ChurnFlag"] = (df["Churn"] == "Yes").astype(int)

# ----------------------------
# 1) 페이지 헤더
# ----------------------------
st.markdown(
    '<div class="fadein"><div class="h1">Early Churn (0–6)</div>'
    '<div class="sub">초기 이탈 구간을 통제 비교로 검증</div></div>',
    unsafe_allow_html=True
)

# ----------------------------
# 2) 초기이탈 세그먼트 테이블 만들기
# ----------------------------
fiber = df[df["InternetService"] == "Fiber optic"]
dsl   = df[df["InternetService"] == "DSL"]

def churn_rate_tbl(d, label):
    if len(d) == 0:
        return {"segment": label, "n": 0, "churn_rate_%": np.nan}
    return {
        "segment": label,
        "n": len(d),
        "churn_rate_%": round(d["ChurnFlag"].mean() * 100, 1)
    }

fiber_0_6 = fiber[fiber["tenure"].between(0, 6)]
dsl_0_6   = dsl[dsl["tenure"].between(0, 6)]

fiber_mm_0_6 = fiber[(fiber["Contract"] == "Month-to-month") & (fiber["tenure"].between(0, 6))]
dsl_mm_0_6   = dsl[(dsl["Contract"] == "Month-to-month") & (dsl["tenure"].between(0, 6))]

initial_tbl = pd.DataFrame([
    churn_rate_tbl(fiber_0_6, "Fiber optic (tenure 0–6)"),
    churn_rate_tbl(dsl_0_6, "DSL (tenure 0–6)"),
    churn_rate_tbl(fiber_mm_0_6, "Fiber optic (Month-to-month & 0–6)"),
    churn_rate_tbl(dsl_mm_0_6, "DSL (Month-to-month & 0–6)"),
])

st.dataframe(initial_tbl, use_container_width=True)

# ----------------------------
# 3) 시각화(4색, 핑크/하늘 제외)
# ----------------------------
plot_tbl = initial_tbl.copy()
plot_tbl["segment_wrapped"] = (
    plot_tbl["segment"]
    .str.replace(" (", "<br>(", regex=False)
    .str.replace(" & ", "<br>&<br>", regex=False)
)

fig = px.bar(
    plot_tbl,
    x="segment_wrapped",
    y="churn_rate_%",
    text="churn_rate_%",
    color="segment_wrapped",
    # ✅ 핑크/하늘 제외한 파스텔 4색
    color_discrete_sequence=["#A7E8D6", "#C7B3FF", "#FFD6A5", "#D8F3DC"],
    title="Initial churn comparison (0–6 months)",
)

fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
fig.update_yaxes(title="Churn rate (%)", range=[0, max(5, plot_tbl["churn_rate_%"].max() + 10)])
fig.update_layout(
    showlegend=False,
    margin=dict(l=10, r=10, t=60, b=140),
    xaxis_title="",
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# 4) 해석 카드
# ----------------------------
st.markdown(
    '<div class="card fadein" style="margin-top:12px;">'
    '<b>Interpretation</b><br>'
    '월단위 계약(Contract)을 통제한 상태에서도 Fiber/DSL의 초기 이탈 차이가 유지되는지 확인하면, '
    '기술(서비스) 요인인지 가격/계약 구조 요인인지 더 명확해집니다.'
    '</div>',
    unsafe_allow_html=True
)
