"""
NLP 자연어 처리 관련 라우터
"""
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
from pathlib import Path
import sys
import logging

# 공통 모듈 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from app.nlp.emma.emma_wordcloud import NLTKService
from app.nlp.samsung.samsung_wordcloud import SamsungWordcloud
from common.utils import create_response, create_error_response

logger = logging.getLogger(__name__)

router = APIRouter(tags=["nlp"])

# 서비스 인스턴스 생성 (싱글톤 패턴)
_service_instance: Optional[NLTKService] = None


def get_service() -> NLTKService:
    """NLTKService 싱글톤 인스턴스 반환"""
    global _service_instance
    if _service_instance is None:
        _service_instance = NLTKService()
    return _service_instance


@router.get("/")
async def nlp_root():
    """NLP 서비스 루트"""
    return create_response(
        data={"service": "mlservice", "module": "nlp", "status": "running"},
        message="NLP Service is running"
    )

@router.get("/samsung")
async def generate_samsung_wordcloud():
    """삼성전자 지속가능경영보고서 2018 워드클라우드 생성"""
    try:
        # 삼성 워드클라우드 서비스 초기화
        samsung_service = SamsungWordcloud()
        
        # 텍스트 처리 및 워드클라우드 생성
        result = samsung_service.text_process()
        
        # 빈도 분석 결과를 딕셔너리로 변환
        freq_data = {}
        if 'freq_txt' in result and hasattr(result['freq_txt'], 'to_dict'):
            freq_data = result['freq_txt'].head(30).to_dict()
        
        return create_response(
            data={
                "processing_status": result.get('전처리 결과', '완료'),
                "top_keywords": [
                    {"word": word, "frequency": int(freq)} 
                    for word, freq in freq_data.items()
                ],
                "keyword_count": len(freq_data),
                "saved_file": result.get('saved_file', {}),
                "report_info": {
                    "title": "삼성전자 지속가능경영보고서 2018",
                    "source": "kr-Report_2018.txt"
                }
            },
            message="삼성전자 워드클라우드 분석이 완료되었습니다"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"삼성 워드클라우드 분석 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"삼성 워드클라우드 분석 실패: {str(e)}"
        )


@router.get("/emma")
async def generate_emma_wordcloud(
    width: int = Query(1000, description="워드클라우드 이미지 너비"),
    height: int = Query(600, description="워드클라우드 이미지 높이"),
    background_color: str = Query("white", description="배경색 (white, black, blue 등)"),
    max_words: int = Query(100, description="최대 단어 수")
):
    """
    Emma 소설 워드클라우드 생성
    - Jane Austen의 Emma 소설에서 등장인물 이름을 추출하여 워드클라우드 생성
    - 고유명사(NNP) 태그를 가진 단어들을 우선적으로 사용
    - 결과는 base64 인코딩된 이미지로 반환
    """
    try:
        service = get_service()
        
        # Emma 텍스트 샘플 로드
        logger.info("Emma 텍스트 로드 중...")
        text_sample = service.load_text_sample("austen-emma.txt", max_chars=50000)
        
        if "error" in text_sample:
            raise HTTPException(
                status_code=404,
                detail=f"Emma 텍스트를 로드할 수 없습니다: {text_sample['error']}"
            )
        
        emma_text = text_sample["sample"]
        logger.info(f"Emma 텍스트 로드 완료: {len(emma_text)} 문자")
        
        # 워드클라우드 생성
        logger.info("워드클라우드 생성 중...")
        wordcloud_result = service.generate_wordcloud(
            text=emma_text,
            width=width,
            height=height,
            background_color=background_color,
            max_words=max_words
        )
        
        if "error" in wordcloud_result:
            raise HTTPException(
                status_code=500,
                detail=f"워드클라우드 생성 실패: {wordcloud_result['error']}"
            )
        
        logger.info("워드클라우드 생성 완료")
        
        return create_response(
            data={
                "wordcloud": wordcloud_result,
                "text_info": {
                    "filename": text_sample["filename"],
                    "total_length": text_sample["total_length"],
                    "sample_length": text_sample["sample_length"]
                }
            },
            message="Emma 워드클라우드가 성공적으로 생성되었습니다"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Emma 워드클라우드 생성 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"워드클라우드 생성 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/corpus")
