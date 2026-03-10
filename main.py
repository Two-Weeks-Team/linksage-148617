import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from routes import router
from models import Base, engine

app = FastAPI()


@app.middleware("http")
async def normalize_api_prefix(request: Request, call_next):
    if request.scope.get("path", "").startswith("/api/"):
        request.scope["path"] = request.scope["path"][4:] or "/"
    return await call_next(request)

app.include_router(router)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <html lang=\"en\">
    <head>
        <meta charset=\"UTF-8\">
        <title>LinkSage API</title>
        <style>
            body {background-color:#121212;color:#e0e0e0;font-family:Arial,Helvetica,sans-serif;padding:2rem;}
            h1 {color:#ff9800;}
            a {color:#64b5f6;}
            .endpoint {margin-bottom:1rem;padding:0.5rem;background:#1e1e1e;border-radius:4px;}
            .stack {margin-top:2rem;}
        </style>
    </head>
    <body>
        <h1>LinkSage – AI‑powered Bookmark Insights</h1>
        <p>Transform bookmarks into actionable summaries, tags and connections.</p>
        <h2>Available Endpoints</h2>
        <div class=\"endpoint\">GET <code>/health</code> – health check</div>
        <div class=\"endpoint\">POST <code>/bookmarks</code> – create bookmark (AI summary & tags)</div>
        <div class=\"endpoint\">GET <code>/bookmarks/{id}</code> – retrieve a bookmark</div>
        <div class=\"endpoint\">GET <code>/bookmarks</code> – list bookmarks (pagination)</div>
        <div class=\"endpoint\">POST <code>/summarize</code> – generate summary for URL or raw text</div>
        <div class=\"endpoint\">POST <code>/tags/suggest</code> – auto‑suggest tags for URL or raw text</div>
        <h2>Technology Stack</h2>
        <ul>
            <li>FastAPI 0.115.0</li>
            <li>PostgreSQL (SQLAlchemy 2.0)</li>
            <li>DigitalOcean Serverless Inference (openai‑gpt‑oss‑120b)</li>
            <li>Python 3.12+</li>
        </ul>
        <p>Interactive docs: <a href=\"/docs\">/docs</a> | <a href=\"/redoc\">/redoc</a></p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

# Create tables on startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
