import React from 'react';
import { MessageList } from './MessageList';
import { ChatInput } from './ChatInput';
import { ErrorState } from '../common/ErrorState';
import { Message, Source } from '../../types';

interface ChatWindowProps {
  messages: Message[];
  isLoadingMessages: boolean;
  isSendingMessage: boolean;
  error: Error | null;
  sourcesMap: Record<string, Source[]>;
  onSendMessage: (content: string) => void;
  onOpenArtifact?: (artifactId: string) => void;
}

export const ChatWindow: React.FC<ChatWindowProps> = ({
  messages,
  isLoadingMessages,
  isSendingMessage,
  error,
  sourcesMap,
  onSendMessage,
  onOpenArtifact,
}) => {
  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden bg-slate-950">
      {error && (
        <div className="px-4 pt-2">
          <ErrorState error={error} />
        </div>
      )}

      <MessageList
        messages={messages}
        isLoadingMessages={isLoadingMessages}
        isSendingMessage={isSendingMessage}
        sourcesMap={sourcesMap}
        onSelectPrompt={onSendMessage}
        onOpenArtifact={onOpenArtifact}
      />

      <ChatInput onSendMessage={onSendMessage} disabled={isSendingMessage} />
    </div>
  );
};