async def get_corpus_info():
    """
    NLTK 말뭉치 정보 조회
    - Gutenberg 말뭉치의 파일 목록과 정보 반환
    """
    try:
        service = get_service()
        corpus_info = service.get_corpus_info()
        
        if "error" in corpus_info:
            raise HTTPException(
                status_code=500,
                detail=f"말뭉치 정보 조회 실패: {corpus_info['error']}"
            )
        
        return create_response(
            data=corpus_info,
            message="말뭉치 정보 조회가 완료되었습니다"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"말뭉치 정보 조회 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"말뭉치 정보 조회 중 오류가 발생했습니다: {str(e)}"
        )


@router.post("/analyze")
async def analyze_text_endpoint(
    request: Dict[str, Any]
):
    """
    텍스트 종합 분석
    - 요청 본문: {"text": "분석할 텍스트", "name": "문서명(선택사항)"}
    - 토큰화, 품사 태깅, 빈도 분석 등 종합적인 텍스트 분석 수행
    """
    try:
        text = request.get("text")
        name = request.get("name", "Document")
        
        if not text:
            raise HTTPException(
                status_code=400,
                detail="분석할 텍스트가 제공되지 않았습니다"
            )
        
        service = get_service()
        analysis_result = service.analyze_text(text, name)
        
        if "error" in analysis_result:
            raise HTTPException(
                status_code=500,
                detail=f"텍스트 분석 실패: {analysis_result['error']}"
            )
        
        return create_response(
            data=analysis_result,
            message="텍스트 분석이 완료되었습니다"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"텍스트 분석 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"텍스트 분석 중 오류가 발생했습니다: {str(e)}"
        )


@router.post("/wordcloud")
async def generate_custom_wordcloud(
    request: Dict[str, Any]
):
    """
    커스텀 워드클라우드 생성
    - 요청 본문: {"text": "텍스트", "width": 1000, "height": 600, "background_color": "white", "max_words": 100}
    - 사용자가 제공한 텍스트로 워드클라우드 생성
    """
    try:
        text = request.get("text")
        width = request.get("width", 1000)
        height = request.get("height", 600)
        background_color = request.get("background_color", "white")
        max_words = request.get("max_words", 100)
        
        if not text:
            raise HTTPException(
                status_code=400,
                detail="워드클라우드 생성을 위한 텍스트가 제공되지 않았습니다"
            )
        
        service = get_service()
        wordcloud_result = service.generate_wordcloud(
            text=text,
            width=width,
            height=height,
            background_color=background_color,
            max_words=max_words
        )
        
        if "error" in wordcloud_result:
            raise HTTPException(
                status_code=500,
                detail=f"워드클라우드 생성 실패: {wordcloud_result['error']}"
            )
        
        return create_response(
            data=wordcloud_result,
            message="커스텀 워드클라우드가 성공적으로 생성되었습니다"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"커스텀 워드클라우드 생성 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"워드클라우드 생성 중 오류가 발생했습니다: {str(e)}"
        )


@router.post("/pos-tagging")
async def pos_tagging_endpoint(
    request: Dict[str, Any]
):
    """
    품사 태깅 분석
    - 요청 본문: {"text": "분석할 텍스트"}
    - 텍스트의 각 단어에 품사 태그를 부착하여 반환
    """
    try:
        text = request.get("text")
        
        if not text:
            raise HTTPException(
                status_code=400,
                detail="품사 태깅을 위한 텍스트가 제공되지 않았습니다"
            )
        
        service = get_service()
        pos_result = service.pos_tagging(text)
        
        if "error" in pos_result:
            raise HTTPException(
                status_code=500,
                detail=f"품사 태깅 실패: {pos_result['error']}"
            )
        
        return create_response(
            data=pos_result,
            message="품사 태깅이 완료되었습니다"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"품사 태깅 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"품사 태깅 중 오류가 발생했습니다: {str(e)}"
        )


