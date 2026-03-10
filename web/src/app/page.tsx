"use client";
import Hero from '@/components/Hero';
import InsightPanel from '@/components/InsightPanel';
import CollectionPanel from '@/components/CollectionPanel';
import StatsStrip from '@/components/StatsStrip';
import StatePanel from '@/components/StatePanel';

export default function HomePage() {
  return (
    <main className="flex flex-col gap-8 p-4 md:p-8 max-w-7xl mx-auto">
      <Hero />
      <StatsStrip />
      {/* InsightPanel will be rendered inside Hero after a summary is generated */}
      <CollectionPanel />
      <StatePanel />
    </main>
  );
}