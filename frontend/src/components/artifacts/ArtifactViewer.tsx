import React from 'react';
import { ArtifactHeader } from './ArtifactHeader';
import { MarkdownArtifact } from './MarkdownArtifact';
import { HtmlArtifact } from './HtmlArtifact';
import { LoadingState } from '../common/LoadingState';
import { ErrorState } from '../common/ErrorState';
import { Artifact } from '../../types';
import { Layers } from 'lucide-react';

interface ArtifactViewerProps {
  artifact: Artifact | null;
  isLoading?: boolean;
  error?: Error | null;
  onClose: () => void;
}

export const ArtifactViewer: React.FC<ArtifactViewerProps> = ({
  artifact,
  isLoading = false,
  error = null,
  onClose,
}) => {
  if (isLoading) {
    return (
      <div className="flex-1 flex flex-col h-full bg-slate-900 border-l border-slate-800">
        <ArtifactHeader title="Loading..." type="markdown" onClose={onClose} content="" />
        <LoadingState message="Creating artifact..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex-1 flex flex-col h-full bg-slate-900 border-l border-slate-800 p-4">
        <ArtifactHeader title="Error" type="markdown" onClose={onClose} content="" />
        <ErrorState error={error} />
      </div>
    );
  }

  if (!artifact) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center p-6 text-center text-slate-500 bg-slate-900 border-l border-slate-800">
        <Layers className="w-8 h-8 text-slate-600 mb-2" />
        <h3 className="text-sm font-semibold text-slate-300">No artifact selected</h3>
        <p className="text-xs text-slate-500 mt-1 max-w-xs">
          Ask the assistant to generate a Ship 30 essay, Markdown outline, or HTML page.
        </p>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden bg-slate-900 border-l border-slate-800">
      <ArtifactHeader
        title={artifact.title || 'Untitled Artifact'}
        type={artifact.type}
        onClose={onClose}
        content={artifact.content}
      />

      {artifact.type === 'html' ? (
        <HtmlArtifact content={artifact.content} />
      ) : (
        <MarkdownArtifact content={artifact.content} />
      )}
    </div>
  );
};
