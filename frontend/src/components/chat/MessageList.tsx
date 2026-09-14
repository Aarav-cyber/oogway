import React, { useEffect, useRef } from 'react';
import { Message, Source } from '../../types';
import { MessageBubble } from './MessageBubble';
import { TypingIndicator } from './TypingIndicator';
import { EmptyState } from '../common/EmptyState';

interface MessageListProps {
  messages: Message[];
  isLoadingMessages: boolean;
  isSendingMessage: boolean;
  sourcesMap: Record<string, Source[]>;
  onSelectPrompt: (prompt: string) => void;
  onOpenArtifact?: (artifactId: string) => void;
}

export const MessageList: React.FC<MessageListProps> = ({
  messages,
  isLoadingMessages,
  isSendingMessage,
  sourcesMap,
  onSelectPrompt,
  onOpenArtifact,
}) => {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isSendingMessage]);

  if (messages.length === 0 && !isLoadingMessages && !isSendingMessage) {
    return <EmptyState onSelectPrompt={onSelectPrompt} />;
  }

  return (
    <div className="flex-1 overflow-y-auto px-4 py-6 space-y-2">
      {messages.map((message) => {
        const sources = sourcesMap[message.id];
        return (
          <MessageBubble
            key={message.id}
            message={message}
            sources={sources}
            onOpenArtifact={onOpenArtifact}
          />
        );
      })}

      {isSendingMessage && <TypingIndicator />}
      <div ref={bottomRef} />
    </div>
  );
};
