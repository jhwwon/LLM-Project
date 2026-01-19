# Transfer Learning (전이 학습) 완벽 가이드

## 📚 개념 정리

### Transfer Learning이란?

**정의**: 한 작업(Task A)에서 학습한 지식을 다른 작업(Task B)에 전이(Transfer)하여 활용하는 기법

```
Task A (ImageNet 분류)          Task B (주조 결함 검사)
├─ 데이터: 120만 장              ├─ 데이터: 400장
├─ 클래스: 1000개                ├─ 클래스: 2개
└─ 학습 시간: 수주               └─ 학습 시간: 수시간

         ↓ Transfer Learning ↓
         
사전 학습된 지식 활용
- 엣지 검출
- 텍스처 인식
- 패턴 매칭
→ 주조 결함 검사에 적용!
```

## 🏗️ 프로젝트 적용 사례

### 1. 원본 EfficientNet-B0 구조

```python
# ImageNet으로 사전 학습된 모델
model = models.efficientnet_b0(weights='IMAGENET1K_V1')

# 내부 구조
EfficientNet-B0
├─ features (Feature Extractor)
│   ├─ Conv2d (3 → 32)
│   ├─ MBConv Blocks × 16
│   ├─ Conv2d (320 → 1280)
│   └─ AdaptiveAvgPool2d
│       └─ 출력: [batch, 1280]
│
└─ classifier (분류기)
    └─ Linear(1280, 1000)  ← 1000개 클래스
        ├─ 0: 'tench'
        ├─ 1: 'goldfish'
        ├─ ...
        └─ 999: 'toilet tissue'
```

### 2. 커스터마이징 (Fine-tuning)

```python
# classifiers/image_classifier.py

def _build_model(self):
    # 1단계: 사전 학습된 모델 불러오기
    model = models.efficientnet_b0(weights=None)
    
    # 2단계: 분류기 교체
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.5),
        nn.Linear(1280, 2)  # 1000 → 2로 변경
    )
    
    return model
```

**변경 사항:**

| 레이어 | 원본 | 수정 후 |
|--------|------|---------|
| **features** | 그대로 유지 | ✅ 재사용 |
| **classifier** | Linear(1280, 1000) | ❌ 교체 → Linear(1280, 2) |
| **출력** | 1000개 확률 | 2개 확률 (정상/불량) |

### 3. 최종 모델 구조

```python
수정된 EfficientNet-B0 (주조 결함 검사용)
├─ features (Feature Extractor) ← ImageNet 가중치 활용
│   ├─ Conv2d (3 → 32)
│   ├─ MBConv Blocks × 16
│   ├─ Conv2d (320 → 1280)
│   └─ AdaptiveAvgPool2d
│       └─ 출력: [batch, 1280]
│
└─ classifier (새로운 분류기) ← 주조 데이터로 학습
    ├─ Dropout(p=0.5)
    └─ Linear(1280, 2)  ← 2개 클래스
        ├─ 0: '정상 (Normal)'
        └─ 1: '불량 (Defective)'
```

## 🎯 핵심 질문 답변

### Q1: "1000개 클래스에 2개를 추가한 건가요?"

**A: 아니요, '교체'했습니다.**

```
❌ 잘못된 이해:
1000개 + 2개 = 1002개 클래스

✅ 올바른 이해:
1000개 제거 → 2개로 교체
```

**코드로 보면:**

```python
# 원본
model.classifier = Linear(1280, 1000)  # 1000개 출력

# 수정 (교체)
model.classifier = nn.Sequential(
    nn.Dropout(p=0.5),
    nn.Linear(1280, 2)  # 2개 출력
)
```

### Q2: "데이터가 이미 라벨링되어 있었는데, 맞나요?"

**A: 네, 완전히 정상입니다!**

**데이터 구조:**

