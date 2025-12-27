import streamlit as st
import random
from gtts import gTTS
import io
import base64
import streamlit.components.v1 as components

# ---------------------------------------------------------
# 1. 完整單字資料庫 (整合 1200 單字)
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
    {"en": "pants", "zh": "長褲", "cat": "衣服配件"}, {"en": "pocket", "zh": "口袋", "cat": "衣服配件"},
    {"en": "shirt", "zh": "襯衫", "cat": "衣服配件"}, {"en": "shoes", "zh": "鞋子", "cat": "衣服配件"},
    {"en": "shorts", "zh": "短褲", "cat": "衣服配件"}, {"en": "skirt", "zh": "裙子", "cat": "衣服配件"},
    {"en": "socks", "zh": "襪子", "cat": "衣服配件"}, {"en": "sweater", "zh": "毛衣", "cat": "衣服配件"},
    {"en": "T-shirt", "zh": "T恤", "cat": "衣服配件"}, {"en": "umbrella", "zh": "傘", "cat": "衣服配件"},
    {"en": "wear", "zh": "穿/戴", "cat": "衣服配件"},
    # --- 顏色 ---
    {"en": "black", "zh": "黑色的", "cat": "顏色"}, {"en": "blue", "zh": "藍色的", "cat": "顏色"},
    {"en": "brown", "zh": "咖啡色的", "cat": "顏色"}, {"en": "color", "zh": "顏色", "cat": "顏色"},
    {"en": "gray", "zh": "灰色的", "cat": "顏色"}, {"en": "green", "zh": "綠色的", "cat": "顏色"},
    {"en": "orange", "zh": "橘色的", "cat": "顏色"}, {"en": "pink", "zh": "粉紅色的", "cat": "顏色"},
    {"en": "purple", "zh": "紫色的", "cat": "顏色"}, {"en": "red", "zh": "紅色的", "cat": "顏色"},
    {"en": "white", "zh": "白色的", "cat": "顏色"}, {"en": "yellow", "zh": "黃色的", "cat": "顏色"},
    # --- 家庭 ---
    {"en": "aunt", "zh": "阿姨/姑姑", "cat": "家庭"}, {"en": "brother", "zh": "哥哥/弟弟", "cat": "家庭"},
    {"en": "cousin", "zh": "堂表兄弟姊妹", "cat": "家庭"}, {"en": "dad", "zh": "爸爸(口語)", "cat": "家庭"},
    {"en": "daughter", "zh": "女兒", "cat": "家庭"}, {"en": "family", "zh": "家庭/家人", "cat": "家庭"},
    {"en": "father", "zh": "父親", "cat": "家庭"}, {"en": "grandfather", "zh": "祖父/外公", "cat": "家庭"},
    {"en": "grandma", "zh": "祖母/外婆(口語)", "cat": "家庭"}, {"en": "grandmother", "zh": "祖母/外婆", "cat": "家庭"},
    {"en": "grandpa", "zh": "祖父/外公(口語)", "cat": "家庭"}, {"en": "mom", "zh": "媽媽(口語)", "cat": "家庭"},
    {"en": "mother", "zh": "母親", "cat": "家庭"}, {"en": "parent", "zh": "父母親", "cat": "家庭"},
    {"en": "sister", "zh": "姐姐/妹妹", "cat": "家庭"}, {"en": "son", "zh": "兒子", "cat": "家庭"},
    {"en": "uncle", "zh": "叔叔/舅舅", "cat": "家庭"},
    # --- 食物/飲料 ---
    {"en": "apple", "zh": "蘋果", "cat": "食物/飲料"}, {"en": "banana", "zh": "香蕉", "cat": "食物/飲料"},
    {"en": "beef", "zh": "牛肉", "cat": "食物/飲料"}, {"en": "bread", "zh": "麵包", "cat": "食物/飲料"},
    {"en": "breakfast", "zh": "早餐", "cat": "食物/飲料"}, {"en": "cake", "zh": "蛋糕", "cat": "食物/飲料"},
    {"en": "candy", "zh": "糖果", "cat": "食物/飲料"}, {"en": "chicken", "zh": "雞肉", "cat": "食物/飲料"},
    {"en": "chocolate", "zh": "巧克力", "cat": "食物/飲料"}, {"en": "coffee", "zh": "咖啡", "cat": "食物/飲料"},
    {"en": "coke", "zh": "可樂", "cat": "食物/飲料"}, {"en": "cook", "zh": "做飯/廚師", "cat": "食物/飲料"},
    {"en": "cookies", "zh": "餅乾", "cat": "食物/飲料"}, {"en": "dinner", "zh": "晚餐", "cat": "食物/飲料"},
    {"en": "drink", "zh": "喝/飲料", "cat": "食物/飲料"}, {"en": "dumpling", "zh": "水餃", "cat": "食物/飲料"},
    {"en": "eat", "zh": "吃", "cat": "食物/飲料"}, {"en": "egg", "zh": "蛋", "cat": "食物/飲料"},
    {"en": "fish", "zh": "魚肉", "cat": "食物/飲料"}, {"en": "food", "zh": "食物", "cat": "食物/飲料"},
    {"en": "fruit", "zh": "水果", "cat": "食物/飲料"}, {"en": "full", "zh": "飽的", "cat": "食物/飲料"},
    {"en": "grape", "zh": "葡萄", "cat": "食物/飲料"}, {"en": "hamburger", "zh": "漢堡", "cat": "食物/飲料"},
    {"en": "hungry", "zh": "餓的", "cat": "食物/飲料"}, {"en": "ice cream", "zh": "冰淇淋", "cat": "食物/飲料"},
    {"en": "juice", "zh": "果汁", "cat": "食物/飲料"}, {"en": "lemon", "zh": "檸檬", "cat": "食物/飲料"},
    {"en": "lunch", "zh": "午餐", "cat": "食物/飲料"}, {"en": "milk", "zh": "牛奶", "cat": "食物/飲料"},
    {"en": "noodles", "zh": "麵", "cat": "食物/飲料"}, {"en": "orange", "zh": "橘子", "cat": "食物/飲料"},
    {"en": "peach", "zh": "桃子", "cat": "食物/飲料"}, {"en": "pie", "zh": "派", "cat": "食物/飲料"},
    {"en": "pizza", "zh": "披薩", "cat": "食物/飲料"}, {"en": "pork", "zh": "豬肉", "cat": "食物/飲料"},
    {"en": "pumpkin", "zh": "南瓜", "cat": "食物/飲料"}, {"en": "rice", "zh": "米飯", "cat": "食物/飲料"},
    {"en": "salad", "zh": "沙拉", "cat": "食物/飲料"}, {"en": "sandwich", "zh": "三明治", "cat": "食物/飲料"},
    {"en": "soup", "zh": "湯", "cat": "食物/飲料"}, {"en": "strawberry", "zh": "草莓", "cat": "食物/飲料"},
    {"en": "sweet", "zh": "甜的", "cat": "食物/飲料"}, {"en": "tea", "zh": "茶", "cat": "食物/飲料"},
    {"en": "thirsty", "zh": "口渴的", "cat": "食物/飲料"}, {"en": "water", "zh": "水", "cat": "食物/飲料"},
    {"en": "watermelon", "zh": "西瓜", "cat": "食物/飲料"}, {"en": "yummy", "zh": "好吃的", "cat": "食物/飲料"},
    # --- 學校 ---
    {"en": "book", "zh": "書本", "cat": "學校"}, {"en": "classroom", "zh": "教室", "cat": "學校"},
    {"en": "eraser", "zh": "橡皮擦", "cat": "學校"}, {"en": "friend", "zh": "朋友", "cat": "學校"},
    {"en": "homework", "zh": "作業", "cat": "學校"}, {"en": "library", "zh": "圖書館", "cat": "學校"},
    {"en": "pen", "zh": "原子筆", "cat": "學校"}, {"en": "pencil", "zh": "鉛筆", "cat": "學校"},
    {"en": "ruler", "zh": "尺", "cat": "學校"}, {"en": "school", "zh": "學校", "cat": "學校"},
    {"en": "student", "zh": "學生", "cat": "學校"}, {"en": "study", "zh": "研讀", "cat": "學校"},
    {"en": "teacher", "zh": "老師", "cat": "學校"}, {"en": "test", "zh": "考試", "cat": "學校"},
    # --- 身體部位 ---
    {"en": "arm", "zh": "手臂", "cat": "身體部位"}, {"en": "back", "zh": "背部", "cat": "身體部位"},
    {"en": "ear", "zh": "耳朵", "cat": "身體部位"}, {"en": "eye", "zh": "眼睛", "cat": "身體部位"},
    {"en": "face", "zh": "臉", "cat": "身體部位"}, {"en": "foot", "zh": "腳", "cat": "身體部位"},
    {"en": "hair", "zh": "頭髮", "cat": "身體部位"}, {"en": "hand", "zh": "手", "cat": "身體部位"},
    {"en": "head", "zh": "頭", "cat": "身體部位"}, {"en": "leg", "zh": "腿", "cat": "身體部位"},
    {"en": "mouth", "zh": "嘴巴", "cat": "身體部位"}, {"en": "nose", "zh": "鼻子", "cat": "身體部位"},
    {"en": "tooth", "zh": "牙齒", "cat": "身體部位"},
    # --- 地點/方位 ---
    {"en": "bank", "zh": "銀行", "cat": "地點"}, {"en": "beach", "zh": "海灘", "cat": "地點"},
    {"en": "hospital", "zh": "醫院", "cat": "地點"}, {"en": "market", "zh": "市場", "cat": "地點"},
    {"en": "park", "zh": "公園", "cat": "地點"}, {"en": "restaurant", "zh": "餐廳", "cat": "地點"},
    {"en": "store", "zh": "商店", "cat": "地點"}, {"en": "zoo", "zh": "動物園", "cat": "地點"},
    # --- 運輸 ---
    {"en": "airplane", "zh": "飛機", "cat": "運輸"}, {"en": "bicycle", "zh": "腳踏車", "cat": "運輸"},
    {"en": "boat", "zh": "船", "cat": "運輸"}, {"en": "bus", "zh": "公車", "cat": "運輸"},
    {"en": "car", "zh": "汽車", "cat": "運輸"}, {"en": "drive", "zh": "開車", "cat": "運輸"},
    {"en": "motorcycle", "zh": "重型機車", "cat": "運輸"}, {"en": "scooter", "zh": "輕型機車", "cat": "運輸"},
    {"en": "ship", "zh": "輪船", "cat": "運輸"}, {"en": "taxi", "zh": "計程車", "cat": "運輸"},
    {"en": "train", "zh": "火車", "cat": "運輸"}, {"en": "truck", "zh": "卡車", "cat": "運輸"},
    # --- 房子 ---
    {"en": "bathroom", "zh": "浴室", "cat": "房子"}, {"en": "bed", "zh": "床", "cat": "房子"},
    {"en": "bedroom", "zh": "臥室", "cat": "房子"}, {"en": "chair", "zh": "椅子", "cat": "房子"},
    {"en": "clean", "zh": "乾淨的/打掃", "cat": "房子"}, {"en": "computer", "zh": "電腦", "cat": "房子"},
    {"en": "desk", "zh": "書桌", "cat": "房子"}, {"en": "door", "zh": "門", "cat": "房子"},
    {"en": "floor", "zh": "地板", "cat": "房子"}, {"en": "home", "zh": "家", "cat": "房子"},
    {"en": "house", "zh": "房子", "cat": "房子"}, {"en": "key", "zh": "鑰匙", "cat": "房子"},
    {"en": "kitchen", "zh": "廚房", "cat": "房子"}, {"en": "living room", "zh": "客廳", "cat": "房子"},
    {"en": "sofa", "zh": "沙發", "cat": "房子"}, {"en": "table", "zh": "桌子", "cat": "房子"},
    {"en": "telephone", "zh": "電話", "cat": "房子"}, {"en": "TV", "zh": "電視", "cat": "房子"},
    {"en": "window", "zh": "窗戶", "cat": "房子"},
    # --- 其他 ---
    {"en": "happy", "zh": "快樂的", "cat": "狀態/動作"}, {"en": "sad", "zh": "難過的", "cat": "狀態/動作"},
    {"en": "angry", "zh": "生氣的", "cat": "狀態/動作"}, {"en": "tired", "zh": "疲累的", "cat": "狀態/動作"},
    {"en": "jump", "zh": "跳", "cat": "狀態/動作"}, {"en": "run", "zh": "跑", "cat": "狀態/動作"},
    {"en": "sing", "zh": "唱歌", "cat": "狀態/動作"}, {"en": "dance", "zh": "跳舞", "cat": "狀態/動作"},
    {"en": "swim", "zh": "游泳", "cat": "狀態/動作"}, {"en": "sleep", "zh": "睡覺", "cat": "狀態/動作"},
    {"en": "walk", "zh": "走路", "cat": "狀態/動作"}, {"en": "write", "zh": "寫字", "cat": "狀態/動作"}
]

