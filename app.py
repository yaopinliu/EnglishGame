import streamlit as st
import random
from gtts import gTTS
import io
import base64
import streamlit.components.v1 as components
from datetime import datetime
import pandas as pd

# ---------------------------------------------------------
# 1. 完整單字資料庫 (精選 GEPT Kids 各分類核心單字)
# ---------------------------------------------------------
WORD_BANK = [
    # 動物
    {"en": "animal", "zh": "動物", "cat": "動物/昆蟲"}, {"en": "bear", "zh": "熊", "cat": "動物/昆蟲"}, {"en": "bee", "zh": "蜜蜂", "cat": "動物/昆蟲"}, {"en": "bird", "zh": "鳥", "cat": "動物/昆蟲"}, {"en": "butterfly", "zh": "蝴蝶", "cat": "動物/昆蟲"}, {"en": "cat", "zh": "貓", "cat": "動物/昆蟲"}, {"en": "dog", "zh": "狗", "cat": "動物/昆蟲"}, {"en": "elephant", "zh": "大象", "cat": "動物/昆蟲"}, {"en": "fish", "zh": "魚", "cat": "動物/昆蟲"}, {"en": "lion", "zh": "獅子", "cat": "動物/昆蟲"}, {"en": "monkey", "zh": "猴子", "cat": "動物/昆蟲"}, {"en": "panda", "zh": "大貓熊", "cat": "動物/昆蟲"}, {"en": "rabbit", "zh": "兔子", "cat": "動物/昆蟲"}, {"en": "tiger", "zh": "老虎", "cat": "動物/昆蟲"}, {"en": "zebra", "zh": "斑馬", "cat": "動物/昆蟲"},
    # 衣服
    {"en": "bag", "zh": "袋子", "cat": "衣服配件"}, {"en": "cap", "zh": "棒球帽", "cat": "衣服配件"}, {"en": "clothes", "zh": "衣服", "cat": "衣服配件"}, {"en": "dress", "zh": "洋裝", "cat": "衣服配件"}, {"en": "glasses", "zh": "眼鏡", "cat": "衣服配件"}, {"en": "jacket", "zh": "夾克", "cat": "衣服配件"}, {"en": "shoes", "zh": "鞋子", "cat": "衣服配件"}, {"en": "T-shirt", "zh": "T恤", "cat": "衣服配件"},
    # 顏色
    {"en": "black", "zh": "黑色", "cat": "顏色"}, {"en": "blue", "zh": "藍色", "cat": "顏色"}, {"en": "brown", "zh": "咖啡色", "cat": "顏色"}, {"en": "green", "zh": "綠色", "cat": "顏色"}, {"en": "orange", "zh": "橘色", "cat": "顏色"}, {"en": "pink", "zh": "粉紅色", "cat": "顏色"}, {"en": "purple", "zh": "紫色", "cat": "顏色"}, {"en": "red", "zh": "紅色", "cat": "顏色"}, {"en": "white", "zh": "白色", "cat": "顏色"}, {"en": "yellow", "zh": "黃色", "cat": "顏色"},
    # 家庭
    {"en": "aunt", "zh": "阿姨/姑姑", "cat": "家庭"}, {"en": "brother", "zh": "兄弟", "cat": "家庭"}, {"en": "dad", "zh": "爸爸", "cat": "家庭"}, {"en": "family", "zh": "家庭", "cat": "家庭"}, {"en": "father", "zh": "爸爸", "cat": "家庭"}, {"en": "grandma", "zh": "奶奶/外婆", "cat": "家庭"}, {"en": "grandpa", "zh": "爺爺/外公", "cat": "家庭"}, {"en": "mother", "zh": "媽媽", "cat": "家庭"}, {"en": "sister", "zh": "姊妹", "cat": "家庭"}, {"en": "son", "zh": "兒子", "cat": "家庭"}, {"en": "uncle", "zh": "叔叔/舅舅", "cat": "家庭"},
    # 食物
    {"en": "apple", "zh": "蘋果", "cat": "食物/飲料"}, {"en": "banana", "zh": "香蕉", "cat": "食物/飲料"}, {"en": "bread", "zh": "麵包", "cat": "食物/飲料"}, {"en": "cake", "zh": "蛋糕", "cat": "食物/飲料"}, {"en": "candy", "zh": "糖果", "cat": "食物/飲料"}, {"en": "chocolate", "zh": "巧克力", "cat": "食物/飲料"}, {"en": "egg", "zh": "蛋", "cat": "食物/飲料"}, {"en": "hamburger", "zh": "漢堡", "cat": "食物/飲料"}, {"en": "milk", "zh": "牛奶", "cat": "食物/飲料"}, {"en": "pizza", "zh": "披薩", "cat": "食物/飲料"}, {"en": "rice", "zh": "米飯", "cat": "食物/飲料"}, {"en": "soup", "zh": "湯", "cat": "食物/飲料"},
    # 運輸
    {"en": "airplane", "zh": "飛機", "cat": "運輸"}, {"en": "bicycle", "zh": "腳踏車", "cat": "運輸"}, {"en": "bus", "zh": "公車", "cat": "運輸"}, {"en": "car", "zh": "車子", "cat": "運輸"}, {"en": "motorcycle", "zh": "摩托車", "cat": "運輸"}, {"en": "train", "zh": "火車", "cat": "運輸"}
]

