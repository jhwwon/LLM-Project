"""
ImageClassifier / Prediction
"""
import torch
import torch.nn as nn
from torchvision import models
import config
from utils.imaging import get_inference_transform

class ImageClassifier:
    def __init__(self, model_path=None):
        self.device = torch.device(config.DEVICE if torch.cuda.is_available() else 'cpu')
        self.model = self._build_model()
        if model_path:
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.transform = get_inference_transform()

    def _build_model(self):
        """EfficientNet-B0 모델 생성"""
        model = models.efficientnet_b0(weights=None)
        # EfficientNet의 classifier 구조 수정
        model.classifier = nn.Sequential(
            nn.Dropout(p=0.5),
            nn.Linear(1280, 2)  # EfficientNet-B0의 마지막 채널은 1280
        )
        return model.to(self.device).eval()

    def predict(self, image):
        input_tensor = self.transform(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            outputs = self.model(input_tensor)
            probs = torch.softmax(outputs, dim=1)[0]
            pred = torch.argmax(probs).item()
        return {
            'prediction': pred,
            'confidence': probs[pred].item(),
            'class_name': config.CLASS_NAMES[pred],
            'probabilities': {
                config.CLASS_NAMES[0]: probs[0].item(),  # 정상 확률
                config.CLASS_NAMES[1]: probs[1].item()   # 불량 확률
            },
            'input_tensor': input_tensor
        }
