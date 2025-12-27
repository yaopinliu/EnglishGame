import streamlit as st
import random
from gtts import gTTS
import io
import base64
import streamlit.components.v1 as components
from datetime import datetime
import pandas as pd

# ---------------------------------------------------------
# 1. 完整單字資料庫 (整合 GEPT Kids 核心單字)
# ---------------------------------------------------------
WORD_BANK = [
    # --- 這裡放入您之前的 1200 單字庫內容 (為了長度縮減，此處省略重複列表，請保留您原本的列表) ---
    {"en": "animal", "zh": "動物", "cat": "動物/昆蟲"}, {"en": "bear", "zh": "熊", "cat": "動物/昆蟲"},
    {"en": "apple", "zh": "蘋果", "cat": "食物/飲料"}, {"en": "banana", "zh": "香蕉", "cat": "食物/飲料"},
    {"en": "car", "zh": "汽車", "cat": "運輸"}, {"en": "bus", "zh": "公車", "cat": "運輸"},
    {"en": "book", "zh": "書本", "cat": "學校"}, {"en": "teacher", "zh": "老師", "cat": "學校"},
    {"en": "eye", "zh": "眼睛", "cat": "身體部位"}, {"en": "hand", "zh": "手", "cat": "身體部位"},
    {"en": "run", "zh": "跑", "cat": "動作"}, {"en": "jump", "zh": "跳", "cat": "動作"}
] # 請確保將您之前的完整 WORD_BANK 貼回這裡

# ---------------------------------------------------------
# 2. 核心功能: 語音與工具
# ---------------------------------------------------------

