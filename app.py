import streamlit as st
import random
from gtts import gTTS
import io
import base64
import time

# ---------------------------------------------------------
# 1. 單字資料庫 (內容不變)
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
    {"en": "panda", "zh": "大貓熊", "cat": "動物/昆蟲"}, {"en": "rabbit", "zh": "兔子", "cat": "動物/昆蟲"},
    {"en": "sheep", "zh": "綿羊", "cat": "動物/昆蟲"}, {"en": "snake", "zh": "蛇", "cat": "動物/昆蟲"},
    {"en": "tiger", "zh": "老虎", "cat": "動物/昆蟲"}, {"en": "whale", "zh": "鯨魚", "cat": "動物/昆蟲"},
    {"en": "zebra", "zh": "斑馬", "cat": "動物/昆蟲"},
    # --- 衣服配件 ---
    {"en": "bag", "zh": "袋子", "cat": "衣服配件"}, {"en": "cap", "zh": "棒球帽", "cat": "衣服配件"},
    {"en": "clothes", "zh": "衣服", "cat": "衣服配件"}, {"en": "coat", "zh": "外套", "cat": "衣服配件"},
    {"en": "dress", "zh": "洋裝", "cat": "衣服配件"}, {"en": "glasses", "zh": "眼鏡", "cat": "衣服配件"},
    {"en": "hat", "zh": "帽子", "cat": "衣服配件"}, {"en": "jacket", "zh": "夾克", "cat": "衣服配件"},
    {"en": "pants", "zh": "長褲", "cat": "衣服配件"}, {"en": "shoes", "zh": "鞋子", "cat": "衣服配件"},
    {"en": "shorts", "zh": "短褲", "cat": "衣服配件"}, {"en": "skirt", "zh": "裙子", "cat": "衣服配件"},
    {"en": "socks", "zh": "襪子", "cat": "衣服配件"}, {"en": "sweater", "zh": "毛衣", "cat": "衣服配件"},
    {"en": "T-shirt", "zh": "T恤", "cat": "衣服配件"}, {"en": "umbrella", "zh": "傘", "cat": "衣服配件"},
    # --- 顏色 ---
    {"en": "black", "zh": "黑色的", "cat": "顏色"}, {"en": "blue", "zh": "藍色的", "cat": "顏色"},
    {"en": "brown", "zh": "咖啡色的", "cat": "顏色"}, {"en": "gray", "zh": "灰色的", "cat": "顏色"},
    {"en": "green", "zh": "綠色的", "cat": "顏色"}, {"en": "orange", "zh": "橘色的", "cat": "顏色"},
    {"en": "pink", "zh": "粉紅色的", "cat": "顏色"}, {"en": "purple", "zh": "紫色的", "cat": "顏色"},
    {"en": "red", "zh": "紅色的", "cat": "顏色"}, {"en": "white", "zh": "白色的", "cat": "顏色"},
    {"en": "yellow", "zh": "黃色的", "cat": "顏色"},
    # --- 家庭 ---
    {"en": "aunt", "zh": "阿姨、姑姑", "cat": "家庭"}, {"en": "brother", "zh": "哥哥、弟弟", "cat": "家庭"},
    {"en": "cousin", "zh": "堂表兄弟姊妹", "cat": "家庭"}, {"en": "daughter", "zh": "女兒", "cat": "家庭"},
    {"en": "family", "zh": "家庭、家人", "cat": "家庭"}, {"en": "father", "zh": "爸爸", "cat": "家庭"},
    {"en": "grandfather", "zh": "外公、爺爺", "cat": "家庭"}, {"en": "mother", "zh": "媽媽", "cat": "家庭"},
    {"en": "sister", "zh": "姐姐、妹妹", "cat": "家庭"}, {"en": "son", "zh": "兒子", "cat": "家庭"},
    {"en": "uncle", "zh": "叔叔、舅舅", "cat": "家庭"},
    # --- 食物/飲料 ---
    {"en": "apple", "zh": "蘋果", "cat": "食物/飲料"}, {"en": "banana", "zh": "香蕉", "cat": "食物/飲料"},
    {"en": "beef", "zh": "牛肉", "cat": "食物/飲料"}, {"en": "bread", "zh": "麵包", "cat": "食物/飲料"},
    {"en": "cake", "zh": "蛋糕", "cat": "食物/飲料"}, {"en": "candy", "zh": "糖果", "cat": "食物/飲料"},
    {"en": "chocolate", "zh": "巧克力", "cat": "食物/飲料"}, {"en": "dumpling", "zh": "水餃", "cat": "食物/飲料"},
    {"en": "hamburger", "zh": "漢堡", "cat": "食物/飲料"}, {"en": "ice cream", "zh": "冰淇淋", "cat": "食物/飲料"},
    {"en": "juice", "zh": "果汁", "cat": "食物/飲料"}, {"en": "milk", "zh": "牛奶", "cat": "食物/飲料"},
    {"en": "noodles", "zh": "麵", "cat": "食物/飲料"}, {"en": "pizza", "zh": "披薩", "cat": "食物/飲料"},
    {"en": "sandwich", "zh": "三明治", "cat": "食物/飲料"}, {"en": "soup", "zh": "湯", "cat": "食物/飲料"},
    {"en": "strawberry", "zh": "草莓", "cat": "食物/飲料"}, {"en": "water", "zh": "水", "cat": "食物/飲料"},
    # --- 運輸 ---
    {"en": "airplane", "zh": "飛機", "cat": "運輸"}, {"en": "bicycle", "zh": "腳踏車", "cat": "運輸"},
    {"en": "bus", "zh": "公車", "cat": "運輸"}, {"en": "car", "zh": "車子", "cat": "運輸"},
    {"en": "motorcycle", "zh": "摩托車", "cat": "運輸"}, {"en": "train", "zh": "火車", "cat": "運輸"},
    {"en": "taxi", "zh": "計程車", "cat": "運輸"}, {"en": "scooter", "zh": "輕型機車", "cat": "運輸"},
    # --- 學校 ---
    {"en": "book", "zh": "書本", "cat": "學校"}, {"en": "classroom", "zh": "教室", "cat": "學校"},
    {"en": "eraser", "zh": "橡皮擦", "cat": "學校"}, {"en": "homework", "zh": "作業", "cat": "學校"},
    {"en": "pencil", "zh": "鉛筆", "cat": "學校"}, {"en": "teacher", "zh": "老師", "cat": "學校"},
    # --- 身體部位 ---
    {"en": "arm", "zh": "手臂", "cat": "身體部位"}, {"en": "ear", "zh": "耳朵", "cat": "身體部位"},
    {"en": "eye", "zh": "眼睛", "cat": "身體部位"}, {"en": "face", "zh": "臉", "cat": "身體部位"},
    {"en": "foot", "zh": "腳", "cat": "身體部位"}, {"en": "hand", "zh": "手", "cat": "身體部位"},
    {"en": "mouth", "zh": "嘴巴", "cat": "身體部位"}, {"en": "nose", "zh": "鼻子", "cat": "身體部位"},
    # --- 地點/方位 ---
    {"en": "bank", "zh": "銀行", "cat": "地點"}, {"en": "hospital", "zh": "醫院", "cat": "地點"},
    {"en": "park", "zh": "公園", "cat": "地點"}, {"en": "restaurant", "zh": "餐廳", "cat": "地點"},
    {"en": "zoo", "zh": "動物園", "cat": "地點"},
    # --- 動作 ---
    {"en": "run", "zh": "跑", "cat": "動作"}, {"en": "jump", "zh": "跳", "cat": "動作"},
    {"en": "sing", "zh": "唱歌", "cat": "動作"}, {"en": "swim", "zh": "游泳", "cat": "動作"},
    {"en": "dance", "zh": "跳舞", "cat": "動作"}, {"en": "sleep", "zh": "睡覺", "cat": "動作"}
]

