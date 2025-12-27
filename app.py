import streamlit as st
import random
from gtts import gTTS
import io

# 完整小學英檢單字資料庫 (依據提供資料整理)
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
    {"en": "hat", "zh": "帽子", "cat": "衣服配件"}, {"en": "jacket", "zh": "夾克", "cat": "衣服配件"},
    {"en": "pants", "zh": "長褲", "cat": "衣服配件"}, {"en": "shoes", "zh": "鞋子", "cat": "衣服配件"},
    {"en": "socks", "zh": "襪子", "cat": "衣服配件"}, {"en": "sweater", "zh": "毛衣", "cat": "衣服配件"},
    {"en": "T-shirt", "zh": "T恤", "cat": "衣服配件"}, {"en": "umbrella", "zh": "傘", "cat": "衣服配件"},

    # 顏色 [cite: 5]
    {"en": "black", "zh": "黑色的", "cat": "顏色"}, {"en": "blue", "zh": "藍色的", "cat": "顏色"},
    {"en": "brown", "zh": "咖啡色", "cat": "顏色"}, {"en": "green", "zh": "綠色", "cat": "顏色"},
    {"en": "orange", "zh": "橘色", "cat": "顏色"}, {"en": "pink", "zh": "粉紅色", "cat": "顏色"},
    {"en": "purple", "zh": "紫色", "cat": "顏色"}, {"en": "red", "zh": "紅色", "cat": "顏色"},
    {"en": "white", "zh": "白色", "cat": "顏色"}, {"en": "yellow", "zh": "黃色", "cat": "顏色"},

    # 家庭 [cite: 5, 8]
    {"en": "aunt", "zh": "阿姨/姑姑", "cat": "家庭"}, {"en": "brother", "zh": "兄弟", "cat": "家庭"},
    {"en": "cousin", "zh": "堂表兄弟姊妹", "cat": "家庭"}, {"en": "dad", "zh": "爸爸", "cat": "家庭"},
    {"en": "family", "zh": "家庭", "cat": "家庭"}, {"en": "father", "zh": "爸爸", "cat": "家庭"},
    {"en": "grandma", "zh": "奶奶/外婆", "cat": "家庭"}, {"en": "grandpa", "zh": "爺爺/外公", "cat": "家庭"},
    {"en": "mother", "zh": "媽媽", "cat": "家庭"}, {"en": "sister", "zh": "姊妹", "cat": "家庭"},
    {"en": "son", "zh": "兒子", "cat": "家庭"}, {"en": "uncle", "zh": "叔叔/舅舅", "cat": "家庭"},

    # 食物/飲料 [cite: 8, 11]
    {"en": "apple", "zh": "蘋果", "cat": "食物/飲料"}, {"en": "banana", "zh": "香蕉", "cat": "食物/飲料"},
    {"en": "beef", "zh": "牛肉", "cat": "食物/飲料"}, {"en": "bread", "zh": "麵包", "cat": "食物/飲料"},
    {"en": "cake", "zh": "蛋糕", "cat": "食物/飲料"}, {"en": "candy", "zh": "糖果", "cat": "食物/飲料"},
    {"en": "chocolate", "zh": "巧克力", "cat": "食物/飲料"}, {"en": "coffee", "zh": "咖啡", "cat": "食物/飲料"},
    {"en": "dumpling", "zh": "水餃", "cat": "食物/飲料"}, {"en": "egg", "zh": "蛋", "cat": "食物/飲料"},
    {"en": "hamburger", "zh": "漢堡", "cat": "食物/飲料"}, {"en": "ice cream", "zh": "冰淇淋", "cat": "食物/飲料"},
    {"en": "milk", "zh": "牛奶", "cat": "食物/飲料"}, {"en": "pizza", "zh": "披薩", "cat": "食物/飲料"},
    {"en": "sandwich", "zh": "三明治", "cat": "食物/飲料"}, {"en": "soup", "zh": "湯", "cat": "食物/飲料"},

    # 運輸 [cite: 39, 42]
    {"en": "airplane", "zh": "飛機", "cat": "運輸"}, {"en": "bicycle", "zh": "腳踏車", "cat": "運輸"},
    {"en": "bus", "zh": "公車", "cat": "運輸"}, {"en": "car", "zh": "車子", "cat": "運輸"},
    {"en": "motorcycle", "zh": "摩托車", "cat": "運輸"}, {"en": "train", "zh": "火車", "cat": "運輸"},

    # 學校 [cite: 30, 33]
    {"en": "book", "zh": "書本", "cat": "學校"}, {"en": "classroom", "zh": "教室", "cat": "學校"},
    {"en": "eraser", "zh": "橡皮擦", "cat": "學校"}, {"en": "homework", "zh": "作業", "cat": "學校"},
    {"en": "pencil", "zh": "鉛筆", "cat": "學校"}, {"en": "teacher", "zh": "老師", "cat": "學校"},

    # 其他形容詞/動詞 [cite: 51, 54, 57]
    {"en": "happy", "zh": "高興的", "cat": "形容詞"}, {"en": "angry", "zh": "生氣的", "cat": "形容詞"},
    {"en": "beautiful", "zh": "美麗的", "cat": "形容詞"}, {"en": "jump", "zh": "跳", "cat": "動詞"},
    {"en": "sing", "zh": "唱歌", "cat": "動詞"}, {"en": "swim", "zh": "游泳", "cat": "動詞"}
    # ... 根據您的資料庫持續擴增 ...
]

