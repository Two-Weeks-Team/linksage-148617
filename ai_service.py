import os
import json
import re
import httpx
from typing import Any, Dict, List, Optional

Inference_URL = "https://inference.do-ai.run/v1/chat/completions"
Inference_Key = os.getenv("DIGITALOCEAN_INFERENCE_KEY")
Model_Name = os.getenv("DO_INFERENCE_MODEL", "openai-gpt-oss-120b")

def _extract_json(text: str) -> str:
    m = re.search(r"```(?:json)?\s*\n?([\s\S]*?)\n?\s*```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    m = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return text.strip()

def _coerce_unstructured_payload(raw_text: str) -> Dict[str, Any]:
    compact = raw_text.strip()
    tags = [part.strip(" -•\t") for part in re.split(r",|\\n", compact) if part.strip(" -•\t")]
    return {
        "note": "Model returned plain text instead of JSON",
        "raw": compact,
        "text": compact,
        "summary": compact,
        "tags": tags[:6],
    }


async def _call_inference(messages: List[Dict[str, str]], max_tokens: int = 512) -> Dict[str, Any]:
    headers = {
        "Authorization": f"Bearer {Inference_Key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": Model_Name,
        "messages": messages,
        "max_completion_tokens": max_tokens,
    }
    try:
        async with httpx.AsyncClient(timeout=90.0) as client:
            resp = await client.post(Inference_URL, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            # Assume the model returns a single message in choices[0].message.content
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            json_str = _extract_json(content)
            return json.loads(json_str)
    except Exception as e:
        # Fallback response that the caller can handle gracefully
        return {"note": f"AI service unavailable: {str(e)}"}

async def summarize_text(url: Optional[str] = None, text: Optional[str] = None) -> Dict[str, Any]:
    if not url and not text:
        return {"note": "No content provided for summarization"}
    prompt = (
        "You are an expert summarizer. Produce a JSON object with two keys: 'short' (a concise 50‑100 word summary) "
        "and 'long' (a detailed 200‑500 word summary)."
    )
    if url:
        prompt += f" Summarize the content at this URL: {url}"
    if text:
        prompt += f" Summarize the following text: \n{text}"
    messages = [{"role": "user", "content": prompt}]
    result = await _call_inference(messages)
    # Ensure expected shape
    if isinstance(result, dict) and "short" in result and "long" in result:
        return {"summary": {"short": result["short"], "long": result["long"]}}
    # Fallback
    return {"summary": {"short": None, "long": None}, "note": result.get("note", "Unexpected AI response")}

async def suggest_tags(url: Optional[str] = None, text: Optional[str] = None) -> Dict[str, Any]:
    if not url and not text:
        return {"note": "No content provided for tag suggestion"}
    prompt = (
        "You are a content tagging assistant. Return a JSON array of up to 8 concise, relevant tags for the given content."
    )
    if url:
        prompt += f" Content URL: {url}"
    if text:
        prompt += f" Content text: \n{text}"
    messages = [{"role": "user", "content": prompt}]
    result = await _call_inference(messages)
    if isinstance(result, list):
        return {"tags": result}
    if isinstance(result, dict) and "tags" in result:
        return {"tags": result["tags"]}
    return {"tags": [], "note": result.get("note", "Unexpected AI response")}
