"""
주조 결함 AI 검사 시스템 - 프로페셔널 웹 앱
탭 구조: 홈 | AI 검사 | 프로젝트 소개 | 핵심 코드 설명
"""
import os
# Windows 콘솔 인코딩 문제 해결
os.environ['PYTHONIOENCODING'] = 'utf-8'

import streamlit as st
import config
from utils.imaging import load_image
from datetime import datetime
import plotly.graph_objects as go
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="주조 결함 AI 검사 시스템",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3em;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #1f4788 0%, #2c5aa0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 20px 0;
    }
    .info-card {
        background: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f4788;
        margin: 10px 0;
    }
    .metric-card {
        background: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .code-block {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 5px;
        border-left: 3px solid #28a745;
        margin: 10px 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 10px 20px;
        background-color: #f0f2f6;
        border-radius: 5px 5px 0 0;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f4788;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# 오케스트레이터 초기화
@st.cache_resource(ttl=60)  # 60초마다 캐시 갱신
def init_orchestrator():
    """오케스트레이터 초기화 - 모든 모듈을 통합 관리"""
    from services.inspection_orchestrator import InspectionOrchestrator
    return InspectionOrchestrator()

try:
    orchestrator = init_orchestrator()
except Exception as e:
    st.error(f"⚠️ 시스템 초기화 오류: {e}")
    st.info("💡 모델 파일이 `models/` 폴더에 있는지 확인해주세요.")
    st.stop()

# 사이드바
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/factory.png", width=150)
    st.markdown("---")
    st.markdown("### 📊 시스템 정보")
    st.info(f"""
    **모델**: EfficientNet-B0  
    **정확도**: 99.86%  
    **처리 속도**: 실시간  
    **AI 엔진**: claude-sonnet-4-5
    """)
    
    st.markdown("---")
    st.markdown("### 📌 주요 기능")
    st.markdown("""
    ✅ 실시간 결함 판정  
    ✅ AI 판단 근거 시각화  
    ✅ 상세 분석 보고서  
    ✅ PDF 다운로드
    """)
    
    st.markdown("---")
    st.caption("© 2026 Casting AI System")

# 메인 헤더
st.markdown('<div class="main-header">🏭 주조 결함 AI 검사 시스템</div>', unsafe_allow_html=True)
st.markdown("### 딥러닝과 LLM을 결합한 차세대 품질 관리 솔루션")
st.markdown("---")



# 탭 생성 (5개로 확장)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 홈", 
    "🔍 AI 검사", 
    " 📊 일일 통계", 
    "📚 프로젝트 소개", 
    "💻 핵심 코드"
])

# ==================== 탭 1: 홈 ====================
with tab1:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <h3>🎯 프로젝트 목표</h3>
            <p>제조 현장에서 육안 검사로 놓치기 쉬운 미세 결함을 AI가 자동으로 감지하여 불량률을 획기적으로 감소시킵니다.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <h3>🚀 핵심 기술</h3>
            <p>전이학습(Transfer Learning) + 파인튜닝으로 최적화된 EfficientNet 모델과 Grad-CAM 시각화 기술을 활용합니다.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-card">
            <h3>🤖 LLM 통합</h3>
            <p>Claude AI가 결함 원인 분석, 조치 방안까지 자동으로 작성하여 전문 보고서를 생성합니다.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📊 시스템 성능 지표")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h1 style="color: #1f4788;">99.86%</h1>
            <p><b>검증 정확도</b></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h1 style="color: #28a745;">0.006</h1>
            <p><b>손실률 (Loss)</b></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h1 style="color: #dc3545;">< 1초</h1>
            <p><b>판정 속도</b></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h1 style="color: #6c757d;">5.3M</h1>
            <p><b>모델 파라미터</b></p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 성능 그래프 이미지 표시
    st.markdown("### 📈 모델 학습 결과 및 성능 분석")
    
    col_img1, col_img2 = st.columns(2)
    
    with col_img1:
        st.markdown("**📉 학습 손실 및 정확도 (Training Loss & Accuracy)**")
        st.image("assets/accuracy_loss.png", caption="Training & Validation Metrics", use_container_width=True)
    
    with col_img2:
        st.markdown("**📊 혼동 행렬 (Confusion Matrix)**")
        st.image("assets/confusion_matrix.png", caption="Test Set Confusion Matrix", use_container_width=True)
        
    st.info("💡 **분석**: EfficientNet-B0 모델은 16 Epoch에서 최적 성능(99.86%)을 달성했으며, Test 데이터셋 검증 결과 오분류가 단 2건(0.28%)에 불과합니다.")