```
casting_data/
├─ train/
│   ├─ ok_front/      ← 폴더 이름 = 라벨 (정상)
│   │   ├─ cast_ok_0_1.jpeg
│   │   ├─ cast_ok_0_2.jpeg
│   │   └─ ...
│   └─ def_front/     ← 폴더 이름 = 라벨 (불량)
│       ├─ cast_def_0_1.jpeg
│       ├─ cast_def_0_2.jpeg
│       └─ ...
└─ test/
    ├─ ok_front/
    └─ def_front/
```

**PyTorch가 자동으로 처리:**

```python
from torchvision.datasets import ImageFolder

# 폴더 구조를 자동으로 라벨로 인식
train_dataset = ImageFolder('casting_data/train')

# 내부 동작
# ok_front 폴더 → 라벨 0 (알파벳 순서)
# def_front 폴더 → 라벨 1

print(train_dataset.classes)
# ['def_front', 'ok_front']

print(train_dataset.class_to_idx)
# {'def_front': 0, 'ok_front': 1}
```

**이것은:**
- ✅ 지도 학습(Supervised Learning)의 표준 방식
- ✅ 라벨링 = 폴더별 분류
- ✅ 추가 작업 불필요

## 📊 Transfer Learning의 장점

### 비교표

| 항목 | 처음부터 학습 (From Scratch) | Transfer Learning |
|------|------------------------------|-------------------|
| **필요 데이터** | 수만~수십만 장 | 수백~수천 장 |
| **학습 시간** | 수일~수주 | 수시간~수일 |
| **GPU 요구사항** | 고성능 필수 | 중급 GPU 가능 |
| **성능** | 데이터 많으면 최고 | 데이터 적어도 우수 |
| **적용 난이도** | 높음 | 낮음 |

### 당신의 프로젝트

| 항목 | 값 | 평가 |
|------|-----|------|
| **데이터 수** | 400장 | 적은 편 |
| **선택한 방법** | Transfer Learning | ✅ 올바른 선택 |
| **사전 학습 데이터** | ImageNet (120만 장) | 풍부한 사전 지식 |
| **학습 시간** | 수시간 | 효율적 |
| **최종 성능** | 높음 | 성공적 |

## 🔬 Transfer Learning의 원리

### 왜 작동하는가?

**1. 저수준 특징 (Low-level Features)**

```
초기 레이어에서 학습하는 특징:
├─ 엣지 (Edges)
├─ 코너 (Corners)
├─ 색상 (Colors)
└─ 텍스처 (Textures)

→ 이러한 특징은 모든 이미지에 공통적!
→ ImageNet에서 학습한 것을 재사용 가능!
```

**2. 고수준 특징 (High-level Features)**

```
후반 레이어에서 학습하는 특징:
├─ 물체의 형태
├─ 패턴 조합
└─ 복잡한 구조

→ 작업별로 다름
→ 주조 데이터로 재학습 필요!
```

**3. 레이어별 역할**

```
EfficientNet-B0 레이어
├─ Layer 1-5   (저수준) ← ImageNet 가중치 유지
├─ Layer 6-10  (중수준) ← ImageNet 가중치 유지
├─ Layer 11-15 (고수준) ← 부분적으로 재학습
└─ Classifier  (최종)  ← 완전히 새로 학습
```

## 💻 코드 예시

### 전체 학습 프로세스

```python
import torch
import torch.nn as nn
from torchvision import models

# 1단계: 사전 학습된 모델 불러오기
model = models.efficientnet_b0(weights='IMAGENET1K_V1')
print(f"원래 출력 크기: {model.classifier[1].out_features}")  # 1000

# 2단계: 분류기 교체
num_classes = 2  # 정상/불량
model.classifier = nn.Sequential(
    nn.Dropout(p=0.5),
    nn.Linear(1280, num_classes)
)
print(f"수정 후 출력 크기: {model.classifier[1].out_features}")  # 2

# 3단계: Feature Extractor 동결 (선택사항)
# 옵션 A: 전체 재학습
for param in model.parameters():
    param.requires_grad = True

# 옵션 B: Classifier만 학습 (빠름)
for param in model.features.parameters():
    param.requires_grad = False  # Feature Extractor 동결
for param in model.classifier.parameters():
    param.requires_grad = True   # Classifier만 학습

# 4단계: 학습
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

for epoch in range(10):
    for images, labels in train_loader:
        outputs = model(images)
        loss = criterion(outputs, labels)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
```

