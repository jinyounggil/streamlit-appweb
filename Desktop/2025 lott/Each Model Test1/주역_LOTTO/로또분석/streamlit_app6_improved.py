import streamlit as st
import pandas as pd
from pathlib import Path
import random
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="띠별 로또 분석 YouTube Shorts 생성기",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------------
# 전역 CSS - 애니메이션 효과
# ---------------------------
st.markdown("""
<style>
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }
    
    @keyframes bounce {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-10px);
        }
    }
    
    @keyframes shine {
        0% {
            box-shadow: 0 0 5px rgba(255,215,0,0.5);
        }
        50% {
            box-shadow: 0 0 20px rgba(255,215,0,0.8), 0 0 30px rgba(255,215,0,0.6);
        }
        100% {
            box-shadow: 0 0 5px rgba(255,215,0,0.5);
        }
    }
    
    @keyframes rotate {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }
    
    .ball-appear {
        animation: fadeInUp 0.6s ease-out forwards;
    }
    
    .stTextArea textarea {
        font-family: 'Malgun Gothic', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center;'>🎯 띠별 로또 분석 YouTube Shorts 생성기</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>1회차 ~ 1201회차 실제 데이터 + 오행 + 성별(홀/짝)</p>", unsafe_allow_html=True)

# ---------------------------
# 1. CSV 불러오기
# ---------------------------
CSV_PATH = Path("추천회차(streamlit).csv")

@st.cache_data
def load_lotto_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, header=None, encoding="utf-8")
    df.columns = ["회차", "번호1", "번호2", "번호3", "번호4", "번호5", "번호6", "보너스"]
    return df

try:
    df = load_lotto_data(CSV_PATH)
except Exception:
    st.error("CSV 파일을 불러오지 못했습니다. 파일 이름과 위치를 확인해주세요: 추천회차(streamlit).csv")
    st.stop()

st.markdown(f"총 **{len(df)}회차** 데이터가 로드되었습니다. (1회차 ~ {df['회차'].max()}회차)")

# ---------------------------
# 2. 사용자 선택 영역
# ---------------------------
st.markdown("---")

zodiacs = ["쥐띠", "소띠", "호랑이띠", "토끼띠", "용띠", "뱀띠", "말띠", "양띠", "원숭이띠", "닭띠", "개띠", "돼지띠"]
zodiac = st.selectbox("띠를 선택하세요", zodiacs, index=6)

gender = st.radio("성별을 선택하세요", ["남성", "여성"], horizontal=True)

period_label = st.selectbox(
    "분석 기준 회차 구간을 선택하세요",
    ["최근 150회", "최근 75회", "최근 30회"],
    index=1
)

if period_label == "최근 150회":
    period_n = 150
    period_explain = "장기 흐름입니다. 꾸준히 나오는 번호의 큰 흐름을 보여줍니다."
elif period_label == "최근 75회":
    period_n = 75
    period_explain = "중기 흐름입니다. 최근 몇 달간 강하게 나온 번호를 보여줍니다."
else:
    period_n = 30
    period_explain = "단기 흐름입니다. 최근 한두 달 사이 급상승·급하락 흐름을 보여줍니다."

st.markdown("---")

# ---------------------------
# 3. 오행 숫자 규칙
# ---------------------------
five_elements = {
    "수": {"남성": 1, "여성": 6},
    "목": {"남성": 3, "여성": 8},
    "화": {"남성": 7, "여성": 2},
    "토": {"남성": 5, "여성": 0},
    "금": {"남성": 9, "여성": 4},
}

gender_label = "남성" if gender == "남성" else "여성"
element_numbers = {e: five_elements[e][gender_label] for e in five_elements}

today_element = "토"
today_digit = element_numbers[today_element]

st.markdown("### 🧿 오행 + 성별(홀/짝) 기준")
st.markdown(f"- 선택한 띠: **{zodiac}**")
st.markdown(f"- 선택한 성별: **{gender}**")
st.markdown(f"- 오늘 적용하는 기준 오행: **{today_element}**")

st.markdown("**성별에 따른 오행 숫자:**")
for e, num in element_numbers.items():
    st.markdown(f"- {e} : {gender_label} 기준 숫자 **{num}**")

st.markdown("---")

# ---------------------------
# 4. 최근 N회차 데이터 분석
# ---------------------------
st.markdown("### 📊 최근 구간 데이터 기반 번호 출현 분석")

recent_df = df.tail(period_n).copy()
numbers_only = recent_df[["번호1", "번호2", "번호3", "번호4", "번호5", "번호6"]].values.flatten()
freq = pd.Series(numbers_only).value_counts().sort_index()
ranked = freq.sort_values(ascending=False)

hot_nums = ranked.index[:15].tolist()
mid_nums = ranked.index[15:30].tolist()
cold_nums = ranked.index[30:45].tolist()

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**🔥 HOT (1~15위)**")
    st.write(sorted(hot_nums))
with col2:
    st.markdown("**🌤 MID (16~30위)**")
    st.write(sorted(mid_nums))
with col3:
    st.markdown("**❄ COLD (31~45위)**")
    st.write(sorted(cold_nums))

# 차트 시각화 추가
st.markdown("#### 📈 번호별 출현 빈도 차트")
chart_data = ranked.head(15).reset_index()
chart_data.columns = ['번호', '출현횟수']

fig = px.bar(chart_data, x='번호', y='출현횟수', 
             title=f'{period_label} HOT 번호 출현 빈도',
             color='출현횟수',
             color_continuous_scale='reds')
fig.update_layout(height=300)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ---------------------------
# 5. 로또 공 생성 함수 (애니메이션 포함)
# ---------------------------
def lotto_ball_animated(num, delay=0):
    """애니메이션 효과가 있는 로또 공"""
    if 1 <= num <= 9:
        outer_bg = "radial-gradient(circle at 30% 30%, #4A90E2, #003C8F)"
        color_name = "파랑"
    elif 10 <= num <= 18:
        outer_bg = "radial-gradient(circle at 30% 30%, #FF6B6B, #C62828)"
        color_name = "빨강"
    elif 19 <= num <= 27:
        outer_bg = "radial-gradient(circle at 30% 30%, #FFD54F, #F9A825)"
        color_name = "황색"
    elif 28 <= num <= 36:
        outer_bg = "radial-gradient(circle at 30% 30%, #F4E04D, #C9B037)"
        color_name = "금색"
    elif 37 <= num <= 45:
        outer_bg = "radial-gradient(circle at 30% 30%, #B39DDB, #673AB7)"
        color_name = "보라"
    else:
        outer_bg = "radial-gradient(circle at 30% 30%, #ffffff, #e0e0e0)"
        color_name = "기본"

    return f"""
    <div style="
        display: inline-block;
        animation: fadeInUp 0.8s ease-out {delay}s both, pulse 2s ease-in-out {delay + 0.8}s infinite;
    ">
        <div style="
            background: {outer_bg};
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            position: relative;
        ">
            <div style="
                background: #ffffff;
                width: 44px;
                height: 44px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 22px;
                font-weight: bold;
                color: #000000;
                box-shadow: inset 0 0 6px rgba(0,0,0,0.2);
            ">
                {num}
            </div>
        </div>
    </div>
    """

# ---------------------------
# 6. 추천 번호 생성
# ---------------------------
def match_element(num: int, el_digit: int) -> bool:
    return num % 10 == el_digit

hot_match = [n for n in hot_nums if match_element(n, today_digit)]
recommend_pool = hot_match + [n for n in hot_nums if n not in hot_match] + mid_nums

seen = set()
unique_pool = []
for n in recommend_pool:
    if n not in seen:
        seen.add(n)
        unique_pool.append(n)

final_pool = unique_pool
if len(final_pool) < 6:
    for n in cold_nums:
        if n not in seen:
            seen.add(n)
            final_pool.append(n)

final_recommend = sorted(final_pool[:6])
final_str = ", ".join(str(n) for n in final_recommend)

# ---------------------------
# 7. Shorts 모드 토글
# ---------------------------
st.markdown("---")
shorts_mode = st.toggle("🎬 **Shorts 프리뷰 모드** (9:16 세로 화면)")

if shorts_mode:
    st.markdown("""
    <style>
        .shorts-preview {
            max-width: 400px;
            margin: 0 auto;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            padding: 30px 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }
    </style>
    """, unsafe_allow_html=True)

    preview_html = f"""
    <div class='shorts-preview'>
        <h2 style='text-align:center; color:white; font-size:28px; margin-bottom:10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);'>
            ✨ {zodiac} {gender}님 ✨
        </h2>
        <h3 style='text-align:center; color:#FFD700; font-size:22px; margin-bottom:25px; text-shadow: 1px 1px 3px rgba(0,0,0,0.5);'>
            오늘의 행운 번호
        </h3>
        <div style='display:flex; justify-content:center; flex-wrap:wrap; gap:12px; margin-bottom:25px;'>
    """
    
    for idx, num in enumerate(final_recommend):
        preview_html += lotto_ball_animated(num, idx * 0.2)
    
    preview_html += f"""
        </div>
        <p style='text-align:center; color:white; font-size:18px; margin-top:20px; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);'>
            💫 {today_element}행 기운이 함께합니다 💫
        </p>
        <p style='text-align:center; color:#FFD700; font-size:16px; margin-top:15px; font-weight:bold;'>
            👍 구독 & 좋아요 & 알림설정
        </p>
    </div>
    """
    
    st.markdown(preview_html, unsafe_allow_html=True)

else:
    st.markdown("### 🎯 오늘 추천 번호 (로또 공 스타일)")
    
    balls_html = "<div style='display:flex; justify-content:center; gap:8px; flex-wrap:wrap; max-width:500px; margin:0 auto;'>"
    for idx, n in enumerate(final_recommend):
        balls_html += lotto_ball_animated(n, idx * 0.15)
    balls_html += "</div>"
    
    st.markdown(balls_html, unsafe_allow_html=True)

st.markdown("---")

# ---------------------------
# 8. 여러 조합 자동 생성
# ---------------------------
st.markdown("### 🧮 추천 번호 여러 조합 자동 생성")

combo_count = st.slider("생성할 조합 개수를 선택하세요", min_value=1, max_value=10, value=5)

def generate_combinations(hot, mid, cold, today_digit, count=5, size=6):
    all_combos = []
    hot = sorted(hot)
    mid = sorted(mid)
    cold = sorted(cold)
    element_match = [n for n in hot + mid if n % 10 == today_digit]

    for _ in range(count):
        combo = set()
        random.shuffle(element_match)
        for n in element_match:
            if len(combo) < 2:
                combo.add(n)

        hot_pool = hot.copy()
        random.shuffle(hot_pool)
        for n in hot_pool:
            if len(combo) >= size:
                break
            combo.add(n)

        mid_pool = mid.copy()
        random.shuffle(mid_pool)
        for n in mid_pool:
            if len(combo) >= size:
                break
            combo.add(n)

        cold_pool = cold.copy()
        random.shuffle(cold_pool)
        for n in cold_pool:
            if len(combo) >= size:
                break
            combo.add(n)

        combo = sorted(combo)
        if combo not in all_combos and len(combo) == size:
            all_combos.append(combo)

    return all_combos

combos = generate_combinations(hot_nums, mid_nums, cold_nums, today_digit, count=combo_count, size=6)

st.markdown("**생성된 조합들:**")
for i, combo in enumerate(combos, start=1):
    st.markdown(f"- 조합 {i}: {', '.join(str(n) for n in combo)}")

st.markdown("---")

# ---------------------------
# 9. YouTube Shorts 스크립트 생성
# ---------------------------
st.markdown("## 🎬 YouTube Shorts 스크립트 & 제작 가이드")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["⚡ 15초 후킹", "📺 30초 완성", "🎭 순차 등장", "📖 스토리텔링", "🎥 제작 가이드"])

with tab1:
    st.markdown("### ⚡ 15초 후킹 버전 (짧고 임팩트)")
    
    hooking_script = f"""
[0-2초] 🎯 {zodiac} {gender}님! 잠깐만요!

[2-5초] 오늘 {period_label} 데이터로 분석한
행운의 번호가 나왔습니다!

[5-10초] 🔥 {final_str} 🔥

[10-13초] {today_element}행 기운이 강한 날!
오늘이 바로 그날입니다!

[13-15초] 👇 댓글로 당신의 띠를 알려주세요!
구독 좋아요 부탁드려요! 💫
"""
    
    st.text_area("15초 후킹 스크립트", value=hooking_script.strip(), height=300, key="hook")
    
    st.markdown("#### 🎵 추천 BGM")
    st.markdown("- 유튜브 오디오 라이브러리: 'Energetic', 'Upbeat', 'Positive' 태그")
    st.markdown("- BPM: 120-140 (빠른 템포)")
    st.markdown("- 분위기: 신나고 긍정적인 느낌")
    
    st.markdown("#### 🎬 효과음 타이밍")
    st.markdown("- 0초: 알림음 (띵동!)")
    st.markdown("- 2초: 스와이프 효과음")
    st.markdown("- 5초: 반짝임 효과음 (각 숫자마다)")
    st.markdown("- 13초: 버튼 클릭 효과음")

with tab2:
    st.markdown("### 📺 30초 완성 버전 (자세한 설명)")
    
    complete_script = f"""
[0-3초] 안녕하세요! {zodiac} {gender}님!
오늘의 로또 분석 시작합니다! 🎯

[3-7초] {period_label} 실제 당첨 데이터를
빅데이터로 분석했습니다!

[7-10초] HOT 번호는 이렇게 나왔고요,
오행 '{today_element}' 기운을 반영했습니다.

[10-15초] 자, 오늘의 추천 번호 공개합니다!
🥁 드럼롤~

[15-20초] 🎊 {final_str} 🎊

[20-25초] {gender} 기준으로
{today_element}행({today_digit}) 끝자리가 
특히 강력합니다!

[25-28초] 오늘 꼭 구매하세요!
작은 투자가 인생을 바꿀 수 있습니다! 💰

[28-30초] 구독, 좋아요, 알림설정 필수!
당첨되면 꼭 댓글 남겨주세요! 🔔
"""
    
    st.text_area("30초 완성 스크립트", value=complete_script.strip(), height=400, key="complete")
    
    st.markdown("#### 📊 화면 구성")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**상단 1/3**")
        st.markdown("- 제목 텍스트")
        st.markdown("- 띠 이모지")
    with col2:
        st.markdown("**중단 1/3**")
        st.markdown("- 로또 공 애니메이션")
        st.markdown("- 번호 강조")
    
    st.markdown("**하단 1/3**: CTA 버튼 (구독/좋아요)")

with tab3:
    st.markdown("### 🎭 순차 등장 버전 (서스펜스)")
    
    effect_lines = []
    for i, n in enumerate(final_recommend, start=1):
        effect_lines.append(f"[{2 + i*2}-{3 + i*2}초] {i}번째 숫자... {n}! {'🔥' if n in hot_nums else '⭐'}")
    
    sequential_script = f"""
[0-2초] {zodiac} {gender}님!
지금부터 번호를 하나씩 공개합니다! 😱

{chr(10).join(effect_lines)}

[15-18초] 이렇게 6개 번호가 나왔습니다!
{final_str}

[18-22초] {today_element}행 기운이
오늘 하루를 지배합니다! 💫

[22-25초] 지금 바로 로또 구매하러 가세요!

[25-27초] 당첨되면 댓글로 인증해주세요! 📝

[27-30초] 구독자님들의 당첨 소식을
기다리고 있겠습니다! 🎉
"""
    
    st.text_area("순차 등장 스크립트", value=sequential_script.strip(), height=400, key="seq")
    
    st.markdown("#### 🎬 편집 팁")
    st.markdown("- 각 숫자마다 0.5초 정지 프레임 삽입")
    st.markdown("- 숫자 등장 시 확대 효과 (Zoom In)")
    st.markdown("- 반짝임 효과 레이어 추가")
    st.markdown("- 드럼롤 BGM 지속")

with tab4:
    st.markdown("### 📖 스토리텔링 버전 (감성 자극)")
    
    story_script = f"""
[0-4초] 여러분, 혹시 아시나요?
로또 당첨자의 70%가
띠와 오행을 고려했다는 사실을... 🤔

[4-8초] 오늘은 {zodiac}에게
특별한 날입니다.

[8-12초] {today_element}행의 기운이
우주에서 강하게 흐르고 있습니다. 🌟

[12-16초] 1201회차 빅데이터 분석 결과,
이 6개 숫자가 나왔습니다.

[16-20초] ✨ {final_str} ✨

[20-24초] 특히 끝자리 {today_digit}인 숫자는
{gender}에게 금전운을 가져다줍니다. 💰

[24-27초] 오늘 로또를 구매하지 않으면
평생 후회할 수도 있습니다.

[27-30초] 지금 바로 편의점으로!
구독하면 행운이 2배! 🍀
"""
    
    st.text_area("스토리텔링 스크립트", value=story_script.strip(), height=400, key="story")
    
    st.markdown("#### 🎨 비주얼 연출")
    st.markdown("- 우주/별/은하 배경 영상")
    st.markdown("- 부드러운 트랜지션 (페이드)")
    st.markdown("- 감성적인 BGM (잔잔한 피아노)")
    st.markdown("- 따뜻한 색감 필터")

with tab5:
    st.markdown("### 🎥 YouTube Shorts 제작 가이드")
    
    st.markdown("#### 📱 영상 사양")
    st.markdown("- **해상도**: 1080 x 1920 (9:16 세로)")
    st.markdown("- **프레임**: 30fps 또는 60fps")
    st.markdown("- **길이**: 15-60초 (추천: 15-30초)")
    st.markdown("- **포맷**: MP4 (H.264 코덱)")
    
    st.markdown("#### 🎨 썸네일 디자인")
    thumbnail_text = f"""
상단: "{zodiac} {gender} 필독!"
중앙: 큰 숫자 "{final_recommend[0]}, {final_recommend[1]}, {final_recommend[2]}..."
하단: "오늘의 행운번호 💰"
배경: 화려한 그라데이션 (금색/보라색)
"""
    st.text_area("썸네일 텍스트", value=thumbnail_text.strip(), height=150, key="thumb")
    
    st.markdown("#### 🎬 추천 편집 앱")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**모바일**")
        st.markdown("- CapCut (무료)")
        st.markdown("- InShot (무료)")
        st.markdown("- VivaVideo")
    with col2:
        st.markdown("**PC**")
        st.markdown("- Adobe Premiere Pro")
        st.markdown("- DaVinci Resolve (무료)")
        st.markdown("- Vegas Pro")
    
    st.markdown("#### 📊 업로드 최적화")
    st.markdown("**제목 (70자 이내)**")
    title_example = f"{zodiac} {gender} 오늘의 로또번호 🎯 {final_str} | {today_element}행 | {period_label} 빅데이터"
    st.code(title_example, language=None)
    
    st.markdown("**설명 (5000자 이내)**")
    description_example = f"""
안녕하세요! 로또 분석 전문 채널입니다 🎯

오늘은 {zodiac} {gender}님을 위한
특별한 번호 분석을 준비했습니다!

✅ {period_label} 실제 당첨 데이터 분석
✅ {today_element}행 오행 기운 반영
✅ HOT/MID/COLD 번호 조합

📊 오늘의 추천 번호
{final_str}

💡 이 번호의 특징
- {gender} 기준 오행 숫자 포함
- HOT 번호 {len([n for n in final_recommend if n in hot_nums])}개 포함
- {today_element}행 끝자리({today_digit}) 강조

🎯 구매 팁
1. 오늘 저녁 6시 전에 구매
2. 복권방보다 편의점 추천
3. 긍정적인 마음으로 구매

📌 당첨되면 댓글로 꼭 알려주세요!
여러분의 행운을 응원합니다! 🍀

#로또 #{zodiac} #로또분석 #로또번호추천 #행운번호
#오행 #로또당첨 #로또예상번호 #로또1등
"""
    st.text_area("영상 설명", value=description_example.strip(), height=300, key="desc")
    
    st.markdown("**해시태그 (15개 추천)**")
    hashtags = f"#로또 #로또분석 #{zodiac} #로또번호 #로또추천 #행운번호 #로또당첨 #로또예상 #{today_element}행 #오행 #빅데이터 #로또1등 #{gender} #운세 #로또공략"
    st.code(hashtags, language=None)
    
    st.markdown("#### 🎯 첫 3초 후킹 전략")
    st.info("""
    **중요!** Shorts는 처음 3초가 생명입니다!
    
    1. 큰 텍스트로 띠 호명 ("{zodiac}님!")
    2. 강렬한 효과음 (알림음)
    3. 물음표 자막 ("오늘의 행운은?")
    4. 빠른 템포의 BGM
    5. 화려한 색상 (금색, 빨강)
    """)
    
    st.markdown("#### 📈 업로드 시간대")
    st.markdown("- **최고**: 저녁 7-9시 (퇴근 시간)")
    st.markdown("- **좋음**: 점심 12-1시, 밤 10-11시")
    st.markdown("- **추천 요일**: 금요일 저녁 (주말 로또 구매 전)")
    
    st.markdown("#### 💬 댓글 유도 전략")
    st.success("""
    영상 끝에 이렇게 질문하세요:
    
    - "당신은 무슨 띠인가요? 댓글로 알려주세요!"
    - "이 번호로 당첨되면 댓글 남기기 약속!"
    - "다음엔 어떤 띠를 분석해볼까요?"
    - "구독하면 매일 행운번호 알림!"
    """)

st.markdown("---")

# ---------------------------
# 10. 추가 인터랙티브 콘텐츠 아이디어
# ---------------------------
st.markdown("## 💡 추가 콘텐츠 아이디어")

with st.expander("🎮 인터랙티브 콘텐츠"):
    st.markdown("""
    ### 시청자 참여 유도 방법
    
    1. **번호 맞추기 게임**
       - "이 중 HOT 번호는 몇 개일까요? 댓글로 맞춰보세요!"
       - 정답자 중 추첨으로 커피 쿠폰 증정
    
    2. **투표 기능 활용**
       - "오늘 로또 구매하실 건가요? 👍 / 👎"
       - 커뮤니티 탭에서 투표 진행
    
    3. **연속 시리즈**
       - "12띠 시리즈" - 매일 다른 띠 업로드
       - "요일별 오행" - 월(수), 화(화), 수(목)...
    
    4. **챌린지**
       - "#로또챌린지 - 추천번호로 구매 인증샷"
       - 당첨자 나오면 축하 영상 제작
    
    5. **라이브 방송**
       - 매주 금요일 저녁 추첨 전 생방송
       - 실시간 번호 추천 & 채팅 소통
    """)

with st.expander("📊 데이터 시각화 콘텐츠"):
    st.markdown("""
    ### 영상에 넣을 그래프/차트
    
    1. **히트맵** - 번호별 출현 빈도를 색상으로
    2. **라인차트** - 최근 10회차 번호 추이
    3. **파이차트** - HOT/MID/COLD 비율
    4. **워드클라우드** - 자주 나온 숫자를 크게
    5. **애니메이션 차트** - 숫자가 움직이며 순위 변동
    """)

with st.expander("🎵 BGM & 효과음 라이브러리"):
    st.markdown("""
    ### 무료 음원 사이트
    
    **배경음악 (BGM)**
    - YouTube 오디오 라이브러리 (무료, 저작권 걱정 없음)
    - Epidemic Sound (유료, 품질 최고)
    - Artlist (유료, 다양한 장르)
    - Bensound (무료, 상업용 가능)
    
    **효과음 (SFX)**
    - Freesound.org
    - Zapsplat
    - Mixkit
    - 효과음 추천:
      * 틱톡 소리 (시계)
      * 반짝임 (마법)
      * 드럼롤
      * 당첨 소리 (종소리, 박수)
      * 스와이프 (휙!)
    """)

# ---------------------------
# 11. 행운 행동 가이드
# ---------------------------
st.markdown("---")
st.markdown("## 🍀 오늘의 행운 행동 가이드")

guide = f"""
### {zodiac} {gender}님을 위한 오늘의 행운 행동 💫

#### 🎨 행운의 색상
- **추천**: 금색, 노란색 ({today_element}행 색상)
- **패션**: 노란 액세서리, 금색 시계
- **소품**: 노란색 펜, 금색 카드케이스

#### ⏰ 행운의 시간대
- **오전**: 9시-11시 (기운 상승)
- **오후**: 3시-5시 (금전운 최고)
- **저녁**: 7시-9시 (로또 구매 최적)

#### 📍 행운의 방향
- {today_element}행 방향: 중앙/중심
- 로또 구매 시 가게 중앙 기계 이용
- 집에서 남쪽 방향 창문 열기

#### 🎯 행운 행동 체크리스트
✅ 아침에 물 한 잔 마시기 (수 기운)
✅ 지갑 정리하고 깨끗하게 (금전운)
✅ 웃는 얼굴로 하루 시작 (긍정 에너지)
✅ 로또 구매 전 심호흡 3번
✅ 편의점 직원에게 인사하기
✅ 복권을 받으면 감사 인사

#### 🚫 피해야 할 행동
❌ 부정적인 말/생각
❌ 어두운 색 옷 (검정, 회색)
❌ 서두르거나 조급해하기
❌ 복권을 구겨서 보관
❌ 당첨 전에 돈 계산하기

#### 💰 로또 구매 의식(儀式)
1. 편의점 들어가기 전 심호흡
2. "오늘은 내 행운의 날" 3번 속삭이기
3. 웃으며 "로또 주세요" 말하기
4. 복권 받으면 두 손으로 감싸기
5. 지갑에 정성스럽게 넣기

오늘의 추천 번호: **{final_str}**

행운을 빕니다! 🍀✨
"""

st.markdown(guide)

# ---------------------------
# 12. 최종 패키지 다운로드
# ---------------------------
st.markdown("---")
st.markdown("## 📦 최종 패키지 (복사해서 사용)")

final_package = f"""
{'='*60}
🎯 {zodiac} {gender}님 맞춤 로또 분석 패키지
{'='*60}

📅 분석일: 2025년 12월 8일
📊 데이터: {period_label} ({period_n}회차)
🧿 오행: {today_element}행 (끝자리 {today_digit})
🎲 추천번호: {final_str}

{'='*60}
📈 번호 분석
{'='*60}

🔥 HOT 번호 (빈출): {sorted(hot_nums)}
🌤 MID 번호 (중간): {sorted(mid_nums)}
❄ COLD 번호 (저출): {sorted(cold_nums)}

추천 번호 구성:
- HOT 번호: {[n for n in final_recommend if n in hot_nums]}
- MID 번호: {[n for n in final_recommend if n in mid_nums]}
- COLD 번호: {[n for n in final_recommend if n in cold_nums]}
- {today_element}행({today_digit}) 끝자리: {[n for n in final_recommend if n % 10 == today_digit]}

{'='*60}
📝 YouTube Shorts 제목 (복사용)
{'='*60}

{zodiac} {gender} 로또 행운번호 🎯 {final_str} | {today_element}행 | {period_label} 빅데이터

{'='*60}
#️⃣  해시태그 (복사용)
{'='*60}

#로또 #로또분석 #{zodiac} #로또번호추천 #행운번호 #로또당첨 #{today_element}행 #오행 #빅데이터 #로또1등 #운세 #{gender} #로또예상번호 #로또공략 #금주의로또

{'='*60}
🎬 15초 스크립트
{'='*60}

[0-2초] {zodiac} {gender}님! 잠깐!
[2-5초] {period_label} 분석 완료!
[5-10초] {final_str} 🔥
[10-13초] {today_element}행 기운 최고!
[13-15초] 구독 좋아요! 💫

{'='*60}
💡 제작 팁
{'='*60}

✅ 해상도: 1080x1920 (9:16)
✅ 길이: 15-30초
✅ BGM: 밝고 경쾌한 음악
✅ 효과음: 반짝임, 드럼롤
✅ 업로드: 금요일 저녁 7-9시
✅ 썸네일: 큰 숫자 + 금색 배경

{'='*60}
🍀 행운을 빕니다!
{'='*60}
"""

st.text_area("📦 전체 패키지 (Ctrl+A로 전체 선택 후 복사)", value=final_package, height=600, key="package")

st.success("✅ 모든 준비가 완료되었습니다! 영상 제작 후 업로드하세요! 📹")
st.balloons()
