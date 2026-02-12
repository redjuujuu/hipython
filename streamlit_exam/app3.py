import streamlit as st

# layout 요소 2

# st.sidebar.radio(
#     "이동",
#     ["메인페이지", "분석보고서", "설정"]

# )

# st.sidebar.metric('접속자수:', '백만명', "+백만명")

if st.sidebar.button('눌러봐!!!'):
    st.balloons()


#바이브를 위한 프롬프트
#파이썬 스트림릿 대시보드를 만들어주세요.
#아래의 구조를 실행가능한 파이썬 코드로 완성하세요
#기본구성
#페이지 제목 표시, 이미지 1장 넣기
#사이드바는 컨트롤 센터로 지정 - 이동 대신에 컨트롤센터
#사이드바에 메뉴이동 라디오버튼 (메인페이지, 분석보고서, 설정)
#메인페이지
# 2개의 컬럼으로 kpi 대시보드 구성
# 방문자수, 활성 사용자수를 메트릭 카드로 구성
# 분석페이지
#탭으로 구성(차트/데이터/설정)
# 차트탭에는 간단한 사용자 방문현황 그래프
# 데이터탭에는 데이터 테이블 출력
# 설정 탭에는 연결시 옵션 체크박스
#추가요구사항
#streamlit 함수 : 기발하고 예쁜 것 위주로 적용
#코드 전체를 한번에 출력
# 꼭 실행가능한 코드여야 함

#streamlit run app3.py




# import streamlit as st
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from datetime import datetime, timedelta

# # -----------------------------
# # 0) 페이지 기본 설정
# # -----------------------------
# st.set_page_config(
#     page_title="Mini Dashboard",
#     page_icon="📊",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # -----------------------------
# # 1) 간단한 더미 데이터 생성 (실데이터로 교체 가능)
# # -----------------------------
# @st.cache_data
# def make_demo_data(days: int = 30) -> pd.DataFrame:
#     rng = np.random.default_rng(42)
#     dates = [datetime.today().date() - timedelta(days=i) for i in range(days)][::-1]
#     visits = np.maximum(0, np.cumsum(rng.normal(0, 8, size=days)) + 120).round().astype(int)
#     active = np.maximum(0, (visits * rng.uniform(0.35, 0.65, size=days))).round().astype(int)

#     df = pd.DataFrame({
#         "date": dates,
#         "visits": visits,
#         "active_users": active
#     })
#     return df

# df = make_demo_data(30)

# # 최신/이전 값(델타용)
# visits_now = int(df["visits"].iloc[-1])
# visits_prev = int(df["visits"].iloc[-2])
# active_now = int(df["active_users"].iloc[-1])
# active_prev = int(df["active_users"].iloc[-2])

# # -----------------------------
# # 2) 사이드바: 컨트롤 센터
# # -----------------------------
# st.sidebar.title("🕹️ 컨트롤 센터")
# page = st.sidebar.radio(
#     "메뉴 이동",
#     ["메인페이지", "분석보고서", "설정"],
#     horizontal=False
# )

# st.sidebar.divider()
# st.sidebar.caption("옵션(예시)")
# date_window = st.sidebar.slider("분석 기간(일)", min_value=7, max_value=60, value=30, step=1)
# show_raw = st.sidebar.toggle("원본 데이터 보기", value=False)

# # 선택된 기간으로 데이터 자르기
# df_view = df.tail(date_window).reset_index(drop=True)

# # -----------------------------
# # 3) 상단: 제목 + 이미지 1장
# # -----------------------------
# st.title("📊 파이썬 Streamlit 미니 대시보드")

# # 이미지: 외부 URL (실무에서 안정적으로 바로 보이게)
# st.image(
#     "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1400&q=60",
#     caption="Dashboard Preview Image",
#     use_container_width=True
# )

# # 예쁜 구분선
# st.divider()

# # -----------------------------
# # 4) 페이지별 UI
# # -----------------------------
# if page == "메인페이지":
#     st.subheader("📌 KPI 대시보드")

#     # 2개의 컬럼 KPI 카드
#     col1, col2 = st.columns(2, gap="large")

