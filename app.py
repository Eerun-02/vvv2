import streamlit as st
import pandas as pd
import numpy as np

# --- Configuration ---
st.set_page_config(
    page_title="VVV Setting Estimator",
    page_icon="🎰",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for VVV Theme (Black, Red, Gold) ---
def local_css():
    st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0e0e0e;
        color: #ffffff;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        color: #ffffff;
        background-color: #262626;
        border: 1px solid #FFD700; /* Gold Border */
    }
    .stNumberInput > div > div > input {
        color: #ffffff;
        background-color: #262626;
        border: 1px solid #FFD700;
    }
    
    /* Buttons */
    div.stButton > button:first-child {
        background-color: #8B0000; /* Dark Red */
        color: #FFD700; /* Gold Text */
        border: 1px solid #FFD700;
        border-radius: 5px;
        font-weight: bold;
    }
    div.stButton > button:active {
        background-color: #FF0000;
        color: #ffffff;
    }
    div.stButton > button:focus {
        border-color: #FFD700;
        box-shadow: 0 0 0 0.2rem rgba(255, 215, 0, 0.5);
        color: #FFD700;
        background-color: #8B0000;
    }

    /* Headings */
    h1, h2, h3 {
        color: #FFD700 !important; /* Gold */
        font-family: 'Arial Black', sans-serif;
        text-shadow: 2px 2px 4px #000000;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1a1a1a;
        border-right: 1px solid #8B0000;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background-color: #FFD700;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #FF0000 !important;
        font-weight: bold;
    }
    [data-testid="stMetricLabel"] {
        color: #cccccc !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #262626;
        color: #FFD700;
        border: 1px solid #8B0000;
    }
    
    </style>
    """, unsafe_allow_html=True)

local_css()

# --- Password Protection ---
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == "vvv666": # Simple hardcoded password
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "パスワードを入力してください ", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password validation error
        st.text_input(
            "パスワードを入力してください ", type="password", on_change=password_entered, key="password"
        )
        st.error("パスワードが間違っています。")
        return False
    else:
        # Password correct.
        return True

if not check_password():
    st.stop()

# --- Application Logic ---
st.title("🎰 VVV Setting Estimator")
st.markdown("### ヴァルヴレイヴ 設定推測ツール")

# --- Custom Counter Component for Mobile ---
def counter_input(label, key_suffix, initial_value=0):
    if key_suffix not in st.session_state:
        st.session_state[key_suffix] = initial_value

    cols = st.columns([2, 1, 1, 1])
    with cols[0]:
        st.markdown(f"**{label}**")
    
    # Logic for button clicks using callbacks or simple reruns
    def increment():
        st.session_state[key_suffix] += 1
    def decrement():
        if st.session_state[key_suffix] > 0:
            st.session_state[key_suffix] -= 1

    with cols[1]:
        st.button("➖", key=f"dec_{key_suffix}", on_click=decrement, use_container_width=True)
    with cols[2]:
        st.markdown(f"<div style='text-align: center; font-size: 20px; font-weight: bold; color: #FFD700;'>{st.session_state[key_suffix]}</div>", unsafe_allow_html=True)
    with cols[3]:
        st.button("➕", key=f"inc_{key_suffix}", on_click=increment, use_container_width=True)
    
    return st.session_state[key_suffix]

# --- Main Area Inputs (Frequent Use) ---
st.subheader("📊 終了画面・示唆カウント")
screen_default = counter_input("デフォルト", "s_def")
screen_odd = counter_input("奇数示唆", "s_odd")
screen_even = counter_input("偶数示唆", "s_even")
screen_high_weak = counter_input("高設定示唆 (弱)", "s_hw")
screen_high_strong = counter_input("高設定示唆 (強)", "s_hs")
screen_456 = counter_input("設定4以上濃厚", "s_456")
screen_56 = counter_input("設定5以上濃厚", "s_56")
screen_6 = counter_input("設定6濃厚", "s_6")

# --- Sidebar Inputs (Less Frequent) ---
with st.sidebar:
    st.header("⚙️ 数値入力")
    
    total_spins = st.number_input("総回転数 (G)", min_value=0, step=10, value=0)
    cz_count = st.number_input("CZ当選回数", min_value=0, step=1, value=0)
    
    st.subheader("ボーナス回数")
    bonus_rev = st.number_input("革命ボーナス", min_value=0, step=1, value=0)
    bonus_bat = st.number_input("決戦ボーナス", min_value=0, step=1, value=0)

    st.markdown("---")
    if st.button("🔄 データリセット", type="primary"):
        for key in st.session_state.keys():
            if key.startswith("s_"):
                st.session_state[key] = 0
        st.rerun()

# --- Calculation Logic ---

# 1. CZ Probability
cz_prob = 0.0
cz_denom = 0.0
if cz_count > 0:
    cz_denom = total_spins / cz_count
    cz_prob = 1 / cz_denom if cz_denom > 0 else 0

# Setting Expectations for CZ (Approximate)
# 1: 1/277, 2: 1/274, 3: 1/269, 4: 1/259, 5: 1/254, 6: 1/249
cz_settings = {
    1: 1/277, 2: 1/274, 3: 1/269, 4: 1/259, 5: 1/254, 6: 1/249
}

# 2. Points Calculation
# Start with neutral points
points = {1: 10, 2: 10, 3: 10, 4: 10, 5: 10, 6: 10}

# CZ Impact (Simple distance based weight)
if cz_count > 5: # Only apply if enough samples
    for s, prob in cz_settings.items():
        # Closer to theoretical prob = more points
        # Calculate deviation %
        diff = abs((1/cz_denom) - prob)
        # Weight: 10 points max, decreasing with diff
        weight = max(0, 10 - (diff * 10000)) # Simple scaling
        points[s] += weight

# Ending Screen Impact
# Logic: Add points based on screen counts
# These are arbitrary weights for estimation simulation
points[1] += screen_odd * 2 + screen_default * 1
points[2] += screen_even * 2 + screen_default * 1
points[3] += screen_odd * 2 + screen_default * 1
points[4] += screen_even * 2 + screen_high_weak * 2 + screen_high_strong * 4 + screen_456 * 20
points[5] += screen_odd * 2 + screen_high_weak * 2 + screen_high_strong * 4 + screen_456 * 20 + screen_56 * 50
points[6] += screen_even * 2 + screen_high_weak * 2 + screen_high_strong * 4 + screen_456 * 20 + screen_56 * 50 + screen_6 * 100

# Handling "Negations" (If 4+ shows up, 1,2,3 become 0)
if screen_456 > 0:
    points[1] = 0
    points[2] = 0
    points[3] = 0
if screen_56 > 0:
    points[1] = 0
    points[2] = 0
    points[3] = 0
    points[4] = 0
if screen_6 > 0:
    for s in range(1, 6):
        points[s] = 0

# Normalize to Percentage
total_points = sum(points.values())
percentages = {k: (v / total_points * 100) if total_points > 0 else 0 for k, v in points.items()}

# --- Display Results ---

st.markdown("---")
st.markdown("## 📊 推測結果")

# Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("CZ確率", f"1/{cz_denom:.1f}" if cz_count > 0 else "-")
with col2:
    st.metric("総回転数", f"{total_spins} G")
with col3:
    st.metric("ボーナス合計", f"{bonus_rev + bonus_bat} 回")

st.markdown("### 設定期待度")

# Sort by percentage descending for a better view? Or keep 1-6 for order?
# Keeping 1-6 is standard for setting estimators.
df_res = pd.DataFrame.from_dict(percentages, orient='index', columns=['Expectation'])
df_res['Setting'] = df_res.index

# Progress bars for each setting
for s in range(1, 7):
    p = percentages[s]
    cols = st.columns([1, 4, 1])
    with cols[0]:
        st.markdown(f"**設定 {s}**")
    with cols[1]:
        # Custom color based on value?
        bar_color = "red" if p > 30 else "gold"
        st.progress(int(p))
    with cols[2]:
        st.markdown(f"**{p:.1f}%**")

# Highlight if high setting confirmed
if screen_6 > 0:
    st.success("🎉 設定6 濃厚！ (Supreme Confirmed!)")
    st.balloons()
elif screen_56 > 0:
    st.warning("🔥 設定5以上 濃厚！")
elif screen_456 > 0:
    st.info("✨ 設定4以上 濃厚！")

# Debug/Info about screens (optional)
with st.expander("詳細データ & ロジックについて"):
    st.write("現在入力されている終了画面カウント:")
    st.json({
        "Default": screen_default,
        "Odd": screen_odd,
        "Even": screen_even,
        "High(Weak)": screen_high_weak,
        "High(Strong)": screen_high_strong,
        "4+": screen_456,
        "5+": screen_56,
        "6+": screen_6
    })
    st.info("※ このツールは独自の簡易ロジックに基づいています。実際の設定とは異なる場合があります。")

st.markdown("---")
st.caption("© 2024 VVV Setting Estimator | Designed for Valvrave Fans")

