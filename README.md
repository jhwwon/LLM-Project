# 🏭 AI 기반 주조 결함 검사 시스템

## 📋 프로젝트 개요
**딥러닝(EfficientNet-B0) + LLM(Claude Sonnet 4.5)**을 결합한 차세대 AI 기반 주조 제품 결함 자동 검사 시스템

### 주요 특징
- 🎯 **99.86% 정확도** (EfficientNet-B0 기반)
- 🤖 **Claude AI 분석**: 전문가 수준의 결함 분석 및 조치 제안
- 📊 **실시간 통계 대시보드**: 일일/주간 검사 현황 한눈에 파악
- 🔥 **Grad-CAM 시각화**: AI 판단 근거 명확히 제시
- 📄 **PDF 보고서 자동 생성**: 한글 지원, 전문 양식

---

## 🚀 빠른 시작

### 1️⃣ 저장소 클론
```bash
git clone https://github.com/YOUR_USERNAME/LLM_Project.git
cd LLM_Project/casting_app
```

### 2️⃣ 패키지 설치
```bash
pip install -r requirements.txt
```

### 3️⃣ 환경 변수 설정
`.env` 파일 생성 후 Claude API 키 추가:
```env
ANTHROPIC_API_KEY=your_api_key_here
```

### 4️⃣ 모델 파일 준비
- `models/final_efficientnet_b0.pth` 파일 필요
- (용량 문제로 GitHub에 미포함, 별도 다운로드 필요)

### 5️⃣ Streamlit 앱 실행
```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 접속

---

## 📊 기술 스택

### 딥러닝 & AI
- **PyTorch 2.0+**: 딥러닝 프레임워크
- **EfficientNet-B0**: 경량화된 고성능 CNN 모델
- **Transfer Learning**: ImageNet 사전 학습 모델 활용
- **Grad-CAM**: XAI (설명 가능한 AI)

### LLM & 백엔드
- **Claude Sonnet 4.5**: 차세대 언어 모델
- **Anthropic API**: LLM 연동
- **Streamlit**: 웹 UI 프레임워크
- **ReportLab**: PDF 생성 (한글 지원)
- **Plotly**: 인터랙티브 차트

---

## 🎯 주요 기능

### 🏠 홈 탭
- 프로젝트 목표 및 핵심 기술 소개
- 시스템 성능 지표 (정확도, 손실률, 속도)
- 학습 성능 그래프 (Plotly 인터랙티브 차트)

### 🔍 AI 검사 탭
1. **검사 모드 선택**
   - 📁 파일 업로드: 직접 이미지 업로드
   - 🎯 샘플 이미지: 미리 준비된 8개 샘플 선택

2. **실시간 AI 분석**
   - 원본 이미지 표시
   - Grad-CAM 히트맵 (컬러 스펙트럼 가이드 포함)
   - 클래스별 확률 바 차트
   - 검사 일시 기록

3. **Claude AI 상세 분석**
   - 판정 요약
   - 신뢰도 분석
   - 예상 원인 분석
   - 권장 조치 사항

4. **PDF 보고서 생성**
   - 전문 보고서 양식
   - 한글 폰트 지원
   - 이미지 + 분석 통합

### 📊 일일 통계 대시보드 탭
- 기간 선택 (오늘 / 최근 7일 / 최근 30일)
- 핵심 지표 카드
- 시간대별 검사 추이
- 판정 비율 도넛 차트
- 최근 검사 기록 테이블

---

## 📈 모델 성능

| 지표 | 값 |
|------|-----|
| **검증 정확도** | 99.86% |
| **테스트 정확도** | 99.72% |
| **손실률 (Loss)** | 0.006 |
| **학습 Epoch** | 16 (Early Stopping) |
| **모델 크기** | 16.3 MB |
| **파라미터 수** | 5.3M |
| **추론 속도** | < 1초 |

---

## 🏗️ 프로젝트 구조

```
casting_app/
├── app.py                              # 🎭 메인 애플리케이션
├── config.py                           # ⚙️ 전역 설정
├── requirements.txt                    # 📦 필수 패키지
├── .env                                # 🔐 환경 변수 (API 키)
│
├── models/
│   └── final_efficientnet_b0.pth      # 🧠 학습된 모델
│
├── assets/                             # 🖼️ 샘플 이미지
│
├── classifiers/
│   └── image_classifier.py            # 🔍 이미지 분류
│
├── explainers/
│   └── gradcam.py                     # 🔥 Grad-CAM 시각화
│
├── llm/
│   ├── client.py                      # 💬 Claude API 클라이언트
│   ├── prompt.py                      # 📝 프롬프트 빌더
│   └── analyzer.py                    # 🧐 LLM 결함 분석기
│
├── services/
│   ├── inspection_orchestrator.py     # 🔬 검사 오케스트레이터
│   ├── pdf_generator.py               # 📄 PDF 보고서 생성
│   └── history.py                     # 📊 검사 이력 관리
│
└── utils/
    └── imaging.py                     # 🎨 이미지 전처리
```

---

## 🔧 트러블슈팅

### 1. `ModuleNotFoundError`
```bash
pip install -r requirements.txt
```

### 2. PDF 생성 오류
```bash
pip install reportlab
```

### 3. CUDA 오류 (GPU 없는 경우)
`config.py`에서 `DEVICE = "cpu"` 로 변경

### 4. 모델 파일 없음
- `models/` 폴더에 `final_efficientnet_b0.pth` 파일 필요
- 별도 다운로드 또는 학습 필요

---

## 📝 라이선스
MIT License

---

## 📧 문의
프로젝트 관련 문의사항이나 개선 제안이 있으시면 Issue를 등록해주세요!

---

**© 2026 Casting AI System - Advanced AI Quality Management Solution**
