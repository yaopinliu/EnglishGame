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
    # --- 動物/昆蟲 ---
    {"en": "animal", "zh": "動物", "cat": "動物/昆蟲"}, {"en": "bear", "zh": "熊", "cat": "動物/昆蟲"},
    {"en": "bee", "zh": "蜜蜂", "cat": "動物/昆蟲"}, {"en": "bird", "zh": "鳥", "cat": "動物/昆蟲"},
    {"en": "butterfly", "zh": "蝴蝶", "cat": "動物/昆蟲"}, {"en": "cat", "zh": "貓", "cat": "動物/昆蟲"},
    {"en": "chicken", "zh": "雞", "cat": "動物/昆蟲"}, {"en": "cow", "zh": "乳牛", "cat": "動物/昆蟲"},
    {"en": "dog", "zh": "狗", "cat": "動物/昆蟲"}, {"en": "duck", "zh": "鴨子", "cat": "動物/昆蟲"},
    {"en": "elephant", "zh": "大象", "cat": "動物/昆蟲"}, {"en": "fish", "zh": "魚", "cat": "動物/昆蟲"},
    {"en": "frog", "zh": "青蛙", "cat": "動物/昆蟲"}, {"en": "hippo", "zh": "河馬", "cat": "動物/昆蟲"},
    {"en": "horse", "zh": "馬", "cat": "動物/昆蟲"}, {"en": "koala", "zh": "無尾熊", "cat": "動物/昆蟲"},
    {"en": "lion", "zh": "獅子", "cat": "動物/昆蟲"}, {"en": "monkey", "zh": "猴子", "cat": "動物/昆蟲"},
    {"en": "mouse", "zh": "老鼠", "cat": "動物/昆蟲"}, {"en": "panda", "zh": "大貓熊", "cat": "動物/昆蟲"},
    {"en": "pet", "zh": "寵物", "cat": "動物/昆蟲"}, {"en": "pig", "zh": "豬", "cat": "動物/昆蟲"},
    {"en": "rabbit", "zh": "兔子", "cat": "動物/昆蟲"}, {"en": "sheep", "zh": "綿羊", "cat": "動物/昆蟲"},
    {"en": "snake", "zh": "蛇", "cat": "動物/昆蟲"}, {"en": "spider", "zh": "蜘蛛", "cat": "動物/昆蟲"},
    {"en": "tiger", "zh": "老虎", "cat": "動物/昆蟲"}, {"en": "turtle", "zh": "烏龜", "cat": "動物/昆蟲"},
    {"en": "whale", "zh": "鯨魚", "cat": "動物/昆蟲"}, {"en": "zebra", "zh": "斑馬", "cat": "動物/昆蟲"},
    # --- 衣服配件 ---
    {"en": "bag", "zh": "袋子", "cat": "衣服配件"}, {"en": "cap", "zh": "棒球帽", "cat": "衣服配件"},
    {"en": "clothes", "zh": "衣服", "cat": "衣服配件"}, {"en": "coat", "zh": "外套", "cat": "衣服配件"},
    {"en": "dress", "zh": "洋裝", "cat": "衣服配件"}, {"en": "glasses", "zh": "眼鏡", "cat": "衣服配件"},
    {"en": "hat", "zh": "帽子", "cat": "衣服配件"}, {"en": "jacket", "zh": "夾克", "cat": "衣服配件"},
    {"en": "pants", "zh": "長褲", "cat": "衣服配件"}, {"en": "shirt", "zh": "襯衫", "cat": "衣服配件"},
    {"en": "shoes", "zh": "鞋子", "cat": "衣服配件"}, {"en": "socks", "zh": "襪子", "cat": "衣服配件"},
    {"en": "sweater", "zh": "毛衣", "cat": "衣服配件"}, {"en": "T-shirt", "zh": "T恤", "cat": "衣服配件"},
    {"en": "umbrella", "zh": "傘", "cat": "衣服配件"},
    # --- 顏色 ---
    {"en": "black", "zh": "黑色的", "cat": "顏色"}, {"en": "blue", "zh": "藍色的", "cat": "顏色"},
    {"en": "brown", "zh": "咖啡色的", "cat": "顏色"}, {"en": "gray", "zh": "灰色的", "cat": "顏色"},
    {"en": "green", "zh": "綠色的", "cat": "顏色"}, {"en": "orange", "zh": "橘色的", "cat": "顏色"},
    {"en": "pink", "zh": "粉紅色的", "cat": "顏色"}, {"en": "purple", "zh": "紫色的", "cat": "顏色"},
    {"en": "red", "zh": "紅色的", "cat": "顏色"}, {"en": "white", "zh": "白色的", "cat": "顏色"},
    {"en": "yellow", "zh": "黃色的", "cat": "顏色"},
    # --- 家庭 ---
    {"en": "aunt", "zh": "阿姨/姑姑", "cat": "家庭"}, {"en": "brother", "zh": "哥哥/弟弟", "cat": "家庭"},
    {"en": "dad", "zh": "爸爸", "cat": "家庭"}, {"en": "daughter", "zh": "女兒", "cat": "家庭"},
    {"en": "family", "zh": "家庭/家人", "cat": "家庭"}, {"en": "father", "zh": "父親", "cat": "家庭"},
    {"en": "mother", "zh": "母親", "cat": "家庭"}, {"en": "sister", "zh": "姐姐/妹妹", "cat": "家庭"},
    {"en": "son", "zh": "兒子", "cat": "家庭"}, {"en": "uncle", "zh": "叔叔/舅舅", "cat": "家庭"},
    # --- 食物/飲料 ---
    {"en": "apple", "zh": "蘋果", "cat": "食物/飲料"}, {"en": "banana", "zh": "香蕉", "cat": "食物/飲料"},
    {"en": "bread", "zh": "麵包", "cat": "食物/飲料"}, {"en": "cake", "zh": "蛋糕", "cat": "食物/飲料"},
    {"en": "candy", "zh": "糖果", "cat": "食物/飲料"}, {"en": "chicken", "zh": "雞肉", "cat": "食物/飲料"},
    {"en": "chocolate", "zh": "巧克力", "cat": "食物/飲料"}, {"en": "coffee", "zh": "咖啡", "cat": "食物/飲料"},
    {"en": "coke", "zh": "可樂", "cat": "食物/飲料"}, {"en": "dumpling", "zh": "水餃", "cat": "食物/飲料"},
    {"en": "egg", "zh": "蛋", "cat": "食物/飲料"}, {"en": "fruit", "zh": "水果", "cat": "食物/飲料"},
    {"en": "hamburger", "zh": "漢堡", "cat": "食物/飲料"}, {"en": "ice cream", "zh": "冰淇淋", "cat": "食物/飲料"},
    {"en": "juice", "zh": "果汁", "cat": "食物/飲料"}, {"en": "milk", "zh": "牛奶", "cat": "食物/飲料"},
    {"en": "noodles", "zh": "麵", "cat": "食物/飲料"}, {"en": "pizza", "zh": "披薩", "cat": "食物/飲料"},
    {"en": "rice", "zh": "米飯", "cat": "食物/飲料"}, {"en": "sandwich", "zh": "三明治", "cat": "食物/飲料"},
    {"en": "soup", "zh": "湯", "cat": "食物/飲料"}, {"en": "strawberry", "zh": "草莓", "cat": "食物/飲料"},
    {"en": "water", "zh": "水", "cat": "食物/飲料"},
    # --- 學校 ---
    {"en": "book", "zh": "書本", "cat": "學校"}, {"en": "classroom", "zh": "教室", "cat": "學校"},
    {"en": "eraser", "zh": "橡皮擦", "cat": "學校"}, {"en": "homework", "zh": "作業", "cat": "學校"},
    {"en": "pencil", "zh": "鉛筆", "cat": "學校"}, {"en": "teacher", "zh": "老師", "cat": "學校"}
]
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





