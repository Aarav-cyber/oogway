import React from 'react';
import { Sparkles, ArrowRight } from 'lucide-react';

interface EmptyStateProps {
  onSelectPrompt: (prompt: string) => void;
}

const SUGGESTED_PROMPTS = [
  "What can Lenny's guests teach us about product retention?",
  "How should startups structure their activation and onboarding funnel?",
  "Write me a Ship 30 for 30 essay on product-led growth strategy.",
  "Create an HTML artifact showing a dashboard summary for SaaS metrics.",
];

export const EmptyState: React.FC<EmptyStateProps> = ({ onSelectPrompt }) => {
  return (
    <div className="flex-1 flex flex-col items-center justify-center p-6 text-center max-w-2xl mx-auto">
      <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 mb-4 shadow-lg shadow-emerald-500/5">
        <Sparkles className="w-6 h-6" />
      </div>

      <h2 className="text-2xl font-bold text-slate-100 tracking-tight mb-2">
        Lenny Growth Assistant
      </h2>

      <p className="text-sm text-slate-400 mb-8 max-w-lg">
        Ask grounded product strategy questions based on Lenny’s Podcast & Newsletter transcripts, write Ship 30 essays, or build interactive artifacts.
      </p>

      <div className="w-full grid grid-cols-1 md:grid-cols-2 gap-3">
        {SUGGESTED_PROMPTS.map((prompt, idx) => (
          <button
            key={idx}
            onClick={() => onSelectPrompt(prompt)}
            className="group flex items-start text-left p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 hover:border-emerald-500/40 hover:bg-slate-800/60 transition-all duration-200"
          >
            <span className="text-xs text-slate-300 group-hover:text-emerald-300 font-medium flex-1">
              {prompt}
            </span>
            <ArrowRight className="w-4 h-4 text-slate-600 group-hover:text-emerald-400 group-hover:translate-x-0.5 transition-all ml-2 flex-shrink-0" />
          </button>
        ))}
      </div>
    </div>
  );
};
