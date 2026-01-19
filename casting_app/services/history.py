"""
검사 이력 관리 모듈
"""
import pandas as pd
from pathlib import Path
from datetime import datetime
import json


class InspectionHistory:
    """검사 이력 저장 및 조회"""
    
    def __init__(self, history_file="inspection_history.csv"):
        self.history_file = Path(history_file)
        self._init_history()
    
    def _init_history(self):
        """이력 파일 초기화"""
        if not self.history_file.exists():
            df = pd.DataFrame(columns=[
                'timestamp', 'prediction', 'class_name', 
                'confidence', 'normal_prob', 'defect_prob'
            ])
            df.to_csv(self.history_file, index=False)
    
    def add_record(self, result):
        """검사 결과 추가"""
        record = {
            'timestamp': result.get('inspection_time', datetime.now()).strftime('%Y-%m-%d %H:%M:%S'),
            'prediction': result['prediction'],
            'class_name': result['class_name'],
            'confidence': result['confidence'],
            'normal_prob': result['probabilities'][list(result['probabilities'].keys())[0]],
            'defect_prob': result['probabilities'][list(result['probabilities'].keys())[1]]
        }
        
        df = pd.read_csv(self.history_file)
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
        df.to_csv(self.history_file, index=False)
    
    def get_history(self, days=1):
        """최근 N일 이력 조회"""
        if not self.history_file.exists():
            return pd.DataFrame()
        
        df = pd.read_csv(self.history_file)
        if df.empty:
            return df
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # 최근 N일 필터
        cutoff = pd.Timestamp.now() - pd.Timedelta(days=days)
        df = df[df['timestamp'] >= cutoff]
        
        return df
    
    def get_statistics(self, days=1):
        """통계 계산"""
        df = self.get_history(days)
        
        if df.empty:
            return {
                'total': 0,
                'normal': 0,
                'defect': 0,
                'normal_rate': 0.0,
                'defect_rate': 0.0,
                'avg_confidence': 0.0
            }
        
        total = len(df)
        normal = len(df[df['prediction'] == 0])
        defect = len(df[df['prediction'] == 1])
        
        return {
            'total': total,
            'normal': normal,
            'defect': defect,
            'normal_rate': (normal / total * 100) if total > 0 else 0.0,
            'defect_rate': (defect / total * 100) if total > 0 else 0.0,
            'avg_confidence': df['confidence'].mean() * 100
        }
