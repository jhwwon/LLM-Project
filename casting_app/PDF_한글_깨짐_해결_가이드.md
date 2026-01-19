# PDF 한글 깨짐 문제 해결 가이드

## 🔍 문제 원인

Streamlit에서 ReportLab을 사용하여 PDF 보고서를 생성할 때 한글이 깨지는 주요 원인은 다음과 같습니다:

### 1. **폰트 서브셋(Font Subsetting) 문제**
- ReportLab은 기본적으로 PDF 파일 크기를 줄이기 위해 **폰트 서브셋**을 사용합니다
- 서브셋은 실제로 사용된 글자만 PDF에 포함시키는 기능
- 한글은 **조합형 문자**이기 때문에 서브셋 처리 시 글리프(glyph) 매핑이 잘못될 수 있음
- 특히 초성, 중성, 종성의 조합으로 이루어진 한글의 특성상 서브셋 알고리즘이 제대로 작동하지 않을 수 있음

### 2. **폰트 임베딩 방식**
- TTFont 객체 생성 시 기본 설정이 서브셋을 활성화함
- `font.face.subset = None`로 설정해도 ReportLab 내부에서 다시 활성화될 수 있음

### 3. **PDF 압축**
- PDF 생성 시 압축이 활성화되면 폰트 데이터가 손상될 수 있음

## ✅ 해결 방법

### 적용된 수정사항

#### 1. **폰트 등록 시 서브셋 완전 비활성화**

```python
# services/pdf_generator.py

# 기존 코드 (문제 있음)
font = TTFont('Malgun', malgun_abs_path)
font.face.subset = None
pdfmetrics.registerFont(font)

# 수정된 코드 (다중 방어)
font = TTFont('Malgun', malgun_abs_path, subfontIndex=0)

# 서브셋 완전 비활성화 (다중 방어)
if hasattr(font, 'face'):
    font.face.subset = None
if hasattr(font, 'subset'):
    font.subset = None
    
pdfmetrics.registerFont(font)
```

**주요 변경점:**
- `subfontIndex=0` 명시적 지정
- `hasattr()` 체크로 안전하게 속성 접근
- `font.face.subset`과 `font.subset` 모두 비활성화

#### 2. **PDF 생성 시 압축 비활성화**

```python
# services/pdf_generator.py - generate_report()

doc = SimpleDocTemplate(
    buffer,
    pagesize=A4,
    topMargin=1.5*cm,
    bottomMargin=1.5*cm,
    leftMargin=1.5*cm,
    rightMargin=1.5*cm,
    invariant=1,  # 폰트 깨짐 방지를 위한 고정 설정
    compress=0    # 압축 비활성화 (한글 깨짐 방지) ← 추가
)
```

**주요 변경점:**
- `compress=0` 옵션 추가로 PDF 압축 비활성화
- 파일 크기는 증가하지만 한글 깨짐 방지

#### 3. **디버깅 정보 추가**

```python
# 폰트 로드 후 상태 확인
subset_status = getattr(font.face, 'subset', 'N/A') if hasattr(font, 'face') else 'N/A'
print(f"✅ 맑은 고딕 폰트 로드 성공")
print(f"   경로: {malgun_abs_path}")
print(f"   서브셋 상태: {subset_status}")  # None이어야 정상
print(f"   파일 크기: {os.path.getsize(malgun_abs_path):,} bytes")
```

## 📝 테스트 방법

### 1. 간단한 테스트

```bash
cd c:\LLMProject\casting_app
python test_korean_pdf.py
```

생성된 `test_korean.pdf` 파일을 열어서 한글이 제대로 표시되는지 확인

### 2. 종합 테스트 (모든 해결책 적용)

```bash
python test_korean_final.py
```

생성된 `test_korean_final.pdf` 파일 확인

### 3. Streamlit 앱에서 테스트

```bash
streamlit run app.py
```

이미지 업로드 후 PDF 보고서 생성 → 다운로드 → 한글 확인

## 🔧 추가 해결 방법 (위 방법으로 해결 안 될 경우)

### 방법 A: 다른 한글 폰트 사용

맑은 고딕 대신 다른 폰트 시도:
- 나눔고딕: https://hangeul.naver.com/font
- 나눔바른고딕
- 본고딕 (Noto Sans KR)

```python
# 나눔고딕 사용 예시
font = TTFont('NanumGothic', 'NanumGothic.ttf', subfontIndex=0)
if hasattr(font, 'face'):
    font.face.subset = None
pdfmetrics.registerFont(font)
```

### 방법 B: Windows 시스템 폰트 직접 사용

```python
import os
font_path = r'C:\Windows\Fonts\malgun.ttf'
if os.path.exists(font_path):
    font = TTFont('Malgun', font_path, subfontIndex=0)
    # ... 서브셋 비활성화
```

### 방법 C: ReportLab 버전 다운그레이드

일부 버전에서 한글 처리에 문제가 있을 수 있음:

```bash
pip uninstall reportlab
pip install reportlab==3.6.13
```

### 방법 D: 폰트 플래그 초기화

```python
font = TTFont('Malgun', malgun_abs_path, subfontIndex=0)
if hasattr(font, 'face'):
    font.face.subset = None
    font.face.flags = 0  # 폰트 플래그 초기화
pdfmetrics.registerFont(font)
```

## 📊 현재 환경

- **OS**: Windows
- **Python**: 3.10
- **ReportLab**: 4.4.7
- **폰트**: 맑은 고딕 (malgun.ttf, malgunbd.ttf)
- **폰트 위치**: `c:\LLMProject\casting_app\Font\`

## ✨ 최종 체크리스트

- [x] `subfontIndex=0` 명시적 지정
- [x] `font.face.subset = None` 설정
- [x] `font.subset = None` 설정 (있는 경우)
- [x] `invariant=1` 옵션 사용
- [x] `compress=0` 옵션 사용
- [x] 폰트 파일 존재 확인
- [x] 폰트 파일 크기 확인 (손상 여부)
- [x] 디버깅 정보 출력

## 🎯 결론

위의 수정사항을 모두 적용하면 대부분의 한글 깨짐 문제가 해결됩니다.
핵심은 **폰트 서브셋을 완전히 비활성화**하고 **PDF 압축을 끄는 것**입니다.

만약 여전히 문제가 발생한다면:
1. 생성된 PDF 파일을 Adobe Acrobat Reader로 열어보기
2. 다른 PDF 뷰어에서도 테스트
3. 폰트 파일 자체를 다시 다운로드
4. 다른 한글 폰트로 교체

---

**작성일**: 2026-01-13
**버전**: 1.0