#     with col1:
#         st.metric(
#             label="방문자수",
#             value=f"{visits_now:,}",
#             delta=f"{visits_now - visits_prev:+,}",
#             delta_color="normal"  # 증가=초록, 감소=빨강
#         )

#     with col2:
#         st.metric(
#             label="활성 사용자수",
#             value=f"{active_now:,}",
#             delta=f"{active_now - active_prev:+,}",
#             delta_color="normal"
#         )

#     # 추가로 예쁜 요소(상태 메시지 + 진행률 느낌)
#     st.success("✅ 시스템 상태: 정상 동작 중")
#     ratio = (active_now / visits_now) if visits_now else 0
#     st.progress(min(max(ratio, 0), 1.0), text=f"활성/방문 비율: {ratio:.1%}")

#     if show_raw:
#         st.divider()
#         st.caption("원본 데이터(최근 기간)")
#         st.dataframe(df_view, use_container_width=True, hide_index=True)

# elif page == "분석보고서":
#     st.subheader("📈 분석 보고서")

#     tab_chart, tab_data, tab_setting = st.tabs(["차트", "데이터", "설정"])

#     with tab_chart:
#         st.caption("최근 방문/활성 사용자 추이")

#         # Matplotlib 간단 그래프 (streamlit에 안정적)
#         fig = plt.figure(figsize=(9, 4))
#         plt.plot(df_view["date"], df_view["visits"], marker="o", linewidth=1.5, label="Visits")
#         plt.plot(df_view["date"], df_view["active_users"], marker="o", linewidth=1.5, label="Active Users")
#         plt.xticks(rotation=45)
#         plt.xlabel("Date")
#         plt.ylabel("Count")
#         plt.legend()
#         plt.tight_layout()
#         st.pyplot(fig, use_container_width=True)

#         # 작은 인사이트 박스
#         st.info(
#             f"최근 {date_window}일 기준: 방문자수 평균 {df_view['visits'].mean():.1f}, "
#             f"활성 사용자 평균 {df_view['active_users'].mean():.1f}"
#         )

#     with tab_data:
#         st.caption("데이터 테이블")
#         st.dataframe(df_view, use_container_width=True, hide_index=True)

#         # 다운로드 버튼(예쁨 + 실무에서 자주 씀)
#         csv_bytes = df_view.to_csv(index=False).encode("utf-8-sig")
#         st.download_button(
#             label="⬇️ CSV 다운로드",
#             data=csv_bytes,
#             file_name="user_activity.csv",
#             mime="text/csv"
#         )

#     with tab_setting:
#         st.caption("연결/옵션 설정(예시)")

#         # 체크박스 옵션
#         enable_db = st.checkbox("DB 연결 사용", value=False)
#         enable_api = st.checkbox("외부 API 연동 사용", value=False)
#         enable_cache = st.checkbox("캐시 사용(성능 향상)", value=True)

#         st.divider()

#         # 설정 요약
#         st.write("현재 설정 요약")
#         st.json({
#             "DB 연결": enable_db,
#             "API 연동": enable_api,
#             "캐시 사용": enable_cache,
#             "분석 기간(일)": date_window
#         })

#         if enable_db or enable_api:
#             st.warning("⚠️ 실데이터 연결이 활성화되면 인증키/환경변수 관리가 필요합니다.")
#         else:
#             st.success("✅ 현재는 데모 데이터 모드입니다.")

# elif page == "설정":
#     st.subheader("⚙️ 설정")

#     st.write("대시보드 전반 설정을 관리하는 페이지(예시)입니다.")
#     theme = st.selectbox("테마 스타일(예시)", ["기본", "미니멀", "강조"], index=0)
#     refresh = st.number_input("자동 새로고침(초) - 0이면 비활성", min_value=0, max_value=3600, value=0, step=10)

#     st.divider()
#     st.write("설정 미리보기")
#     st.json({"테마": theme, "자동 새로고침(초)": int(refresh)})

#     st.toast("설정이 반영되었습니다(데모).", icon="✅")