# ==================== 탭 2: AI 검사 ====================
with tab2:
    st.markdown("### 🔬 이미지 업로드 및 결함 검사")
    
    # 검사 모드 선택
    test_mode = st.radio(
        "검사 모드 선택",
        ["📁 파일 업로드", "🎯 샘플 이미지"],
        horizontal=True,
        help="직접 업로드하거나 미리 준비된 샘플을 선택하세요"
    )
    
    st.markdown("---")
    
    img = None
    
    if test_mode == "🎯 샘플 이미지":
        # 샘플 이미지 딕셔너리 (간단하게 통합)
        sample_images = {
            "✅ 정상 - 샘플 1": "assets/sample_normal_cast_ok_0_10.jpeg",
            "✅ 정상 - 샘플 2": "assets/sample_normal_cast_ok_0_1001.jpeg",
            "✅ 정상 - 샘플 3": "assets/sample_normal_cast_ok_0_1002.jpeg",
            "✅ 정상 - 샘플 4": "assets/sample_normal_cast_ok_0_1003.jpeg",
            "❌ 불량 - 샘플 1": "assets/sample_defect_cast_def_0_1059.jpeg",
            "❌ 불량 - 샘플 2": "assets/sample_defect_cast_def_0_1063.jpeg",
            "❌ 불량 - 샘플 3": "assets/sample_defect_cast_def_0_108.jpeg",
            "❌ 불량 - 샘플 4": "assets/sample_defect_cast_def_0_1096.jpeg"
        }
        
        # 샘플 선택 (미리보기 없이)
        selected_sample = st.selectbox(
            "테스트할 샘플을 선택하세요",
            options=list(sample_images.keys()),
            index=0
        )
        
        # 샘플 이미지 로드
        from PIL import Image
        img = Image.open(sample_images[selected_sample])
        st.success(f"✅ 선택 완료: {selected_sample}")
    
    else:  # 파일 업로드 모드
        uploaded_file = st.file_uploader(
            "검사할 제품 이미지를 업로드하세요 (JPG, PNG)",
            type=['jpg', 'jpeg', 'png'],
            help="주조 제품의 상단 사진을 업로드하면 AI가 자동으로 결함을 판정합니다."
        )
        
        if uploaded_file:
            img = load_image(uploaded_file)
    
    # 이미지가 선택되었을 때 (업로드 or 샘플)
    if img is not None:
        # 진행바
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("이미지 로딩 중...")
        progress_bar.progress(20)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 📷 원본 이미지")
            st.image(img, use_container_width=True, caption="업로드된 제품 이미지")
        
        status_text.text("AI 분석 중...")
        progress_bar.progress(50)
        
        # 오케스트레이터로 전체 검사 실행
        result = orchestrator.run_inspection(img)
        cam_img = result['cam_image']
        
        progress_bar.progress(70)
        
        with col2:
            st.markdown("#### 🔥 Grad-CAM 히트맵")
            st.image(cam_img, use_container_width=True, caption="AI 판단 근거 시각화")
            
            # 컬러 스펙트럼 설명
            st.markdown("**🎨 컬러 스펙트럼 가이드**")
            
            # 컬러바를 텍스트와 색상으로 표시
            st.markdown("""
            <div style="background: linear-gradient(to right, #0000ff, #00ffff, #00ff00, #ffff00, #ff0000); 
                        height: 30px; 
                        border-radius: 5px; 
                        border: 2px solid #ddd;
                        margin-bottom: 10px;">
            </div>
            """, unsafe_allow_html=True)
            
            # 범례 설명
            col_legend1, col_legend2, col_legend3 = st.columns(3)
            
            with col_legend1:
                st.markdown("🔵 **낮음**  \n중요도: 0~30%")
            with col_legend2:
                st.markdown("🟡 **중간**  \n중요도: 30~70%")
            with col_legend3:
                st.markdown("🔴 **높음**  \n중요도: 70~100%")
            
            st.info("""
            **📖 해석 방법**  
            - **🔴 빨간색**: AI가 가장 집중한 영역 (결함 가능성 높음)  
            - **🟡 노란색**: 부분적으로 주목한 영역  
            - **🔵 파란색**: 거의 주목하지 않은 영역
            """)

        
        progress_bar.progress(90)
        
        with col3:
            st.markdown("#### 🎯 판정 결과")
            
            if result['prediction'] == 0:
                st.success(f"### ✅ {result['class_name']}")
            else:
                st.error(f"### ❌ {result['class_name']}")
            
            st.markdown("---")
            
            # 각 클래스별 확률 시각화
            st.markdown("**📊 클래스별 확률 분석**")
            
            probs = result['probabilities']
            
            # 확률 바 차트 (Plotly)
            fig_prob = go.Figure()
            
            colors = ['#28a745', '#dc3545']  # 정상: 초록, 불량: 빨강
            class_names = list(probs.keys())
            prob_values = [probs[name] * 100 for name in class_names]
            
            # 각 값에 대한 텍스트 위치 결정 (낮은 값은 inside)
            text_positions = ['inside' if val < 5 else 'outside' for val in prob_values]
            
            fig_prob.add_trace(go.Bar(
                x=class_names,
                y=prob_values,
                marker=dict(
                    color=colors,
                    line=dict(color='white', width=2)
                ),
                text=[f"{val:.2f}%" for val in prob_values],  # 소수점 2자리
                textposition=text_positions,
                textfont=dict(size=13, color='white', family='Arial Black'),
                insidetextfont=dict(color='white'),
                outsidetextfont=dict(color='black')
            ))
            
            fig_prob.update_layout(
                title=dict(
                    text="AI 예측 확률",
                    font=dict(size=14, color='#333')
                ),
                yaxis=dict(
                    title="확률 (%)",
                    range=[0, 110],  # 범위 확대
                    showgrid=True,
                    gridcolor='lightgray'
                ),
                xaxis=dict(
                    title="",
                    tickfont=dict(size=12, family='Arial')
                ),
                height=320,
                margin=dict(t=50, b=50, l=50, r=50),
                plot_bgcolor='white',
                paper_bgcolor='white',
                showlegend=False,
                bargap=0.3
            )
            
            st.plotly_chart(fig_prob, use_container_width=True)
            
            # 검사 시간 표시
            st.markdown("---")
            st.info(f"""
            **🕐 검사 일시**  
            {result['inspection_time'].strftime('%Y년 %m월 %d일')}  
            {result['inspection_time'].strftime('%H시 %M분 %S초')}
            """)
            
            # 검사 이력은 오케스트레이터에서 자동 저장됨
        
        progress_bar.progress(100)
        status_text.text("✅ 분석 완료!")
        
        st.markdown("---")
        
        # AI 상세 분석
        if st.button("🚀 Claude AI 상세 분석 리포트 생성", type="primary", use_container_width=True):
            with st.spinner("🤖 Claude AI가 결함을 분석하고 있습니다..."):
                report = orchestrator.generate_ai_analysis(result)
                
            st.markdown("---")
            st.markdown("### 📊 AI 분석 리포트")
            
            # 보고서를 예쁘게 표시
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #1f4788;">
            {report}
            </div>
            """, unsafe_allow_html=True)
            
            # PDF 생성
            st.markdown("---")
            st.markdown("### 📥 보고서 다운로드")
            
            with st.spinner("📄 PDF 문서 생성 중..."):
                try:
                    pdf_buffer = orchestrator.generate_pdf_report(result, report, img, cam_img)
                    filename = f"casting_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.download_button(
                            label="📥 PDF 보고서 다운로드",
                            data=pdf_buffer,
                            file_name=filename,
                            mime="application/pdf",
                            type="primary",
                            use_container_width=True
                        )
                    st.success("✅ PDF 보고서가 생성되었습니다!")
                except Exception as e:
                    st.error(f"PDF 생성 오류: {e}")

# ==================== 탭 3: 일일 통계 ====================
with tab3:
    st.markdown("## 📊 일일 검사 통계 대시보드")
    
    # 기간 선택
    col_period1, col_period2 = st.columns([1, 3])
    
    with col_period1:
        period = st.selectbox(
            "조회 기간",
            ["오늘", "최근 7일", "최근 30일"],
            index=0
        )
    
    days_map = {"오늘": 1, "최근 7일": 7, "최근 30일": 30}
    selected_days = days_map[period]
    
    # 통계 가져오기 (오케스트레이터 사용)
    stats = orchestrator.get_statistics(days=selected_days)
    df_history = orchestrator.get_history(days=selected_days)
    
    st.markdown("---")
    
    # 주요 지표 카드
    st.markdown(f"### 📅 {period} 검사 현황")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="총 검사 건수",
            value=f"{stats['total']}건",
            delta=None
        )
    
    with col2:
        st.metric(
            label="✅ 정상",
            value=f"{stats['normal']}건",
            delta=f"{stats['normal_rate']:.1f}%"
        )
    
    with col3:
        st.metric(
            label="❌ 불량",
            value=f"{stats['defect']}건",
            delta=f"-{stats['defect_rate']:.1f}%",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            label="평균 신뢰도",
            value=f"{stats['avg_confidence']:.1f}%"
        )
    
    st.markdown("---")
    
    if not df_history.empty:
        # 시간대별 검사 추이
        st.markdown("### 📈 시간대별 검사 추이")
        
        # 시간대별 집계
        df_history['hour'] = pd.to_datetime(df_history['timestamp']).dt.hour
        hourly_counts = df_history.groupby(['hour', 'class_name']).size().unstack(fill_value=0)
        
        fig_trend = go.Figure()
        
        if '정상 (OK)' in hourly_counts.columns:
            fig_trend.add_trace(go.Bar(
                name='정상',
                x=hourly_counts.index,
                y=hourly_counts['정상 (OK)'],
                marker_color='#28a745'
            ))
        
        if '불량 (Defective)' in hourly_counts.columns:
            fig_trend.add_trace(go.Bar(
                name='불량',
                x=hourly_counts.index,
                y=hourly_counts['불량 (Defective)'],
                marker_color='#dc3545'
            ))
        
        fig_trend.update_layout(
            xaxis_title="시간 (Hour)",
            yaxis_title="검사 건수",
            barmode='stack',
            height=400,
            hovermode='x unified',
            template='plotly_white'
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)
        
        st.markdown("---")
        
        # 파이 차트
        col_pie1, col_pie2 = st.columns(2)
        
        with col_pie1:
            st.markdown("### 📊 판정 비율")
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=['정상', '불량'],
                values=[stats['normal'], stats['defect']],
                marker=dict(colors=['#28a745', '#dc3545']),
                textinfo='label+percent',
                hole=0.4
            )])
            
            fig_pie.update_layout(
                height=350,
                showlegend=True,
                template='plotly_white'
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col_pie2:
            st.markdown("### 📋 최근 검사 기록")
            
            # 최근 10건 표시
            recent_df = df_history.tail(10)[['timestamp', 'class_name', 'confidence']].copy()
            recent_df['신뢰도'] = (recent_df['confidence'] * 100).round(1).astype(str) + '%'
            recent_df = recent_df[['timestamp', 'class_name', '신뢰도']]
            recent_df.columns = ['시간', '판정', '신뢰도']
            recent_df = recent_df.sort_values('시간', ascending=False)
            
            st.dataframe(
                recent_df,
                use_container_width=True,
                hide_index=True,
                height=300
            )
        
    else:
        st.info("📭 아직 검사 이력이 없습니다. AI 검사 탭에서 제품을 검사해보세요!")

# ==================== 탭 4: 프로젝트 소개 ====================
with tab4:
    st.markdown("## 📘 프로젝트 개요")
    
    st.markdown("""
    ### 🎯 개발 배경
    
    제조업 현장에서 주조 제품의 결함 검사는 전통적으로 **숙련된 검수자의 육안 검사**에 의존해왔습니다.
    하지만 이러한 방식은 다음과 같은 한계가 있습니다:
    
    - ⚠️ **인적 오류**: 피로도, 집중력 저하로 인한 불량품 누락
    - ⏱️ **시간 소요**: 대량 생산 시 검사 시간이 병목 구간
    - 📊 **일관성 부족**: 검수자마다 판단 기준이 상이
    - 💰 **인건비 부담**: 숙련 인력 확보 및 유지 비용
    
    본 프로젝트는 **AI 기술**을 도입하여 이러한 문제를 해결하고자 합니다.
    """)
    
    st.markdown("---")
    
    st.markdown("### 🛠️ 기술 스택")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🧠 딥러닝 & AI
        - **PyTorch 2.0**: 딥러닝 프레임워크
        - **EfficientNet-B0**: 경량화된 고성능 CNN 모델
        - **Transfer Learning**: ImageNet 사전 학습 모델 활용
        - **Fine-tuning**: 도메인 특화 재학습
        - **Grad-CAM**: 설명 가능한 AI (XAI) 기법
        """)
    
    with col2:
        st.markdown("""
        #### 🤖 LLM & 백엔드
        - **claude-sonnet-4-5**: 고급 언어 모델
        - **Anthropic API**: LLM 연동
        - **Streamlit**: 웹 인터페이스
        - **ReportLab**: PDF 생성
        - **Plotly**: 인터랙티브 차트
        """)
    
    st.markdown("---")
    
    st.markdown("### 🏗️ 시스템 아키텍처")
    
    st.markdown("""
    ```
    [ 사용자 ] 
         ↓ (이미지 업로드)
    [ Streamlit UI ]
         ↓
    [ Image Classifier (EfficientNet-B0) ]
         ├─→ [ 결함 판정: 정상/불량 ]
         └─→ [ Grad-CAM Explainer ]
                ├─→ [ 히트맵 시각화 ]
                └─→ [ LLM Analyzer (Claude) ]
                       ├─→ [ 상세 분석 ]
                       ├─→ [ 원인 추정 ]
                       ├─→ [ 조치 제안 ]
                       └─→ [ PDF 보고서 생성 ]
    ```
    """)
    
    st.markdown("---")
    
    st.markdown("### 📊 데이터셋 & 학습")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **📦 데이터셋 정보**
        - 출처: Kaggle - Casting Product Image Data
        - 총 이미지: 7,348장
        - 클래스: 정상(OK) / 불량(Defective)
        - 분할 비율: Train 70% / Val 15% / Test 15%
        """)
    
    with col2:
        st.success("""
        **🎓 학습 전략 (Training Strategy)**
        - **Epoch**: 10 (Early Stopping 적용)
        - **Batch Size**: 32
        - **Optimizer**: Adam (LR=0.001)
        - **Pre-trained**: ImageNet 가중치 사용
        - **데이터 증강**: 회전, 상하좌우 반전, 색상 변화
        """)

# ==================== 탭 5: 핵심 코드 ====================
with tab5:
    st.markdown("## 💻 핵심 코드 설명")
    
    st.markdown("### 1️⃣ 모델 아키텍처 (EfficientNet-B0 + 파인튜닝)")
    
    st.code("""