# ---------------------------------------------------------
# 2. 核心功能函數: 修正版
# ---------------------------------------------------------

def get_audio_html(text, unique_key, autoplay_switch=True):
    """
    產生一個 HTML5 audio 標籤。
    新增 autoplay_switch 參數：控制是否自動播放。
    """
    try:
        # 產生聲音資料
        tts = gTTS(text=text, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        audio_base64 = base64.b64encode(fp.read()).decode()
        
        # 產生唯一 ID
        player_id = f"audio_{unique_key}_{int(time.time())}"
        
        # 決定是否加入 autoplay 屬性
        autoplay_attr = "autoplay" if autoplay_switch else ""
        
        # HTML 結構 (加入 onerror 處理與 JS 輔助)
        audio_html = f"""
        <audio id="{player_id}" controls {autoplay_attr} style="width: 100%;">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            您的瀏覽器不支援音訊播放。
        </audio>
        """
        
        # 如果需要自動播放，為了確保在換題時真的會播，
        # 我們加入一段 JS 來 "推" 它一把 (針對某些頑固的瀏覽器)
        if autoplay_switch:
            audio_html += f"""
            <script>
                var audio = document.getElementById("{player_id}");
                if (audio) {{
                    audio.play().catch(function(error) {{
                        console.log("Autoplay blocked: " + error);
                    }});
                }}
            </script>
            """
            
        return audio_html
    except Exception as e:
        return f"<div>語音載入錯誤: {str(e)}</div>"

def safe_rerun():
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

# ---------------------------------------------------------
# 3. Session State 初始化
# ---------------------------------------------------------
if 'game_state' not in st.session_state:
    st.session_state.update({
        'game_state': "START", 
        'score': 0, 
        'current_idx': 0,
        'questions': [], 
        'wrong_list': [], 
        'options': [], 
        'ans_checked': False, 
        'selected_opt': None
    })

# ---------------------------------------------------------
# 4. 介面與邏輯
# ---------------------------------------------------------
st.set_page_config(page_title="GEPT Kids 單字練習", page_icon="📝")
st.title("小學英檢單字王")

# --- 階段 A: 開始選單 ---
if st.session_state.game_state == "START":
    cats = sorted(list(set([w['cat'] for w in WORD_BANK])))
    selected = st.selectbox("請選擇練習主題：", ["全部隨機"] + cats)
    
    if st.button("開始挑戰 (20題)", use_container_width=True):
        pool = WORD_BANK if selected == "全部隨機" else [w for w in WORD_BANK if w['cat'] == selected]
        num_q = min(len(pool), 20)
        st.session_state.questions = random.sample(pool, num_q)
        st.session_state.game_state = "PLAYING"
        st.session_state.current_idx = 0
        st.session_state.score = 0
        st.session_state.wrong_list = []
        st.session_state.options = []
        st.session_state.ans_checked = False
        st.session_state.selected_opt = None
        safe_rerun()

# --- 階段 B: 遊戲進行中 ---
elif st.session_state.game_state == "PLAYING":
    q_list = st.session_state.questions
    idx = st.session_state.current_idx
    q = q_list[idx]
    
    st.caption(f"進度：第 {idx + 1} 題 / 共 {len(q_list)} 題")
    st.header(q['en'])
    
    # ------------------------------------------------
    # 聲音播放區域 (重點修正)
    # ------------------------------------------------
    # 在遊戲進行中，我們希望自動播放，所以 autoplay_switch=True
    html_player = get_audio_html(q['en'], f"q{idx}_{q['en']}", autoplay_switch=True)
    st.markdown(html_player, unsafe_allow_html=True)
    
    # 選項產生
    if not st.session_state.options:
        wrong_candidates = [w['zh'] for w in WORD_BANK if w['zh'] != q['zh']]
        opts = random.sample(wrong_candidates, 3) + [q['zh']]
        random.shuffle(opts)
        st.session_state.options = opts

    st.write("---") 

    # === 選項顯示區域 ===
    if not st.session_state.ans_checked:
        st.subheader("請選擇正確意思：")
        for opt in st.session_state.options:
            if st.button(opt, use_container_width=True):
                st.session_state.selected_opt = opt
                st.session_state.ans_checked = True
                if opt == q['zh']:
                    st.session_state.score += 5
                else:
                    st.session_state.wrong_list.append(q)
                safe_rerun()

    else:
        st.subheader("答案核對：")
        for opt in st.session_state.options:
            if opt == q['zh']:
                st.success(f"{opt} (正確答案)")
            elif opt == st.session_state.selected_opt:
                st.error(f"{opt} (您的選擇)")
            else:
                st.info(opt)

        st.write("") 
        st.write("---") 
        if st.button("下一題", use_container_width=True, type="primary"):
            st.session_state.current_idx += 1
            st.session_state.options = []
            st.session_state.ans_checked = False
            st.session_state.selected_opt = None
            if st.session_state.current_idx >= len(q_list):
                st.session_state.game_state = "FINISH"
            safe_rerun()

# --- 階段 C: 結算畫面 ---
elif st.session_state.game_state == "FINISH":
    st.balloons()
    st.header("挑戰結束！")
    
    st.metric("最終得分", f"{st.session_state.score} 分")
    
    if st.session_state.score == 100:
        st.success("太厲害了！全部答對！")
    elif st.session_state.score >= 80:
        st.info("很棒喔！繼續保持！")
    else:
        st.warning("再接再厲，多練習幾次會更強！")

    if st.session_state.wrong_list:
        st.markdown("### 錯題複習")
        st.info("點擊播放器按鈕聆聽發音") # 提示使用者手動播放
        for i, w in enumerate(st.session_state.wrong_list):
            st.write("---")
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(w['en'])
                st.write(w['zh'])
            with col2:
                # ------------------------------------------------
                # 複習區域 (重點修正)
                # ------------------------------------------------
                # 在列表顯示時，絕對不能自動播放，否則會全部一起響
                # 設定 autoplay_switch=False
                review_html = get_audio_html(w['en'], f"rev_{i}_{w['en']}", autoplay_switch=False)
                st.markdown(review_html, unsafe_allow_html=True)
    
    st.write("---")
    if st.button("回首頁重新開始", use_container_width=True):
        st.session_state.game_state = "START"
        safe_rerun()


