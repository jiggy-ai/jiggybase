from loguru import logger
import json

def extract_content_from_sse_bytes(sse_bytes: bytes) -> str:
    """
    Extracts the "content" value from the raw SSE byte string. This is the incremental model output text.
    """
    sse_str = sse_bytes.decode('utf-8')
    lines = sse_str.strip().split('\n\n')
    results = ""
    for line in lines:        
        if line.startswith("data:"):
            event_str = line.split(":", 1)[1].strip()
            if '[DONE]' in event_str:
                continue
            try:
                event_data = json.loads(event_str)
                content = event_data.get("choices", [])[0].get("delta", {}).get("content", "")
                results += content
            except (json.JSONDecodeError, IndexError, KeyError, TypeError) as e:
                logger.error(f"Failed to parse SSE event data for line: '{line}'")
                logger.error(f"Failed to parse SSE event data with err: {e}")
                continue
    return results