# classifiers/image_classifier.py

def _build_model(self):
    '''EfficientNet-B0 모델 생성 및 커스터마이징'''
    
    # ImageNet으로 사전 학습된 모델 불러오기 (전이학습)
    model = models.efficientnet_b0(weights=None)
    
    # 분류기(Classifier) 부분을 우리 문제에 맞게 교체
    # - 원래: 1000개 클래스 분류
    # - 수정 후: 2개 클래스 (정상/불량)
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.5),      # 과적합 방지
        nn.Linear(1280, 2)       # 최종 출력: 2개 클래스
    )
    
    return model.to(self.device).eval()
    """, language='python')
    
    st.markdown("""
    **💡 핵심 포인트:**
    - **전이학습 (Transfer Learning)**: ImageNet에서 배운 일반적인 시각 특징을 활용
    - **파인튜닝 (Fine-tuning)**: 전체 네트워크를 주조 데이터로 재학습
    - **Dropout(0.5)**: 학습 시 50%의 뉴런을 무작위로 비활성화하여 과적합 방지
    """)
    
    st.markdown("---")
    
    st.markdown("### 2️⃣ Grad-CAM (시각화 - AI가 어디를 보고 판단했는가?)")
    
    st.code("""
# explainers/gradcam.py

def generate(self, input_tensor, original_image):
    '''Grad-CAM 히트맵 생성'''
    
    # 1. Forward Pass (순전파)
    output = self.model(input_tensor)
    pred = torch.argmax(output, dim=1)
    
    # 2. Backward Pass (역전파) - 그래디언트 계산
    self.model.zero_grad()
    class_score = output[0, pred]
    class_score.backward()
    
    # 3. Target Layer의 그래디언트와 Feature Map 추출
    gradients = self.target_layer.gradient  # 어느 픽셀이 중요한가?
    activations = self.target_layer.output  # 어떤 특징이 활성화되었나?
    
    # 4. 가중치 평균 계산 (Grad-CAM 공식)
    weights = torch.mean(gradients, dim=(2, 3))
    cam = torch.sum(weights * activations, dim=1).squeeze()
    
    # 5. ReLU 적용 (양수 영역만 강조)
    cam = F.relu(cam)
    
    # 6. 원본 이미지에 오버레이
    return overlay_heatmap(cam, original_image)
    """, language='python')
    
    st.markdown("""
    **💡 핵심 포인트:**
    - **Gradient**: 특정 클래스 예측에 영향을 준 정도 (중요도)
    - **Activation**: 각 영역에서 활성화된 특징 맵
    - **Weighted Sum**: 중요도 × 활성화 맵 = "AI의 시선"
    """)
    
    st.markdown("---")
    
    st.markdown("### 3️⃣ LLM 통합 (Claude API로 분석 보고서 자동 생성)")
    
    st.code("""
