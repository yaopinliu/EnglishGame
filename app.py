import streamlit as st
import random
from gtts import gTTS
impoimport streamlit as st
import random
from gtts import gTTS
import io
import base64
import streamlit.components.v1 as components

# ---------------------------------------------------------
# 1. 單字資料庫 (包含 1200 單字核心內容)
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
# 2. 核心功能: JS Audio Player & 工具函數
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
        <button onclick="play_{audio_id}()" style="background:#4CAF50;color:white;border:none;padding:10px;width:100%;border-radius:8px;cursor:pointer;">🔊 聽發音</button>
    """
    components.html(html, height=55)

def safe_rerun():
    try: st.rerun()
    except: st.experimental_rerun()

def create_cloze_word(word):
    """ 將單字挖空，例如 'apple' -> 'a _ _ l e' """
    if len(word) <= 2: return word
    chars = list(word)
    num_mask = max(1, int(len(word) * 0.4))
    indices = list(range(1, len(word) - 1))
    for i in random.sample(indices, min(len(indices), num_mask)):
        chars[i] = "_"
    return " ".join(chars)

# ---------------------------------------------------------
# 3. Session State
# ---------------------------------------------------------
if 'mode' not in st.session_state: st.session_state.mode = "MAIN"
if 'game_state' not in st.session_state:
    st.session_state.update({'game_state': "START", 'score': 0, 'current_idx': 0, 'questions': [], 'wrong_list': [], 'ans_checked': False})

# ---------------------------------------------------------
# 4. 測驗模式邏輯
# ---------------------------------------------------------
st.set_page_config(page_title="GEPT Kids 單字王", page_icon="📝")

# --- 模式 A: 聽力測驗 ---
def run_listening_mode():
    st.title("🎧 聽力測驗")
    if st.button("⬅ 回選單"): 
        st.session_state.mode = "MAIN"
        safe_rerun()

    if st.session_state.game_state == "START":
        cats = sorted(list(set([w['cat'] for w in WORD_BANK])))
        selected = st.selectbox("主題：", ["全部隨機"] + cats)
        if st.button("開始測驗"):
            pool = WORD_BANK if selected == "全部隨機" else [w for w in WORD_BANK if w['cat'] == selected]
            st.session_state.questions = random.sample(pool, min(len(pool), 20))
            st.session_state.game_state = "PLAY"
            st.session_state.current_idx = 0
            st.session_state.score = 0
            st.session_state.wrong_list = []
            st.session_state.ans_checked = False
            safe_rerun()

    elif st.session_state.game_state == "PLAY":
        q = st.session_state.questions[st.session_state.current_idx]
        st.write(f"題目 {st.session_state.current_idx + 1} / {len(st.session_state.questions)}")
        play_audio_js(q['en'], f"lis_{st.session_state.current_idx}")
        
        # 聽力測驗保留選擇題
        if 'opts' not in st.session_state or st.session_state.last_idx != st.session_state.current_idx:
            wrong = [w['zh'] for w in WORD_BANK if w['zh'] != q['zh']]
            opts = random.sample(wrong, 3) + [q['zh']]
            random.shuffle(opts)
            st.session_state.opts = opts
            st.session_state.last_idx = st.session_state.current_idx

        if not st.session_state.ans_checked:
            for o in st.session_state.opts:
                if st.button(o, use_container_width=True):
                    st.session_state.ans_checked = True
                    st.session_state.user_choice = o
                    if o == q['zh']: st.session_state.score += 5
                    else: st.session_state.wrong_list.append(q)
                    safe_rerun()
        else:
            st.info(f"單字：{q['en']}")
            if st.session_state.user_choice == q['zh']: st.success("正確！")
            else: st.error(f"錯誤！答案是：{q['zh']}")
            if st.button("下一題"):
                st.session_state.current_idx += 1
                st.session_state.ans_checked = False
                if st.session_state.current_idx >= len(st.session_state.questions): st.session_state.game_state = "END"
                safe_rerun()

    elif st.session_state.game_state == "END": show_results()

# --- 模式 B: 克漏字測驗 (手動輸入版) ---
def run_cloze_mode():
    st.title("🔤 單字拼寫測驗")
    if st.button("⬅ 回選單"): 
        st.session_state.mode = "MAIN"
        safe_rerun()

    if st.session_state.game_state == "START":
        cats = sorted(list(set([w['cat'] for w in WORD_BANK])))
        selected = st.selectbox("主題：", ["全部隨機"] + cats)
        if st.button("開始拼寫測驗"):
            pool = WORD_BANK if selected == "全部隨機" else [w for w in WORD_BANK if w['cat'] == selected]
            st.session_state.questions = random.sample(pool, min(len(pool), 20))
            st.session_state.game_state = "PLAY"
            st.session_state.current_idx = 0
            st.session_state.score = 0
            st.session_state.wrong_list = []
            st.session_state.ans_checked = False
            safe_rerun()

    elif st.session_state.game_state == "PLAY":
        q = st.session_state.questions[st.session_state.current_idx]
        st.write(f"題目 {st.session_state.current_idx + 1} / {len(st.session_state.questions)}")
        
        # 顯示中文與挖空字
        st.subheader(f"中文意思：{q['zh']}")
        if 'cur_cloze' not in st.session_state or st.session_state.last_cl_idx != st.session_state.current_idx:
            st.session_state.cur_cloze = create_cloze_word(q['en'])
            st.session_state.last_cl_idx = st.session_state.current_idx
        
        st.markdown(f"## `{st.session_state.cur_cloze}`")
        play_audio_js(q['en'], f"cl_{st.session_state.current_idx}")

        # 手動輸入拼寫
        if not st.session_state.ans_checked:
            user_input = st.text_input("請輸入完整的英文單字：", key=f"input_{st.session_state.current_idx}").strip().lower()
            if st.button("送出答案"):
                if user_input:
                    st.session_state.ans_checked = True
                    st.session_state.user_typed = user_input
                    if user_input == q['en'].lower(): st.session_state.score += 5
                    else: st.session_state.wrong_list.append(q)
                    safe_rerun()
                else: st.warning("請先輸入文字再送出喔！")
        else:
            if st.session_state.user_typed == q['en'].lower():
                st.success(f"太棒了！拼寫正確：{q['en']}")
            else:
                st.error(f"拼錯了喔！正確單字是：{q['en']}")
                st.write(f"您的輸入：{st.session_state.user_typed}")
            
            if st.button("下一題"):
                st.session_state.current_idx += 1
                st.session_state.ans_checked = False
                if st.session_state.current_idx >= len(st.session_state.questions): st.session_state.game_state = "END"
                safe_rerun()

    elif st.session_state.game_state == "END": show_results()

def show_results():
    st.header("🏆 挑戰結束！")
    st.metric("總得分", f"{st.session_state.score}")
    if st.session_state.wrong_list:
        st.write("複習錯題：")
        for i, w in enumerate(st.session_state.wrong_list):
            c1, c2 = st.columns([3, 1])
            c1.write(f"{w['en']} ({w['zh']})")
            with c2: play_audio_js(w['en'], f"res_{i}")
    if st.button("回主選單"):
        st.session_state.mode = "MAIN"
        st.session_state.game_state = "START"
        safe_rerun()

# --- 主進入點 ---
if st.session_state.mode == "MAIN":
    st.title("🎓 小學英檢單字王")
    st.write("選擇練習模式：")
    if st.button("🎧 聽力測驗 (選中文)", use_container_width=True):
        st.session_state.mode = "LISTENING"
        st.session_state.game_state = "START"
        safe_rerun()
    if st.button("✍️ 拼寫測驗 (打英文字)", use_container_width=True):
        st.session_state.mode = "CLOZE"
        st.session_state.game_state = "START"
        safe_rerun()
elif st.session_state.mode == "LISTENING": run_listening_mode()
elif st.session_state.mode == "CLOZE": run_cloze_mode()