# ---------------------------------------------------------
# 2. 核心功能: 語音、工具、紀錄
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
        <button onclick="play_{audio_id}()" style="background:#4CAF50;color:white;border:none;padding:12px;width:100%;border-radius:10px;cursor:pointer;font-weight:bold;font-size:16px;">🔊 播放發音 (Play)</button>
    """
    components.html(html, height=65)

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
# 3. Session State
# ---------------------------------------------------------
if 'mode' not in st.session_state: st.session_state.mode = "MAIN"
if 'history' not in st.session_state: st.session_state.history = []
if 'game_state' not in st.session_state:
    st.session_state.update({
        'game_state': "START", 'score': 0, 'current_idx': 0, 
        'questions': [], 'wrong_list': [], 'ans_checked': False,
        'selected_opt': None, 'user_typed': "", 'options': [], 'results_saved': False
    })

# ---------------------------------------------------------
# 4. 學習紀錄儲存
# ---------------------------------------------------------
def save_to_history(mode_name, selected_cat, total_q, score):
    if not st.session_state.results_saved:
        acc = (score / (total_q * 5)) * 100
        st.session_state.history.append({
            "日期": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "模式": mode_name, "主題": selected_cat,
            "得分": score, "正確率": f"{acc:.1f}%"
        })
        st.session_state.results_saved = True

# ---------------------------------------------------------
# 5. 介面流程
# ---------------------------------------------------------
st.set_page_config(page_title="GEPT Kids 單字王", page_icon="🎓")

# --- 主選單 ---
if st.session_state.mode == "MAIN":
    st.title("🎓 小學英檢單字王")
    if st.button("🎧 聽力測驗 (選中文)", use_container_width=True):
        st.session_state.mode = "LISTENING"; st.session_state.game_state = "START"; safe_rerun()
    if st.button("✍️ 拼寫測驗 (打英文)", use_container_width=True):
        st.session_state.mode = "CLOZE"; st.session_state.game_state = "START"; safe_rerun()
    st.write("---")
    if st.button("📊 查看學習統計", use_container_width=True):
        st.session_state.mode = "STATS"; safe_rerun()

# --- 聽力模式 ---
elif st.session_state.mode == "LISTENING":
    st.title("聽力測驗")
    if st.session_state.game_state == "START":
        st.session_state.results_saved = False
        cats = sorted(list(set([w['cat'] for w in WORD_BANK])))
        sel = st.selectbox("主題：", ["全部隨機"] + cats)
        if st.button("開始挑戰"):
            pool = WORD_BANK if sel == "全部隨機" else [w for w in WORD_BANK if w['cat'] == sel]
            st.session_state.update({'questions': random.sample(pool, min(len(pool), 20)), 'game_state': "PLAY", 'current_idx': 0, 'score': 0, 'wrong_list': [], 'selected_cat': sel})
            safe_rerun()
    elif st.session_state.game_state == "PLAY":
        idx = st.session_state.current_idx; q = st.session_state.questions[idx]
        st.write(f"進度：{idx+1}/20"); st.header(q['en'])
        play_audio_js(q['en'], f"lis_{idx}")
        if not st.session_state.options:
            wrong = [w['zh'] for w in WORD_BANK if w['zh'] != q['zh']]
            opts = random.sample(wrong, 3) + [q['zh']]; random.shuffle(opts)
            st.session_state.options = opts
        
        if not st.session_state.ans_checked:
            for o in st.session_state.options:
                if st.button(o, use_container_width=True):
                    st.session_state.ans_checked = True; st.session_state.selected_opt = o
                    if o == q['zh']: st.session_state.score += 5
                    else: st.session_state.wrong_list.append(q)
                    safe_rerun()
        else:
            for o in st.session_state.options:
                if o == q['zh']: st.success(o)
                elif o == st.session_state.selected_opt: st.error(o)
                else: st.info(o)
            if st.button("下一題", use_container_width=True, type="primary"):
                st.session_state.current_idx += 1; st.session_state.ans_checked = False; st.session_state.options = []
                if st.session_state.current_idx >= len(st.session_state.questions): st.session_state.game_state = "END"
                safe_rerun()
    elif st.session_state.game_state == "END":
        save_to_history("聽力測驗", st.session_state.selected_cat, len(st.session_state.questions), st.session_state.score)
        st.balloons(); st.header("挑戰結束！"); st.metric("得分", st.session_state.score)
        if st.button("回主選單"): st.session_state.mode = "MAIN"; safe_rerun()

# --- 拼寫模式 ---
elif st.session_state.mode == "CLOZE":
    st.title("拼寫測驗")
    if st.session_state.game_state == "START":
        st.session_state.results_saved = False
        cats = sorted(list(set([w['cat'] for w in WORD_BANK])))
        sel = st.selectbox("主題：", ["全部隨機"] + cats)
        if st.button("開始挑戰"):
            pool = WORD_BANK if sel == "全部隨機" else [w for w in WORD_BANK if w['cat'] == sel]
            st.session_state.update({'questions': random.sample(pool, min(len(pool), 20)), 'game_state': "PLAY", 'current_idx': 0, 'score': 0, 'wrong_list': [], 'selected_cat': sel})
            safe_rerun()
    elif st.session_state.game_state == "PLAY":
        idx = st.session_state.current_idx; q = st.session_state.questions[idx]
        st.write(f"進度：{idx+1}/20"); st.subheader(f"中文：{q['zh']}")
        if 'cl' not in st.session_state or st.session_state.last_cl != idx:
            st.session_state.cl = create_cloze_word(q['en']); st.session_state.last_cl = idx
        st.markdown(f"## `{st.session_state.cl}`")
        play_audio_js(q['en'], f"cl_{idx}")
        
        if not st.session_state.ans_checked:
            user_in = st.text_input("輸入拼寫：", key=f"in_{idx}").strip().lower()
            if st.button("送出答案"):
                if user_in:
                    st.session_state.ans_checked = True; st.session_state.user_typed = user_in
                    if user_in == q['en'].lower(): st.session_state.score += 5
                    else: st.session_state.wrong_list.append(q)
                    safe_rerun()
        else:
            if st.session_state.user_typed == q['en'].lower(): st.success(f"正確：{q['en']}")
            else: st.error(f"錯誤！答案是：{q['en']}")
            if st.button("下一題", use_container_width=True, type="primary"):
                st.session_state.current_idx += 1; st.session_state.ans_checked = False
                if st.session_state.current_idx >= len(st.session_state.questions): st.session_state.game_state = "END"
                safe_rerun()
    elif st.session_state.game_state == "END":
        save_to_history("拼寫測驗", st.session_state.selected_cat, len(st.session_state.questions), st.session_state.score)
        st.balloons(); st.header("挑戰結束！"); st.metric("得分", st.session_state.score)
        if st.button("回主選單"): st.session_state.mode = "MAIN"; safe_rerun()

# --- 統計模式 ---
elif st.session_state.mode == "STATS":
    st.title("📊 學習統計紀錄")
    if not st.session_state.history: st.info("尚無紀錄")
    else: st.table(pd.DataFrame(st.session_state.history))
    if st.button("返回主選單"): st.session_state.mode = "MAIN"; safe_rerun()




