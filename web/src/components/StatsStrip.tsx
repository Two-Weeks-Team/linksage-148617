"use client";
export default function StatsStrip() {
  // Placeholder stats – in a production version these would be fetched from an endpoint.
  const stats = [
    { label: 'Bookmarks', value: 0 },
    { label: 'Tags', value: 0 },
    { label: 'AI Summaries', value: 0 }
  ];

  return (
    <section className="flex justify-around bg-muted rounded-lg p-4">
      {stats.map((s) => (
        <div key={s.label} className="text-center">
          <p className="text-2xl font-bold text-primary">{s.value}</p>
          <p className="text-sm text-muted">{s.label}</p>
        </div>
      ))}
    </section>
  );
}