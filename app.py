# 로또 회차 계산 함수
def get_lotto_round(now=None):
    if now is None:
        now = datetime.now()
    base_dt = datetime(2025, 12, 13, 21, 0, 0)
    base_round = 1202
    if now < base_dt:
        return base_round
    else:
        delta = now - base_dt
        weeks = delta.days // 7
        # 21시 이후면 당일도 포함
        if delta.days % 7 > 0 or now.hour >= 21 or now.minute > 0 or now.second > 0:
            weeks += 1
        return base_round + weeks

import streamlit as st
import streamlit.components.v1 as components
import random
import json
from datetime import datetime

st.set_page_config(
    page_title="로또 공 애니메이션",
    page_icon="🍀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 64괘 이름과 설명 (주역)
hexagram_data = {
    0: ("건위천", "하늘의 기운, 강건함과 창조력의 상징"),
    1: ("곤위지", "대지의 기운, 포용과 수용의 상징"),
    2: ("수뢰둔", "시작의 어려움, 인내가 필요한 시기"),
    3: ("산수몽", "배움의 시작, 경험을 통한 성장"),
    4: ("수천수", "기다림의 지혜, 때를 기다리는 인내"),
    5: ("천수송", "분쟁과 갈등, 화해가 필요한 때"),
    6: ("지수사", "많은 사람의 힘, 협력의 중요성"),
    7: ("수지비", "친밀함과 화합, 좋은 관계의 형성"),
    8: ("풍천소축", "작은 축적, 조금씩 모으는 지혜"),
    9: ("천택이", "예절과 질서, 바른 행동의 중요성"),
    10: ("지천태", "평화와 번영, 조화로운 시기"),
    11: ("천지비", "막힘과 정체, 인내로 극복"),
    12: ("천화동인", "사람들과의 조화, 협력의 힘"),
    13: ("화천대유", "큰 소유, 풍요와 번영"),
    14: ("지산겸", "겸손의 미덕, 낮은 자세의 가치"),
    15: ("뇌지예", "기쁨과 즐거움, 긍정의 에너지"),
    16: ("택뢰수", "따름과 순응, 흐름에 맡기기"),
    17: ("산풍고", "부패를 바로잡음, 개혁의 시기"),
    18: ("지택림", "다가옴과 발전, 좋은 기운"),
    19: ("풍지관", "관찰과 성찰, 내면을 돌아봄"),
    20: ("화뢰서합", "물어뜯음, 결단의 시기"),
    21: ("산화비", "꾸밈과 아름다움, 외적 발전"),
    22: ("산지박", "벗겨짐, 불필요한 것을 떨쳐냄"),
    23: ("지뢰복", "돌아옴과 회복, 재기의 시작"),
    24: ("천뢰무망", "순수한 마음, 거짓 없는 진실"),
    25: ("산천대축", "큰 축적, 실력을 쌓는 시기"),
    26: ("산뢰이", "기름과 양육, 성장의 시기"),
    27: ("택풍대과", "큰 넘침, 과함을 조절해야"),
    28: ("감위수", "물의 흐름, 위험을 극복"),
    29: ("이위화", "불의 밝음, 빛과 열정"),
    30: ("택산함", "감응과 교감, 마음의 통함"),
    31: ("뇌풍항", "오래 지속됨, 항구불변의 가치"),
    32: ("천산둔", "물러남의 지혜, 때를 기다림"),
    33: ("뇌천대장", "큰 힘과 강함, 정의로운 힘"),
    34: ("화지진", "전진과 발전, 나아가는 힘"),
    35: ("지화명이", "밝음의 상처, 시련 속 희망"),
    36: ("풍화가인", "가정의 화목, 내부의 조화"),
    37: ("화택규", "어긋남과 대립, 이해가 필요"),
    38: ("수산건", "어려움의 극복, 난관 돌파"),
    39: ("뇌수해", "풀어짐과 해소, 문제 해결"),
    40: ("산택손", "덜어냄의 지혜, 손해를 통한 이득"),
    41: ("풍뢰익", "더함과 이익, 증가의 시기"),
    42: ("택천쾌", "결단과 결정, 단호함이 필요"),
    43: ("천풍구", "만남과 조우, 우연한 기회"),
    44: ("택지췌", "모임과 결집, 사람들의 화합"),
    45: ("지풍승", "올라감과 상승, 발전의 기운"),
    46: ("택수곤", "곤궁함, 어려움 속 희망"),
    47: ("수풍정", "우물처럼 고임, 내실을 다짐"),
    48: ("택화혁", "변혁과 개혁, 새로운 변화"),
    49: ("화풍정", "솥과 안정, 기반을 다짐"),
    50: ("진위뢰", "우레의 놀람, 각성의 순간"),
    51: ("간위산", "산의 고요함, 멈춤과 성찰"),
    52: ("풍산점", "점진적 발전, 조금씩 나아감"),
    53: ("뇌택귀매", "결혼과 귀속, 정착의 시기"),
    54: ("뇌화풍", "풍요와 번성, 최고의 정점"),
    55: ("화산려", "나그네의 여정, 이동과 변화"),
    56: ("손위풍", "바람처럼 부드러움, 유연함"),
    57: ("태위택", "기쁨과 즐거움, 행복한 시기"),
    58: ("풍수환", "흩어짐과 모임, 재결합"),
    59: ("수택절", "절제와 조절, 균형의 중요성"),
    60: ("풍택중부", "믿음과 신의, 진실한 마음"),
    61: ("뇌산소과", "작은 넘침, 사소한 과함"),
    62: ("수화기제", "이미 완성됨, 성취의 순간"),
    63: ("화수미제", "아직 완성 안됨, 계속 노력")
}

# 현재 시간 기반 64괘 계산
def calculate_hexagram(dt):
    # 년월일시를 조합하여 64괘 중 하나 선택
    year = dt.year
    month = dt.month
    day = dt.day
    hour = dt.hour
    
    # 64괘 계산 (년+월+일+시를 조합)
    hexagram_num = ((year + month + day + hour) % 64)
    return hexagram_num, hexagram_data[hexagram_num]

# 64괘 기반 추천 번호 8개 생성
def generate_lucky_numbers(dt):
    # 시간 기반 시드 설정
    seed = dt.year * 10000 + dt.month * 100 + dt.day + dt.hour
    random.seed(seed)
    
    # 1~45 중 8개 선택
    numbers = sorted(random.sample(range(1, 46), 8))
    
    # 시드 초기화 (다른 랜덤 함수에 영향 안 주도록)
    random.seed()
    
    return numbers

# 현재 접속 시간
current_time = datetime.now()
hexagram_num, (hexagram_name, hexagram_desc) = calculate_hexagram(current_time)
lucky_numbers = generate_lucky_numbers(current_time)

# 번호별 색상 반환 함수
def get_ball_color(num):
    if num <= 9:
        return 'linear-gradient(135deg, #3b82f6, #1d4ed8)'
    elif num <= 18:
        return 'linear-gradient(135deg, #ef4444, #dc2626)'
    elif num <= 27:
        return 'linear-gradient(135deg, #a16207, #78350f)'
    elif num <= 36:
        return 'linear-gradient(135deg, #fbbf24, #f59e0b)'
    else:
        return 'linear-gradient(135deg, #8b5cf6, #7c3aed)'

# 8개 중 6개 조합 생성 (최대 5개 조합 추천)
from itertools import combinations
all_combinations = list(combinations(lucky_numbers, 6))
# 랜덤하게 5개 조합 선택
import random as rand_module
recommended_combos = rand_module.sample(all_combinations, min(5, len(all_combinations)))

# 최종 번호 생성
final_numbers = sorted(random.sample(range(1, 46), 6))
final_str = ','.join(map(str, final_numbers))

# 회차별 당첨 번호 샘플 데이터 생성
def generate_draw_history(rounds):
    # 각 회차별로 6개의 번호 추첨 기록
    history = []
    for _ in range(rounds):
        draw = random.sample(range(1, 46), 6)
        history.append(draw)
    
    # 번호별 출현 빈도 계산
    stats = {}
    for num in range(1, 46):
        count = sum(1 for draw in history for n in draw if n == num)
        stats[str(num)] = count
    
    return stats, history

stats_150, history_150 = generate_draw_history(150)
stats_75, history_75 = generate_draw_history(75)
stats_45, history_45 = generate_draw_history(45)
stats_30, history_30 = generate_draw_history(30)
stats_15, history_15 = generate_draw_history(15)

# JSON으로 변환
stats_data = {
    '150': {'stats': stats_150, 'history': history_150},
    '75': {'stats': stats_75, 'history': history_75},
    '45': {'stats': stats_45, 'history': history_45},
    '30': {'stats': stats_30, 'history': history_30},
    '15': {'stats': stats_15, 'history': history_15}
}
stats_json = json.dumps(stats_data)

# HTML + JavaScript로 애니메이션 구현
html_template = """
<!DOCTYPE html>
<html>
<head>
<style>
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    body {{
        font-family: 'Arial', sans-serif;
        background: linear-gradient(135deg, #ec4899 0%, #8b5cf6 50%, #3b82f6 100%);
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        padding: 20px;
        overflow-x: hidden;
        position: relative;
    }}
    
    /* 배경 애니메이션 효과 */
    .particle {{
        position: absolute;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        pointer-events: none;
    }}
    

    
    @keyframes float {{
        0%, 100% {{ transform: translateY(0) rotate(0deg); }}
        50% {{ transform: translateY(-20px) rotate(180deg); }}
    }}
    
    #title {{
        font-size: 24px;
        font-weight: bold;
        color: white;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
        margin-bottom: 12px;
        background: linear-gradient(135deg, #10b981, #059669);
        padding: 12px 60px;
        border-radius: 20px;
        display: inline-block;
        position: relative;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        white-space: nowrap;
    }}
    
    #title::before {{
        content: '🍀';
        position: absolute;
        left: 12px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 32px;
        filter: drop-shadow(0 0 8px gold) hue-rotate(45deg);
        animation: cloverSpin 3s linear infinite;
    }}
    
    #title::after {{
        content: '🍀';
        position: absolute;
        right: 12px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 32px;
        filter: drop-shadow(0 0 8px gold) hue-rotate(45deg);
        animation: cloverSpin 3s linear infinite reverse;
    }}
    
    @keyframes cloverSpin {{
        0% {{ transform: translateY(-50%) rotate(0deg); }}
        100% {{ transform: translateY(-50%) rotate(360deg); }}
    }}
    
    #subtitle {
        display: none;
    }
    
    #subtitle::before {{
        content: '⭐';
        position: absolute;
        left: 8px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 22px;
        filter: drop-shadow(0 0 10px yellow);
        animation: starTwinkle 1.5s ease-in-out infinite;
    }}
    
    #subtitle::after {{
        content: '⭐';
        position: absolute;
        right: 8px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 22px;
        filter: drop-shadow(0 0 10px yellow);
        animation: starTwinkle 1.5s ease-in-out infinite 0.75s;
    }}
    
    @keyframes starTwinkle {{
        0%, 100% {{ 
            transform: translateY(-50%) scale(1);
            opacity: 1;
        }}
        50% {{ 
            transform: translateY(-50%) scale(1.3);
            opacity: 0.7;
        }}
    }}
    
    #ball-container {{
        text-align: center;
        padding: 40px 30px 15px 30px;
        min-height: 280px;
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 20px;
        margin-bottom: 15px;
        box-shadow: 
            inset 0 8px 20px rgba(0,0,0,0.1),
            0 10px 35px rgba(0,0,0,0.3);
        transition: transform 0.1s;
        max-width: 700px;
        width: 100%;
        border: 5px solid #334155;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
        position: relative;
    }}
    
    #ball-container::before {{
        content: '🎰 LOTTO 🎰';
        position: absolute;
        top: 8px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 14px;
        font-weight: bold;
        color: #475569;
        letter-spacing: 1px;
    }}
    
    .ball {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 45px;
        height: 45px;
        border-radius: 50%;
        font-size: 18px;
        font-weight: bold;
        color: white;
        margin: 4px;
        box-shadow: 
            inset -2px -2px 8px rgba(0,0,0,0.3),
            inset 2px 2px 8px rgba(255,255,255,0.5),
            0 3px 10px rgba(0,0,0,0.3);
        border: 2px solid rgba(255,255,255,0.8);
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        position: relative;
    }}
    
    .ball::after {{
        content: '';
        position: absolute;
        top: 15%;
        left: 20%;
        width: 12px;
        height: 12px;
        background: rgba(255,255,255,0.4);
        border-radius: 50%;
        filter: blur(4px);
    }}
    
    .ball-0 {{ background: linear-gradient(135deg, #3b82f6, #1e40af); }}
    .ball-1 {{ background: linear-gradient(135deg, #ef4444, #b91c1c); }}
    .ball-2 {{ background: linear-gradient(135deg, #fbbf24, #f59e0b); }}
    .ball-3 {{ background: linear-gradient(135deg, #10b981, #059669); }}
    .ball-4 {{ background: linear-gradient(135deg, #a855f7, #7e22ce); }}
    .ball-5 {{ background: linear-gradient(135deg, #f97316, #ea580c); }}
    
    .balls-row {{
        display: flex;
        flex-wrap: nowrap;
        justify-content: center;
        align-items: center;
        gap: 3px;
        padding: 10px 0;
    }}
    
    .spinning {{
        animation: machineShake 0.15s infinite;
    }}
    
    .spinning .ball {{
        animation: ballBounce 0.3s infinite;
    }}
    
    @keyframes machineShake {{
        0%, 100% {{ transform: translateY(0) rotate(0deg); }}
        25% {{ transform: translateY(-3px) rotate(-1deg); }}
        50% {{ transform: translateY(3px) rotate(1deg); }}
        75% {{ transform: translateY(-2px) rotate(-0.5deg); }}
    }}
    
    @keyframes ballBounce {{
        0%, 100% {{ transform: translateY(0) scale(1); }}
        50% {{ transform: translateY(-10px) scale(1.05); }}
    }}
    
    #result {{
        text-align: center;
        font-size: 18px;
        color: #000000;
        font-weight: 700;
        padding: 12px 24px;
        background: #e5e7eb; /* 연한 회색 배경 */
        border-radius: 12px;
        margin-bottom: 12px;
        min-height: 56px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-shadow: none;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.08);
        max-width: 700px;
        width: 100%;
    }}
    
    #button-container {{
        display: none;
    }}
    
    button {{
        padding: 10px 20px;
        font-size: 20px;
        font-weight: bold;
        background: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%);
        color: white;
        border: 2px solid white;
        border-radius: 12px;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        transition: all 0.3s;
        position: relative;
        min-width: 80px;
    }}
    
    button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.4);
    }}
    
    button:active {{
        transform: translateY(0);
    }}
    
    button:disabled {{
        background: #6b7280;
        cursor: not-allowed;
        transform: none;
    }}
    
    .final {{
        animation: finalPulse 1s ease-out;
    }}
    
    .final .ball {{
        animation: ballPop 0.5s ease-out;
        box-shadow: 0 6px 20px rgba(0,0,0,0.4);
        transform: scale(1.1);
    }}
    
    @keyframes finalPulse {{
        0% {{ transform: scale(0.8); opacity: 0; }}
        50% {{ transform: scale(1.1); }}
        100% {{ transform: scale(1); opacity: 1; }}
    }}
    
    @keyframes ballPop {{
        0% {{ transform: scale(0.5); opacity: 0; }}
        70% {{ transform: scale(1.15); }}
        100% {{ transform: scale(1); opacity: 1; }}
    }}
    
    .confetti {{
        position: absolute;
        width: 10px;
        height: 10px;
        background: #fbbf24;
        animation: confettiFall 3s linear;
    }}
    
    @keyframes confettiFall {{
        to {{ transform: translateY(100vh) rotate(360deg); opacity: 0; }}
    }}
    
    /* 64괘 섹션 스타일 */
    #hexagram-container {{
        max-width: 100%;
        width: 100%;
        background: linear-gradient(135deg, #fef3c7, #fde68a);
        border-radius: 15px;
        padding: 25px 20px;
        margin-top: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.3);
        border: 3px solid #f59e0b;
    }}
    
    .hexagram-title {{
        font-size: 22px;
        font-weight: bold;
        color: #92400e;
        text-align: center;
        margin-bottom: 15px;
    }}
    
    .hexagram-info {{
        background: white;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    
    .time-display {{
        font-size: 16px;
        color: #78350f;
        text-align: center;
        margin-bottom: 10px;
        font-weight: bold;
    }}
    
    .hexagram-name {{
        font-size: 28px;
        font-weight: bold;
        color: #b45309;
        text-align: center;
        margin: 10px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }}
    
    .lucky-numbers {{
        background: linear-gradient(135deg, #dc2626, #991b1b);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
    }}
    
    .lucky-title {{
        font-size: 16px;
        color: #fef3c7;
        margin-bottom: 10px;
        font-weight: bold;
    }}
    
    .lucky-balls {{
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 8px;
    }}
    
    .lucky-ball {{
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: linear-gradient(135deg, #fbbf24, #f59e0b);
        color: #78350f;
        font-size: 18px;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.3);
        border: 2px solid white;
    }}
    
    .hexagram-desc {{
        font-size: 14px;
        color: #92400e;
        text-align: center;
        font-style: italic;
        margin-top: 5px;
    }}
    
    /* 조합 추천 섹션 */
    #combo-container {{
        max-width: 100%;
        width: 100%;
        background: linear-gradient(135deg, #dbeafe, #bfdbfe);
        border-radius: 15px;
        padding: 25px 20px;
        margin-top: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.3);
        border: 3px solid #3b82f6;
    }}
    
    .combo-title {{
        font-size: 22px;
        font-weight: bold;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 15px;
    }}
    
    .combo-item {{
        background: white;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    }}
    
    .combo-numbers {{
        display: flex;
        gap: 6px;
        flex: 1;
    }}
    
    .combo-ball {{
        width: 55px;
        height: 32px;
        border-radius: 16px;
        font-size: 16px;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        position: relative;
    }}
    
    .combo-ball::before {{
        content: '';
        position: absolute;
        inset: 4px;
        border-radius: 12px;
        background: white;
        z-index: 0;
    }}
    
    .combo-ball span {{
        position: relative;
        z-index: 1;
        color: #000000;
        font-weight: bold;
    }}
    
    .copy-btn {{
        padding: 8px 16px;
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        cursor: pointer;
        font-size: 13px;
        transition: all 0.3s;
        margin: 0 auto;
        display: inline-block;
    }}
    
    .copy-btn:hover {{
        background: linear-gradient(135deg, #059669, #047857);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
    }}

    /* 연도 버튼 (작고 심플하게) */
    .year-btn {{
        padding: 6px 10px;
        background: #ffffff;
        color: #111827;
        border: 1px solid rgba(17,24,39,0.08);
        border-radius: 8px;
        font-weight: 700;
        cursor: pointer;
        font-size: 13px;
        transition: all 0.18s;
    }}

    .year-btn:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 14px rgba(17,24,39,0.06);
        background: #f3f4f6;
    }}

    /* 결과 카드 닫기 버튼 */
    .close-card-btn {{
        position: absolute;
        top: 6px;
        right: 8px;
        padding: 4px 8px;
        font-size: 12px;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        background: #111827;
        color: #ffffff;
    }}
    
    /* 사용자 선택 섹션 */
    #custom-container {{
        max-width: 100%;
        width: 100%;
        background: linear-gradient(135deg, #fce7f3, #fbcfe8);
        border-radius: 15px;
        padding: 25px 20px;
        margin-top: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.3);
        border: 3px solid #ec4899;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }}
    
    #custom-container > * {{
        width: 100%;
        text-align: center;
    }}
    
    .custom-title {{
        font-size: 22px;
        font-weight: bold;
        color: #831843;
        text-align: center;
        margin-bottom: 15px;
    }}
    
    .number-grid {{
        display: grid;
        grid-template-columns: repeat(9, minmax(8vw, 60px));
        gap: 2vw;
        margin: 0 auto 15px auto;
        justify-content: center;
        justify-items: center;
        align-items: center;
    }}

    .number-btn {{
        width: 8vw;
        min-width: 36px;
        max-width: 60px;
        height: 32px;
        border-radius: 16px;
        border: none;
        font-size: 13px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    @media (max-width: 600px) {{
        .number-grid {{
            grid-template-columns: repeat(5, minmax(14vw, 48px));
            gap: 3vw;
        }}
        .number-btn {{
            width: 14vw;
            min-width: 32px;
            max-width: 48px;
            font-size: 4vw;
        }}
    }}
    
    .number-btn::before {{
        content: '';
        position: absolute;
        inset: 3px;
        border-radius: 9px;
        background: white;
        z-index: 0;
    }}
    
    .number-btn span {{
        position: relative;
        z-index: 1;
        color: #000000;
        font-weight: bold;
    }}
    
    /* 1-9: 파랑 */
    .number-btn[data-num="1"], .number-btn[data-num="2"], .number-btn[data-num="3"],
    .number-btn[data-num="4"], .number-btn[data-num="5"], .number-btn[data-num="6"],
    .number-btn[data-num="7"], .number-btn[data-num="8"], .number-btn[data-num="9"] {{
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    }}
    
    /* 10-18: 빨강 */
    .number-btn[data-num="10"], .number-btn[data-num="11"], .number-btn[data-num="12"],
    .number-btn[data-num="13"], .number-btn[data-num="14"], .number-btn[data-num="15"],
    .number-btn[data-num="16"], .number-btn[data-num="17"], .number-btn[data-num="18"] {{
        background: linear-gradient(135deg, #ef4444, #dc2626);
    }}
    
    /* 19-27: 토지색(갈색) */
    .number-btn[data-num="19"], .number-btn[data-num="20"], .number-btn[data-num="21"],
    .number-btn[data-num="22"], .number-btn[data-num="23"], .number-btn[data-num="24"],
    .number-btn[data-num="25"], .number-btn[data-num="26"], .number-btn[data-num="27"] {{
        background: linear-gradient(135deg, #a16207, #78350f);
    }}
    
    /* 28-36: 금색 */
    .number-btn[data-num="28"], .number-btn[data-num="29"], .number-btn[data-num="30"],
    .number-btn[data-num="31"], .number-btn[data-num="32"], .number-btn[data-num="33"],
    .number-btn[data-num="34"], .number-btn[data-num="35"], .number-btn[data-num="36"] {{
        background: linear-gradient(135deg, #fbbf24, #f59e0b);
    }}
    
    /* 37-45: 보라색 */
    .number-btn[data-num="37"], .number-btn[data-num="38"], .number-btn[data-num="39"],
    .number-btn[data-num="40"], .number-btn[data-num="41"], .number-btn[data-num="42"],
    .number-btn[data-num="43"], .number-btn[data-num="44"], .number-btn[data-num="45"] {{
        background: linear-gradient(135deg, #8b5cf6, #7c3aed);
    }}
    
    .number-btn:hover {{
        transform: scale(1.1);
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }}
    
    .number-btn.selected {{
        transform: scale(1.15);
        box-shadow: 0 0 0 2px #fbbf24, 0 4px 12px rgba(251, 191, 36, 0.5);
        outline: 2px solid #fbbf24;
        outline-offset: 1px;
    }}
    
    .selected-display {{
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        width: 100%;
        max-width: 500px;
        margin-left: auto;
        margin-right: auto;
        text-align: center;
    }}
    
    .selected-title {{
        font-size: 14px;
        color: #831843;
        font-weight: bold;
        margin-bottom: 10px;
        text-align: center;
    }}
    
    #selected-numbers {{
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
        min-height: 50px;
    }}
    
    .qr-container {{
        text-align: center;
        margin-top: 15px;
        padding: 15px;
        background: white;
        border-radius: 10px;
    }}
    
    .warning-notice {{
        text-align: center;
        padding: 20px 15px;
        margin-top: 30px;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 183, 77, 0.5);
        color: white;
        font-size: 13px;
        line-height: 1.6;
    }}
    
    .warning-notice strong {{
        display: block;
        font-size: 15px;
        margin-bottom: 8px;
        color: #fbbf24;
    }}
    
    .qr-code {{
        margin: 10px auto;
    }}
    
    /* 통계 그래프 스타일 */
    #stats-container {{
        max-width: 100%;
        width: 100%;
        background: white;
        border-radius: 15px;
        padding: 30px;
        margin-top: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.3);
    }}
    
    .stats-title {{
        font-size: 28px;
        font-weight: bold;
        color: #1e293b;
        text-align: center;
        margin-bottom: 20px;
    }}
    
    .selector-container {{
        display: flex;
        flex-direction: column;
        gap: 10px;
        margin-bottom: 12px;
    }}
    
    .round-selector {{
        display: flex;
        justify-content: center;
        gap: 5px;
        flex-wrap: wrap;
    }}
    
    .zodiac-selector {{
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 5px;
        max-width: 600px;
        width: 100%;
        margin: 0;
        padding: 0;
    }}
    
    .round-btn, .zodiac-btn {{
        padding: 8px 16px;
        font-size: 14px;
        font-weight: bold;
        background: white;
        color: #334155;
        border: 2px solid #cbd5e1;
        border-radius: 18px;
        cursor: pointer;
        transition: all 0.3s;
        position: relative;
        min-width: 60px;
    }}
    
    .round-btn::before {{
        content: '🎲';
        margin-right: 3px;
        font-size: 12px;
    }}
    
    .round-btn:hover, .zodiac-btn:hover {{
        background: #f1f5f9;
        transform: translateY(-1px);
        box-shadow: 0 3px 8px rgba(0,0,0,0.1);
    }}
    
    .round-btn.active {{
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
        border-color: #dc2626;
        box-shadow: 0 3px 12px rgba(239, 68, 68, 0.4);
    }}
    
    .zodiac-btn.active {{
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        border-color: #059669;
        box-shadow: 0 3px 12px rgba(16, 185, 129, 0.4);
    }}
    
    #chart {{
        width: 100%;
        height: 500px;
        position: relative;
        background: white;
        border-radius: 12px;
        padding: 30px;
        border: 1px solid #e2e8f0;
    }}
    
    #lineChart {{
        width: 100%;
        height: 100%;
        position: relative;
    }}
    
    .chart-svg {{
        width: 100%;
        height: 100%;
    }}
    
    .grid-line {{
        stroke: #f1f5f9;
        stroke-width: 0.5;
    }}
    
    .line-path {{
        fill: none;
        stroke: url(#lineGradient);
        stroke-width: 5;
        stroke-linecap: round;
        stroke-linejoin: round;
        filter: drop-shadow(0 3px 6px rgba(59, 130, 246, 0.4));
    }}
    
    .point {{
        fill: white;
        stroke: #3b82f6;
        stroke-width: 4;
        cursor: pointer;
        transition: all 0.3s;
        filter: drop-shadow(0 3px 6px rgba(59, 130, 246, 0.5));
    }}
    
    .point:hover {{
        fill: #ef4444;
        stroke: white;
        stroke-width: 4;
        r: 9;
        filter: drop-shadow(0 4px 8px rgba(239, 68, 68, 0.6));
    }}
    
    .point-label {{
        font-size: 11px;
        font-weight: bold;
        fill: #475569;
        text-anchor: middle;
    }}
    
    .axis-label {{
        font-size: 12px;
        fill: #64748b;
        font-weight: bold;
    }}
    
    .tooltip {{
        position: absolute;
        background: rgba(0,0,0,0.85);
        color: white;
        padding: 8px 12px;
        border-radius: 8px;
        font-size: 13px;
        pointer-events: none;
        display: none;
        z-index: 1000;
        white-space: nowrap;
    }}
    
    .social-container {{
        position: fixed;
        top: 15px;
        left: 15px;
        display: flex;
        gap: 6px;
        z-index: 1000;
    }}
    
    .social-btn {{
        padding: 5px 10px;
        border-radius: 15px;
        border: none;
        font-weight: bold;
        font-size: 10px;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }}
    
    .youtube-btn {{
        background: #FF0000;
        color: white;
    }}
    
    .youtube-btn:hover {{
        background: #CC0000;
        transform: translateY(-1px);
    }}
    
    .share-btn {{
        background: #10b981;
        color: white;
    }}
    
    .share-btn:hover {{
        background: #059669;
        transform: translateY(-1px);
    }}
    
    .share-menu {{
        position: absolute;
        top: 35px;
        left: 0;
        background: white;
        border-radius: 8px;
        padding: 6px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        display: none;
        min-width: 120px;
    }}
    
    .share-menu.active {{
        display: block;
    }}
    
    .share-option {{
        padding: 6px 10px;
        cursor: pointer;
        border-radius: 5px;
        transition: all 0.2s;
        font-size: 11px;
        color: #374151;
    }}
    
    .share-option:hover {{
        background: #f3f4f6;
    }}
    
    .pointer-animation {{
        position: fixed;
        top: 45px;
        left: 40px;
        font-size: 20px;
        z-index: 999;
        animation: pointUp 1s ease-in-out infinite;
    }}
    
    @keyframes pointUp {{
        0%, 100% {{
            transform: translateY(0px);
        }}
        50% {{
            transform: translateY(-5px);
        }}
    }}
</style>
</head>
<body>
    <!-- YouTube 및 공유 버튼 -->
    <div class="pointer-animation">👆</div>
    <div class="social-container">
        <div style="position:fixed;top:13px;right:13px;font-size:1.25rem;font-weight:bold;color:#fff;z-index:1001;background:rgba(16,185,129,0.98);padding:7px 22px;border-radius:18px;box-shadow:0 3px 12px rgba(0,0,0,0.20);letter-spacing:0.7px;line-height:1.15;">
            로또 추천회차 <span style="color:#fff;">@@ROUND@@</span>
        </div>
        <button class="social-btn youtube-btn" onclick="goToYoutube()">
            ▶️ 구독하기
        </button>
        <div style="position: relative;">
            <button class="social-btn share-btn" onclick="toggleShareMenu()">
                🔗 공유
            </button>
            <div class="share-menu" id="shareMenu">
                <div class="share-option" onclick="shareKakao()">
                    🟡 카카오톡
                </div>
                <div class="share-option" onclick="shareFacebook()">
                    🔵 페이스북
                </div>
                <div class="share-option" onclick="shareTwitter()">
                    🔵 트위터
                </div>
                <div class="share-option" onclick="copyURL()">
                    📋 URL 복사
                </div>
            </div>
        </div>
    </div>
    
    <div id="title">이걸 본 당신, 행운 잡으세요</div>
    
    <div id="button-container">
        <button id="startBtn" onclick="startAnimation()">🎲</button>
    </div>
    
    <div id="ball-container">
        <div class="balls-row" id="balls"></div>
        <div class="zodiac-selector">
            <button class="zodiac-btn" onclick="selectZodiac('쥐')">🐭쥐</button>
            <button class="zodiac-btn" onclick="selectZodiac('소')">🐮소</button>
            <button class="zodiac-btn" onclick="selectZodiac('호랑이')">🐯호랑이</button>
            <button class="zodiac-btn" onclick="selectZodiac('토끼')">🐰토끼</button>
            <button class="zodiac-btn" onclick="selectZodiac('용')">🐲용</button>
            <button class="zodiac-btn" onclick="selectZodiac('뱀')">🐍뱀</button>
            <button class="zodiac-btn" onclick="selectZodiac('말')">🐴말</button>
            <button class="zodiac-btn" onclick="selectZodiac('양')">🐑양</button>
            <button class="zodiac-btn" onclick="selectZodiac('원숭이')">🐵원숭이</button>
            <button class="zodiac-btn" onclick="selectZodiac('닭')">🐔닭</button>
            <button class="zodiac-btn" onclick="selectZodiac('개')">🐶개</button>
            <button class="zodiac-btn" onclick="selectZodiac('돼지')">🐷돼지</button>
        </div>
    </div>
    
    <div id="result" style="display:none;"></div>
    
    <div id="hexagram-container">
        <div class="hexagram-title">🔮 주역 64괘 행운 번호 🔮</div>
        <div class="hexagram-info">
                <div class="time-display">📅 @@CURRENT_TIME@@</div>
            <div class="hexagram-name">✨ @@HEXAGRAM_NAME@@ (제@@HEXAGRAM_NUM@@괘) ✨</div>
        </div>
        <div class="lucky-numbers">
            <div class="lucky-title">🍀 당신의 행운 번호 8개</div>
            <div class="lucky-balls">
                @@LUCKY_BALLS@@
            </div>
        </div>
        <div class="hexagram-desc">
            @@HEXAGRAM_DESC@@
        </div>
    </div>
    
    <div id="combo-container">
        <div class="stats-title">🎯 추천 조합 (6개 번호)</div>
        <div class="combo-items">
            @@RECOMMENDED_COMBOS@@
        </div>
    </div>
    
    <div id="custom-container">
        <div class="stats-title">✨ 직접 번호 선택하기</div>
        <div style="text-align: center; color: #831843; font-size: 13px; margin-bottom: 12px; font-weight: 500;">
            💡 위의 추천 번호를 참고하여 선택하면 더 좋습니다!
        </div>
        <div style="display: flex; justify-content: center; width: 100%;">
            <div class="number-grid">
                <!-- 1~45번 번호 선택 버튼 복구 -->
                @@NUMBER_BUTTONS@@
            </div>
        </div>
        <div class="selected-display">
            <div class="selected-title">선택한 번호 (<span id="selected-count">0</span>/30)</div>
            <div id="selected-numbers"></div>
            <div style="display: flex; justify-content: center; gap: 10px; margin-top: 10px;">
                <button class="copy-btn" id="custom-copy-btn" onclick="copyCustom()" style="display:none;">📋 선택 번호 복사</button>
                <button class="copy-btn" id="qr-btn" onclick="generateQR()" style="display:none;">📱 QR 코드 생성</button>
            </div>
        </div>
        <div class="qr-container" id="qr-container" style="display:none;">
            <canvas id="qr-canvas"></canvas>
        </div>
    </div>
    
    <div id="stats-container">
        <div class="stats-title">📊 통계</div>
        <div class="round-selector">
            <button class="round-btn active" onclick="changeRound(150)">150</button>
            <button class="round-btn" onclick="changeRound(75)">75</button>
            <button class="round-btn" onclick="changeRound(45)">45</button>
            <button class="round-btn" onclick="changeRound(30)">30</button>
            <button class="round-btn" onclick="changeRound(15)">15</button>
        </div>
        <div id="chart">
            <svg id="lineChart" class="chart-svg"></svg>
            <div class="tooltip" id="tooltip"></div>
        </div>
    </div>
    
    <div class="warning-notice">
        <strong style="font-size: 18px; color: #fbbf24;">⚠️ 중요 안내</strong>
        <div style="font-size: 15px; font-weight: bold; margin-top: 10px; line-height: 1.8;">
            본 영상은 재미와 참고용입니다. 로또는 확률게임 이며 당첨을 보장하지 않읍니다<br>
            무리한 구매는 삼가 하세요
        </div>
    </div>


<script>
    const colors = ["🔵", "🔴", "🟡", "🟢", "🟣", "🟠"];
    const finalNumbers = [@@FINAL_STR@@];
    let isRunning = false;
    
    // 배경 파티클 생성
    function createParticles() {{
        for(let i = 0; i < 20; i++) {{
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.width = Math.random() * 50 + 10 + 'px';
            particle.style.height = particle.style.width;
            particle.style.left = Math.random() * 100 + '%';
            particle.style.top = Math.random() * 100 + '%';
            particle.style.animation = `float ${{Math.random() * 3 + 2}}s infinite`;
            particle.style.animationDelay = Math.random() * 2 + 's';
            document.body.appendChild(particle);
        }}
    }}
    

    
    // 폭죽 효과
    function createConfetti() {{
        for(let i = 0; i < 50; i++) {{
            setTimeout(() => {{
                const confetti = document.createElement('div');
                confetti.className = 'confetti';
                confetti.style.left = Math.random() * 100 + '%';
                confetti.style.top = '-10px';
                confetti.style.background = ['#fbbf24', '#ef4444', '#3b82f6', '#10b981'][Math.floor(Math.random() * 4)];
                document.body.appendChild(confetti);
                setTimeout(() => confetti.remove(), 3000);
            }}, i * 30);
        }}
    }}

    function getRandomNumbers() {{
        const nums = [];
        while(nums.length < 6) {{
            const r = Math.floor(Math.random() * 45) + 1;
            if(!nums.includes(r)) nums.push(r);
        }}
        return nums;
    }}

    function displayBalls(numbers, isFinal = false, spinning = false) {{
        const ballsDiv = document.getElementById('balls');
        const container = document.getElementById('ball-container');
        
        let html = '';
        numbers.forEach((num, i) => {{
            html += `<div class="ball ball-${{i}}">${{String(num).padStart(2, '0')}}</div>`;
        }});
        
        ballsDiv.innerHTML = html;
        
        if(isFinal) {{
            container.className = 'final';
        }} else if(spinning) {{
            container.className = 'spinning';
        }} else {{
            container.className = '';
        }}
    }}
    
    // 초기 화면
    displayBalls([8, 14, 15, 19, 31, 32]);

    function startAnimation() {{
        if(isRunning) return;
        isRunning = true;
        
        const btn = document.getElementById('startBtn');
        const result = document.getElementById('result');
        
        btn.disabled = true;
        btn.innerHTML = '⏳';
        result.style.display = 'flex';
        result.innerHTML = '⚙️ 추첨기 가동 중... ⚙️';
        
        let count = 0;
        const interval = setInterval(() => {{
            const randomNums = getRandomNumbers();
            displayBalls(randomNums, false, true);
            count++;
            
            if(count >= 60) {{
                clearInterval(interval);
                displayBalls(finalNumbers, true, false);
                result.style.display = 'flex';
                result.innerHTML = '🎉 당첨 번호: ' + finalNumbers.join(' - ');
                btn.innerHTML = '🎲';
                btn.disabled = false;
                isRunning = false;
                createConfetti();
            }}
        }}, 70);
    }}
    
    // 통계 데이터
    const statsData = @@STATS_JSON@@;
    let currentRound = 150;
    
    // 꺾은선 그래프 그리기
    function drawChart(round) {{
        const roundData = statsData[round.toString()];
        const stats = roundData.stats;
        const svg = document.getElementById('lineChart');
        const tooltip = document.getElementById('tooltip');
        
        // SVG 크기
        const width = svg.clientWidth;
        const height = svg.clientHeight;
        const padding = 40;
        const chartWidth = width - padding * 2;
        const chartHeight = height - padding * 2;
        
        // 데이터를 번호 순서대로 정렬
        let sortedData = Object.entries(stats)
            .sort((a, b) => parseInt(a[0]) - parseInt(b[0]));
        
        // 띠별 필터링
        if(selectedZodiac) {{
            const zodiacNums = zodiacNumbers[selectedZodiac];
            sortedData = sortedData.filter(([num]) => zodiacNums.includes(parseInt(num)));
        }}
        
        const maxValue = Math.max(...sortedData.map(item => item[1]));
        const minValue = Math.min(...sortedData.map(item => item[1]));
        
        // SVG 초기화
        svg.innerHTML = '';
        
        // 그라데이션 정의
        const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
        const gradient = document.createElementNS('http://www.w3.org/2000/svg', 'linearGradient');
        gradient.setAttribute('id', 'lineGradient');
        gradient.setAttribute('x1', '0%');
        gradient.setAttribute('y1', '0%');
        gradient.setAttribute('x2', '100%');
        gradient.setAttribute('y2', '0%');
        
        const stop1 = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
        stop1.setAttribute('offset', '0%');
        stop1.setAttribute('style', 'stop-color:#3b82f6;stop-opacity:1');
        
        const stop2 = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
        stop2.setAttribute('offset', '100%');
        stop2.setAttribute('style', 'stop-color:#8b5cf6;stop-opacity:1');
        
        gradient.appendChild(stop1);
        gradient.appendChild(stop2);
        defs.appendChild(gradient);
        svg.appendChild(defs);
        
        // 격자선 그리기
        for(let i = 0; i <= 5; i++) {{
            const y = padding + (chartHeight / 5) * i;
            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            line.setAttribute('x1', padding);
            line.setAttribute('y1', y);
            line.setAttribute('x2', width - padding);
            line.setAttribute('y2', y);
            line.setAttribute('class', 'grid-line');
            svg.appendChild(line);
            
            // Y축 라벨
            const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            const value = Math.round(maxValue - (maxValue - minValue) / 5 * i);
            label.setAttribute('x', padding - 10);
            label.setAttribute('y', y + 5);
            label.setAttribute('text-anchor', 'end');
            label.setAttribute('class', 'axis-label');
            label.textContent = value;
            svg.appendChild(label);
        }}
        
        // 선 그리기 위한 경로
        let pathData = '';
        const points = [];
        
        sortedData.forEach(([num, freq], index) => {{
            const x = padding + (chartWidth / (sortedData.length - 1)) * index;
            const y = padding + chartHeight - ((freq - minValue) / (maxValue - minValue)) * chartHeight;
            
            points.push({{ x, y, num, freq }});
            
            if(index === 0) {{
                pathData += `M ${{x}} ${{y}}`;
            }} else {{
                pathData += ` L ${{x}} ${{y}}`;
            }}
        }});
        
        // 선 그리기
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', pathData);
        path.setAttribute('class', 'line-path');
        svg.appendChild(path);
        
        // 포인트와 라벨 그리기
        points.forEach((point, index) => {{
            // 포인트
            const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            circle.setAttribute('cx', point.x);
            circle.setAttribute('cy', point.y);
            circle.setAttribute('r', 4);
            circle.setAttribute('class', 'point');
            
            // 툴팁 이벤트
            circle.addEventListener('mouseenter', (e) => {{
                tooltip.innerHTML = `${{point.num}}번: ${{point.freq}}회`;
                tooltip.style.display = 'block';
                tooltip.style.left = e.pageX + 10 + 'px';
                tooltip.style.top = e.pageY - 30 + 'px';
            }});
            
            circle.addEventListener('mouseleave', () => {{
                tooltip.style.display = 'none';
            }});
            
            svg.appendChild(circle);
            
            // X축 라벨 (5개마다 표시)
            if(index % 5 === 0 || index === points.length - 1) {{
                const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                label.setAttribute('x', point.x);
                label.setAttribute('y', height - padding + 20);
                label.setAttribute('class', 'point-label');
                label.textContent = point.num;
                svg.appendChild(label);
            }}
        }});
    }}
    
    // 회차 변경
    function changeRound(round) {{
        currentRound = round;
        
        // 버튼 활성화 상태 변경
        document.querySelectorAll('.round-btn').forEach(btn => {{
            btn.classList.remove('active');
        }});
        event.target.classList.add('active');
        
        // 그래프 업데이트
        drawChart(round);
    }}
    
    // 띠별 번호 매핑 (12지신 기준)
    const zodiacNumbers = {{
        '쥐': [1, 13, 25, 37],
        '소': [2, 14, 26, 38],
        '호랑이': [3, 15, 27, 39],
        '토끼': [4, 16, 28, 40],
        '용': [5, 17, 29, 41],
        '뱀': [6, 18, 30, 42],
        '말': [7, 19, 31, 43],
        '양': [8, 20, 32, 44],
        '원숭이': [9, 21, 33, 45],
        '닭': [10, 22, 34],
        '개': [11, 23, 35],
        '돼지': [12, 24, 36]
    }};
    
    const zodiacEmoji = {{
        '쥐': '🐭',
        '소': '🐮',
        '호랑이': '🐯',
        '토끼': '🐰',
        '용': '🐲',
        '뱀': '🐍',
        '말': '🐴',
        '양': '🐑',
        '원숭이': '🐵',
        '닭': '🐔',
        '개': '🐶',
        '돼지': '🐷'
    }};

    // 띠별 대표 출생 연도 (5개씩, 12년 주기)
    const zodiacYears = {{
        '쥐': [1948, 1960, 1972, 1984, 1996],
        '소': [1949, 1961, 1973, 1985, 1997],
        '호랑이': [1950, 1962, 1974, 1986, 1998],
        '토끼': [1951, 1963, 1975, 1987, 1999],
        '용': [1952, 1964, 1976, 1988, 2000],
        '뱀': [1953, 1965, 1977, 1989, 2001],
        '말': [1954, 1966, 1978, 1990, 2002],
        '양': [1955, 1967, 1979, 1991, 2003],
        '원숭이': [1956, 1968, 1980, 1992, 2004],
        '닭': [1957, 1969, 1981, 1993, 2005],
        '개': [1958, 1970, 1982, 1994, 2006],
        '돼지': [1959, 1971, 1983, 1995, 2007]
    }};
    
    let selectedZodiac = null;
    
    // 띠 선택
    function selectZodiac(zodiac) {{
        if(isRunning) return;
        
        const result = document.getElementById('result');
        
        // 버튼 활성화 상태 변경
        document.querySelectorAll('.zodiac-btn').forEach(btn => {{
            btn.classList.remove('active');
        }});
        
        if(selectedZodiac === zodiac) {{
            selectedZodiac = null; // 토글
            // 초기 화면으로 (애니메이션 없이)
            displayBalls([8, 14, 15, 19, 31, 32]);
            result.style.display = 'none';
        }} else {{
            selectedZodiac = zodiac;
            event.target.classList.add('active');
            
            // 해당 띠의 번호 계산
            const numbers = [...zodiacNumbers[zodiac]];
            
            // 6개가 안되면 랜덤 번호 추가 (중복 제거)
            const allNumbers = Array.from({{length: 45}}, (_, i) => i + 1);
            const availableNumbers = allNumbers.filter(n => !numbers.includes(n));
            
            while(numbers.length < 6 && availableNumbers.length > 0) {{
                const randomIndex = Math.floor(Math.random() * availableNumbers.length);
                numbers.push(availableNumbers[randomIndex]);
                availableNumbers.splice(randomIndex, 1);
            }}
            
            // 정렬
            const sortedNumbers = numbers.sort((a, b) => a - b);
            
            // 애니메이션 시작
            isRunning = true;
            const container = document.getElementById('ball-container');
            container.classList.add('spinning');
            
            let count = 0;
            const interval = setInterval(() => {{
                displayBalls(getRandomNumbers(), false, true);
                count++;
                
                if(count >= 60) {{
                    clearInterval(interval);
                    container.classList.remove('spinning');
                    displayBalls(sortedNumbers, true);
                    createConfetti();
                        isRunning = false;

                        // 선택한 띠의 대표 출생 연도 5개 표시 (각 연도를 클릭하면 연도별 추천 번호 생성)
                        const years = zodiacYears[zodiac] || [];
                        let yearsHtml = '';
                        for(let i = 0; i < years.length; i++) {{
                        yearsHtml += `<button class="year-btn" style="margin:4px; min-width:70px;" onclick="selectYear('${{zodiac}}', ${{years[i]}})">${{years[i]}}</button>`;
                    }}
                        result.style.display = 'flex';
                        // 한 행에 간단히 표시 (출생년도 테스트) + 하단에 결과를 쌓을 영역 추가
                        result.innerHTML = `<div style="display:flex;flex-direction:column;gap:8px;width:100%;">
                            <div style="display:flex;flex-direction:row;align-items:center;gap:10px;flex-wrap:wrap;">
                                <div style="font-size:16px; font-weight:700;">출생년도 테스트:</div>
                                <div style="display:flex;gap:6px;align-items:center;">${{yearsHtml}}</div>
                            </div>
                            <div id="year-results" style="width:100%; display:flex;flex-direction:column;gap:6px;align-items:center;"></div>
                        </div>`;

                        // 주역 기반 오행 2개 선택(자동 날짜 사용)
                        (function() {{
                            // 현재 시간 사용 (개인정보 보호: 사용자 입력 없음)
                            const now = new Date();
                            const y = now.getFullYear();
                            const m = now.getMonth() + 1;
                            const d = now.getDate();
                            const h = now.getHours();

                            // 간단한 hexagram 계산 (서버와 동일한 방식)
                            const hexNum = ((y + m + d + h) % 64);
                            const top1 = hexNum;
                            const top2 = (hexNum + 1) % 64;
                            const rep1 = (top1 % 45) + 1;
                            const rep2 = (top2 % 45) + 1;

                            function getElementByNum(n) {{
                                if(n <= 9) return '목';
                                if(n <= 18) return '화';
                                if(n <= 27) return '토';
                                if(n <= 36) return '금';
                                return '수';
                            }}

                            const elIcons = {{ '목':'🌳', '화':'🔥', '토':'⛰️', '금':'⚙️', '수':'💧' }};
                            const elColors = {{ '목':'#10b981', '화':'#ef4444', '토':'#a16207', '금':'#f59e0b', '수':'#3b82f6' }};

                            function makeBadge(el, num) {{
                                const icon = elIcons[el] || '•';
                                const color = elColors[el] || '#999999';
                                return `<span style="display:inline-flex;align-items:center;gap:8px;margin:0 6px;">
                                            <span style="width:28px;height:28px;border-radius:8px;background:${{color}};display:inline-flex;align-items:center;justify-content:center;color:white;font-weight:700;">${{icon}}</span>
                                            <span style="font-size:14px;color:#111;">${{el}} ${{num}}</span>
                                        </span>`;
                            }

                            // mulberry32 PRNG
                            function mulberry32(a) {{
                                return function() {{
                                    var t = a += 0x6D2B79F5;
                                    t = Math.imul(t ^ t >>> 15, t | 1);
                                    t ^= t + Math.imul(t ^ t >>> 7, t | 61);
                                    return ((t ^ t >>> 14) >>> 0) / 4294967296;
                                }};
                            }}

                            function pickFromElement(el, seedVal) {{
                                const ranges = {{ '목':[1,9], '화':[10,18], '토':[19,27], '금':[28,36], '수':[37,45] }};
                                const r = ranges[el];
                                const pool = [];
                                for(let i = r[0]; i <= r[1]; i++) pool.push(i);
                                const rnd = mulberry32(seedVal >>> 0);
                                const idx = Math.floor(rnd() * pool.length);
                                return pool[idx];
                            }}

                            const el1 = getElementByNum(rep1);
                            const el2 = getElementByNum(rep2);
                            const seedA = y * 10000 + m * 100 + d + h + rep1;
                            const seedB = y * 10000 + m * 100 + d + h + rep2;
                            const pickA = pickFromElement(el1, seedA);
                            const pickB = pickFromElement(el2, seedB);

                            // 결과 카드 표시
                            const yearResultsDiv = document.getElementById('year-results');
                            if(yearResultsDiv) {{
                                const card = document.createElement('div');
                                card.style.width = '100%';
                                card.style.maxWidth = '680px';
                                card.style.background = '#e5e7eb';
                                card.style.color = '#000000';
                                card.style.borderRadius = '10px';
                                card.style.padding = '10px 14px';
                                card.style.boxShadow = '0 4px 12px rgba(0,0,0,0.06)';
                                card.style.fontWeight = '700';
                                card.style.textAlign = 'center';
                                card.style.position = 'relative';
                                card.innerHTML = `<div style="font-size:14px;">${{zodiacEmoji[zodiac]}} ${{zodiac}} - 주역상위괘: ${{top1}}/${{top2}} → ` + makeBadge(el1, pickA) + makeBadge(el2, pickB) + `</div>`;

                                const closeBtn = document.createElement('button');
                                closeBtn.className = 'close-card-btn';
                                closeBtn.textContent = '닫기';
                                closeBtn.onclick = function() {{
                                    if(card && card.parentNode) card.parentNode.removeChild(card);
                                }};
                                card.appendChild(closeBtn);

                                yearResultsDiv.insertBefore(card, yearResultsDiv.firstChild);
                            }}
                        }})();
                }}
            }}, 70);
            
            // 결과 메시지 숨김
            result.style.display = 'none';
        }}
        
        // 띠 선택 시 그래프는 다시 그리지 않음 (150,75,45,30,15 버튼으로만 변경)
    }}
    
    // 특정 연도 선택 시 해당 연도를 시드로 사용하여 추천 번호 생성
    function selectYear(zodiac, year) {{
        if(isRunning) return;
        const result = document.getElementById('result');

        // 간단한 시드 기반 PRNG (mulberry32)
        function mulberry32(a) {{
            return function() {{
                var t = a += 0x6D2B79F5;
                t = Math.imul(t ^ t >>> 15, t | 1);
                t ^= t + Math.imul(t ^ t >>> 7, t | 61);
                return ((t ^ t >>> 14) >>> 0) / 4294967296;
            }};
        }}

        // 시드 생성: 연도 기반 + 띠의 문자 코드 값 조합
        const seedVal = parseInt(year, 10) * 9973 + zodiac.charCodeAt(0);
        const rnd = mulberry32(seedVal >>> 0);

        // 1~45에서 중복 없이 6개 선택
        const pool = Array.from({{length:45}}, (_, i) => i + 1);
        const nums = [];
        while(nums.length < 6 && pool.length > 0) {{
            const idx = Math.floor(rnd() * pool.length);
            nums.push(pool[idx]);
            pool.splice(idx, 1);
        }}
        nums.sort((a, b) => a - b);

        // 볼 표시 및 결과 카드를 하단에 추가
        const yearResults = document.getElementById('year-results');
        const container = document.getElementById('ball-container');
        if(!yearResults) {{
            // 안전 장치: 만약 year-results 영역이 없으면 기존 방식으로 출력
            displayBalls(nums, true);
            result.style.display = 'flex';
            result.innerHTML = `${{zodiacEmoji[zodiac]}} ${{zodiac}} 띠 ${{year}}년 출생 추천 번호: ${{nums.join(' - ')}}`;
            return;
        }}

        // 스핀 애니메이션 시작 (짧은 미리보기)
        let spinCount = 0;
        container.classList.add('spinning');
        const spinInterval = setInterval(() => {{
            displayBalls(getRandomNumbers(), false, true);
            spinCount++;
            if(spinCount >= 18) {{
                clearInterval(spinInterval);
                container.classList.remove('spinning');
                // 최종 번호 표시 및 폭죽
                displayBalls(nums, true);
                createConfetti();

                // 결과 카드 생성
                const card = document.createElement('div');
                card.style.width = '100%';
                card.style.maxWidth = '680px';
                card.style.background = '#e5e7eb';
                card.style.color = '#000000';
                card.style.borderRadius = '10px';
                card.style.padding = '10px 14px';
                card.style.boxShadow = '0 4px 12px rgba(0,0,0,0.06)';
                card.style.fontWeight = '700';
                card.style.textAlign = 'center';
                const elIcons_local = {{ '목':'🌳', '화':'🔥', '토':'⛰️', '금':'⚙️', '수':'💧' }};
                const elColors_local = {{ '목':'#10b981', '화':'#ef4444', '토':'#a16207', '금':'#f59e0b', '수':'#3b82f6' }};
                function getElementLocal(n) {{
                    if(n <= 9) return '목';
                    if(n <= 18) return '화';
                    if(n <= 27) return '토';
                    if(n <= 36) return '금';
                    return '수';
                }
                const badges = nums.map(n => {{
                    const el = getElementLocal(n);
                    const icon = elIcons_local[el] || '•';
                    const color = elColors_local[el] || '#999999';
                    return `<span style="display:inline-flex;align-items:center;gap:8px;margin:0 6px;">
                                <span style="width:26px;height:26px;border-radius:7px;background:${{color}};display:inline-flex;align-items:center;justify-content:center;color:white;font-weight:700;">${{icon}}</span>
                                <span style="font-size:14px;color:#111;">${{n}}</span>
                            </span>`;
                }}).join('');
                card.innerHTML = `<div style="display:flex;flex-direction:column;align-items:center;gap:6px;"><div style="font-size:14px;">${{zodiacEmoji[zodiac]}} ${{zodiac}} 띠 ${{year}}년 출생 추천 번호</div><div style="display:flex;flex-wrap:wrap;justify-content:center;">${{badges}}</div></div>`;

                // 닫기 버튼 추가 (사용자가 직접 닫음)
                card.style.position = 'relative';
                const closeBtn = document.createElement('button');
                closeBtn.className = 'close-card-btn';
                closeBtn.textContent = '닫기';
                closeBtn.onclick = function() {{
                    if(card && card.parentNode) card.parentNode.removeChild(card);
                    // 기본 공으로 복원
                    displayBalls([8, 14, 15, 19, 31, 32]);
                }};
                card.appendChild(closeBtn);

                // 하단에 추가
                yearResults.insertBefore(card, yearResults.firstChild);
            }}
        }}, 70);
    }}

    // 조합 복사 기능
    function copyCombo(numbers) {{
        const text = numbers.join(', ');
        navigator.clipboard.writeText(text).then(() => {{
            alert('복사되었습니다: ' + text);
        }}).catch(err => {{
            alert('복사 실패');
        }});
    }}
    
    // 선택된 조합들 (최대 5개 조합)
    let combinations = [];
    let currentCombo = [];
    
    // 번호 선택
    function toggleNumber(num) {{
        const btn = event.target;
        
        // 이미 5조합 완성되었으면 더 선택 불가
        if(combinations.length >= 5 && currentCombo.length === 0) {{
            alert('최대 5개 조합까지만 선택 가능합니다!');
            return;
        }}
        
        // 현재 조합에 추가
        if(currentCombo.length < 6) {{
            currentCombo.push(num);
            btn.classList.add('selected');
            btn.disabled = true;
            
            // 6개가 되면 조합 완성
            if(currentCombo.length === 6) {{
                currentCombo.sort((a, b) => a - b);
                combinations.push([...currentCombo]);
                currentCombo = [];
            }}
        }}
        
        // 화면 업데이트
        updateSelectedDisplay();
    }}
    
    // 전체 초기화 버튼
    function resetAllSelections() {{
        combinations = [];
        currentCombo = [];
        
        // 모든 버튼 초기화
        document.querySelectorAll('.number-btn').forEach(btn => {{
            btn.classList.remove('selected');
            btn.disabled = false;
        }});
        
        updateSelectedDisplay();
    }}
    
    // 번호별 색상 클래스 반환
    function getNumberColor(num) {{
        if(num <= 9) return 'linear-gradient(135deg, #3b82f6, #1d4ed8)';
        if(num <= 18) return 'linear-gradient(135deg, #ef4444, #dc2626)';
        if(num <= 27) return 'linear-gradient(135deg, #a16207, #78350f)';
        if(num <= 36) return 'linear-gradient(135deg, #fbbf24, #f59e0b)';
        return 'linear-gradient(135deg, #8b5cf6, #7c3aed)';
    }}
    
    // 선택된 번호 표시 업데이트
    function updateSelectedDisplay() {{
        const countSpan = document.getElementById('selected-count');
        const numbersDiv = document.getElementById('selected-numbers');
        const qrBtn = document.getElementById('qr-btn');
        
        const totalSelected = combinations.length * 6 + currentCombo.length;
        countSpan.textContent = totalSelected;
        
        if(combinations.length === 0 && currentCombo.length === 0) {{
            numbersDiv.innerHTML = '<div style="color: rgba(255,255,255,0.6);">번호를 6개씩 선택하세요 (최대 5조합)</div>';
            qrBtn.style.display = 'none';
        }} else {{
            let html = '<div style="width: 100%;">';
            
            // 완성된 조합들 표시
            combinations.forEach((comboNums, i) => {{
                html += `
                    <div style="background: white; border-radius: 10px; padding: 10px; margin-bottom: 8px;">
                        <div style="font-size: 12px; color: #831843; font-weight: bold; margin-bottom: 5px;">조합 ${{i + 1}} ✓</div>
                        <div style="display: flex; justify-content: center; gap: 6px; margin-bottom: 8px;">
                            ${{comboNums.map(num => 
                                `<div class="combo-ball" style="background: ${{getNumberColor(num)}}; width: 30px; height: 30px; font-size: 14px;"><span>${{num}}</span></div>`
                            ).join('')}}
                        </div>
                        <button class="copy-btn" style="font-size: 11px; padding: 6px 12px;" onclick="copyCombo(${{JSON.stringify(comboNums)}})">📋 복사</button>
                    </div>
                `;
            }});
            
            // 현재 선택 중인 번호들 표시
            if(currentCombo.length > 0) {{
                html += `
                    <div style="background: rgba(255,255,255,0.5); border-radius: 10px; padding: 10px; margin-bottom: 8px; border: 2px dashed #ec4899;">
                        <div style="font-size: 12px; color: #831843; font-weight: bold; margin-bottom: 5px;">선택 중... (${{currentCombo.length}}/6)</div>
                        <div style="display: flex; justify-content: center; gap: 6px;">
                            ${{currentCombo.map(num => 
                                `<div class="combo-ball" style="background: ${{getNumberColor(num)}}; width: 30px; height: 30px; font-size: 14px;"><span>${{num}}</span></div>`
                            ).join('')}}
                        </div>
                    </div>
                `;
            }}
            
            // 초기화 버튼
            html += '<button class="copy-btn" style="margin-top: 10px; background: linear-gradient(135deg, #ef4444, #dc2626);" onclick="resetAllSelections()">🔄 전체 초기화</button>';
            
            html += '</div>';
            numbersDiv.innerHTML = html;
            
            // QR 버튼은 1개 이상 조합 완성 시 표시
            qrBtn.style.display = combinations.length > 0 ? 'inline-block' : 'none';
        }}
    }}
    
    // QR 코드 생성
    function generateQR() {{
        if(combinations.length === 0) {{
            alert('최소 1개 조합을 완성해주세요!');
            return;
        }}
        
        const qrContainer = document.getElementById('qr-container');
        const canvas = document.getElementById('qr-canvas');
        
        // 간단한 QR 코드 대체 (실제 구현은 QR 라이브러리 필요)
        // 여기서는 텍스트 형태로 표시
        const ctx = canvas.getContext('2d');
        const numCombos = combinations.length;
        canvas.width = 400;
        canvas.height = Math.max(300, 150 + numCombos * 30);
        
        // 흰 배경
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // 검은 테두리
        ctx.strokeStyle = '#000000';
        ctx.lineWidth = 3;
        ctx.strokeRect(10, 10, canvas.width - 20, canvas.height - 20);
        
        // 번호 텍스트
        ctx.fillStyle = '#000000';
        ctx.font = 'bold 22px Arial';
        ctx.textAlign = 'center';
        const centerX = canvas.width / 2;
        ctx.fillText('🎰 로또 번호 ' + combinations.length + '개 조합 🎰', centerX, 50);
        
        // 각 조합을 표시
        ctx.font = 'bold 16px Arial';
        let yPos = 90;
        combinations.forEach((combo, i) => {{
            ctx.fillText(`조합 ${{i+1}}`, centerX, yPos);
            ctx.font = 'bold 18px Arial';
            ctx.fillText(combo.join(' - '), centerX, yPos + 25);
            ctx.font = 'bold 16px Arial';
            yPos += 55;
        }});
        
        ctx.font = 'bold 16px Arial';
        ctx.fillText('🍀 행운을 빕니다! 🍀', centerX, yPos + 15);
        
        // QR 컨테이너 표시
        qrContainer.style.display = 'flex';
        
        // 스크롤 이동
        qrContainer.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
    }}
    
    // YouTube 이동 (채널 생성 후 URL 변경)
    function goToYoutube() {{
        // TODO: YouTube 채널 생성 후 아래 URL을 본인 채널 URL로 변경하세요
        window.open('https://www.youtube.com/@YourChannelName', '_blank');
        // 예: window.open('https://www.youtube.com/@LuckyLotto777', '_blank');
    }}
    
    // 공유 메뉴 토글
    function toggleShareMenu() {{
        const menu = document.getElementById('shareMenu');
        menu.classList.toggle('active');
    }}
    
    // 카카오톡 공유
    function shareKakao() {{
        const url = window.location.href;
        const text = '🍀 로또 행운번호 생성기! 당신의 행운을 찾아보세요!';
        window.open(`https://sharer.kakao.com/talk/friends?url=${{encodeURIComponent(url)}}&text=${{encodeURIComponent(text)}}`, '_blank');
        toggleShareMenu();
    }}
    
    // 페이스북 공유
    function shareFacebook() {{
        const url = window.location.href;
        window.open(`https://www.facebook.com/sharer/sharer.php?u=${{encodeURIComponent(url)}}`, '_blank');
        toggleShareMenu();
    }}
    
    // 트위터 공유
    function shareTwitter() {{
        const url = window.location.href;
        const text = '🍀 로또 행운번호 생성기! 당신의 행운을 찾아보세요!';
        window.open(`https://twitter.com/intent/tweet?url=${{encodeURIComponent(url)}}&text=${{encodeURIComponent(text)}}`, '_blank');
        toggleShareMenu();
    }}
    
    // URL 복사
    function copyURL() {{
        const url = window.location.href;
        navigator.clipboard.writeText(url).then(() => {{
            alert('링크가 복사되었습니다! 친구들과 공유해보세요 🎉');
        }}).catch(() => {{
            alert('복사 실패. 다시 시도해주세요.');
        }});
        toggleShareMenu();
    }}
    
    // 외부 클릭 시 공유 메뉴 닫기
    document.addEventListener('click', function(e) {{
        const shareMenu = document.getElementById('shareMenu');
        const shareBtn = e.target.closest('.share-btn');
        if (!shareBtn && !e.target.closest('.share-menu')) {{
            shareMenu.classList.remove('active');
        }}
    }});
    
    // 페이지 로드 시 파티클 생성 및 초기 그래프 표시
    createParticles();
    drawChart(150);
    updateSelectedDisplay();
</script>
</body>
</html>
"""

# Replace placeholders with actual values (do replacements after template to avoid f-string brace issues)
# The template was authored with doubled braces to avoid f-string issues; convert them back to single braces for valid HTML/JS/CSS
html_template = html_template.replace('{{', '{').replace('}}', '}')
html_code = html_template.replace('@@CURRENT_TIME@@', current_time.strftime('%Y년 %m월 %d일 %H시'))
html_code = html_code.replace('@@HEXAGRAM_NAME@@', hexagram_name)
html_code = html_code.replace('@@HEXAGRAM_NUM@@', str(hexagram_num + 1))
html_code = html_code.replace('@@LUCKY_BALLS@@', ''.join([f'<div class="lucky-ball">{num}</div>' for num in lucky_numbers]))
html_code = html_code.replace('@@HEXAGRAM_DESC@@', hexagram_desc)

# recommended combos HTML
recommended_html = ''.join([f'''
            <div class="combo-item">
                <div class="combo-numbers">
                    {''.join([f'<div class="combo-ball" style="background: {get_ball_color(num)}"><span>{num}</span></div>' for num in sorted(combo)])}
                </div>
                <button class="copy-btn" onclick="copyCombo({list(sorted(combo))})">📋 복사</button>
            </div>
            ''' for combo in recommended_combos])
html_code = html_code.replace('@@RECOMMENDED_COMBOS@@', recommended_html)

# number buttons
number_buttons = ''.join([f'<button class="number-btn" data-num="{i}" onclick="toggleNumber({i})"><span>{i}</span></button>' for i in range(1, 46)])
html_code = html_code.replace('@@NUMBER_BUTTONS@@', number_buttons)

# stats and final numbers
html_code = html_code.replace('@@STATS_JSON@@', stats_json)
html_code = html_code.replace('@@FINAL_STR@@', final_str)

# 회차 계산 및 반영
current_round = get_lotto_round(current_time)
html_code = html_code.replace('@@ROUND@@', str(current_round))

components.html(html_code, height=1200, scrolling=True)