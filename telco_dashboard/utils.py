import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.io as pio
from pathlib import Path

DATA_PATH = "data/cust_data_v1.csv"

# ---------------------------
# Data
# ---------------------------
def _clean_strings(df: pd.DataFrame) -> pd.DataFrame:
    obj_cols = df.select_dtypes(include="object").columns
    for c in obj_cols:
        df[c] = df[c].replace(r"^\s*$", np.nan, regex=True)
        df[c] = df[c].astype("string").str.strip()
    return df

def _coerce_totalcharges(df: pd.DataFrame) -> pd.DataFrame:
    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    return df

def _fill_internet_dependent(df: pd.DataFrame) -> pd.DataFrame:
    internet_dependent = [
        "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",
        "StreamingTV", "StreamingMovies"
    ]
    internet_dependent = [c for c in internet_dependent if c in df.columns]

    for c in internet_dependent:
        df.loc[df["InternetService"] == "No", c] = "No internet service"
        df[c] = df[c].fillna("Unknown")
    return df

@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df = _clean_strings(df)
    df = _coerce_totalcharges(df)
    df = _fill_internet_dependent(df)

    df["ChurnFlag"] = df["Churn"].map({"Yes": 1, "No": 0})
    df["InternetYN"] = np.where(df["InternetService"] == "No", "No", "Yes")
    return df

def apply_filters(df: pd.DataFrame,
                  tenure_range,
                  contracts,
                  internet_services,
                  payment_methods,
                  include_unknown=True) -> pd.DataFrame:
    d = df.copy()

    if "tenure" in d.columns and tenure_range:
        d = d[d["tenure"].between(tenure_range[0], tenure_range[1])]

    if contracts:
        d = d[d["Contract"].isin(contracts)]

    if internet_services:
        d = d[d["InternetService"].isin(internet_services)]

    if payment_methods:
        d = d[d["PaymentMethod"].isin(payment_methods)]

    d.attrs["include_unknown"] = include_unknown
    return d

def churn_rate(df: pd.DataFrame) -> float:
    if len(df) == 0:
        return float("nan")
    return round(df["ChurnFlag"].mean() * 100, 1)

def segment_size(df: pd.DataFrame) -> int:
    return int(len(df))

# ---------------------------
# Theme (Plotly)
# ---------------------------
PASTEL_SEQ = ["#9ED0FF", "#A7E8D6", "#C7B3FF", "#FFD6A5", "#D8F3DC"]  # 핑크 제외

def apply_plotly_theme():
    pio.templates.default = "plotly_white"
    px.defaults.template = "plotly_white"
    px.defaults.color_discrete_sequence = PASTEL_SEQ

# ---------------------------
# CSS
# ---------------------------
def inject_style():
    st.markdown("""
    <style>
    .stApp .main .block-container,
    section.main > div.block-container,
    [data-testid="stAppViewContainer"] .main .block-container{
        padding-top: 3.4rem !important;
        padding-bottom: 2.2rem !important;
    }

    header[data-testid="stHeader"]{
        background: transparent !important;
    }

    h1, .stMarkdown h1, [data-testid="stTitle"] h1{
        font-size: 40px !important;
        font-weight: 850 !important;
        line-height: 1.15 !important;
        margin-top: 0.2rem !important;
        margin-bottom: 0.8rem !important;
        padding-top: 0.2rem !important;
    }

    .h1{
        font-size: 40px !important;
        font-weight: 850 !important;
        line-height: 1.15 !important;
        margin: 0 0 6px 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------
# Logo: Top (main area)
# ---------------------------
def render_top_logo(img_path: str, title: str = "Telco_dashboard", subtitle: str = ""):
    import base64 as b64

    logo_file = Path(img_path)
    if not logo_file.exists():
        st.warning(f"Logo not found: {img_path}")
        return

    logo_b64 = b64.b64encode(logo_file.read_bytes()).decode("utf-8")
    sub_html = f'<div class="telco-top-sub">{subtitle}</div>' if subtitle else ""

    st.markdown(
        f"""
        <style>
          .telco-topbar {{
            display:flex; align-items:center; gap:16px;
            padding: 10px 6px 14px 6px;
          }}
          .telco-topbar img {{
            width: 68px; height:auto;
            filter: drop-shadow(0 10px 18px rgba(0,0,0,0.18));
          }}
          .telco-top-title {{
            font-size: 40px; font-weight: 900; line-height: 1.1;
            margin: 0;
          }}
          .telco-top-sub {{
            margin-top: 4px;
            color: #6b6b6b;
            font-size: 14px;
          }}
          .telco-divider {{
            height:1px; background:#f2b6c8; opacity:.7;
            margin: 0 0 18px 0;
          }}
        </style>

        <div class="telco-topbar">
          <img src="data:image/png;base64,{logo_b64}" alt="logo"/>
          <div>
            <div class="telco-top-title">{title}</div>
            {sub_html}
          </div>
        </div>
        <div class="telco-divider"></div>
        """,
        unsafe_allow_html=True
    )

# ---------------------------
# Logo: Sidebar fixed (single version only!)
# ---------------------------
def render_sidebar_logo_fixed(
    img_path: str,
    link_to: str = "./",
    max_width_px: int = 260,
    top_px: int = 10,
    nav_pad_px: int = 150,
):
    import base64 as b64

    p = Path(img_path)
    if not p.exists():
        st.sidebar.warning(f"Logo not found: {img_path}")
        return

    logo_b64 = b64.b64encode(p.read_bytes()).decode("utf-8")

    st.markdown(
        f"""
        <style>
          [data-testid="stSidebarNav"] {{
            padding-top: {nav_pad_px}px !important;
          }}

          .telco-sidebar-logo {{
            position: fixed;
            top: {top_px}px;
            left: 12px;
            z-index: 999999;
            width: calc(var(--sidebar-width, 300px) - 24px);
            pointer-events: none;
          }}

          .telco-sidebar-logo a {{
            pointer-events: auto;
            display: block;
          }}

          .telco-sidebar-logo img {{
            width: 100% !important;
            max-width: {max_width_px}px !important;
            height: auto !important;
            display: block;
            margin: 0 auto;
            filter: drop-shadow(0 10px 18px rgba(0,0,0,0.18));
          }}
        </style>

        <div class="telco-sidebar-logo">
          <a href="{link_to}" target="_self" style="text-decoration:none;">
            <img src="data:image/png;base64,{logo_b64}" alt="Telco Dashboard Logo"/>
          </a>
        </div>
        """,
        unsafe_allow_html=True
    )
