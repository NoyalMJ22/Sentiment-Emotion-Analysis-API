import asyncio
import json
import hashlib
from typing import List, Dict
import redis.asyncio as redis
from transformers import pipeline
from langdetect import detect
from app.core.logger import logger
from app.core.config import settings

# Initialize Redis client asynchronously
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

class TextAnalyzerService:
    def __init__(self):
        logger.info("Initializing HuggingFace models (this may take a minute on first run)...")
        try:
            self.sentiment_pipe = pipeline(
                "sentiment-analysis", 
                model=settings.SENTIMENT_MODEL, 
                truncation=True, 
                max_length=512
            )
            self.emotion_pipe = pipeline(
                "text-classification", 
                model=settings.EMOTION_MODEL,
                top_k=None, 
                truncation=True, 
                max_length=512
            )
            logger.info("Models loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            raise

    def detect_language(self, text: str) -> str:
        try:
            return detect(text)
        except Exception:
            return "unknown"

    def _analyze_single(self, text: str) -> dict:
        """
        Internal sync method performing the heavy CPU ML inference.
        """
        # 1. Detect language
        lang = self.detect_language(text)
        
        # 2. Analyze Sentiment
        sentiment_out = self.sentiment_pipe(text)[0]
        sentiment_label = sentiment_out['label'].lower()
        sentiment_score = round(sentiment_out['score'], 4)
        
        # 3. Analyze Emotion
        emotions_out = self.emotion_pipe(text)[0]
        emotions_dict = {}
        for item in emotions_out:
            label = item['label'].lower()
            emotions_dict[label] = round(item['score'], 4)
        
        return {
            "text": text,
            "language": lang,
            "sentiment": sentiment_label,
            "confidence": sentiment_score,
            "emotions": emotions_dict
        }

    async def analyze(self, text: str) -> dict:
        """
        Analyze text with Distributed Redis Caching implemented!
        """
        # Generate predictable cache key based on the sentence
        cache_key = f"sentiment:{hashlib.md5(text.encode()).hexdigest()}"
        
        try:
            # Check Redis Distributed Cache FIRST
            cached_result = await redis_client.get(cache_key)
            if cached_result:
                logger.info("Cache HIT! ⚡ Returning lightning fast response from Redis!")
                return json.loads(cached_result)
        except Exception as e:
            logger.warning(f"Redis get error (Is redis server running on port 6379?): {e}")

        # Cache MISS - Generate prediction computationally
        logger.info("Cache MISS 🧠 Running ML model inference...")
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, self._analyze_single, text)
        
        try:
            # Store prediction in Redis for the next time (expires in 1 hour)
            await redis_client.setex(cache_key, 3600, json.dumps(result))
        except Exception as e:
            logger.warning(f"Redis set error: {e}")
            
        return result

    async def analyze_batch(self, texts: List[str]) -> List[dict]:
        tasks = [self.analyze(text) for text in texts]
        return await asyncio.gather(*tasks)

# Singleton Pattern
analyzer_service = None

def get_analyzer() -> TextAnalyzerService:
    global analyzer_service
    if analyzer_service is None:
        analyzer_service = TextAnalyzerService()
    return analyzer_service
