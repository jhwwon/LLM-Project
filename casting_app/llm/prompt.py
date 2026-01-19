"""
프롬프트 빌더 - 프로페셔널 버전 (수정)
제조 현장에 맞는 체계적인 보고서 생성
"""


class PromptBuilder:
    """프롬프트 생성 클래스 (현장 보고서 형식)"""
    
    @staticmethod
    def build_defect_analysis_prompt(prediction, confidence, class_name):
        """
        결함 분석 프롬프트 생성 (체계적 보고서 형식)
        
        Args:
            prediction: 예측 결과 (0 or 1)
            confidence: 신뢰도
            class_name: 클래스 이름
            
        Returns:
            str: 프롬프트
        """
        status = "정상" if prediction == 0 else "불량"
        confidence_pct = f"{confidence:.2%}"
        
        # f-string 안에서 백슬래시 사용을 피하기 위해 변수로 분리
        normal_causes = "제품이 규격 기준을 충족한 이유를 2가지 서술"
        defect_causes = "결함 발생 가능 원인을 3가지 이상 구체적으로 서술 (예: 금형 온도, 주입 압력, 냉각 속도, 재료 불순물 등)"
        
        normal_actions = "출하 승인 및 다음 공정 진행, 데이터 기록 보관"
        defect_actions = "즉시 격리 후 재작업/폐기 결정, 공정 변수 점검 (온도/압력/시간), 동일 LOT 전수 검사 고려"
        
        cause_instruction = normal_causes if prediction == 0 else defect_causes
        action_instruction = normal_actions if prediction == 0 else defect_actions
        
        return f"""
당신은 제조업 품질관리(QC) 전문가이자 주조 공정 전문 엔지니어입니다.
아래 AI 검사 결과를 바탕으로 **제조 현장용 전문 보고서**를 작성해주세요.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 AI 검사 결과
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
▪ 판정 결과: {class_name}
▪ AI 신뢰도: {confidence_pct}
▪ 분석 모델: EfficientNet-B0 (전이학습, 정확도 99.86%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 작성 지침
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

다음 구조로 **정확히** 작성하되, 각 섹션은 반드시 구분하여 작성하세요:

### 1. 판정 요약
- 제품 상태를 한 문장으로 명확히 설명 (정상/불량 여부 강조)
- 신뢰도 수준 평가 (95% 이상: 높음, 80~95%: 중간, 80% 미만: 낮음)

### 2. 신뢰도 분석
신뢰도 {confidence_pct}에 대한 해석을 다음 기준으로 작성:
- **95% 이상**: "AI 판단이 매우 확실함. 추가 검증 불필요"
- **80~95%**: "AI 판단이 신뢰할 만함. 단, 육안 재확인 권장"
- **60~80%**: "AI 판단이 불확실함. 반드시 전문가 육안 검사 필요"
- **60% 미만**: "AI 판단 신뢰 불가. 전문가 정밀 검사 필수"

해당 범위에 맞춰 1~2문장으로 설명하세요.

### 3. 예상 원인 분석
**{status} 판정 시**: {cause_instruction}

### 4. 권장 조치 사항
**{status} 제품**: {action_instruction}

### 5. 추가 검토 사항
- 전문가가 육안으로 재확인해야 할 부위
- 측정 장비로 확인할 항목 (두께, 경도 등)
- 다음 생산 시 주의사항

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 작성 시 주의사항
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 반드시 위 5가지 항목 순서를 지켜주세요
2. 각 항목은 "### 번호. 제목" 형식으로 시작
3. 전문 용어를 사용하되 설명을 병기
4. 구체적인 수치와 기준을 명시
5. 불필요한 장황함 없이 핵심만 간결하게

지금 바로 작성을 시작하세요.
"""
    
    @staticmethod
    def build_recommendation_prompt(prediction, confidence):
        """
        권장 조치 프롬프트 생성
        
        Args:
            prediction: 예측 결과
            confidence: 신뢰도
            
        Returns:
            str: 프롬프트
        """
        status = "정상" if prediction == 0 else "불량"
        confidence_pct = f"{confidence:.2%}"
        
        prompt = f"""
주조 제품이 '{status}'으로 판정되었습니다. (AI 신뢰도: {confidence_pct})

현장 작업자와 품질관리 담당자를 위한 **즉각 조치사항**을 작성하세요.

다음 구조로 작성하세요:

### 작업자 조치 (3가지 이내)
- 첫 번째 조치
- 두 번째 조치  
- 세 번째 조치

### QC 담당자 확인사항 (2가지)
- 첫 번째 확인 사항
- 두 번째 확인 사항

{status} 판정에 맞는 구체적이고 실행 가능한 조치를 작성하세요.
간결하고 명확하게 작성하세요.
"""
        return prompt