# services/analyzer.py

def run_analysis(self, result):
    '''Claude를 사용한 결함 분석'''
    
    # LLM Analyzer 호출
    analysis_result = self.analyzer.analyze(result)
    
    # 보고서 포맷팅
    report = f\"\"\"
### 🧐 상세 분석 결과
{analysis_result['analysis']}

### 🛠️ 권장 조치 사항
{analysis_result['recommendation']}
    \"\"\"
    
    return report
    """, language='python')
    
    st.code("""
# llm/analyzer.py

def analyze(self, prediction_result):
    '''Claude에게 프롬프트 전송'''
    
    # 분석 프롬프트 생성
    prompt = f\"\"\"
    다음은 AI 모델이 주조 제품을 검사한 결과입니다:
    - 판정: {class_name}
    - 신뢰도: {confidence * 100:.2f}%
    
    이 결과를 바탕으로:
    1. 결함의 가능한 원인을 3가지 이상 분석해주세요.
    2. 생산 공정 개선을 위한 구체적인 조치 방안을 제시해주세요.
    3. 전문가가 육안으로 재확인해야 할 사항을 알려주세요.
    \"\"\"
    
    # Claude API 호출
    response = self.llm_client.generate(prompt)
    
    return response
    """, language='python')
    
    st.markdown("""
    **💡 핵심 포인트:**
    - **Prompt Engineering**: AI가 제품을 어떻게 판단했는지 맥락 제공
    - **Domain Knowledge**: 주조 공정 전문 용어 및 배경 지식 활용
    - **Structured Output**: 분석 → 원인 → 조치 순서로 체계적인 보고서 생성
    """)
    
    st.markdown("---")
    
    st.markdown("### 4️⃣ 데이터 증강 (Data Augmentation)")
    
    st.code("""
