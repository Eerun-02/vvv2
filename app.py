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
        padding-top: 10px;
        padding-bottom: 10px;
        font-size: 1.2rem;
        border: 1px solid #FFD700;
    }
    
    /* Buttons */
    div.stButton > button {
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
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #262626;
        border-radius: 5px;
        color: #ffffff;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFD700 !important;
        color: #000000 !important;
        font-weight: bold;
    }
    
    </style>
    """, unsafe_allow_html=True)

local_css()

# --- Password Protection ---
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        if st.session_state["password"] == "135eva":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("パスワード", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("パスワード", type="password", on_change=password_entered, key="password")
        st.error("パスワードが間違っています。")
        return False
    else:
        return True

if not check_password():
    st.stop()

# --- Application Logic ---
st.title("🎰 VVV Setting Estimator")

# --- Custom Counter ---
def counter_input(label, key_suffix, initial_value=0):
    if key_suffix not in st.session_state:
        st.session_state[key_suffix] = initial_value

    cols = st.columns([2, 1, 1, 1])
    with cols[0]:
        st.markdown(f"**{label}**")
    
    def increment():
        st.session_state[key_suffix] += 1
    def decrement():
        if st.session_state[key_suffix] > 0:
            st.session_state[key_suffix] -= 1

    with cols[1]:
        st.button("➖", key=f"dec_{key_suffix}", on_click=decrement, use_container_width=True)
    with cols[2]:
        val = st.session_state[key_suffix]
        st.markdown(f"<div style='text-align: center; font-size: 20px; font-weight: bold; color: #FFD700; padding: 5px;'>{val}</div>", unsafe_allow_html=True)
    with cols[3]:
        st.button("➕", key=f"inc_{key_suffix}", on_click=increment, use_container_width=True)
    
    return st.session_state[key_suffix]

# --- Main Logic Inputs ---
st.markdown("### 📊 設定示唆要素 (補助)")
st.caption("※ ボーナス終了画面やハラキリドライブの回数を入力してください")

# Tabs for organization
tab1, tab2 = st.tabs(["🔥 ハラキリドライブ", "📺 終了画面"])

with tab1:
    st.markdown("##### ハラキリドライブ (50G以上)")
    drive_count = counter_input("発生回数", "d_count")
    
    st.markdown("##### 枚数示唆 (濃厚演出)")
    cols_drive = st.columns(3)
    with cols_drive[0]:
        drive_456 = st.checkbox("456G (4以上)", key="d_456")
    with cols_drive[1]:
        drive_666 = st.checkbox("666G (6確)", key="d_666")
    with cols_drive[2]:
        drive_555 = st.checkbox("555G (5以上)", key="d_555")

with tab2:
    st.markdown("##### 終了画面カウント")
    screen_default = counter_input("デフォルト", "s_def")
    screen_odd = counter_input("奇数示唆", "s_odd")
    screen_even = counter_input("偶数示唆", "s_even")
    screen_high_weak = counter_input("高設定示唆 (弱)", "s_hw")
    screen_high_strong = counter_input("高設定示唆 (強)", "s_hs")
    screen_456 = counter_input("設定4以上濃厚", "s_456")
    screen_56 = counter_input("設定5以上濃厚", "s_56")
    screen_6 = counter_input("設定6濃厚", "s_6")

# --- Sidebar Inputs (Main Factor) ---
with st.sidebar:
    st.header("⚙️ 回転数・ボーナス (重要)")
    
    total_spins = st.number_input("総回転数 (G)", min_value=0, step=10, value=0)
    cz_count = st.number_input("CZ当選回数", min_value=0, step=1, value=0)
    
    st.markdown("---")
    st.subheader("ボーナス内訳")
    bonus_rev = st.number_input("革命ボーナス", min_value=0, step=1, value=0)
    bonus_bat = st.number_input("決戦ボーナス", min_value=0, step=1, value=0)

    st.markdown("---")
    if st.button("🔄 データリセット", type="primary"):
        for key in st.session_state.keys():
            if key.startswith("s_") or key.startswith("d_"):
                if isinstance(st.session_state[key], bool): # Reset checkboxes
                   st.session_state[key] = False
                else:
                   st.session_state[key] = 0
        st.rerun()

# --- Calculation Logic (Refined) ---

cz_denom = 0.0
if cz_count > 0:
    cz_denom = total_spins / cz_count

# Bonus Probability (Using this as main factor instead of CZ per user request)
# Total Bonuses / Total Spins
total_bonus = bonus_rev + bonus_bat
bonus_denom = 0.0
if total_bonus > 0:
    bonus_denom = total_spins / total_bonus

# Bonus Probability Settings (Approximate for L Valvrave 2 / VVV2)
# Setting 1: 1/476, Setting 6: 1/456 (Difference is small)
# Using a slightly exaggerated scale for estimation responsiveness
bonus_settings = {
    1: 1/476, 2: 1/472, 3: 1/468, 4: 1/464, 5: 1/460, 6: 1/456
}

# Initialize Probabilities (Uniform Prior)
scores = {1: 1.0, 2: 1.0, 3: 1.0, 4: 1.0, 5: 1.0, 6: 1.0}

# --- Phase 1: Bonus Probability (Main Statistical Factor) ---
# Use Poisson or Binomial approximation for likelihood based on Bonus Count
if total_bonus > 0 and total_spins > 0:
    for s, prob in bonus_settings.items():
        # Using Gaussian approximation
        mean = total_spins * prob
        variance = total_spins * prob * (1 - prob)
        std_dev = np.sqrt(variance)
        
        if std_dev == 0: std_dev = 1e-9

        # Calculate Probability Density Function (PDF) value
        diff = total_bonus - mean
        likelihood = (1 / (std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * (diff / std_dev) ** 2)
        
        # Avoid zero likelihood
        likelihood = max(likelihood, 1e-9)
        
        scores[s] *= likelihood

# --- Phase 2: Supportive Elements (Screen & Drive) ---
# Multipliers based on inputs

# 2a. Screen Hints
if screen_odd > 0:
    for s in [1, 3, 5]: scores[s] *= (1.2 ** screen_odd)
if screen_even > 0:
    for s in [2, 4, 6]: scores[s] *= (1.2 ** screen_even)

# High Setting Hints
if screen_high_weak > 0:
    for s in [4, 5, 6]: scores[s] *= (1.3 ** screen_high_weak)
    scores[2] *= 1.1 
    
if screen_high_strong > 0:
    for s in [5, 6]: scores[s] *= (1.5 ** screen_high_strong)
    scores[4] *= 1.3

# 2b. Harakiri Drive (Supportive Boost)
# Adjusted boost to be supportive rather than dominant.
if drive_count > 0:
    # Boost Setting 6 massively per drive, Setting 5 moderately
    scores[6] *= (1.6 ** drive_count)
    scores[5] *= (1.3 ** drive_count)
    scores[4] *= (1.1 ** drive_count)

# Specific Payout Amounts (Definitive)
if drive_456:
    scores[1] = 0; scores[2] = 0; scores[3] = 0
if drive_555:
    scores[1] = 0; scores[2] = 0; scores[3] = 0; scores[4] = 0
if drive_666:
    for s in range(1, 6): scores[s] = 0


# --- Phase 3: Definitive Flags (Override) ---
# These set impossible settings to 0
if screen_456 > 0:
    scores[1] = 0; scores[2] = 0; scores[3] = 0
if screen_56 > 0:
    scores[1] = 0; scores[2] = 0; scores[3] = 0; scores[4] = 0
if screen_6 > 0:
    for s in range(1, 6): scores[s] = 0


# Normalize to Percentage
total_score = sum(scores.values())
percentages = {k: (v / total_score * 100) if total_score > 0 else 0.0 for k, v in scores.items()}

# --- Display Results ---

st.markdown("---")
st.markdown("## 📊 推測結果")

# Main result visualization
# Identify likely settings (Top 2)
sorted_settings = sorted(percentages.items(), key=lambda x: x[1], reverse=True)
top_setting = sorted_settings[0][0]
top_prob = sorted_settings[0][1]

# Metrics
c1, c2, c3 = st.columns(3)
c1.metric("ボーナス合算確率", f"1/{bonus_denom:.1f}" if total_bonus > 0 else "-")
c2.metric("総回転数", f"{total_spins} G")
c3.metric("CZ確率 (参考)", f"1/{cz_denom:.1f}" if cz_count > 0 else "-") # Display Only

# Progress Bars
st.write("#### 設定期待度詳細")
for s in range(1, 7):
    p = percentages[s]
    cols = st.columns([1, 4, 1])
    cols[0].write(f"**設定 {s}**")
    
    # Dynamic Color
    color = "red" if p >= 40 else "green" if p >= 20 else "gray"
    if s == top_setting and p > 30: color = "red" # Highlight top candidate
    
    cols[1].progress(int(p), text=None)
    cols[2].write(f"{p:.1f}%")

# Analysis Comment
st.info(f"現在のデータでは **設定{top_setting}** の可能性が最も高いです。")

# Definitive message
confirmed = False
if screen_6 > 0 or drive_666:
    st.balloons()
    st.success("🎉 設定6 濃厚！ (Supreme Confirmed!)")
    confirmed = True
elif screen_56 > 0 or drive_555:
    if not confirmed: st.warning("🔥 設定5以上 濃厚！")
    confirmed = True
elif screen_456 > 0 or drive_456:
    if not confirmed: st.info("✨ 設定4以上 濃厚！")

with st.expander("ロジックの詳細"):
    st.markdown("""
    - **ボーナス確率（メイン判定）**: ユーザー様のご意見に基づき、CZ確率は共通として扱い、ボーナス初当り確率（約1/476～1/456）をメインの推測要素としました。
    - **ハラキリドライブ**: 回数入力による加点（補助）として扱っています。
    - **CZ確率**: 参考値として表示していますが、推測ロジックには影響しません。
    """)

