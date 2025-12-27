import streamlit as st
import random
from gtts import gTTS
import io

# 完整單字庫資料 (依據 PDF 1-19 頁提取)
WORD_BANK = [
    # 動物/昆蟲 [cite: 2]
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
    # 衣服配件 [cite: 2, 5]
    {"en": "bag", "zh": "袋子", "cat": "衣服配件"}, {"en": "cap", "zh": "棒球帽", "cat": "衣服配件"},
    {"en": "clothes", "zh": "衣服", "cat": "衣服配件"}, {"en": "coat", "zh": "外套", "cat": "衣服配件"},
    {"en": "dress", "zh": "洋裝", "cat": "衣服配件"}, {"en": "glasses", "zh": "眼鏡", "cat": "衣服配件"},
    {"en": "hat", "zh": "帽子", "cat": "衣服配件"}, {"en": "jacket", "zh": "夾克、外套", "cat": "衣服配件"},
    {"en": "pants", "zh": "長褲", "cat": "衣服配件"}, {"en": "shoes", "zh": "鞋子", "cat": "衣服配件"},
    {"en": "shorts", "zh": "短褲", "cat": "衣服配件"}, {"en": "skirt", "zh": "裙子", "cat": "衣服配件"},
    {"en": "socks", "zh": "襪子", "cat": "衣服配件"}, {"en": "sweater", "zh": "毛衣", "cat": "衣服配件"},
    {"en": "T-shirt", "zh": "T恤", "cat": "衣服配件"}, {"en": "umbrella", "zh": "傘", "cat": "衣服配件"},
    # 顏色 [cite: 5]
    {"en": "black", "zh": "黑色的", "cat": "顏色"}, {"en": "blue", "zh": "藍色的", "cat": "顏色"},
    {"en": "brown", "zh": "咖啡色的", "cat": "顏色"}, {"en": "gray", "zh": "灰色的", "cat": "顏色"},
    {"en": "green", "zh": "綠色的", "cat": "顏色"}, {"en": "orange", "zh": "橘色的", "cat": "顏色"},
    {"en": "pink", "zh": "粉紅色的", "cat": "顏色"}, {"en": "purple", "zh": "紫色的", "cat": "顏色"},
    {"en": "red", "zh": "紅色的", "cat": "顏色"}, {"en": "white", "zh": "白色的", "cat": "顏色"},
    {"en": "yellow", "zh": "黃色的", "cat": "顏色"},
    # 家庭 [cite: 5, 8]
    {"en": "aunt", "zh": "阿姨、姑姑、伯母、舅媽", "cat": "家庭"}, {"en": "brother", "zh": "哥哥、弟弟", "cat": "家庭"},
    {"en": "cousin", "zh": "堂兄(弟、姊、妹)", "cat": "家庭"}, {"en": "daughter", "zh": "女兒", "cat": "家庭"},
    {"en": "family", "zh": "家庭、家人", "cat": "家庭"}, {"en": "father", "zh": "爸爸", "cat": "家庭"},
    {"en": "grandfather", "zh": "外公、爺爺", "cat": "家庭"}, {"en": "mother", "zh": "媽媽", "cat": "家庭"},
    {"en": "sister", "zh": "姐姐、妹妹", "cat": "家庭"}, {"en": "son", "zh": "兒子", "cat": "家庭"},
    {"en": "uncle", "zh": "叔叔、舅舅、姑丈、姨丈", "cat": "家庭"},
    # 食物/飲料 [cite: 8, 11]
    {"en": "apple", "zh": "蘋果", "cat": "食物/飲料"}, {"en": "banana", "zh": "香蕉", "cat": "食物/飲料"},
    {"en": "beef", "zh": "牛肉", "cat": "食物/飲料"}, {"en": "bread", "zh": "麵包", "cat": "食物/飲料"},
    {"en": "cake", "zh": "蛋糕", "cat": "食物/飲料"}, {"en": "candy", "zh": "糖果", "cat": "食物/飲料"},
    {"en": "chocolate", "zh": "巧克力", "cat": "食物/飲料"}, {"en": "dumpling", "zh": "水餃", "cat": "食物/飲料"},
    {"en": "hamburger", "zh": "漢堡", "cat": "食物/飲料"}, {"en": "ice cream", "zh": "冰淇淋", "cat": "食物/飲料"},
    {"en": "juice", "zh": "果汁", "cat": "食物/飲料"}, {"en": "milk", "zh": "牛奶", "cat": "食物/飲料"},
    {"en": "noodles", "zh": "麵", "cat": "食物/飲料"}, {"en": "pizza", "zh": "披薩", "cat": "食物/飲料"},
    {"en": "sandwich", "zh": "三明治", "cat": "食物/飲料"}, {"en": "soup", "zh": "湯", "cat": "食物/飲料"},
    {"en": "strawberry", "zh": "草莓", "cat": "食物/飲料"}, {"en": "water", "zh": "水", "cat": "食物/飲料"},
    {"en": "watermelon", "zh": "西瓜", "cat": "食物/飲料"},
    # 運輸 [cite: 39]
    {"en": "airplane", "zh": "飛機", "cat": "運輸"}, {"en": "bicycle", "zh": "腳踏車", "cat": "運輸"},
    {"en": "bus", "zh": "公車", "cat": "運輸"}, {"en": "car", "zh": "車子", "cat": "運輸"},
    {"en": "motorcycle", "zh": "摩托車", "cat": "運輸"}, {"en": "train", "zh": "火車", "cat": "運輸"},
    {"en": "taxi", "zh": "計程車", "cat": "運輸"}, {"en": "scooter", "zh": "輕型機車", "cat": "運輸"},
    # 學校 [cite: 30]
    {"en": "book", "zh": "書、書本", "cat": "學校"}, {"en": "classroom", "zh": "教室", "cat": "學校"},
    {"en": "eraser", "zh": "橡皮擦", "cat": "學校"}, {"en": "homework", "zh": "回家作業", "cat": "學校"},
    {"en": "library", "zh": "圖書館", "cat": "學校"}, {"en": "pencil", "zh": "鉛筆", "cat": "學校"},
    {"en": "teacher", "zh": "老師", "cat": "學校"}, {"en": "test", "zh": "考試", "cat": "學校"},
    # 身體部位 [cite: 21, 24]
    {"en": "arm", "zh": "手臂", "cat": "身體部位"}, {"en": "ear", "zh": "耳朵", "cat": "身體部位"},
    {"en": "eye", "zh": "眼睛", "cat": "身體部位"}, {"en": "face", "zh": "臉", "cat": "身體部位"},
    {"en": "foot", "zh": "腳", "cat": "身體部位"}, {"en": "hair", "zh": "頭髮", "cat": "身體部位"},
    {"en": "hand", "zh": "手", "cat": "身體部位"}, {"en": "mouth", "zh": "嘴巴", "cat": "身體部位"},
    {"en": "nose", "zh": "鼻子", "cat": "身體部位"}, {"en": "tooth", "zh": "牙齒", "cat": "身體部位"},
    # 地點/方位 [cite: 27]
    {"en": "bank", "zh": "銀行", "cat": "地點/方位"}, {"en": "hospital", "zh": "醫院", "cat": "地點/方位"},
    {"en": "market", "zh": "市場", "cat": "地點/方位"}, {"en": "park", "zh": "公園", "cat": "地點/方位"},
    {"en": "restaurant", "zh": "餐廳", "cat": "地點/方位"}, {"en": "zoo", "zh": "動物園", "cat": "地點/方位"}
]

