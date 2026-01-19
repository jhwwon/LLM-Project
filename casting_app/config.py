"""
설정 파일
프로젝트 전역 설정 관리
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 프로젝트 경로
BASE_DIR = Path(__file__).parent
MODEL_DIR = BASE_DIR / "models"

# 모델 설정
MODEL_PATH = MODEL_DIR / "final_efficientnet_b0.pth"
MODEL_NAME = "efficientnet_b0"  # 사용할 모델 아키텍처
CLASS_NAMES = ['정상 (OK)', '불량 (Defective)']

# 디바이스 설정
DEVICE = "cuda"  # 또는 "cpu"

# 이미지 설정
IMAGE_SIZE = (224, 224)
NORMALIZE_MEAN = [0.485, 0.456, 0.406]
NORMALIZE_STD = [0.229, 0.224, 0.225]

# LLM 설정
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
CLAUDE_MODEL = 'claude-sonnet-4-5'
LLM_TEMPERATURE = 0.7
LLM_MAX_TOKENS = 2048