import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# -----------------------------
# 0) 페이지 기본 설정
# -----------------------------
st.set_page_config(
    page_title="🍓 Baby Pink Mini Dashboard",
    page_icon="🍓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# 1) 파스텔 테마 CSS (베이비 핑크 + 민트 + 스카이)
# -----------------------------
THEME_CSS = """
<style>
/* 폰트 (가독성 좋은 Pretendard 계열 + 대체 폰트) */
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;800&display=swap');

:root{
  --pink-50:#FFF5FA;
  --pink-100:#FFE3F1;
  --pink-200:#FFD0E7;

  --mint-100:#DFF7F1;
  --mint-200:#BFEDE2;

  --sky-100:#E6F4FF;
  --sky-200:#CFEAFF;

  --ink:#2B2B2B;
  --ink-soft:#4A4A4A;

  --card:#FFFFFFCC;
  --border:#F4C9DD;
  --shadow: 0 10px 25px rgba(0,0,0,.06);
  --radius: 22px;
}

/* 전체 배경 */
.stApp{
  font-family: "Nunito", -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
  color: var(--ink);
  background:
    radial-gradient(1200px 800px at 10% 10%, var(--pink-100), transparent 55%),
    radial-gradient(1000px 700px at 90% 15%, var(--sky-100), transparent 55%),
    radial-gradient(900px 600px at 20% 90%, var(--mint-100), transparent 55%),
    linear-gradient(180deg, var(--pink-50), #ffffff);
}

/* 사이드바 배경 */
section[data-testid="stSidebar"]{
  background: linear-gradient(180deg, var(--pink-100), var(--sky-100));
  border-right: 1px solid rgba(244,201,221,.7);
}
section[data-testid="stSidebar"] *{
  color: var(--ink);
}

/* 제목/캡션 가독성 */
h1, h2, h3 { color: var(--ink); }
.stCaption, .stMarkdown p, .stMarkdown span { color: var(--ink-soft); }

/* 공통 카드 */
.pastel-card{
  background: var(--card);
  border: 1px solid rgba(244,201,221,.85);
  box-shadow: var(--shadow);
  border-radius: var(--radius);
  padding: 18px 18px 12px 18px;
}

/* KPI 카드 전용 */
.kpi-title{
  font-weight: 800;
  letter-spacing: .2px;
  margin-bottom: 6px;
}
.kpi-sub{
  color: var(--ink-soft);
  font-size: 0.92rem;
  margin-top: -2px;
}

/* 버튼 예쁘게 */
.stButton > button{
  border-radius: 999px !important;
  border: 1px solid rgba(244,201,221,.95) !important;
  background: linear-gradient(90deg, var(--pink-200), var(--sky-200)) !important;
  color: var(--ink) !important;
  font-weight: 800 !important;
  padding: 0.55rem 1.1rem !important;
  box-shadow: 0 10px 18px rgba(0,0,0,.08) !important;
}
.stButton > button:hover{
  transform: translateY(-1px);
  filter: brightness(1.02);
}

/* 탭도 부드럽게 */
button[data-baseweb="tab"]{
  border-radius: 999px !important;
}

/* 데이터프레임 테두리 */
div[data-testid="stDataFrame"]{
  background: rgba(255,255,255,.6);
  border-radius: var(--radius);
  border: 1px solid rgba(244,201,221,.55);
  padding: 8px;
}
</style>
"""
st.markdown(THEME_CSS, unsafe_allow_html=True)

# -----------------------------
# 2) 데모 데이터 생성
# -----------------------------
@st.cache_data
def make_demo_data(days: int = 30) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    dates = [datetime.today().date() - timedelta(days=i) for i in range(days)][::-1]
    visits = np.maximum(0, (np.cumsum(rng.normal(0, 8, size=days)) + 220)).round().astype(int)
    active = np.maximum(0, (visits * rng.uniform(0.35, 0.70, size=days))).round().astype(int)

    # 방문 구성(채널 비율) 예시: organic / ads / referral
    organic = np.maximum(0, (visits * rng.uniform(0.45, 0.65, size=days))).round().astype(int)
    ads = np.maximum(0, (visits * rng.uniform(0.15, 0.35, size=days))).round().astype(int)
    referral = np.maximum(0, visits - organic - ads)

    return pd.DataFrame({
        "date": dates,
        "visits": visits,
        "active_users": active,
        "organic": organic,
        "ads": ads,
        "referral": referral,
    })

df = make_demo_data(60)

# -----------------------------
# 3) 사이드바: 컨트롤 센터
# -----------------------------
st.sidebar.title("🕹️ 컨트롤 센터")
page = st.sidebar.radio("메뉴 이동", ["메인페이지", "분석보고서", "설정"])

st.sidebar.divider()
days = st.sidebar.slider("분석 기간(일)", 7, 60, 30, 1)
show_table = st.sidebar.toggle("표(데이터) 바로 보기", value=False)

df_view = df.tail(days).reset_index(drop=True)

# -----------------------------
# 4) 상단: 제목 + 귀여운 통계 이미지 1장
# -----------------------------
st.markdown("## 🍓 환경/사용자 상태 미니 대시보드")
st.caption("베이비 핑크 톤으로 꾸민 Streamlit 데모 · KPI/차트/데이터/설정까지 한 번에")

# 귀엽고 통계 느낌 나는 이미지(외부 URL)
st.image(
    "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1400&q=60",
    caption="Cute-ish stats vibe (demo image)",
    use_container_width=True,
)

# 신기한 효과 버튼(상단)
c1, c2, c3, c4 = st.columns([1, 1, 1, 2], gap="small")
with c1:
    if st.button("🎈 풍선!"):
        st.balloons()
        st.toast("오늘도 데이터 귀엽게 뿌셔요 🍓", icon="✅")
with c2:
    if st.button("❄️ 눈!"):
        st.snow()
        st.toast("차분하게 분석 모드 ON", icon="❄️")
with c3:
    if st.button("✨ 반짝!"):
        st.toast("반짝반짝 KPI 업데이트 ✨", icon="✨")
with c4:
    st.caption("원하는 효과를 눌러보세요 (balloons/snow/toast)")

st.divider()

# -----------------------------
# 5) 공통 KPI 계산
# -----------------------------
visits_now = int(df_view["visits"].iloc[-1])
visits_prev = int(df_view["visits"].iloc[-2])
active_now = int(df_view["active_users"].iloc[-1])
active_prev = int(df_view["active_users"].iloc[-2])

active_ratio_now = (active_now / visits_now) if visits_now else 0.0
active_ratio_prev = (active_prev / visits_prev) if visits_prev else 0.0

# 방문 구성 비율(최근 하루)
org_now = int(df_view["organic"].iloc[-1])
ads_now = int(df_view["ads"].iloc[-1])
ref_now = int(df_view["referral"].iloc[-1])
total_now = max(org_now + ads_now + ref_now, 1)

org_pct = org_now / total_now
ads_pct = ads_now / total_now
ref_pct = ref_now / total_now

# -----------------------------
# 6) 페이지별 렌더링
# -----------------------------
if page == "메인페이지":
    st.markdown("### 📌 메인 KPI")

    # 2개의 컬럼 KPI 카드
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<div class="pastel-card">', unsafe_allow_html=True)
        st.markdown('<div class="kpi-title">👣 방문자수</div>', unsafe_allow_html=True)
        st.metric(
            label="",
            value=f"{visits_now:,}",
            delta=f"{visits_now - visits_prev:+,}",
            delta_color="normal"
        )
        st.markdown(
            f'<div class="kpi-sub">최근 방문 구성 비율 · Organic {org_pct:.0%} · Ads {ads_pct:.0%} · Referral {ref_pct:.0%}</div>',
            unsafe_allow_html=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="pastel-card">', unsafe_allow_html=True)
        st.markdown('<div class="kpi-title">🫧 활성 사용자수</div>', unsafe_allow_html=True)
        st.metric(
            label="",
            value=f"{active_now:,}",
            delta=f"{active_now - active_prev:+,}",
            delta_color="normal"
        )
        st.metric(
            label="활성/방문 비율",
            value=f"{active_ratio_now:.1%}",
            delta=f"{(active_ratio_now - active_ratio_prev):+.1%}",
            delta_color="normal"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # 예쁜 상태 박스 + 진행률
    st.markdown('<div class="pastel-card">', unsafe_allow_html=True)
    st.success("✅ 시스템 상태: 정상 · 데이터 로드 완료")
    st.progress(min(max(active_ratio_now, 0), 1), text=f"활성/방문 비율: {active_ratio_now:.1%}")
    st.markdown("</div>", unsafe_allow_html=True)

    if show_table:
        st.markdown("#### 📋 최근 데이터")
        st.dataframe(df_view[["date", "visits", "active_users", "organic", "ads", "referral"]],
                     use_container_width=True, hide_index=True)

elif page == "분석보고서":
    st.markdown("### 📈 분석 보고서")
    tab_chart, tab_data, tab_setting = st.tabs(["차트", "데이터", "설정"])

    with tab_chart:
        st.markdown('<div class="pastel-card">', unsafe_allow_html=True)
        st.caption("간단한 사용자 방문 현황 그래프")

        # Streamlit 내장 차트(간단/예쁨/빠름)
        chart_df = df_view.set_index("date")[["visits", "active_users"]]
        st.line_chart(chart_df, height=320)

        st.info(
            f"최근 {days}일 평균 방문자수 {df_view['visits'].mean():.1f}, "
            f"평균 활성 사용자수 {df_view['active_users'].mean():.1f}"
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # 신기한 UI: 팝오버(버튼 눌러서 추가 설명)
        with st.popover("🧁 인사이트 한 스푼"):
            st.write("- 방문자수 ↔ 활성 사용자수의 간극이 커지면 온보딩/리텐션 개선 포인트일 수 있어요.")
            st.write("- Ads 비중이 높아질수록 CAC 관리가 중요해져요.")
            st.write("- 금융권 서비스라면 ‘재방문/재이용’이 핵심 KPI로 연결됩니다.")

    with tab_data:
        st.markdown('<div class="pastel-card">', unsafe_allow_html=True)
        st.caption("데이터 테이블 출력")
        st.dataframe(df_view, use_container_width=True, hide_index=True)

        csv_bytes = df_view.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "⬇️ CSV 다운로드",
            data=csv_bytes,
            file_name="mini_dashboard_data.csv",
            mime="text/csv"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_setting:
        st.markdown('<div class="pastel-card">', unsafe_allow_html=True)
        st.caption("연결 시 옵션 체크박스")

        enable_db = st.checkbox("DB 연결 사용", value=False)
        enable_api = st.checkbox("외부 API 연동 사용", value=False)
        enable_cache = st.checkbox("캐시 사용(성능 향상)", value=True)

        st.divider()
        st.write("현재 설정 요약")
        st.json({
            "DB 연결": enable_db,
            "API 연동": enable_api,
            "캐시 사용": enable_cache,
            "분석 기간(일)": days
        })

        if enable_db or enable_api:
            st.warning("⚠️ 실데이터 연결 모드: 인증키/환경변수(.env) 관리가 필요합니다.")
        else:
            st.success("✅ 현재는 데모 데이터 모드입니다.")
        st.markdown("</div>", unsafe_allow_html=True)

elif page == "설정":
    st.markdown("### ⚙️ 설정")
    st.markdown('<div class="pastel-card">', unsafe_allow_html=True)

    theme_hint = st.selectbox("톤 선택(데모)", ["베이비 핑크 중심", "민트 중심", "스카이 블루 중심"], index=0)
    auto_refresh = st.number_input("자동 새로고침(초) - 0이면 비활성", 0, 3600, 0, 10)

    st.divider()
    st.write("설정 미리보기")
    st.json({"톤": theme_hint, "자동 새로고침(초)": int(auto_refresh)})

    # “신기한” 요소: 상태 컴포넌트(진행 표시)
    with st.status("설정 적용 중…", expanded=True) as status:
        st.write("UI 톤 점검")
        st.write("데이터 로딩 설정 점검")
        st.write("렌더링 최적화 점검")
        status.update(label="설정 적용 완료!", state="complete")

    st.toast("설정이 반영되었습니다(데모).", icon="✅")
    st.markdown("</div>", unsafe_allow_html=True)