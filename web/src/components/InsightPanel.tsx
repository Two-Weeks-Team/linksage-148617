"use client";
interface InsightPanelProps {
  summary: { short: string; long: string };
  tags: string[];
}

export default function InsightPanel({ summary, tags }: InsightPanelProps) {
  return (
    <section className="mt-6 bg-muted rounded-lg p-4">
      <h2 className="text-xl font-semibold mb-2" style={{ color: 'var(--accent)' }}>
        Insight Panel
      </h2>
      <div className="space-y-2">
        <p className="font-medium">Short Summary:</p>
        <blockquote className="border-l-4 border-primary pl-3 italic text-sm">
          {summary.short}
        </blockquote>
        <p className="font-medium mt-3">Full Summary:</p>
        <p className="text-sm leading-relaxed">{summary.long}</p>
        <p className="font-medium mt-3">Suggested Tags:</p>
        <div className="flex flex-wrap gap-2 mt-1">
          {tags.map((tag) => (
            <span
              key={tag}
              className="bg-primary text-white text-xs px-2 py-0.5 rounded"
            >
              {tag}
            </span>
          ))}
        </div>
      </div>
    </section>
  );
}