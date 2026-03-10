import os
from fastapi import APIRouter, HTTPException, Depends, Query, Path, Body
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Any, Dict
from datetime import datetime
from models import SessionLocal, Bookmark
from ai_service import summarize_text, suggest_tags

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Pydantic Schemas ----------
class SummarySchema(BaseModel):
    short: Optional[str] = None
    long: Optional[str] = None

class BookmarkCreateSchema(BaseModel):
    url: str = Field(..., description="URL to process")
    title: Optional[str] = Field(None, max_length=255)

class BookmarkResponseSchema(BaseModel):
    id: str
    url: str
    title: Optional[str]
    summary: SummarySchema
    tags: List[str]
    created_at: datetime

class SummarizeRequestSchema(BaseModel):
    url: Optional[str] = None
    text: Optional[str] = None

    @validator("url", "text", always=True)
    def at_least_one(cls, v, values, **kwargs):
        if not v and not values.get("text") and not values.get("url"):
            raise ValueError("Either url or text must be provided")
        return v

class SummarizeResponseSchema(BaseModel):
    summary: SummarySchema

class TagSuggestRequestSchema(BaseModel):
    url: Optional[str] = None
    text: Optional[str] = None

    @validator("url", "text", always=True)
    def at_least_one(cls, v, values, **kwargs):
        if not v and not values.get("text") and not values.get("url"):
            raise ValueError("Either url or text must be provided")
        return v

class TagSuggestResponseSchema(BaseModel):
    tags: List[str]

# ---------- Endpoints ----------
@router.post("/bookmarks", response_model=BookmarkResponseSchema)
def create_bookmark(payload: BookmarkCreateSchema, db: Any = Depends(get_db)):
    # Generate summary using AI
    summary_res = summarize_text(url=payload.url, text=None)
    # Generate tags using AI
    tags_res = suggest_tags(url=payload.url, text=None)
    summary = summary_res.get("summary", {})
    tags = tags_res.get("tags", [])
    bookmark = Bookmark(
        url=payload.url,
        title=payload.title,
        summary_short=summary.get("short"),
        summary_long=summary.get("long"),
        tags=tags,
    )
    db.add(bookmark)
    db.commit()
    db.refresh(bookmark)
    return BookmarkResponseSchema(
        id=bookmark.id,
        url=bookmark.url,
        title=bookmark.title,
        summary=SummarySchema(short=bookmark.summary_short, long=bookmark.summary_long),
        tags=bookmark.tags,
        created_at=bookmark.created_at,
    )

@router.get("/bookmarks/{bookmark_id}", response_model=BookmarkResponseSchema)
def get_bookmark(bookmark_id: str = Path(..., description="Bookmark UUID"), db: Any = Depends(get_db)):
    bookmark = db.get(Bookmark, bookmark_id)
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return BookmarkResponseSchema(
        id=bookmark.id,
        url=bookmark.url,
        title=bookmark.title,
        summary=SummarySchema(short=bookmark.summary_short, long=bookmark.summary_long),
        tags=bookmark.tags,
        created_at=bookmark.created_at,
    )

@router.get("/bookmarks", response_model=Dict[str, Any])
def list_bookmarks(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    tags: Optional[str] = Query(None),
    db: Any = Depends(get_db),
):
    query = db.query(Bookmark)
    if tags:
        tags_list = [t.strip() for t in tags.split(",") if t.strip()]
        query = query.filter(Bookmark.tags.op("&&")(tags_list))  # PostgreSQL array overlap
    total = query.count()
    items = (
        query.order_by(Bookmark.created_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )
    data = [
        {
            "id": b.id,
            "url": b.url,
            "title": b.title,
            "summary": {"short": b.summary_short},
            "tags": b.tags,
            "created_at": b.created_at,
        }
        for b in items
    ]
    return {"data": data, "pagination": {"total": total, "page": page, "per_page": per_page}}

@router.post("/summarize", response_model=SummarizeResponseSchema)
def api_summarize(req: SummarizeRequestSchema):
    result = summarize_text(url=req.url, text=req.text)
    # Expected format: {"summary": {"short": ..., "long": ...}}
    return SummarizeResponseSchema(**result)

@router.post("/tags/suggest", response_model=TagSuggestResponseSchema)
def api_suggest_tags(req: TagSuggestRequestSchema):
    result = suggest_tags(url=req.url, text=req.text)
    # Expected format: {"tags": [...]}
    return TagSuggestResponseSchema(**result)
