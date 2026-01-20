# AI 기반 주조 결함 검사 시스템 (LLM 통합)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Latest-FF4B4B.svg)](https://streamlit.io/)
[![Claude](https://img.shields.io/badge/Claude-Sonnet%204.5-purple.svg)](https://www.anthropic.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

딥러닝(EfficientNet-B0)과 LLM(Claude Sonnet 4.5)을 결합한 차세대 주조 제품 결함 자동 검사 시스템

## 주요 기능

- **고성능 결함 탐지**: EfficientNet-B0 기반 99.86% 정확도
- **AI 분석 리포트**: Claude Sonnet 4.5가 전문가 수준의 결함 분석 및 조치 제안
- **Grad-CAM 시각화**: AI 판단 근거를 히트맵으로 명확히 제시
- **실시간 대시보드**: 일일/주간/월간 검사 통계 및 추이 분석
- **PDF 보고서 자동 생성**: 한글 지원, 전문 검사 양식

## 빠른 시작

### 1. 설치

```bash
git clone https://github.com/jhwwon/LLM-Project.git
cd LLM-Project/casting_app
pip install -r requirements.txt
```

### 2. 환경 설정

`.env` 파일 생성 및 Claude API 키 추가:

```
ANTHROPIC_API_KEY=your_api_key_here
```

### 3. 모델 준비

`models/final_efficientnet_b0.pth` 파일 필요 (별도 다운로드)

### 4. 실행

```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 접속

## 프로젝트 구조

```
casting_app/
├── app.py                          # 메인 애플리케이션
├── config.py                       # 전역 설정
├── requirements.txt                # 필수 패키지
├── .env                            # 환경 변수 (API 키)
├── models/
│   └── final_efficientnet_b0.pth  # 학습된 모델
├── assets/                         # 샘플 이미지
├── classifiers/
│   └── image_classifier.py        # 이미지 분류기
├── explainers/
│   └── gradcam.py                 # Grad-CAM 시각화
├── llm/
│   ├── client.py                  # Claude API 클라이언트
│   ├── prompt.py                  # 프롬프트 빌더
│   └── analyzer.py                # LLM 결함 분석기
├── services/
│   ├── inspection_orchestrator.py # 검사 오케스트레이터
│   ├── pdf_generator.py           # PDF 보고서 생성
│   └── history.py                 # 검사 이력 관리
└── utils/
    └── imaging.py                 # 이미지 전처리
```

## 모델 성능

- **아키텍처**: EfficientNet-B0 (Transfer Learning)
- **검증 정확도**: 99.86%
- **테스트 정확도**: 99.72%
- **손실률**: 0.006
- **모델 크기**: 16.3 MB
- **추론 속도**: < 1초

## 기술 스택

**딥러닝**
- PyTorch 2.0+
- EfficientNet-B0
- Grad-CAM (설명 가능한 AI)

**LLM & AI**
- Claude Sonnet 4.5
- Anthropic API

**애플리케이션**
- Streamlit (웹 UI)
- ReportLab (PDF 생성)
- Plotly (인터랙티브 차트)

## 주요 탭 기능

### 홈 탭
- 프로젝트 개요 및 성능 지표
- 학습 성능 그래프 (정확도/손실률)

### AI 검사 탭
- 파일 업로드 또는 샘플 이미지 선택
- 실시간 결함 탐지 및 확률 표시
- Grad-CAM 히트맵 시각화
- Claude AI 상세 분석 (판정 요약, 원인 분석, 권장 조치)
- PDF 검사 보고서 생성

### 통계 대시보드 탭
- 기간별 검사 통계 (오늘/7일/30일)
- 시간대별 검사 추이 그래프
- 판정 비율 도넛 차트
- 최근 검사 기록 테이블

## 데이터셋

**출처**: [Kaggle - Casting Product Image Data](https://www.kaggle.com/datasets/ravirajsinh45/real-life-industrial-dataset-of-casting-product)

- **총 이미지**: 7,340장
- **클래스**: 2개 (정상, 불량)

## 라이센스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 참조

## 연락처

- GitHub: [jhwwon](https://github.com/jhwwon)

---

**Version**: 1.0.0  
**Last Updated**: 2026-01-20  
**Made by**: jhwwon