# 跨版本相容的重新整理函數
def safe_rerun():
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

def get_audio(text):
    tts = gTTS(text=text, lang='en')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

# 初始化狀態
if 'game_state' not in st.session_state:
    st.session_state.update({
        'game_state': "START", 'score': 0, 'current_idx': 0,
        'questions': [], 'wrong_list': [], 'options': []
    })

st.set_page_config(page_title="GEPT Kids 單字練習", page_icon="📝")
st.title("📝 小學英檢單字王")

# --- 1. 開始畫面 ---
if st.session_state.game_state == "START":
    cats = sorted(list(set([w['cat'] for w in WORD_BANK])))
    selected = st.selectbox("選擇要練習的主題：", ["全部隨機"] + cats)
    
    if st.button("開始挑戰 (20題)", use_container_width=True):
        pool = WORD_BANK if selected == "全部隨機" else [w for w in WORD_BANK if w['cat'] == selected]
        # 確保不會抽取超過現有數量的題目
        num_q = min(len(pool), 20)
        st.session_state.questions = random.sample(pool, num_q)
        st.session_state.game_state = "PLAYING"
        st.session_state.current_idx = 0
        st.session_state.score = 0
        st.session_state.wrong_list = []
        st.session_state.options = []
        safe_rerun()

# --- 2. 遊戲進行中 ---
elif st.session_state.game_state == "PLAYING":
    q_list = st.session_state.questions
    idx = st.session_state.current_idx
    q = q_list[idx]
    
    st.write(f"進度：{idx + 1} / {len(q_list)}")
    st.header(f"英文單字：{q['en']}")
    
    # 自動播放發音
    audio_data = get_audio(q['en'])
    st.audio(audio_data, format='audio/mp3')
    
    # 準備選項 (僅在換題時重新計算)
    if not st.session_state.options or len(st.session_state.options) == 0:
        wrong_candidates = [w['zh'] for w in WORD_BANK if w['zh'] != q['zh']]
        opts = random.sample(wrong_candidates, 3) + [q['zh']]
        random.shuffle(opts)
        st.session_state.options = opts

    # 顯示按鈕
    for opt in st.session_state.options:
        if st.button(opt, key=f"btn_{idx}_{opt}", use_container_width=True):
            if opt == q['zh']:
                st.success("✅ 答對了！")
                st.session_state.score += 5
            else:
                st.error(f"❌ 答錯了！正確答案是：{q['zh']}")
                st.session_state.wrong_list.append(q)
            
            # 延遲後進入下一題
            st.session_state.current_idx += 1
            st.session_state.options = [] # 清空選項供下一題使用
            
            if st.session_state.current_idx >= len(q_list):
                st.session_state.game_state = "FINISH"
            
            # 使用按鈕觸發重新渲染
            if st.button("點擊進入下一題" if st.session_state.game_state == "PLAYING" else "查看結果"):
                safe_rerun()

# --- 3. 結束與複習 ---
elif st.session_state.game_state == "FINISH":
    st.balloons()
    st.header("🏁 挑戰結束！")
    st.metric("總分", f"{st.session_state.score} 分")
    
    if st.session_state.wrong_list:
        st.subheader("📖 錯題複習 (聽聽看發音)")
        for w in st.session_state.wrong_list:
            col1, col2 = st.columns([3, 1])
            col1.write(f"**{w['en']}** : {w['zh']}")
            if col2.button("🔊", key=f"rev_{w['en']}"):
                st.audio(get_audio(w['en']), autoplay=True)
    else:
        st.success("太強了！完全沒有錯題！")
        
    if st.button("回首頁重新開始", use_container_width=True):
        st.session_state.game_state = "START"
        safe_rerun()
