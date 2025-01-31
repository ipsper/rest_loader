from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

router = APIRouter()

class Chunk(BaseModel):
    host: str
    port: int
    metoderna: str
    endpoint: str
    body: Optional[Dict[str, Any]] = None

class ChunkRequest(BaseModel):
    chunk: Dict[int, Chunk]
    interval: Optional[float]  # Interval in microseconds

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

@router.post("/process_chunks/")
def process_chunks(request: ChunkRequest, workers: int = 10):
    chunks = request.chunk
    interval = request.interval or 0
    results = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_chunk = {executor.submit(send_request, chunk): chunk_id for chunk_id, chunk in chunks.items()}
        for future in as_completed(future_to_chunk):
            chunk_id = future_to_chunk[future]
            try:
                result = future.result()
                if "error" in result:
                    raise HTTPException(status_code=500, detail=f"Error processing chunk {chunk_id}: {result['error']}")
                results.append({"chunk_id": chunk_id, "result": result})
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error processing chunk {chunk_id}: {str(e)}")
            time.sleep(interval)
    return {"results": results}