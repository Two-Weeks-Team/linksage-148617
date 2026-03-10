"use client";
import { useEffect, useState } from 'react';
import LoadingSpinner from '@/components/LoadingSpinner';

export default function StatePanel() {
  const [state, setState] = useState<'idle' | 'loading' | 'error' | 'empty'>('idle');
  const [msg, setMsg] = useState('');

  // Demo placeholder – in a real app this would react to global store / context
  useEffect(() => {
    // Simulate idle -> loading after mount for demo
    setState('loading');
    const timer = setTimeout(() => {
      setState('empty');
      setMsg('No bookmarks yet. Paste a link above to get started.');
    }, 1500);
    return () => clearTimeout(timer);
  }, []);

  if (state === 'loading') {
    return (
      <div className="flex items-center gap-2 text-primary">
        <LoadingSpinner /> Processing your request…
      </div>
    );
  }

  if (state === 'error') {
    return <div className="text-red-600">⚠️ {msg || 'Something went wrong.'}</div>;
  }

  if (state === 'empty') {
    return <div className="text-muted">{msg}</div>;
  }

  return null;
}