def generate_audio(text):
    tts = gTTS(text=text, lang='en')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    return fp

if 'game_state' not in st.session_state:
    st.session_state.update({
        'game_state': "MENU", 'score': 0, 'current_idx': 0, 
        'questions': [], 'wrong_list': []
    })

st.set_page_config(page_title="GEPT Kids 單字王", layout="centered")
st.title("🎓 小學英檢單字挑戰")

if st.session_state.game_state == "MENU":
    cats = sorted(list(set([w['cat'] for w in WORD_BANK])))
    selected = st.selectbox("請選擇練習主題：", ["全部隨機"] + cats)
    if st.button("開始挑戰 (20題)", use_container_width=True):
        pool = WORD_BANK if selected == "全部隨機" else [w for w in WORD_BANK if w['cat'] == selected]
        st.session_state.questions = random.sample(pool, min(len(pool), 20))
        st.session_state.game_state = "QUIZ"
        st.session_state.current_idx = 0
        st.session_state.score = 0
        st.session_state.wrong_list = []
        st.rerun()

elif st.session_state.game_state == "QUIZ":
    q = st.session_state.questions[st.session_state.current_idx]
    st.write(f"題目 {st.session_state.current_idx + 1} / {len(st.session_state.questions)}")
    
    st.subheader("聽聲音選出正確意思：")
    st.markdown(f"### **{q['en']}**")
    st.audio(generate_audio(q['en']), format='audio/mp3', autoplay=True)

    # 產生選項
    if 'opts' not in st.session_state or st.session_state.last_idx != st.session_state.current_idx:
        others = [w['zh'] for w in WORD_BANK if w['zh'] != q['zh']]
        opts = random.sample(others, 3) + [q['zh']]
        random.shuffle(opts)
        st.session_state.opts = opts
        st.session_state.last_idx = st.session_state.current_idx

    for o in st.session_state.opts:
        if st.button(o, use_container_width=True):
            if o == q['zh']:
                st.success("答對了！✨")
                st.session_state.score += 5
            else:
                st.error(f"答錯了！答案是：{q['zh']}")
                st.session_state.wrong_list.append(q)
            
            st.session_state.current_idx += 1
            if st.session_state.current_idx >= len(st.session_state.questions):
                st.session_state.game_state = "RESULT"
            st.rerun()

elif st.session_state.game_state == "RESULT":
    st.header("🏆 挑戰結束！")
    st.metric("總分", f"{st.session_state.score} / 100")
    
    if st.session_state.wrong_list:
        st.subheader("⚠️ 錯題複習 (點擊聽發音)")
        for w in st.session_state.wrong_list:
            c1, c2 = st.columns([3, 1])
            c1.write(f"**{w['en']}** : {w['zh']}")
            if c2.button("🔊", key=w['en']):
                st.audio(generate_audio(w['en']), autoplay=True)
    
    if st.button("回首頁重新開始", use_container_width=True):
        st.session_state.game_state = "MENU"
        st.rerun()