### 학습 전략 비교

```python
# 전략 1: Feature Extractor 동결 (빠름, 데이터 적을 때)
for param in model.features.parameters():
    param.requires_grad = False
# 학습 시간: 짧음
# 필요 데이터: 적음 (수백 장)
# 성능: 중상

# 전략 2: 전체 Fine-tuning (느림, 데이터 충분할 때)
for param in model.parameters():
    param.requires_grad = True
# 학습 시간: 김
# 필요 데이터: 많음 (수천 장)
# 성능: 최고

# 전략 3: 점진적 Fine-tuning (균형)
# 1단계: Classifier만 학습
# 2단계: 후반 레이어 포함
# 3단계: 전체 Fine-tuning
```

## 🎓 선생님께 설명할 때

### 완벽한 답변 템플릿

> **"선생님, 질문 감사합니다!**
> 
> **제가 사용한 방법은 Transfer Learning (전이 학습)입니다.**
> 
> **1. 사전 학습 모델 활용**
> - ImageNet으로 사전 학습된 EfficientNet-B0 모델을 불러왔습니다
> - 이 모델은 원래 1000개 클래스를 분류할 수 있었습니다
> 
> **2. 분류기 교체 (Head Replacement)**
> - 마지막 분류 레이어(Linear(1280, 1000))를 제거했습니다
> - 2개 클래스(정상/불량)를 분류하는 새로운 레이어(Linear(1280, 2))로 교체했습니다
> - 1000개에 2개를 '추가'한 것이 아니라, 1000개를 '제거'하고 2개로 '교체'한 것입니다
> 
> **3. Fine-tuning**
> - 주조 데이터 400장으로 재학습했습니다
> - Feature Extractor는 ImageNet에서 학습한 가중치를 활용했습니다
> - Classifier만 주조 데이터로 새로 학습했습니다
> 
> **4. 데이터 라벨링**
> - 데이터는 폴더별로 분류되어 있었습니다 (ok_front, def_front)
> - PyTorch의 ImageFolder가 폴더 이름을 자동으로 라벨로 인식했습니다
> - 이것은 지도 학습의 표준적인 데이터 구조입니다
> 
> **5. Transfer Learning의 장점**
> - 적은 데이터(400장)로도 높은 성능 달성
> - ImageNet에서 학습한 일반적인 이미지 특징(엣지, 텍스처 등)을 활용
> - 학습 시간 단축 (수주 → 수시간)
> 
> **결론: 1000개 클래스를 2개로 교체하여 주조 결함 검사에 특화된 모델을 만들었습니다.**"

## 📚 참고 자료

### 관련 개념

1. **Transfer Learning**: 사전 학습된 모델의 지식을 새로운 작업에 활용
2. **Fine-tuning**: 사전 학습된 모델을 새로운 데이터로 재학습
3. **Feature Extraction**: Feature Extractor를 동결하고 Classifier만 학습
4. **Domain Adaptation**: 다른 도메인의 데이터로 모델 적응

### 유명한 사전 학습 모델

| 모델 | 파라미터 수 | ImageNet Top-1 정확도 |
|------|-------------|----------------------|
| ResNet-18 | 11M | 69.8% |
| ResNet-50 | 25M | 76.1% |
| **EfficientNet-B0** | **5.3M** | **77.7%** |
| EfficientNet-B7 | 66M | 84.4% |
| ViT-Base | 86M | 81.8% |

**EfficientNet-B0 선택 이유:**
- ✅ 적은 파라미터 (5.3M)
- ✅ 높은 정확도 (77.7%)
- ✅ 빠른 추론 속도
- ✅ 적은 메모리 사용

---

**작성일**: 2026-01-13  
**버전**: 1.0
