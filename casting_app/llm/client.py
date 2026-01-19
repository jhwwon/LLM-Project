"""
Claude AI 클라이언트
Anthropic Claude API 통신
"""

import anthropic
import config


class ClaudeClient:
    """Claude AI 클라이언트 클래스"""
    
    def __init__(self, api_key=None):
        """
        Args:
            api_key: Anthropic API 키
        """
        self.api_key = api_key or config.ANTHROPIC_API_KEY
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY가 설정되지 않았습니다")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model_name = config.CLAUDE_MODEL
        self.temperature = config.LLM_TEMPERATURE
        self.max_tokens = config.LLM_MAX_TOKENS
    
    def generate(self, prompt):
        """
        텍스트 생성
        
        Args:
            prompt: 입력 프롬프트
            
        Returns:
            str: 생성된 텍스트
        """
        try:
            message = self.client.messages.create(
                model=self.model_name,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            return f"오류 발생: {str(e)}"
