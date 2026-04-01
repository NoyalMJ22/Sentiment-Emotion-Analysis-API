from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class AnalyzeRequest(BaseModel):
    text: str = Field(..., description="Text to analyze", min_length=1, max_length=5000)

class BatchAnalyzeRequest(BaseModel):
    texts: List[str] = Field(..., description="List of texts to analyze", max_length=100)

class AnalysisResult(BaseModel):
    text: str
    language: str
    sentiment: str
    confidence: float
    emotions: Dict[str, float]

class BatchAnalysisResult(BaseModel):
    results: List[AnalysisResult]
