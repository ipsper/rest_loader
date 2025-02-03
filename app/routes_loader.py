from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ratelimit import limits, sleep_and_retry
from .logger_config import logger
from typing import Dict, Any, Optional
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from collections import Counter

router = APIRouter()

class Chunk(BaseModel):
    host: str
    port: int
    metoderna: str
    endpoint: str
    body: Optional[Dict[str, Any]] = None

class ChunkRequest(BaseModel):
    chunk: Dict[int, Chunk]
    requests_per_second: Optional[int] = 0  # Default requests per second
    requests_per_minute: Optional[int] = 0  # Default requests per minute

def send_request(chunk: Chunk):
    url = f"http://{chunk.host}:{chunk.port}{chunk.endpoint}"
    method = chunk.metoderna.lower()
    start_time = time.time()
    try:
        if method == "get":
            response = requests.get(url)
        elif method == "post":
            response = requests.post(url, json=chunk.body)
        elif method == "put":
            response = requests.put(url, json=chunk.body)
        elif method == "delete":
            response = requests.delete(url)
        else:
            return {"error": f"Unsupported method: {chunk.metoderna}"}
        end_time = time.time()
        duration = end_time - start_time
        return {"status_code": response.status_code, "response": response.json(), "duration": duration}
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        return {"error": str(e), "duration": duration}

@sleep_and_retry
def send_request_with_limits(chunk: Chunk, calls: int, period: int):
    @limits(calls=calls, period=period)
    def limited_request():
        return send_request(chunk)
    return limited_request()

@router.post("/process_chunks/")
def process_chunks(request: ChunkRequest, workers: int = 10):
    chunks = request.chunk
    requests_per_second = request.requests_per_second
    requests_per_minute = request.requests_per_minute

    # Log the received values for debugging
    logger.info(f"requests_per_second: {requests_per_second}, requests_per_minute: {requests_per_minute}")

    # Bestäm vilken hastighetsbegränsning som ska användas
    if requests_per_second > 0:
        calls = requests_per_second
        period = 1
    elif requests_per_minute > 0:
        calls = requests_per_minute
        period = 60
    else:
        raise HTTPException(status_code=400, detail="Both requests_per_second and requests_per_minute cannot be 0")

    results = []
    status_counter = Counter()
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_chunk = {
            executor.submit(send_request_with_limits, chunk, calls, period): chunk_id
            for chunk_id, chunk in chunks.items()
        }
        for future in as_completed(future_to_chunk):
            chunk_id = future_to_chunk[future]
            try:
                result = future.result()
                if "error" in result:
                    raise HTTPException(status_code=500, detail=f"Error processing chunk {chunk_id}: {result['error']}")
                results.append({"chunk_id": chunk_id, "result": result})
                status_counter[result["status_code"]] += 1
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error processing chunk {chunk_id}: {str(e)}")
            end_time = time.time()
            duration = end_time - start_time
            logger.info(f"Processed chunk {chunk_id} in {duration:.6f} seconds")

    return {"results": results, "status_code_statistics": dict(status_counter)}