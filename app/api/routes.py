from fastapi import APIRouter, HTTPException, Request, Depends, Security
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.models.schemas import AnalyzeRequest, BatchAnalyzeRequest, AnalysisResult, BatchAnalysisResult
from app.services.analyzer import get_analyzer, TextAnalyzerService
from app.api.auth import get_api_key
from app.core.logger import logger

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/analyze", response_model=AnalysisResult, dependencies=[Depends(get_api_key)])
@limiter.limit("60/minute")
async def analyze_text(
    request: Request, 
    payload: AnalyzeRequest, 
    analyzer: TextAnalyzerService = Depends(get_analyzer)
):
    """
    Analyze single text. Requires API Key.
    """
    try:
        logger.info(f"Analyzing text: {payload.text[:50]}...")
        result = await analyzer.analyze(payload.text)
        return result
    except Exception as e:
        logger.error(f"Error analyzing text: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during analysis")

@router.post("/analyze/batch", response_model=BatchAnalysisResult, dependencies=[Depends(get_api_key)])
@limiter.limit("20/minute")
async def analyze_batch_texts(
    request: Request, 
    payload: BatchAnalyzeRequest, 
    analyzer: TextAnalyzerService = Depends(get_analyzer)
):
    """
    Analyze batch texts natively. Requires API Key.
    """
    try:
        logger.info(f"Analyzing batch of {len(payload.texts)} texts")
        results = await analyzer.analyze_batch(payload.texts)
        return {"results": results}
    except Exception as e:
        logger.error(f"Error analyzing batch: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during batch analysis")
