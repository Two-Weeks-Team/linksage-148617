"use client";
interface Bookmark {
  id: string;
  url: string;
  title: string;
  summary: { short: string };
  tags: string[];
  created_at: string;
}

interface Props {
  bookmark: Bookmark;
}

export default function BookmarkCard({ bookmark }: Props) {
  const date = new Date(bookmark.created_at).toLocaleDateString();
  return (
    <article className="bg-card rounded-lg shadow-sm p-4 hover:shadow-md transition-shadow">
      <h3 className="font-semibold text-primary line-clamp-1" title={bookmark.title}>
        {bookmark.title || bookmark.url}
      </h3>
      <p className="text-xs text-muted mt-1">{date}</p>
      <blockquote className="border-l-4 border-accent pl-2 italic text-sm mt-2">
        {bookmark.summary.short}
      </blockquote>
      <div className="flex flex-wrap gap-1 mt-2">
        {bookmark.tags.map((tag) => (
          <span key={tag} className="bg-accent text-white text-xs px-2 py-0.5 rounded">
            {tag}
          </span>
        ))}
      </div>
    </article>
  );
}