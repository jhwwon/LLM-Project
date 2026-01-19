"""
결함 분석기
AI 예측 결과를 LLM으로 분석
"""

from .client import ClaudeClient
from .prompt import PromptBuilder


class DefectAnalyzer:
    """결함 분석 클래스"""
    
    def __init__(self, llm_client=None):
        """
        Args:
            llm_client: Claude 클라이언트 (없으면 자동 생성)
        """
        self.llm_client = llm_client or ClaudeClient()
        self.prompt_builder = PromptBuilder()
    
    def analyze(self, prediction_result):
        """
        예측 결과 분석
        
        Args:
            prediction_result: ImageClassifier의 predict() 결과
            
        Returns:
            dict: {
                'analysis': str (상세 분석),
                'recommendation': str (권장 조치)
            }
        """
        prediction = prediction_result['prediction']
        confidence = prediction_result['confidence']
        class_name = prediction_result['class_name']
        
        # 상세 분석
        analysis_prompt = self.prompt_builder.build_defect_analysis_prompt(
            prediction, confidence, class_name
        )
        analysis = self.llm_client.generate(analysis_prompt)
        
        # 권장 조치
        recommendation_prompt = self.prompt_builder.build_recommendation_prompt(
            prediction, confidence
        )
        recommendation = self.llm_client.generate(recommendation_prompt)
        
        return {
            'analysis': analysis,
            'recommendation': recommendation
        }
    
    def get_simple_recommendation(self, prediction, confidence):
        """
        간단한 권장 조치 (LLM 없이)
        
        Args:
            prediction: 예측 결과 (0 or 1)
            confidence: 신뢰도
            
        Returns:
            str: 권장 조치
        """
        if prediction == 0:  # 정상
            if confidence >= 0.95:
                return "[OK] 정상 제품으로 판정되었습니다. 출하 가능합니다."
            elif confidence >= 0.80:
                return "[WARNING] 정상으로 보이나 신뢰도가 다소 낮습니다. 육안 재확인 권장합니다."
            else:
                return "[WARNING] 판정 신뢰도가 낮습니다. 추가 검사가 필요합니다."
        else:  # 불량
            if confidence >= 0.95:
                return "[NG] 명확한 결함이 감지되었습니다. 즉시 불량 처리하세요."
            elif confidence >= 0.80:
                return "[WARNING] 결함으로 판정되었습니다. 상세 검사 후 조치하세요."
            else:
                return "[WARNING] 결함 가능성이 있으나 신뢰도가 낮습니다. 전문가 확인 필요합니다."
