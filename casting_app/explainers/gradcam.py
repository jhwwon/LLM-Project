"""
GradCAM 시각화 클래스
모델의 판단 근거를 히트맵으로 시각화
"""

import torch
import numpy as np
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image
import config


class GradCAMGenerator:
    """GradCAM 생성기 클래스"""
    
    def __init__(self, model, target_layer):
        """
        Args:
            model: PyTorch 모델
            target_layer: GradCAM을 적용할 레이어
        """
        self.model = model
        self.target_layer = target_layer
        self.cam = GradCAM(model=model, target_layers=[target_layer])
    
    def generate(self, input_tensor, original_image):
        """
        GradCAM 히트맵 생성
        
        Args:
            input_tensor: 전처리된 입력 텐서
            original_image: 원본 이미지 (PIL Image)
            
        Returns:
            numpy.ndarray: GradCAM 히트맵이 적용된 이미지
        """
        # GradCAM 생성
        grayscale_cam = self.cam(input_tensor=input_tensor)[0, :]
        
        # 원본 이미지를 numpy 배열로 변환
        img_array = np.array(original_image.resize(config.IMAGE_SIZE)) / 255.0
        
        # 히트맵 적용
        cam_image = show_cam_on_image(img_array, grayscale_cam, use_rgb=True)
        
        return cam_image
