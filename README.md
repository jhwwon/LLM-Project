# AI 기반 주조 결함 검사 시스템

## 프로젝트 개요
**딥러닝(EfficientNet-B0) + LLM(Claude Sonnet 4.5)**을 결합한 차세대 AI 기반 주조 제품 결함 자동 검사 시스템

### 주요 특징
- **99.86% 정확도** (EfficientNet-B0 기반)
- **Claude AI 분석**: 전문가 수준의 결함 분석 및 조치 제안
- **실시간 통계 대시보드**: 일일/주간 검사 현황 한눈에 파악
- **Grad-CAM 시각화**: AI 판단 근거 명확히 제시
- **PDF 보고서 자동 생성**: 한글 지원, 전문 양식

---

## 프로젝트 구조

```
casting_app/
├── app.py                              # 메인 애플리케이션 (Orchestrator)
├── config.py                           # 전역 설정
├── requirements.txt                    # 필수 패키지
├── .env                                # 환경 변수 (API 키)
│
├── models/
│   └── final_efficientnet_b0.pth      # 학습된 모델 (99.86% 정확도)
│
├── assets/                             # 샘플 이미지
│   ├── sample_normal_*.jpeg           # 정상 샘플 4개
│   └── sample_defect_*.jpeg           # 불량 샘플 4개
│
├── classifiers/
│   └── image_classifier.py            # 이미지 분류 (EfficientNet-B0)
│
├── explainers/
│   └── gradcam.py                     # Grad-CAM 시각화
│
├── llm/
│   ├── client.py                      # Claude API 클라이언트
│   ├── prompt.py                      # 프롬프트 빌더
│   └── analyzer.py                    # LLM 결함 분석기
│
├── services/
│   ├── inspection_orchestrator.py     # 검사 오케스트레이터
│   ├── analyzer.py                    # 분석 서비스
│   ├── pdf_generator.py               # PDF 보고서 생성
│   └── history.py                     # 검사 이력 관리
│
├── utils/
│   └── imaging.py                     # 이미지 전처리
│
├── Font/                              # 한글 폰트 (PDF용)
│   ├── malgun.ttf
│   └── malgunbd.ttf
│
├── ngrok/                             # 외부 접속용
│   └── ngrok.exe
│
└── notebooks/
    └── casting_model_comparison.ipynb # 모델 학습 노트북
```

---

## 실행 방법

### 1. 저장소 클론
```bash
git clone https://github.com/jhwwon/LLM-Project.git
cd LLM-Project/casting_app
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정
`.env` 파일에 Claude API 키 추가:
```env
ANTHROPIC_API_KEY=your_api_key_here
```

### 4. Streamlit 앱 실행
```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 접속

---

## 주요 기능

### 홈 탭
- 프로젝트 목표 및 핵심 기술 소개
- 시스템 성능 지표 (정확도, 손실률, 속도)
- 학습 성능 그래프 (Plotly 인터랙티브 차트)

### AI 검사 탭
1. **검사 모드 선택**
   - 파일 업로드: 직접 이미지 업로드
   - 샘플 이미지: 미리 준비된 8개 샘플 선택

2. **실시간 AI 분석**
   - 원본 이미지 표시
   - Grad-CAM 히트맵 (컬러 스펙트럼 가이드 포함)
   - 클래스별 확률 바 차트
   - 검사 일시 기록

3. **Claude AI 상세 분석** (버튼 클릭)
   - 판정 요약
   - 신뢰도 분석
   - 예상 원인 분석 (공정 파라미터 기반)
   - 권장 조치 사항

4. **PDF 보고서 생성**
   - 전문 보고서 양식
   - 한글 폰트 지원
   - 이미지 + 분석 통합

### 일일 통계 대시보드 탭
- 기간 선택 (오늘 / 최근 7일 / 최근 30일)
- 핵심 지표 카드 (총 검사, 정상/불량 건수 및 비율, 평균 신뢰도)
- 시간대별 검사 추이 (누적 막대 그래프)
- 판정 비율 도넛 차트
- 최근 검사 기록 테이블

### 프로젝트 소개 탭
- 개발 배경 및 기술 스택
- 시스템 아키텍처
- 데이터셋 & 학습 전략

### 핵심 코드 설명 탭
- 모델 아키텍처 (EfficientNet-B0 + 파인튜닝)
- Grad-CAM 원리
- LLM 통합 방법
- 데이터 증강 전략

---

## 핵심 클래스 구조

### ImageClassifier (이미지 분류기)
```python
- _build_model(): EfficientNet-B0 모델 생성
- predict(image): 이미지 예측 + 확률 반환
```

### GradCAMGenerator (설명 가능 AI)
```python
- generate(input_tensor, original_image): Grad-CAM 히트맵 생성
```

### DefectAnalyzer (LLM 분석기)
```python
- run_analysis(result): Claude로 상세 분석
```

### PDFReportGenerator (보고서 생성기)
```python
- generate_report(result, analysis, images): 프로페셔널 PDF 생성
```

### InspectionHistory (이력 관리)
```python
- add_record(result): 검사 결과 저장 (CSV)
- get_statistics(days): 통계 계산
```

---

## 기술 스택

### 딥러닝
- **PyTorch 2.0+**: 딥러닝 프레임워크
- **EfficientNet-B0**: 경량화된 고성능 CNN 모델
- **Transfer Learning**: ImageNet 사전 학습 모델 활용
- **Grad-CAM**: XAI (설명 가능한 AI)

### LLM & AI
- **Claude Sonnet 4.5**: 차세대 언어 모델
- **Anthropic API**: LLM 연동
- **Prompt Engineering**: 제조 현장 맞춤형 프롬프트

### 웹 & 시각화
- **Streamlit**: 웹 UI 프레임워크
- **Plotly**: 인터랙티브 차트
- **ReportLab**: PDF 생성 (한글 지원)

### 데이터 처리
- **Pandas**: 데이터 분석 및 통계
- **NumPy**: 수치 연산
- **Pillow / OpenCV**: 이미지 처리

---

## 모델 성능

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

## 트러블슈팅

### 1. `ModuleNotFoundError`
```bash
pip install -r requirements.txt
```

### 2. `KeyError: probabilities`
- Streamlit 캐시 문제 → 페이지 새로고침 (F5)

### 3. PDF 생성 오류
```bash
pip install reportlab
```

### 4. CUDA 오류 (GPU 없는 경우)
`config.py`에서 `DEVICE = "cpu"` 로 변경

---

## 라이선스
MIT License

---

**© 2026 Casting AI System - Advanced AI Quality Management Solution**
