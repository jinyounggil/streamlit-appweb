# 🎯 로또킹 - AI 로또 번호 추천 앱

과학적 데이터 분석과 전통적 방법을 결합한 로또 번호 추천 시스템

## ✨ 주요 기능

### 1. 🐉 띠별 추천 번호
- 12간지 띠에 따른 행운의 번호 추천
- 각 띠별 맞춤 번호 조합

### 2. 🔮 주역 방위 추천
- 8방위 주역 기반 번호 선택
- 자동/수동 모드 지원
- 전통 주역 이론 적용

### 3. 📊 통계 분석
- 과거 당첨 번호 빈도 분석
- 시각화 차트 제공
- Hot/Cold 번호 분석

### 4. 🧠 AI 통합 추천 (10/10 알고리즘)
- **다층 가중치 시스템**
  - 빈도 분석 50%
  - 최근 추세 30%
  - 미출현 패턴 20%
- **구간 균형 검증** (5개 구간 골고루 분포)
- **홀짝 비율 최적화** (2~4개 홀수 유지)
- **번호 합계 검증** (100~160 범위)
- **연속번호 제어** (3개 이상 방지)
- **중복 조합 제거**

## 🚀 실행 방법

### 로컬 실행
```bash
# 가상환경 활성화
.venv\Scripts\Activate.ps1

# 필요 라이브러리 설치
pip install -r requirements.txt

# 앱 실행
streamlit run mainapp.py
```

### Streamlit Cloud 배포
1. GitHub에 코드 업로드
2. [Streamlit Cloud](https://streamlit.io/cloud) 접속
3. GitHub 저장소 연동
4. 자동 배포 완료!

## 📱 모바일 지원
- 반응형 디자인 적용
- 768px 이하 화면 자동 최적화
- 터치 친화적 UI

## 📦 필요 라이브러리
- streamlit
- pandas
- matplotlib
- Pillow
- requests
- openpyxl
- lxml
- html5lib
- beautifulsoup4
- opencv-python (QR코드 스캔 기능 사용 시)

## 📂 파일 구성
- `mainapp.py` - 메인 애플리케이션
- `past_results.csv` - 과거 당첨 데이터
- `lottoking1.jpg` - 메인 이미지
- `requirements.txt` - 필요 라이브러리 목록

## 🎨 주요 기술
- **Frontend**: Streamlit (Python)
- **Data Analysis**: Pandas, Matplotlib
- **AI Algorithm**: 다층 가중치 분석 시스템
- **Design**: 반응형 CSS, 그라데이션 애니메이션

## 📊 데이터 분석
- 최근 300회 당첨 데이터 분석
- 실시간 회차 및 추첨일 계산
- Hot/Mid/Cold 번호 분류
- 미출현 기간 추적

## 💡 특징
- 🎯 10/10 고급 AI 알고리즘
- 📊 과학적 통계 기반
- 🔮 전통 주역 이론 결합
- 📱 모바일 완벽 지원
- ✨ 애니메이션 효과
- 🎨 직관적 UI/UX

## 📌 업데이트 내역
- v1.0: 초기 버전
- v1.5: AI 알고리즘 8/10 업그레이드
- v2.0: AI 알고리즘 10/10 완성 (다층 가중치, 구간균형, 홀짝비율)
- v2.1: 모바일 반응형 디자인 추가

## 👨‍💻 개발자
로또킹 개발팀

## 📄 라이선스
MIT License

---
**⚠️ 면책 조항**: 본 앱은 참고용 추천 시스템이며, 실제 당첨을 보장하지 않습니다.
