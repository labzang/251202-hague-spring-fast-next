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

import nltk
import matplotlib.pyplot as plt
import io
import base64
from typing import List, Dict, Any, Optional, Tuple
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.stem import PorterStemmer, LancasterStemmer, WordNetLemmatizer
from nltk.tag import pos_tag, untag
from nltk import Text, FreqDist
from wordcloud import WordCloud
import logging

logger = logging.getLogger(__name__)


class NLTKService:
    """NLTK를 활용한 자연어 처리 서비스"""
    
    def __init__(self):
        """서비스 초기화 및 필요한 NLTK 데이터 다운로드"""
        self._download_nltk_data()
        self.porter_stemmer = PorterStemmer()
        self.lancaster_stemmer = LancasterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.regexp_tokenizer = RegexpTokenizer(r"[\w]+")
        self.stopwords = ["Mr.", "Mrs.", "Miss", "Mr", "Mrs", "Dear"]
        
    def _download_nltk_data(self):
        """필요한 NLTK 데이터 다운로드"""
        try:
            nltk.download('book', quiet=True)
            nltk.download('punkt', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
            nltk.download('wordnet', quiet=True)
            logger.info("NLTK 데이터 다운로드 완료")
        except Exception as e:
            logger.error(f"NLTK 데이터 다운로드 실패: {str(e)}")
    
    def get_corpus_info(self) -> Dict[str, Any]:
        """Gutenberg 말뭉치 정보 반환"""
        try:
            fileids = nltk.corpus.gutenberg.fileids()
            return {
                "corpus_name": "Gutenberg",
                "total_files": len(fileids),
                "file_list": fileids,
                "description": "저작권이 말소된 문학작품 말뭉치"
            }
        except Exception as e:
            logger.error(f"말뭉치 정보 조회 실패: {str(e)}")
            return {"error": str(e)}
    
    def load_text_sample(self, filename: str = "austen-emma.txt", max_chars: int = 1302) -> Dict[str, Any]:
        """텍스트 샘플 로드"""
        try:
            raw_text = nltk.corpus.gutenberg.raw(filename)
            return {
                "filename": filename,
                "total_length": len(raw_text),
                "sample": raw_text[:max_chars],
                "sample_length": min(max_chars, len(raw_text))
            }
        except Exception as e:
            logger.error(f"텍스트 로드 실패: {str(e)}")
            return {"error": str(e)}
    
    def tokenize_sentences(self, text: str) -> List[str]:
        """문장 토큰화"""
        try:
            return sent_tokenize(text)
        except Exception as e:
            logger.error(f"문장 토큰화 실패: {str(e)}")
            return []
    
    def tokenize_words(self, text: str) -> List[str]:
        """단어 토큰화"""
        try:
            return word_tokenize(text)
        except Exception as e:
            logger.error(f"단어 토큰화 실패: {str(e)}")
            return []
    
    def tokenize_regexp(self, text: str, pattern: str = r"[\w]+") -> List[str]:
        """정규표현식 토큰화"""
        try:
            tokenizer = RegexpTokenizer(pattern)
            return tokenizer.tokenize(text)
        except Exception as e:
            logger.error(f"정규표현식 토큰화 실패: {str(e)}")
            return []
    
    def stem_words(self, words: List[str], method: str = "porter") -> Dict[str, Any]:
        """어간 추출"""
        try:
            if method.lower() == "porter":
                stemmed = [self.porter_stemmer.stem(word) for word in words]
            elif method.lower() == "lancaster":
                stemmed = [self.lancaster_stemmer.stem(word) for word in words]
            else:
                raise ValueError(f"지원하지 않는 어간 추출 방법: {method}")
            
            return {
                "method": method,
                "original": words,
                "stemmed": stemmed,
                "pairs": list(zip(words, stemmed))
            }
        except Exception as e:
            logger.error(f"어간 추출 실패: {str(e)}")
            return {"error": str(e)}
    
    def lemmatize_words(self, words: List[str], pos: Optional[str] = None) -> Dict[str, Any]:
        """원형 복원"""
        try:
            if pos:
                lemmatized = [self.lemmatizer.lemmatize(word, pos=pos) for word in words]
            else:
                lemmatized = [self.lemmatizer.lemmatize(word) for word in words]
            
            return {
                "pos": pos,
                "original": words,
                "lemmatized": lemmatized,
                "pairs": list(zip(words, lemmatized))
            }
        except Exception as e:
            logger.error(f"원형 복원 실패: {str(e)}")
            return {"error": str(e)}
    
    def pos_tagging(self, text: str) -> Dict[str, Any]:
        """품사 태깅"""
        try:
            tokens = word_tokenize(text)
            tagged = pos_tag(tokens)
            
            # 품사별 분류
            pos_groups = {}
            for word, tag in tagged:
                if tag not in pos_groups:
                    pos_groups[tag] = []
                pos_groups[tag].append(word)
            
            return {
                "text": text,
                "tokens": tokens,
                "tagged": tagged,
                "pos_groups": pos_groups,
                "total_tokens": len(tokens)
            }
        except Exception as e:
            logger.error(f"품사 태깅 실패: {str(e)}")
            return {"error": str(e)}
    
    def extract_nouns(self, text: str) -> List[str]:
        """명사 추출"""
        try:
            tokens = word_tokenize(text)
            tagged = pos_tag(tokens)
            return [word for word, tag in tagged if tag.startswith('NN')]
        except Exception as e:
            logger.error(f"명사 추출 실패: {str(e)}")
            return []
    
    def create_pos_tokenizer(self, text: str) -> List[str]:
        """품사가 포함된 토큰 생성"""
        try:
            tokens = word_tokenize(text)
            tagged = pos_tag(tokens)
            return [f"{word}/{tag}" for word, tag in tagged]
        except Exception as e:
            logger.error(f"품사 토큰 생성 실패: {str(e)}")
            return []
    
    def analyze_text(self, text: str, name: str = "Document") -> Dict[str, Any]:
        """텍스트 종합 분석"""
        try:
            # 토큰화
            tokens = self.regexp_tokenizer.tokenize(text)
            nltk_text = Text(tokens, name=name)
            
            # 빈도 분석
            freq_dist = FreqDist(tokens)
            
            # 품사 태깅
            pos_result = self.pos_tagging(text)
            
            # 고유명사 추출 (NNP 태그)
            proper_nouns = [word for word, tag in pos_result.get('tagged', []) 
                          if tag == 'NNP' and word not in self.stopwords]
            proper_noun_freq = FreqDist(proper_nouns)
            
            return {
                "name": name,
                "total_tokens": len(tokens),
                "unique_tokens": len(set(tokens)),
                "most_common": freq_dist.most_common(10),
                "proper_nouns": proper_noun_freq.most_common(10),
                "pos_summary": pos_result.get('pos_groups', {}),
                "text_length": len(text)
            }
        except Exception as e:
            logger.error(f"텍스트 분석 실패: {str(e)}")
            return {"error": str(e)}
    
    def generate_wordcloud(self, text: str, width: int = 1000, height: int = 600, 
                          background_color: str = "white", max_words: int = 100) -> Dict[str, Any]:
        """워드클라우드 생성"""
        try:
            # 토큰화 및 빈도 계산
            tokens = self.regexp_tokenizer.tokenize(text)
            
            # 품사 태깅으로 고유명사만 추출
            pos_tagged = pos_tag(tokens)
            proper_nouns = [word for word, tag in pos_tagged 
                          if tag == 'NNP' and word not in self.stopwords]
            
            if not proper_nouns:
                # 고유명사가 없으면 모든 토큰 사용
                freq_dist = FreqDist(tokens)
            else:
                freq_dist = FreqDist(proper_nouns)
            
            # 워드클라우드 생성 (D2Coding 폰트 사용)
            font_path = 'app/nlp/data/D2Coding.ttf'
            wc = WordCloud(
                font_path=font_path,
                width=width, 
                height=height, 
                background_color=background_color,
                max_words=max_words,
                random_state=42
            )
            
            # 빈도수 딕셔너리로 워드클라우드 생성
            freq_dict = dict(freq_dist.most_common(max_words))
            wordcloud = wc.generate_from_frequencies(freq_dict)
            
            # save 폴더 경로 설정
            from pathlib import Path
            import datetime
            
            save_dir = Path(__file__).parent / "save"
            save_dir.mkdir(parents=True, exist_ok=True)
            
            # 파일명 생성 (타임스탬프 포함)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"emma_wordcloud_{timestamp}_{width}x{height}.png"
            save_path = save_dir / filename
            
            # 이미지를 base64로 인코딩 및 파일 저장
            img_buffer = io.BytesIO()
            plt.figure(figsize=(width/100, height/100))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.tight_layout(pad=0)
            
            # 메모리 버퍼에 저장 (base64용)
            plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=100)
            
            # 파일로 저장 (save 폴더)
            plt.savefig(save_path, format='png', bbox_inches='tight', dpi=100)
            logger.info(f"워드클라우드 이미지가 저장되었습니다: {save_path}")
            
            plt.close()
            
            img_buffer.seek(0)
            img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
            
            return {
                "status": "success",
                "word_count": len(freq_dict),
                "most_common": list(freq_dict.items())[:10],
                "image_base64": img_base64,
                "saved_file": {
                    "filename": filename,
                    "path": str(save_path),
                    "size_bytes": save_path.stat().st_size if save_path.exists() else 0,
                    "exists": save_path.exists()
                },
                "config": {
                    "width": width,
                    "height": height,
                    "background_color": background_color,
                    "max_words": max_words
                }
            }
        except Exception as e:
            logger.error(f"워드클라우드 생성 실패: {str(e)}")
            return {"error": str(e)}
    
    def text_concordance(self, text: str, word: str, lines: int = 5) -> Dict[str, Any]:
        """단어 용례 검색"""
        try:
            tokens = self.regexp_tokenizer.tokenize(text)
            nltk_text = Text(tokens)
            
            # concordance 결과를 캡처하기 위해 stdout을 리다이렉트
            import sys
            from io import StringIO
            
            old_stdout = sys.stdout
            sys.stdout = captured_output = StringIO()
            
            nltk_text.concordance(word, lines=lines)
            
            sys.stdout = old_stdout
            concordance_result = captured_output.getvalue()
            
            return {
                "word": word,
                "lines": lines,
                "concordance": concordance_result,
                "found": bool(concordance_result.strip())
            }
        except Exception as e:
            logger.error(f"용례 검색 실패: {str(e)}")
            return {"error": str(e)}
    
    def find_similar_words(self, text: str, word: str, num: int = 10) -> Dict[str, Any]:
        """유사한 문맥의 단어 찾기"""
        try:
            tokens = self.regexp_tokenizer.tokenize(text)
            nltk_text = Text(tokens)
            
            # similar 결과를 캡처
            import sys
            from io import StringIO
            
            old_stdout = sys.stdout
            sys.stdout = captured_output = StringIO()
            
            nltk_text.similar(word, num)
            
            sys.stdout = old_stdout
            similar_result = captured_output.getvalue()
            
            # 결과 파싱
            similar_words = similar_result.strip().split() if similar_result.strip() else []
            
            return {
                "target_word": word,
                "similar_words": similar_words,
                "count": len(similar_words)
            }
        except Exception as e:
            logger.error(f"유사 단어 검색 실패: {str(e)}")
            return {"error": str(e)}
    
    def find_collocations(self, text: str, num: int = 10) -> Dict[str, Any]:
        """연어(함께 나타나는 단어) 찾기"""
        try:
            tokens = self.regexp_tokenizer.tokenize(text)
            nltk_text = Text(tokens)
            
            # collocations 결과를 캡처
            import sys
            from io import StringIO
            
            old_stdout = sys.stdout
            sys.stdout = captured_output = StringIO()
            
            nltk_text.collocations(num)
            
            sys.stdout = old_stdout
            collocations_result = captured_output.getvalue()
            
            # 결과 파싱
            collocations = []
            if collocations_result.strip():
                pairs = collocations_result.strip().split('; ')
                collocations = [pair.strip() for pair in pairs if pair.strip()]
            
            return {
                "collocations": collocations,
                "count": len(collocations),
                "requested_num": num
            }
        except Exception as e:
            logger.error(f"연어 검색 실패: {str(e)}")
            return {"error": str(e)}