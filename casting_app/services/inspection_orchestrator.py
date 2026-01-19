"""
검사 워크플로우 오케스트레이터
모든 비즈니스 로직을 조율하는 중앙 관리자
"""
import config
from classifiers.image_classifier import ImageClassifier
from explainers.gradcam import GradCAMGenerator
from services.analyzer import DefectAnalyzer
from services.pdf_generator import PDFReportGenerator
from services.history import InspectionHistory
from datetime import datetime


class InspectionOrchestrator:
    """검사 프로세스 전체를 관리하는 오케스트레이터"""
    
    def __init__(self):
        """모든 필요한 모듈 초기화"""
        # 분류기 초기화
        self.classifier = ImageClassifier(config.MODEL_PATH)
        
        # Grad-CAM 초기화 (EfficientNet-B0의 마지막 conv layer)
        # EfficientNet-B0: features[-1]이 아닌 features[-1][0]을 사용
        target_layer = self.classifier.model.features[-1]
        self.explainer = GradCAMGenerator(self.classifier.model, target_layer)
        
        # 분석기 및 리포트 생성기
        self.analyzer = DefectAnalyzer()
        self.pdf_generator = PDFReportGenerator()
        
        # 검사 이력 관리
        self.history = InspectionHistory()
    
    def run_inspection(self, image):
        # 1. 검사 시간 기록
        inspection_time = datetime.now()
        
        # 2. AI 예측 수행
        result = self.classifier.predict(image)
        result['inspection_time'] = inspection_time
        
        # 3. Grad-CAM 히트맵 생성
        cam_image = self.explainer.generate(result['input_tensor'], image)
        result['cam_image'] = cam_image
        
        # 4. 검사 이력 저장
        try:
            self.history.add_record(result)
        except Exception as e:
            # 이력 저장 실패는 전체 프로세스를 중단시키지 않음
            print(f"Warning: 이력 저장 실패 - {e}")
        
        return result
    
    def generate_ai_analysis(self, result):
        """
        Claude AI를 사용한 상세 분석 리포트 생성
        
        Args:
            result: run_inspection()의 결과
            
        Returns:
            str: 마크다운 형식의 분석 리포트
        """
        return self.analyzer.run_analysis(result)
    
    def generate_pdf_report(self, result, analysis_report, original_image, cam_image):
        """
        PDF 보고서 생성
        
        Args:
            result: 검사 결과
            analysis_report: AI 분석 리포트
            original_image: 원본 이미지
            cam_image: Grad-CAM 이미지
            
        Returns:
            BytesIO: PDF 파일 버퍼
        """
        return self.pdf_generator.generate_report(
            result, 
            analysis_report, 
            original_image, 
            cam_image
        )
    
    def get_statistics(self, days=1):
        """
        검사 통계 조회
        
        Args:
            days: 조회 기간 (일)
            
        Returns:
            dict: 통계 정보
        """
        return self.history.get_statistics(days=days)
    
    def get_history(self, days=1):
        """
        검사 이력 조회
        
        Args:
            days: 조회 기간 (일)
            
        Returns:
            DataFrame: 검사 이력
        """
        return self.history.get_history(days=days)
