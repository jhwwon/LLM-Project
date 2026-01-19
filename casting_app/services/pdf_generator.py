# -*- coding: utf-8 -*-
"""
PDF 보고서 생성기 - 프로페셔널 버전
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus.flowables import HRFlowable
from datetime import datetime
import io


class PDFReportGenerator:
    """주조 결함 검사 보고서 PDF 생성 (프로페셔널 버전)"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_korean_font()
        self._setup_custom_styles()
        
    def _setup_korean_font(self):
        """한글 폰트 설정 - 서브셋 비활성화로 한글 깨짐 방지"""
        import os
        
        # 프로젝트 내 Font 폴더 경로
        font_dir = os.path.join(os.path.dirname(__file__), '..', 'Font')
        malgun_path = os.path.join(font_dir, 'malgun.ttf')
        malgunbd_path = os.path.join(font_dir, 'malgunbd.ttf')
        
        try:
            # 맑은 고딕 폰트 등록 (서브셋 비활성화 필수)
            if os.path.exists(malgun_path):
                malgun_abs_path = os.path.abspath(malgun_path)
                # subfontIndex=0 명시적 지정
                font = TTFont('Malgun', malgun_abs_path, subfontIndex=0)
                
                # 서브셋 완전 비활성화 (다중 방어)
                if hasattr(font, 'face'):
                    font.face.subset = None
                if hasattr(font, 'subset'):
                    font.subset = None
                    
                pdfmetrics.registerFont(font)
                self.korean_font = 'Malgun'
                
                # 디버깅 정보
                subset_status = getattr(font.face, 'subset', 'N/A') if hasattr(font, 'face') else 'N/A'
                print(f"[OK] 맑은 고딕 폰트 로드 성공")
                print(f"   경로: {malgun_abs_path}")
                print(f"   서브셋 상태: {subset_status}")
                print(f"   파일 크기: {os.path.getsize(malgun_abs_path):,} bytes")
            else:
                raise FileNotFoundError(f"맑은 고딕 폰트를 찾을 수 없습니다: {malgun_path}")
            
            # 맑은 고딕 Bold 폰트 등록
            if os.path.exists(malgunbd_path):
                malgunbd_abs_path = os.path.abspath(malgunbd_path)
                # subfontIndex=0 명시적 지정
                font_bold = TTFont('MalgunBold', malgunbd_abs_path, subfontIndex=0)
                
                # 서브셋 완전 비활성화 (다중 방어)
                if hasattr(font_bold, 'face'):
                    font_bold.face.subset = None
                if hasattr(font_bold, 'subset'):
                    font_bold.subset = None
                    
                pdfmetrics.registerFont(font_bold)
                self.korean_font_bold = 'MalgunBold'
                
                # 디버깅 정보
                subset_status_bold = getattr(font_bold.face, 'subset', 'N/A') if hasattr(font_bold, 'face') else 'N/A'
                print(f"[OK] 맑은 고딕 Bold 폰트 로드 성공")
                print(f"   경로: {malgunbd_abs_path}")
                print(f"   서브셋 상태: {subset_status_bold}")
                print(f"   파일 크기: {os.path.getsize(malgunbd_abs_path):,} bytes")
            else:
                # Bold가 없으면 일반 폰트 사용
                self.korean_font_bold = 'Malgun'
                print("[WARNING] 맑은 고딕 Bold 폰트를 찾을 수 없어 일반 폰트를 사용합니다.")
                
        except Exception as e:
            print(f"[ERROR] 폰트 로드 실패: {e}")
            import traceback
            traceback.print_exc()
            self.korean_font = 'Helvetica'
            self.korean_font_bold = 'Helvetica-Bold'
            raise RuntimeError("한글 폰트를 로드할 수 없습니다. PDF 생성이 불가능합니다.")
    
    def _setup_custom_styles(self):
        """커스텀 스타일 정의"""
        # 제목
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontName=self.korean_font_bold,
            fontSize=22,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=10,
            alignment=TA_CENTER,
            leading=26
        )
        
        # 부제
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Normal'],
            fontName=self.korean_font,
            fontSize=12,
            textColor=colors.HexColor('#666666'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        # 섹션 헤더
        self.section_style = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading2'],
            fontName=self.korean_font_bold,
            fontSize=16,
            textColor=colors.white,
            backColor=colors.HexColor('#1f4788'),
            spaceAfter=15,
            spaceBefore=20,
            leftIndent=10,
            rightIndent=10,
            borderPadding=(5, 5, 5, 5)
        )
        
        # 서브섹션
        self.subsection_style = ParagraphStyle(
            'SubSection',
            parent=self.styles['Heading3'],
            fontName=self.korean_font_bold,
            fontSize=13,
            textColor=colors.HexColor('#2c5aa0'),
            spaceAfter=10,
            spaceBefore=15,
            leftIndent=5,
            borderWidth=0,
            borderColor=colors.HexColor('#2c5aa0'),
            borderPadding=3
        )
        
        # 본문
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['BodyText'],
            fontName=self.korean_font,
            fontSize=10,
            leading=16,
            spaceAfter=10,
            alignment=TA_JUSTIFY
        )
        
        # 강조 본문
        self.emphasis_style = ParagraphStyle(
            'Emphasis',
            parent=self.body_style,
            fontName=self.korean_font_bold,
            textColor=colors.HexColor('#d9534f')
        )
    
    def _safe_text(self, text):
        """텍스트를 PDF에 안전하게 사용할 수 있도록 변환"""
        if not text:
            return ""
        
        # 문자열로 변환
        if not isinstance(text, str):
            text = str(text)
        
        # XML 특수문자 이스케이프 (순서 중요!)
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        
        return text
    
    def _create_header(self):
        """보고서 헤더 생성"""
        elements = []
        
        # 상단 색상 바
        header_table = Table([['']], colWidths=[19*cm], rowHeights=[0.5*cm])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1f4788')),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.3*cm))
        
        # 제목
        elements.append(Paragraph("주조 결함 AI 검사 보고서", self.title_style))
        elements.append(Paragraph("Casting Defect Inspection Report by AI", self.subtitle_style))
        
        # 구분선
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1f4788'), spaceAfter=20))
        
        return elements
    
    def _create_inspection_info(self, result):
        """검사 정보 섹션"""
        elements = []
        
        elements.append(Paragraph("검사 정보", self.section_style))
        elements.append(Spacer(1, 0.3*cm))
        
        # 상태에 따른 배경색
        if result['prediction'] == 0:
            status_bg = colors.HexColor('#d4edda')
            status_text = colors.HexColor('#155724')
            status_icon = "[OK]"
        else:
            status_bg = colors.HexColor('#f8d7da')
            status_text = colors.HexColor('#721c24')
            status_icon = "[NG]"
        
        # 테이블용 스타일 (한글 폰트 명시)
        table_header_style = ParagraphStyle(
            'TableHeader',
            fontName=self.korean_font_bold,
            fontSize=11,
            textColor=colors.whitesmoke,
            alignment=TA_CENTER
        )
        
        table_cell_style = ParagraphStyle(
            'TableCell',
            fontName=self.korean_font,
            fontSize=10,
            textColor=colors.black,
            alignment=TA_LEFT
        )
        
        table_label_style = ParagraphStyle(
            'TableLabel',
            fontName=self.korean_font_bold,
            fontSize=10,
            textColor=colors.black,
            alignment=TA_LEFT
        )
        
        # 모든 텍스트를 Paragraph로 감싸기
        inspection_data = [
            [Paragraph('항목', table_header_style), Paragraph('내용', table_header_style)],
            [Paragraph('검사 일시', table_label_style), 
             Paragraph(datetime.now().strftime('%Y년 %m월 %d일 %H시 %M분'), table_cell_style)],
            [Paragraph('보고서 ID', table_label_style), 
             Paragraph(f"RPT-{datetime.now().strftime('%Y%m%d%H%M%S')}", table_cell_style)],
            [Paragraph('판정 결과', table_label_style), 
             Paragraph(f"{status_icon} {result['class_name']}", table_cell_style)],
            [Paragraph('AI 신뢰도', table_label_style), 
             Paragraph(f"{result['confidence']*100:.2f}%", table_cell_style)],
            [Paragraph('분석 모델', table_label_style), 
             Paragraph('EfficientNet-B0 (Fine-tuned)', table_cell_style)],
            [Paragraph('AI 엔진', table_label_style), 
             Paragraph('Claude Sonnet 4.5', table_cell_style)]
        ]
        
        table = Table(inspection_data, colWidths=[6*cm, 13*cm])
        table.setStyle(TableStyle([
            # 헤더 스타일
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#495057')),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            # 첫 번째 열 (라벨)
            ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#e9ecef')),
            
            # 판정 결과 행 강조
            ('BACKGROUND', (0, 3), (-1, 3), status_bg),
            
            # 전체
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#1f4788'))
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.8*cm))
        
        return elements
    
    def _create_image_analysis(self, original_img, gradcam_img):
        """이미지 분석 섹션"""
        import numpy as np
        from PIL import Image as PILImage
        
        elements = []
        
        elements.append(Paragraph("이미지 분석", self.section_style))
        elements.append(Spacer(1, 0.3*cm))
        
        # 이미지를 BytesIO로 변환
        img_buffer1 = io.BytesIO()
        img_buffer2 = io.BytesIO()
        
        if isinstance(original_img, np.ndarray):
            PILImage.fromarray(original_img).save(img_buffer1, format='PNG')
        else:
            original_img.save(img_buffer1, format='PNG')
        
        if isinstance(gradcam_img, np.ndarray):
            if gradcam_img.dtype != np.uint8:
                gradcam_img = (gradcam_img * 255).astype(np.uint8)
            PILImage.fromarray(gradcam_img).save(img_buffer2, format='PNG')
        else:
            gradcam_img.save(img_buffer2, format='PNG')
        
        img_buffer1.seek(0)
        img_buffer2.seek(0)
        
        # 이미지 테이블
        header_data = [[
            Paragraph("<b>원본 이미지</b>", self.body_style),
            Paragraph("<b>AI 판단 근거 (Grad-CAM)</b>", self.body_style)
        ]]
        
        header_table = Table(header_data, colWidths=[9.5*cm, 9.5*cm])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e9ecef')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(header_table)
        
        img_data = [[
            Image(img_buffer1, width=9*cm, height=9*cm),
            Image(img_buffer2, width=9*cm, height=9*cm)
        ]]
        
        img_table = Table(img_data, colWidths=[9.5*cm, 9.5*cm])
        img_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10)
        ]))
        
        elements.append(img_table)
        
        # 설명
        elements.append(Spacer(1, 0.3*cm))
        elements.append(Paragraph(
            "<i>※ Grad-CAM 히트맵은 AI 모델이 결함 판정 시 주목한 영역을 시각화한 것입니다. "
            "붉은색 영역일수록 판단에 큰 영향을 준 부분입니다.</i>",
            self.body_style
        ))
        
        elements.append(Spacer(1, 0.8*cm))
        
        return elements
    
    def _clean_text_for_pdf(self, text):
        """PDF용 텍스트 정제 - 한글 보존하면서 XML 특수문자만 처리"""
        import re
        # XML/HTML 특수 문자만 안전하게 처리 (한글은 그대로 유지)
        # 순서가 중요: & 를 먼저 처리해야 함
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        # 따옴표는 Paragraph에서 문제가 없으므로 처리하지 않음
        return text
    
    def _process_markdown_simple(self, text):
        """마크다운을 안전한 HTML로 변환"""
        import re
        # 먼저 텍스트 정제
        text = self._clean_text_for_pdf(text)
        
        # ** 굵은 글씨 (이미 이스케이프된 텍스트에서 처리)
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        
        return text
    
    def _create_ai_analysis(self, analysis_text):
        """AI 상세 분석 섹션"""
        from reportlab.platypus import Preformatted
        
        elements = []
        
        elements.append(Paragraph("AI 상세 분석", self.section_style))
        elements.append(Spacer(1, 0.3*cm))
        
        # 분석 텍스트를 파싱하여 구조화
        lines = analysis_text.split('\n')
        
        # 안전한 본문 스타일 (Preformatted용)
        safe_body_style = ParagraphStyle(
            'SafeBody',
            parent=self.body_style,
            fontName=self.korean_font,
            fontSize=10,
            leading=16,
            leftIndent=0,
            rightIndent=0
        )
        
        for line in lines:
            line = line.strip()
            if not line:
                elements.append(Spacer(1, 0.2*cm))
                continue
            
            try:
                # 마크다운 헤더 처리 (###)
                if line.startswith('###'):
                    header_text = line.replace('###', '').strip()
                    # 한글 완전 보존
                    safe_text = self._clean_text_for_pdf(header_text)
                    if safe_text.strip():
                        elements.append(Paragraph(f"<b>{safe_text}</b>", safe_body_style))
                    elements.append(Spacer(1, 0.1*cm))
                    
                # 마크다운 헤더 처리 (##)
                elif line.startswith('##'):
                    header_text = line.replace('##', '').strip()
                    # 한글 완전 보존
                    safe_text = self._clean_text_for_pdf(header_text)
                    if safe_text.strip():
                        elements.append(Paragraph(f"<b>{safe_text}</b>", safe_body_style))
                    elements.append(Spacer(1, 0.1*cm))
                    
                # 리스트 항목
                elif line.startswith('-') or line.startswith('•'):
                    list_text = line[1:].strip()
                    # ** 굵은 글씨 처리
                    list_text = self._process_markdown_simple(list_text)
                    elements.append(Paragraph(f"  • {list_text}", safe_body_style))
                    
                # 일반 텍스트
                else:
                    # ** 굵은 글씨 처리
                    processed_text = self._process_markdown_simple(line)
                    elements.append(Paragraph(processed_text, safe_body_style))
                    
            except Exception as e:
                # 에러 발생 시 안전한 fallback - 한글 완전 보존
                print(f"[WARNING] PDF 텍스트 처리 오류: {e}")
                safe_text = self._clean_text_for_pdf(line)
                if safe_text.strip():
                    elements.append(Paragraph(safe_text, safe_body_style))
        
        elements.append(Spacer(1, 0.8*cm))
        
        return elements
    
    def _create_footer(self):
        """보고서 푸터"""
        elements = []
        
        # 구분선
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.grey, spaceBefore=30, spaceAfter=10))
        
        # 주의사항
        warning_style = ParagraphStyle(
            'Warning',
            parent=self.body_style,
            fontSize=8,
            textColor=colors.HexColor('#856404'),
            backColor=colors.HexColor('#fff3cd'),
            borderWidth=1,
            borderColor=colors.HexColor('#ffc107'),
            borderPadding=8,
            alignment=TA_CENTER
        )
        
        elements.append(Paragraph(
            "<b>중요 안내</b><br/>"
            "본 보고서는 AI 시스템에 의해 자동 생성되었으며, 참고용으로 활용하시기 바랍니다.<br/>"
            "최종 품질 판정은 반드시 전문 검수자의 육안 확인을 거쳐야 합니다.",
            warning_style
        ))
        
        elements.append(Spacer(1, 0.5*cm))
        
        # 하단 정보
        footer_style = ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontName=self.korean_font,
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        
        elements.append(Paragraph(
            f"Casting AI System v1.0 | Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            footer_style
        ))
        
        # 하단 색상 바
        footer_bar = Table([['']], colWidths=[19*cm], rowHeights=[0.3*cm])
        footer_bar.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1f4788')),
        ]))
        elements.append(Spacer(1, 0.3*cm))
        elements.append(footer_bar)
        
        return elements
    
    def generate_report(self, result, analysis_text, original_img, gradcam_img):
        """
        프로페셔널 PDF 보고서 생성
        
        Args:
            result: 분류 결과 dict
            analysis_text: Claude 분석 텍스트
            original_img: 원본 이미지
            gradcam_img: Grad-CAM 이미지
            
        Returns:
            BytesIO: PDF 파일 바이너리
        """
        buffer = io.BytesIO()
        print(f"PDF 생성 시작... (사용 폰트: {self.korean_font})")
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            topMargin=1.5*cm,
            bottomMargin=1.5*cm,
            leftMargin=1.5*cm,
            rightMargin=1.5*cm,
            invariant=1,  # 폰트 깨짐 방지를 위한 고정 설정
            compress=0    # 압축 비활성화 (한글 깨짐 방지)
        )
        
        story = []
        
        # 1. 헤더
        story.extend(self._create_header())
        
        # 2. 검사 정보
        story.extend(self._create_inspection_info(result))
        
        # 3. 이미지 분석
        story.extend(self._create_image_analysis(original_img, gradcam_img))
        
        # 페이지 구분
        story.append(PageBreak())
        
        # 4. AI 상세 분석
        story.extend(self._create_ai_analysis(analysis_text))
        
        # 5. 푸터
        story.extend(self._create_footer())
        
        # PDF 생성
        doc.build(story)
        buffer.seek(0)
        return buffer
