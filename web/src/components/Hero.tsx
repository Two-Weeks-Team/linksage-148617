"use client";
import { useState } from 'react';
import { fetchSummary } from '@/lib/api';
import InsightPanel from '@/components/InsightPanel';
import LoadingSpinner from '@/components/LoadingSpinner';

export default function Hero() {
  const [url, setUrl] = useState('');
  const [summary, setSummary] = useState<{ short: string; long: string } | null>(null);
  const [tags, setTags] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const data = await fetchSummary({ url });
      setSummary(data.summary);
      // Simulate tag suggestion – in a real app this would be another endpoint
      setTags(['AI', 'Research', 'Summary']);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="bg-card rounded-lg p-6 shadow-md">
      <h1 className="text-3xl font-bold mb-4" style={{ color: 'var(--primary)' }}>
        {"LinkSage"}
      </h1>
      <p className="mb-6 text-muted">
        Transform bookmarks into actionable insights with AI-powered summarization and smart tagging.
      </p>
      <form onSubmit={handleSubmit} className="flex flex-col md:flex-row gap-2">
        <input
          type="url"
          required
          placeholder="Paste an article URL…"
          className="flex-1 border border-border rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-primary"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-primary hover:bg-primary/90 text-white font-medium px-4 py-2 rounded-md disabled:opacity-50"
        >
          {loading ? <LoadingSpinner /> : 'Summarize'}
        </button>
      </form>
      {error && <p className="text-red-600 mt-2">⚠️ {error}</p>}
      {summary && (
        <InsightPanel summary={summary} tags={tags} />
      )}
    </section>
  );
}