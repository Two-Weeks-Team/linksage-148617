async function throwApiError(res: Response, fallback: string): Promise<never> {
  const raw = await res.text();
  const parsed = raw ? safeParseJson(raw) : null;
  const message = parsed?.error?.message ?? parsed?.detail ?? parsed?.message ?? raw ?? fallback;
  throw new Error(message || fallback);
}

function safeParseJson(raw: string): any {
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? '';

export async function fetchBookmarks() {
  const res = await fetch(`${API_BASE}/bookmarks`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include'
  });
  if (!res.ok) {
    await throwApiError(res, "Failed to fetch bookmarks");
  }
  return res.json();
}

export async function fetchSummary({ url, text }: { url?: string; text?: string }) {
  const payload: any = {};
  if (url) payload.url = url;
  if (text) payload.text = text;

  const res = await fetch(`${API_BASE}/summarize`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
    credentials: 'include'
  });

  if (!res.ok) {
    await throwApiError(res, "Failed to summarize");
  }
  return res.json();
}