def get_audio_base64(text):
    try:
        tts = gTTS(text=text, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return base64.b64encode(fp.read()).decode()
    except: return None

def play_audio_js(text, key_suffix=""):
    b64 = get_audio_base64(text)
    if not b64: return
    audio_id = f"audio_{key_suffix}_{random.randint(0, 99999)}"
    html = f"""
        <audio id="{audio_id}"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>
        <script>function play_{audio_id}(){{document.getElementById("{audio_id}").play();}}</script>
        <button onclick="play_{audio_id}()" style="background:#4CAF50;color:white;border:none;padding:10px;width:100%;border-radius:8px;cursor:pointer;font-weight:bold;">🔊 聽發音</button>
    """
    components.html(html, height=55)

def safe_rerun():
    try: st.rerun()
    except: st.experimental_rerun()

def create_cloze_word(word):
    if len(word) <= 2: return word
    chars = list(word)
    num_mask = max(1, int(len(word) * 0.4))
    indices = list(range(1, len(word) - 1))
    for i in random.sample(indices, min(len(indices), num_mask)):
        chars[i] = "_"
    return " ".join(chars)

# ---------------------------------------------------------
# 3. Session State 初始化 (包含統計歷史)
# ---------------------------------------------------------
if 'mode' not in st.session_state: st.session_state.mode = "MAIN"
if 'history' not in st.session_state: st.session_state.history = [] # 儲存學習紀錄
if 'game_state' not in st.session_state:
    st.session_state.update({
        'game_state': "START", 'score': 0, 'current_idx': 0, 
        'questions': [], 'wrong_list': [], 'ans_checked': False,
        'results_saved': False # 防止重複紀錄
    })

# ---------------------------------------------------------
# 4. 統計畫面邏輯
# ---------------------------------------------------------
def run_stats_mode():
    st.title("📊 學習統計紀錄")
    if st.button("⬅ 返回主選單"):
        st.session_state.mode = "MAIN"
        safe_rerun()

    if not st.session_state.history:
        st.info("目前還沒有測驗紀錄，快去開始挑戰吧！")
    else:
        df = pd.DataFrame(st.session_state.history)
        
        # 總結統計
        col1, col2, col3 = st.columns(3)
        col1.metric("總測驗次數", len(df))
        avg_acc = df["正確率(%)"].mean()
        col2.metric("平均正確率", f"{avg_acc:.1f}%")
        col3.metric("總練習題數", df["題數"].sum())

        st.write("### 詳細歷程回顧")
        st.dataframe(df, use_container_width=True)

        if st.button("清除統計資料"):
            st.session_state.history = []
            safe_rerun()

# ---------------------------------------------------------
# 5. 測驗結束紀錄邏輯
# ---------------------------------------------------------
def save_result_to_history(mode_name, selected_cat, total_q, score):
    if not st.session_state.results_saved:
        accuracy = (score / (total_q * 5)) * 100 # 每題5分
        new_record = {
            "日期時間": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "模式": mode_name,
            "主題": selected_cat,
            "題數": total_q,
            "得分": score,
            "正確率(%)": round(accuracy, 1)
        }
        st.session_state.history.append(new_record)
        st.session_state.results_saved = True

# ---------------------------------------------------------
# 6. 介面流程控制
# ---------------------------------------------------------
st.set_page_config(page_title="GEPT Kids 單字王", page_icon="📝")

# --- 主選單 ---
if st.session_state.mode == "MAIN":
    st.title("🎓 小學英檢單字王")
    st.write("歡迎來到英語學習園地！")
    
    if st.button("🎧 聽力測驗 (聽音選中)", use_container_width=True):
        st.session_state.mode = "LISTENING"
        st.session_state.game_state = "START"
        safe_rerun()
    if st.button("✍️ 拼寫測驗 (看中打英)", use_container_width=True):
        st.session_state.mode = "CLOZE"
        st.session_state.game_state = "START"
        safe_rerun()
    st.write("---")
    if st.button("📊 查看學習統計", use_container_width=True):
        st.session_state.mode = "STATS"
        safe_rerun()

# --- 聽力模式 ---
elif st.session_state.mode == "LISTENING":
    st.title("🎧 聽力測驗")
    if st.session_state.game_state == "START":
        st.session_state.results_saved = False
        cats = sorted(list(set([w['cat'] for w in WORD_BANK])))
        selected_cat = st.selectbox("主題：", ["全部隨機"] + cats)
        if st.button("開始"):
            pool = WORD_BANK if selected_cat == "全部隨機" else [w for w in WORD_BANK if w['cat'] == selected_cat]
            st.session_state.questions = random.sample(pool, min(len(pool), 20))
            st.session_state.selected_cat = selected_cat
            st.session_state.game_state = "PLAY"
            safe_rerun()
    elif st.session_state.game_state == "PLAY":
        # ... (這裡放聽力測驗的 PLAY 邏輯，同之前程式碼) ...
        # (當結束時切換到 END)
        pass # 請將原有的聽力 PLAY 程式碼貼入
    elif st.session_state.game_state == "END":
        save_result_to_history("聽力測驗", st.session_state.selected_cat, len(st.session_state.questions), st.session_state.score)
        # 顯示結果... (同之前程式碼)

# --- 拼寫模式 ---
elif st.session_state.mode == "CLOZE":
    st.title("✍️ 拼寫測驗")
    if st.session_state.game_state == "START":
        st.session_state.results_saved = False
        cats = sorted(list(set([w['cat'] for w in WORD_BANK])))
        selected_cat = st.selectbox("主題：", ["全部隨機"] + cats)
        if st.button("開始"):
            pool = WORD_BANK if selected_cat == "全部隨機" else [w for w in WORD_BANK if w['cat'] == selected_cat]
            st.session_state.questions = random.sample(pool, min(len(pool), 20))
            st.session_state.selected_cat = selected_cat
            st.session_state.game_state = "PLAY"
            safe_rerun()
    elif st.session_state.game_state == "PLAY":
        # ... (這裡放拼寫測驗的 PLAY 邏輯，同之前程式碼) ...
        pass # 請將原有的拼寫 PLAY 程式碼貼入
    elif st.session_state.game_state == "END":
        save_result_to_history("拼寫測驗", st.session_state.selected_cat, len(st.session_state.questions), st.session_state.score)
        # 顯示結果... (同之前程式碼)

# --- 統計模式 ---
elif st.session_state.mode == "STATS":
    run_stats_mode()




