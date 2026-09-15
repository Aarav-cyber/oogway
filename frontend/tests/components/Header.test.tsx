import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { Header } from '../../src/components/layout/Header';

describe('Header LLM Selector Component', () => {
  it('renders active provider and model in selector button', () => {
    render(
      <Header
        onToggleSidebar={vi.fn()}
        activeProvider="ollama"
        activeModel="llama3.2"
        onSelectProvider={vi.fn()}
        isArtifactOpen={false}
        onToggleArtifact={vi.fn()}
        hasArtifact={false}
      />
    );

    expect(screen.getByText('Ollama')).toBeInTheDocument();
    expect(screen.getByText('llama3.2')).toBeInTheDocument();
  });

  it('opens LLM selector dropdown on click and lists options', () => {
    render(
      <Header
        onToggleSidebar={vi.fn()}
        activeProvider="ollama"
        activeModel="llama3.2"
        onSelectProvider={vi.fn()}
        isArtifactOpen={false}
        onToggleArtifact={vi.fn()}
        hasArtifact={false}
      />
    );

    const button = screen.getByRole('button', { name: /select llm provider/i });
    fireEvent.click(button);

    expect(screen.getByText('SELECT LLM')).toBeInTheDocument();
    expect(screen.getByText('Groq')).toBeInTheDocument();
    expect(screen.getByText('openai/gpt-oss-20b')).toBeInTheDocument();
    expect(screen.getByText('Gemini')).toBeInTheDocument();
    expect(screen.getByText('gemini-2.5-flash')).toBeInTheDocument();
  });

  it('calls onSelectProvider when provider option is clicked', async () => {
    const handleSelectProvider = vi.fn().mockResolvedValue(undefined);
    render(
      <Header
        onToggleSidebar={vi.fn()}
        activeProvider="ollama"
        activeModel="llama3.2"
        onSelectProvider={handleSelectProvider}
        isArtifactOpen={false}
        onToggleArtifact={vi.fn()}
        hasArtifact={false}
      />
    );

    const button = screen.getByRole('button', { name: /select llm provider/i });
    fireEvent.click(button);

    const groqOption = screen.getByText('Groq');
    fireEvent.click(groqOption);

    expect(handleSelectProvider).toHaveBeenCalledWith('groq');
  });
});
