"""
Analyzer (오케스트레이션 역할)
"""
from llm.analyzer import DefectAnalyzer as LLMDefectAnalyzer

class DefectAnalyzer:
    def __init__(self):
        self.analyzer = LLMDefectAnalyzer()

    def run_analysis(self, result):
        # Calls the analyze method from the LLM analyzer
        analysis_result = self.analyzer.analyze(result)
        
        # Formatting the output for the UI
        return f"""
### 🧐 상세 분석 결과
{analysis_result['analysis']}

### 🛠️ 권장 조치 사항
{analysis_result['recommendation']}
"""