# ---------------------------------------------------------
# 2. 核心功能: JS Audio Player & 工具函數
# ---------------------------------------------------------

def get_audio_base64(text):
    """將文字轉為 base64 音訊資料"""
    try:
        tts = gTTS(text=text, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return base64.b64encode(fp.read()).decode()
    except Exception:
        return None

def play_audio_js(text, key_suffix="", button_text="🔊 點擊發音"):
    """
    產生隱藏的 Audio 標籤與 JS 播放邏輯 (相容 iOS)
    """
    b64_audio = get_audio_base64(text)
    if not b64_audio:
        return
    
    audio_id = f"audio_{key_suffix}_{random.randint(0, 100000)}"
    
    html_code = f"""
        <audio id="{audio_id}" preload="auto">
            <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
        </audio>
        <script>
            function play_{audio_id}() {{
                var a = document.getElementById("{audio_id}");
                a.currentTime = 0;
                a.play().catch(e => console.log(e));
            }}
        </script>
        <button onclick="play_{audio_id}()" class="play-btn">
            {button_text}
        </button>
        <style>
            /* 按鈕樣式 */
            .play-btn {{
                background-color: #4CAF50; border: none; color: white;
                padding: 10px 16px; text-align: center; text-decoration: none;
                display: inline-block; font-size: 14px; margin: 4px 2px;
                cursor: pointer; border-radius: 8px; width: 100%;
                font-family: "Segoe UI", sans-serif;
            }}
            .play-btn:active {{ background-color: #45a049; transform: scale(0.98); }}
        </style>
    """
    components.html(html_code, height=50)

def safe_rerun():
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

def create_cloze_word(word):
    if len(word) <= 2: return word
    chars = list(word)
    num_to_mask = max(1, int(len(word) * 0.4))
    indices = list(range(1, len(word) - 1))
    if indices:
        mask_indices = random.sample(indices, min(len(indices), num_to_mask))
        for i in mask_indices: chars[i] = "_"
    return " ".join(chars)

# ---------------------------------------------------------
# 3. Session State 初始化
# ---------------------------------------------------------
if 'mode' not in st.session_state: st.session_state.mode = "MAIN_MENU"

# 累計歷史數據
if 'total_correct' not in st.session_state: st.session_state.total_correct = 0
if 'total_questions' not in st.session_state: st.session_state.total_questions = 0

if 'game_state' not in st.session_state:
    st.session_state.update({
        'game_state': "START", 
        'score': 0, 'current_idx': 0, 'questions': [], 
        'wrong_list': [], 'options': [], 
        'ans_checked': False, 'selected_opt': None,
        'user_input': "" # 克漏字輸入暫存
    })

# ---------------------------------------------------------
# 4. 版面調整 CSS (解決左上角遮擋與按鈕樣式)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* 增加頂部間距，解決按鈕被遮擋問題 */
    .block-container { 
        padding-top: 4rem; 
        padding-bottom: 2rem; 
    }
    /* 調整標題大小 */
    h1 { font-size: 1.5rem !important; margin-bottom: 0.5rem !important; }
    h2 { font-size: 1.2rem !important; }
    /* 調整按鈕高度 */
    .stButton button { width: 100%; height: 50px; font-size: 18px; margin-top: 0px; }
    /* 減少垂直間距 */
    div[data-testid="stVerticalBlock"] > div { gap: 0.5rem; }
    /* 大字體樣式 */
    .big-word {
        font-size: 3rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. 主程式邏輯
# ---------------------------------------------------------

# --- 模式 A: 聽力測驗 (Listening) ---
def run_listening_mode():
    col_back, col_info = st.columns([1, 2])
    with col_back:
        # 回主選單按鈕
        if st.button("⬅ 回主選單", key="back_btn_lis"):
            st.session_state.mode = "MAIN_MENU"
            st.session_state.game_state = "START"
            safe_rerun()
    with col_info:
        if st.session_state.game_state == "PLAYING":
            st.caption(f"📊 得分: {st.session_state.score} | 進度: {st.session_state.current_idx + 1}/20")

    if st.session_state.game_state == "START":
        st.header("🎧 聽力測驗")
        cats = sorted(list(set([w['cat'] for w in WORD_BANK])))
        selected = st.selectbox("選擇主題：", ["全部隨機"] + cats)
        if st.button("開始 (20題)", use_container_width=True):
            pool = WORD_BANK if selected == "全部隨機" else [w for w in WORD_BANK if w['cat'] == selected]
            st.session_state.questions = random.sample(pool, min(len(pool), 20))
            st.session_state.game_state = "PLAYING"
            st.session_state.current_idx = 0
            st.session_state.score = 0
            st.session_state.wrong_list = []
            st.session_state.options = []
            st.session_state.ans_checked = False
            st.session_state.selected_opt = None
            safe_rerun()

    elif st.session_state.game_state == "PLAYING":
        q = st.session_state.questions[st.session_state.current_idx]
        
        # 題目區：單字(放大)與發音並排
        # 調整 column 比例讓按鈕不被切到
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown(f"<div class='big-word'>{q['en']}</div>", unsafe_allow_html=True)
        with c2:
            # 使用空容器調整垂直位置，讓按鈕對齊文字中心
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            play_audio_js(q['en'], key_suffix=f"lis_{st.session_state.current_idx}", button_text="🔊")

        if not st.session_state.options:
            wrong = [w['zh'] for w in WORD_BANK if w['zh'] != q['zh']]
            if len(wrong) < 3: wrong = wrong * 3
            opts = random.sample(wrong, 3) + [q['zh']]
            random.shuffle(opts)
            st.session_state.options = opts

        # 選項區 (2x2)
        opts = st.session_state.options
        for i in range(0, 4, 2):
            col_a, col_b = st.columns(2)
            with col_a:
                opt_text = opts[i]
                if st.button(opt_text, key=f"opt_{i}", use_container_width=True, disabled=st.session_state.ans_checked):
                    check_answer(opt_text, q, q['zh'])
            with col_b:
                if i+1 < 4:
                    opt_text = opts[i+1]
                    if st.button(opt_text, key=f"opt_{i+1}", use_container_width=True, disabled=st.session_state.ans_checked):
                        check_answer(opt_text, q, q['zh'])

        # 結果回饋區
        if st.session_state.ans_checked:
            st.write("---")
            if st.session_state.selected_opt == q['zh']:
                st.success("✅ 答對了！")
            else:
                st.error(f"❌ 答錯了！正確是：{q['zh']}")
            
            if st.button("下一題 ➡", use_container_width=True, type="primary"):
                next_question()

    elif st.session_state.game_state == "FINISH":
        show_results()

# --- 模式 B: 克漏字測驗 (Cloze - 填字版) ---
def run_cloze_mode():
    col_back, col_info = st.columns([1, 2])
    with col_back:
        if st.button("⬅ 回主選單", key="back_btn_cloze"):
            st.session_state.mode = "MAIN_MENU"
            st.session_state.game_state = "START"
            safe_rerun()
    with col_info:
        if st.session_state.game_state == "PLAYING":
            st.caption(f"📊 得分: {st.session_state.score} | 進度: {st.session_state.current_idx + 1}/20")

    if st.session_state.game_state == "START":
        st.header("🔤 克漏字")
        cats = sorted(list(set([w['cat'] for w in WORD_BANK])))
        selected = st.selectbox("選擇主題：", ["全部隨機"] + cats)
        if st.button("開始 (20題)", use_container_width=True):
            pool = WORD_BANK if selected == "全部隨機" else [w for w in WORD_BANK if w['cat'] == selected]
            st.session_state.questions = random.sample(pool, min(len(pool), 20))
            st.session_state.game_state = "PLAYING"
            st.session_state.current_idx = 0
            st.session_state.score = 0
            st.session_state.wrong_list = []
            st.session_state.ans_checked = False
            st.session_state.user_input = ""
            safe_rerun()

    elif st.session_state.game_state == "PLAYING":
        q = st.session_state.questions[st.session_state.current_idx]
        
        # 產生挖空單字
        cloze_key = f"cloze_word_{st.session_state.current_idx}"
        if cloze_key not in st.session_state:
            st.session_state[cloze_key] = create_cloze_word(q['en'])

        # 顯示題目與發音按鈕 (並排)
        st.caption(f"中文提示：{q['zh']}")
        
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown(f"<h2 style='text-align: center; letter-spacing: 2px;'>{st.session_state[cloze_key]}</h2>", unsafe_allow_html=True)
        with c2:
            play_audio_js(q['en'], key_suffix=f"cloze_{st.session_state.current_idx}", button_text="🔊 聽提示")

        # 使用 form 來處理輸入
        with st.form(key=f"cloze_form_{st.session_state.current_idx}"):
            # 輸入框
            user_ans = st.text_input("請輸入完整單字：", value="", disabled=st.session_state.ans_checked)
            # 提交按鈕
            submit_btn = st.form_submit_button("提交答案", disabled=st.session_state.ans_checked)
        
        # 處理提交邏輯
        if submit_btn and not st.session_state.ans_checked:
            st.session_state.ans_checked = True
            st.session_state.user_input = user_ans
            st.session_state.total_questions += 1
            
            if user_ans.strip().lower() == q['en'].lower():
                st.session_state.score += 5
                st.session_state.total_correct += 1
                st.session_state.is_correct = True
            else:
                st.session_state.wrong_list.append(q)
                st.session_state.is_correct = False
            safe_rerun()

        # 結果回饋區
        if st.session_state.ans_checked:
            st.write("---")
            if st.session_state.is_correct:
                st.success(f"✅ 正確！答案是：{q['en']}")
            else:
                st.error(f"❌ 錯誤！正確答案是：{q['en']}")
            
            if st.button("下一題 ➡", use_container_width=True, type="primary"):
                # 清除舊的暫存
                old_cloze_key = f"cloze_word_{st.session_state.current_idx}"
                if old_cloze_key in st.session_state: del st.session_state[old_cloze_key]
                next_question()

    elif st.session_state.game_state == "FINISH":
        show_results()

# 共用邏輯函數
def check_answer(selected, question, correct_val):
    st.session_state.selected_opt = selected
    st.session_state.ans_checked = True
    st.session_state.total_questions += 1
    if selected == correct_val:
        st.session_state.score += 5
        st.session_state.total_correct += 1
    else:
        st.session_state.wrong_list.append(question)
    safe_rerun()

def next_question():
    st.session_state.current_idx += 1
    st.session_state.ans_checked = False
    st.session_state.options = []
    st.session_state.user_input = "" # 清空輸入框
    if st.session_state.current_idx >= len(st.session_state.questions):
        st.session_state.game_state = "FINISH"
    safe_rerun()

def show_results():
    st.balloons()
    st.header("🏆 測驗結束")
    st.metric("本輪得分", f"{st.session_state.score} 分")
    
    if st.session_state.wrong_list:
        st.subheader("📖 錯題複習")
        for i, w in enumerate(st.session_state.wrong_list):
            st.write("---")
            c1, c2 = st.columns([3, 1])
            with c1:
                st.write(f"**{w['en']}**")
                st.write(w['zh'])
            with c2:
                play_audio_js(w['en'], key_suffix=f"rev_{i}", button_text="🔊")
    else:
        st.success("全對！太棒了！")

    st.write("---")
    if st.button("回主選單", use_container_width=True):
        st.session_state.mode = "MAIN_MENU"
        st.session_state.game_state = "START"
        safe_rerun()

# --- 主程式進入點 ---
if st.session_state.mode == "MAIN_MENU":
    st.title("🎓 小學英檢單字王")
    
    # 統計數據顯示
    if st.session_state.total_questions > 0:
        acc = int((st.session_state.total_correct / st.session_state.total_questions) * 100)
        st.info(f"📊 累積練習：{st.session_state.total_questions} 題 | 總答對率：{acc}%")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎧 聽力測驗\n(聽英選中)", use_container_width=True):
            st.session_state.mode = "LISTENING"
            st.session_state.game_state = "START"
            safe_rerun()
    with col2:
        if st.button("🔤 克漏字\n(填空練習)", use_container_width=True):
            st.session_state.mode = "CLOZE"
            st.session_state.game_state = "START"
            safe_rerun()

elif st.session_state.mode == "LISTENING":
    run_listening_mode()

elif st.session_state.mode == "CLOZE":
    run_cloze_mode()


