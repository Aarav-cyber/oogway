import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { SourceList } from '../../src/components/chat/SourceList';
import { Source } from '../../src/types';

describe('SourceList Component', () => {
  it('renders transcript sources correctly', () => {
    const mockSources: Source[] = [
      {
        document_id: 'doc-1',
        chunk_id: 'c-1',
        title: 'Brian Chesky Airbnb',
        source_url: 'https://example.com/brian',
      },
      {
        document_id: 'doc-2',
        chunk_id: 'c-2',
        title: 'Shreyas Doshi Strategy',
      },
    ];

    render(<SourceList sources={mockSources} />);

    expect(screen.getByText('TRANSCRIPT SOURCES (2)')).toBeInTheDocument();
    expect(screen.getByText('Brian Chesky Airbnb')).toBeInTheDocument();
    expect(screen.getByText('Shreyas Doshi Strategy')).toBeInTheDocument();
  });
});
