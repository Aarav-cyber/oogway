import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { ChatInput } from '../../src/components/chat/ChatInput';

describe('ChatInput Component', () => {
  it('disables submit button when input is empty', () => {
    render(<ChatInput onSendMessage={vi.fn()} />);
    const button = screen.getByRole('button', { name: /send message/i });
    expect(button).toBeDisabled();
  });

  it('submits message on Enter key press', () => {
    const handleSend = vi.fn();
    render(<ChatInput onSendMessage={handleSend} />);
    const textarea = screen.getByPlaceholderText(/ask about product/i);

    fireEvent.change(textarea, { target: { value: 'How to improve retention?' } });
    fireEvent.keyDown(textarea, { key: 'Enter', code: 'Enter', charCode: 13 });

    expect(handleSend).toHaveBeenCalledWith('How to improve retention?');
  });

  it('allows newline on Shift+Enter key press without submitting', () => {
    const handleSend = vi.fn();
    render(<ChatInput onSendMessage={handleSend} />);
    const textarea = screen.getByPlaceholderText(/ask about product/i);

    fireEvent.change(textarea, { target: { value: 'Line 1' } });
    fireEvent.keyDown(textarea, { key: 'Enter', shiftKey: true });

    expect(handleSend).not.toHaveBeenCalled();
  });
});
