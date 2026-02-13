import streamlit as st
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

# ✅ 팔레트(핑크 제외)
PASTEL_NO_PINK = ["#9ED0FF", "#A7E8D6", "#C7B3FF", "#FFD6A5", "#D8F3DC"]

# ✅ Churn 색 고정(파스텔 블루 / 파스텔 오렌지)
CHURN_MAP = {"No": "#9ED0FF", "Yes": "#FFD6A5"}

# ✅ df 가져오기: filtered 없으면 raw로 fallback + None 방어
df = st.session_state.get("df_filtered")
if df is None:
    df = st.session_state.get("df_raw")

st.markdown(
    '<div class="fadein"><div class="h1">Internet & Price</div>'
    '<div class="sub">막대 대신 분포(violin)로 “가격 민감”을 보여주기</div></div>',
    unsafe_allow_html=True
)

# ✅ df가 없거나 비어있으면 여기서 종료(에러 대신 친절한 안내)
if df is None or len(df) == 0:
    st.error("데이터(df)가 비어있어요. app.py에서 st.session_state['df_raw'], ['df_filtered']가 먼저 세팅되는지 확인해줘.")
    st.stop()

# ─────────────────────────────────────────────
# 1) Violin: MonthlyCharges 분포(InternetService × Churn)
# ─────────────────────────────────────────────
fig = px.violin(
    data_frame=df,                 # ✅ 핵심: df를 data_frame으로 명시
    x="InternetService",
    y="MonthlyCharges",
    color="Churn",
    box=True,
    points="all",
    color_discrete_map=CHURN_MAP,  # ✅ 색 고정 적용
    title="MonthlyCharges distribution by InternetService & Churn",
)

fig.update_layout(
    margin=dict(l=10, r=10, t=60, b=40),
    legend_title_text="Churn"
)
st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────
# 2) Scatter: tenure vs MonthlyCharges (Churn 색)
# ─────────────────────────────────────────────
fig2 = px.scatter(
    data_frame=df,                 # ✅ 동일하게 data_frame 명시
    x="tenure",
    y="MonthlyCharges",
    color="Churn",
    opacity=0.6,
    color_discrete_map=CHURN_MAP,  # ✅ 색 고정 적용
    title="Tenure vs MonthlyCharges (colored by Churn)",
)

fig2.update_layout(
    margin=dict(l=10, r=10, t=60, b=40),
    legend_title_text="Churn"
)
st.plotly_chart(fig2, use_container_width=True)
