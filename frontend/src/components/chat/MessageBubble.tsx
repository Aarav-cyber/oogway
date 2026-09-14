import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { User, Sparkles, Layers } from 'lucide-react';
import { Message, Source } from '../../types';
import { SourceList } from './SourceList';
import { clsx } from 'clsx';
import { Button } from '../common/Button';

interface MessageBubbleProps {
  message: Message;
  sources?: Source[];
  onOpenArtifact?: (artifactId: string) => void;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({
  message,
  sources,
  onOpenArtifact,
}) => {
  const isUser = message.role === 'user';
  const artifactId = message.metadata?.artifact_id;
  const skill = message.metadata?.skill;

  return (
    <div className={clsx('flex items-start space-x-3 my-4 group', isUser ? 'flex-row-reverse space-x-reverse' : 'flex-row')}>
      {/* Avatar */}
      <div
        className={clsx(
          'w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 text-xs font-bold shadow-sm',
          isUser
            ? 'bg-slate-700 text-slate-200 border border-slate-600'
            : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
        )}
      >
        {isUser ? <User className="w-4 h-4" /> : <Sparkles className="w-4 h-4" />}
      </div>

      {/* Message Box */}
      <div
        className={clsx(
          'max-w-[85%] sm:max-w-[78%] rounded-2xl px-4 py-3 text-sm leading-relaxed shadow-sm',
          isUser
            ? 'bg-emerald-600 text-white rounded-tr-sm'
            : 'bg-slate-900 border border-slate-800 text-slate-200 rounded-tl-sm'
        )}
      >
        {/* Markdown Content */}
        <div className="prose prose-invert max-w-none text-slate-200 text-sm leading-relaxed space-y-2">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {message.content}
          </ReactMarkdown>
        </div>

        {/* Artifact Trigger Button if created */}
        {artifactId && onOpenArtifact && (
          <div className="mt-3 pt-2 border-t border-slate-800">
            <Button
              size="sm"
              variant="outline"
              onClick={() => onOpenArtifact(artifactId)}
              leftIcon={<Layers className="w-3.5 h-3.5 text-emerald-400" />}
              className="bg-slate-800/90 hover:bg-slate-700 border-slate-700 text-emerald-300 text-xs"
            >
              Open Generated Artifact
            </Button>
          </div>
        )}

        {/* Sources List */}
        {!isUser && sources && sources.length > 0 && <SourceList sources={sources} />}

        {/* Footer Meta */}
        {!isUser && skill && (
          <div className="mt-2 text-[10px] uppercase font-mono tracking-wider text-slate-500 flex items-center justify-between">
            <span>Skill: {skill}</span>
          </div>
        )}
      </div>
    </div>
  );
};
