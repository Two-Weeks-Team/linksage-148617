"use client";
import { useEffect, useState } from 'react';
import { fetchBookmarks } from '@/lib/api';
import BookmarkCard from '@/components/BookmarkCard';
import LoadingSpinner from '@/components/LoadingSpinner';

export default function CollectionPanel() {
  const [bookmarks, setBookmarks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const data = await fetchBookmarks();
        setBookmarks(data.data ?? []);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  return (
    <section className="mt-8">
      <h2 className="text-2xl font-bold mb-4" style={{ color: 'var(--primary)' }}>Recent Activity</h2>
      {loading && (
        <div className="flex items-center gap-2">
          <LoadingSpinner /> Loading recent bookmarks…
        </div>
      )}
      {error && <p className="text-red-600">⚠️ {error}</p>}
      {!loading && !error && bookmarks.length === 0 && (
        <p className="text-muted">No bookmarks yet. Add a link above to see activity here.</p>
      )}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {bookmarks.map((bm) => (
          <BookmarkCard key={bm.id} bookmark={bm} />
        ))}
      </div>
    </section>
  );
}