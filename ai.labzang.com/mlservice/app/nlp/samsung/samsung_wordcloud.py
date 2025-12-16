"""
NLTK 자연어 처리 서비스
NLTK(Natural Language Toolkit) 패키지를 활용한 자연어 처리 및 문서 분석 서비스

주요 기능:
- 말뭉치 관리
- 토큰 생성
- 형태소 분석
- 품사 태깅
- 텍스트 분석
- 워드클라우드 생성
"""

import re
import pandas as pd

import matplotlib.pyplot as plt


from nltk import FreqDist
from wordcloud import WordCloud
import logging
from konlpy.tag import Okt

logger = logging.getLogger(__name__)


class SamsungWordcloud:
    
    def __init__(self):
        self.okt = Okt()

    def text_process(self):
        freq_txt = self.find_freq()
        file_info = self.draw_wordcloud()
        return {
            '전처리 결과': '완료',
            'freq_txt': freq_txt,
            'saved_file': file_info
        }
        
    def read_file(self):
        self.okt.pos("삼성전자 글로벌센터 전자사업부" , stem=True)
        fname = 'app/nlp/data/kr-Report_2018.txt'
        with open(fname, 'r', encoding='utf-8') as f:
            text = f.read()
        return text

    def extract_hangeul(self, text: str):
        temp = text.replace('\n', ' ')
        tokenizer = re.compile(r'[^ ㄱ-힣]+')
        return tokenizer.sub('',temp)

    def change_token(self, texts):
        return word_tokenize(texts)
    
    def extract_noun(self):
        # 삼성전자의 스마트폰은 -> 삼성전자 스마트폰
        noun_tokens = []
        tokens = self.change_token(self.extract_hangeul(self.read_file()))
        for i in tokens:
            pos = self.okt.pos(i)
            temp = [j[0] for j in pos if j[1] == 'Noun']
            if len(''.join(temp)) > 1 :
                noun_tokens.append(''.join(temp))
        texts = ' '.join(noun_tokens)
        logger.info(texts[:100])
        return texts

    def read_stopword(self):
        self.okt.pos("삼성전자 글로벌센터 전자사업부", stem=True)
        fname = 'app/nlp/data/stopwords.txt'
        with open(fname, 'r', encoding='utf-8') as f:
            stopwords = f.read()
        return stopwords

    def remove_stopword(self):
        texts = self.extract_noun()
        tokens = self.change_token(texts)
        # print('------- 1 명사 -------')
        # print(texts[:30])
        stopwords = self.read_stopword()
        # print('------- 2 스톱 -------')
        # print(stopwords[:30])
        # print('------- 3 필터 -------')
        texts = [text for text in tokens
                 if text not in stopwords]
        # print(texts[:30])
        return texts

    def find_freq(self):
        texts = self.remove_stopword()
        freqtxt = pd.Series(dict(FreqDist(texts))).sort_values(ascending=False)
        logger.info(freqtxt[:30])
        return freqtxt

    def draw_wordcloud(self, save_to_file=True):
        from pathlib import Path
        from datetime import datetime
        
        texts = self.remove_stopword()
        # D2Coding 폰트를 사용한 워드클라우드 생성 (한글 지원)
        font_path = 'app/nlp/data/D2Coding.ttf'
        wcloud = WordCloud(font_path=font_path, relative_scaling=0.2, background_color='white', 
                           width=1200, height=800, max_words=100).generate(" ".join(texts))
        plt.figure(figsize=(12, 12))
        plt.imshow(wcloud, interpolation='bilinear')
        plt.axis('off')
        
        # save 폴더에 이미지 저장
        if save_to_file:
            # save 디렉토리 생성
            save_dir = Path("app/nlp/samsung/save")
            save_dir.mkdir(parents=True, exist_ok=True)
            
            # 타임스탬프가 포함된 파일명 생성
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"samsung_wordcloud_{timestamp}.png"
            save_path = save_dir / filename
            
            # 이미지 저장
            plt.savefig(save_path, dpi=300, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            logger.info(f"🎨 워드클라우드 이미지가 저장되었습니다: {save_path}")
            
            # 파일 정보 반환용
            file_info = {
                "filename": filename,
                "path": str(save_path),
                "size_bytes": save_path.stat().st_size if save_path.exists() else 0,
                "exists": save_path.exists()
            }
            
            plt.show()
            return file_info
        else:
            plt.show()
            return None