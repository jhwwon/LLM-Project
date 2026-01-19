"""
공용 이미지 유틸리티
"""
from PIL import Image
from torchvision import transforms
import config

def get_inference_transform():
    return transforms.Compose([
        transforms.Resize(config.IMAGE_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(config.NORMALIZE_MEAN, config.NORMALIZE_STD)
    ])

def load_image(image_path):
    return Image.open(image_path).convert('RGB')
