import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface MarkdownArtifactProps {
  content: string;
}

export const MarkdownArtifact: React.FC<MarkdownArtifactProps> = ({ content }) => {
  return (
    <div className="flex-1 overflow-y-auto p-6 bg-slate-950 text-slate-200">
      <article className="prose prose-invert max-w-none text-slate-200 text-sm leading-relaxed space-y-4">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
      </article>
    </div>
  );
};