# 학습 시 데이터 변환 파이프라인

train_transform = transforms.Compose([
    transforms.Resize((224, 224)),              # 크기 통일
    transforms.RandomHorizontalFlip(p=0.5),     # 좌우 반전
    transforms.RandomVerticalFlip(p=0.5),       # 상하 반전
    transforms.RandomRotation(45),              # 최대 45도 회전
    transforms.ColorJitter(                     # 색상 변화
        brightness=0.3,                         # 밝기 ±30%
        contrast=0.3                            # 대비 ±30%
    ),
    transforms.RandomAffine(                    # 이동 및 스케일
        degrees=0,
        translate=(0.1, 0.1),                   # 10% 이동
        scale=(0.9, 1.1)                        # 90~110% 크기
    ),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])
    """, language='python')
    
    st.markdown("""
    **💡 핵심 포인트:**
    - **목적**: 적은 데이터로도 과적합을 막고 일반화 성능 향상
    - **효과**: 같은 이미지도 매번 다르게 보이므로 모델이 "암기"하지 못함
    - **실전 대응**: 공장 현장에서 제품 각도, 조명이 다를 때도 잘 판정
    """)
    
    st.markdown("---")
    
    st.success("""
    ### 🎓 학습 포인트 요약
    
    1. **전이학습 + 파인튜닝**: 적은 데이터로 높은 성능 달성
    2. **Grad-CAM**: "블랙박스" AI를 설명 가능하게 만듦
    3. **LLM 통합**: 단순 판정을 넘어 전문가 수준의 분석 제공
    4. **데이터 증강**: 강건한 모델 학습의 핵심
    5. **End-to-End**: 이미지 입력 → PDF 보고서까지 완전 자동화
    """)

st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>Made with ❤️ using Streamlit & PyTorch</div>", unsafe_allow_html=True)
