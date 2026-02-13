import streamlit as st
import pandas as pd
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

PASTEL_NO_PINK = ["#9ED0FF", "#A7E8D6", "#C7B3FF", "#FFD6A5", "#D8F3DC"]
CHURN_MAP = {"No": "#9ED0FF", "Yes": "#FFD6A5"}  # 파랑/주황 파스텔


df = st.session_state.get("df_filtered")

st.markdown('<div class="fadein"><div class="h1">Add-on Value</div><div class="sub">보안/지원/스트리밍이 유지와 어떻게 연결되는지</div></div>', unsafe_allow_html=True)

LONG_TENURE = st.slider("Long-tenure threshold (months)", 12, 72, 49, 1)

fiber_long = df[(df["InternetService"]=="Fiber optic") & (df["tenure"]>=LONG_TENURE)]
keep = fiber_long[fiber_long["Churn"]=="No"]
churn = fiber_long[fiber_long["Churn"]=="Yes"]

def yes_rate(d, col):
    if len(d)==0:
        return None
    return round((d[col]=="Yes").mean()*100, 1)

service_cols = ["TechSupport","OnlineSecurity","StreamingTV","StreamingMovies"]
rows = []
for col in service_cols:
    if col in fiber_long.columns:
        rows.append({
            "Feature": col,
            "Keep (Churn=No)": yes_rate(keep, col),
            "Churn (Churn=Yes)": yes_rate(churn, col),
        })

service_compare = pd.DataFrame(rows)
st.dataframe(service_compare, use_container_width=True)

plot_df = service_compare.melt("Feature", var_name="Group", value_name="YesRate")

fig = px.bar(
    plot_df, x="Feature", y="YesRate", color="Group", barmode="group",
    text="YesRate",
    title=f"Yes-rate comparison in Fiber long customers (tenure ≥ {LONG_TENURE})"
)
fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
fig.update_yaxes(title="Yes rate (%)")
fig.update_layout(xaxis_title="", margin=dict(l=10,r=10,t=40,b=10))
st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="card fadein" style="margin-top:12px;">'
            '<b>So what</b><br>'
            '스트리밍 가입이 높다고 “혜택 강화”로만 가면 역효과가 날 수 있어요. 스트리밍은 품질 민감 고객 신호일 수 있으니, '
            '<b>TechSupport/OnlineSecurity와 결합</b>해 “품질 보장 + 문제 해결” 메시지로 설득력을 올리는 쪽이 좋습니다.'
            '</div>', unsafe_allow_html=True)